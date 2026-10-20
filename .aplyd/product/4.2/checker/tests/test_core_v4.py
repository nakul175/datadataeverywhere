"""Regression tests for scoped proof, trust boundaries and deterministic input errors."""
import contextlib
import copy
import io
from pathlib import Path
import tempfile
import unittest

from test_checker import qc, fixture, profile_catalogue, bind_scoped_reviews, refresh_reviews, trust_fixture


class ScopedReviewTests(unittest.TestCase):
    def setUp(self):
        self.catalogue, self.doc = fixture(profile_catalogue(), assessment_mode="profile")
        self.story = next(item for item in self.doc["elements"] if item["elementType"] == "user_story")
        sibling = copy.deepcopy(self.story)
        sibling["id"] = "user-story-sibling"
        self.doc["elements"].append(sibling)
        refresh_reviews(self.catalogue, self.doc)
        self.sibling = sibling

    def report(self):
        return qc.Checker(self.catalogue, self.doc).run()

    def gates(self, element_id, report=None):
        return [item for item in (report or self.report())["checks"] if item["elementId"] == element_id and item["checkId"].startswith("profile.")]

    def test_local_story_change_preserves_unrelated_sibling_and_reopens_descendants(self):
        self.story["fields"]["user_story.description"]["value"] += " Changed local acceptance boundary."
        report = self.report()
        self.assertTrue(all(item["status"] == "stale" for item in self.gates(self.story["id"], report)))
        self.assertTrue(all(item["status"] == "passed" for item in self.gates(self.sibling["id"], report)))
        criterion = next(item for item in self.doc["elements"] if item["elementType"] == "acceptance_criterion")
        self.assertTrue(all(item["status"] == "stale" for item in self.gates(criterion["id"], report)))
        epic = next(item for item in self.doc["elements"] if item["elementType"] == "epic")
        changed_parent_gates = [item for item in self.gates(epic["id"], report) if item["status"] == "stale"]
        self.assertEqual([item["checkId"] for item in changed_parent_gates], ["profile.planning.epic.01"])
        self.assertTrue(any(link["relation"] == "direct_child_alignment" for link in changed_parent_gates[0]["fingerprintScope"]["dependencyLinks"]))

    def test_transitive_prerequisite_change_invalidates_declared_dependent(self):
        self.sibling["dependencyIds"] = [self.story["id"]]
        refresh_reviews(self.catalogue, self.doc)
        self.story["fields"]["user_story.description"]["value"] += " Material prerequisite change."
        gates = self.gates(self.sibling["id"])
        self.assertTrue(all(item["status"] == "stale" for item in gates))
        self.assertTrue(any(link["relation"] == "blocking_prerequisite" for link in gates[0]["fingerprintScope"]["dependencyLinks"]))

    def test_parent_source_profile_and_catalogue_changes_reopen_affected_scopes(self):
        original = copy.deepcopy(self.doc)
        for change in ("parent", "source", "profile", "catalogue"):
            self.doc = copy.deepcopy(original)
            catalogue = copy.deepcopy(self.catalogue)
            if change == "parent":
                self.doc["elements"][0]["fields"]["vision.description"]["value"] += " Parent policy changed."
            elif change == "source":
                self.doc["sources"][0]["text"] += " Authoritative policy changed."
                self.doc["sourcePins"]["source-001"] = qc.source_hash(self.doc["sources"][0])
            elif change == "profile":
                self.doc["productProfile"]["ai"]["rationale"] += " Scope decision revised."
            else:
                catalogue["profileChecks"][0]["passCriterion"] += " New threshold."
            report = qc.Checker(catalogue, self.doc).run()
            self.assertTrue(all(item["status"] == "stale" for item in self.gates(self.sibling["id"], report)), change)

    def test_queue_revision_audit_and_unused_authority_do_not_invalidate_local_reviews(self):
        global_before = qc.subject_fingerprint(self.doc, self.catalogue)
        self.doc["revision"] += 1
        self.doc["changeReason"] = "Record a non-substantive audit event."
        self.doc["questionDecisionVersions"] = {"unrelated": 2}
        self.doc["qualityState"] = {"status": "not_assessed"}
        self.doc["history"] = [{"event": "Owner answered a retained question."}]
        self.doc["authorities"].append({"id": "unused-reviewer", "permissions": [], "elementIds": [], "authoritySource": "Unused registry row."})
        self.assertNotEqual(global_before, qc.subject_fingerprint(self.doc, self.catalogue))
        self.assertEqual(self.report()["qualityState"]["status"], "synthetic_checks_satisfied")

    def test_unused_source_and_evidence_preserve_checks(self):
        source = {"id": "unused-source", "text": "Retained unrelated research note.", "version": "1", "originality": "original", "approvalStatus": "draft", "protected": True}
        self.doc["sources"].append(source)
        self.doc["sourcePins"][source["id"]] = qc.source_hash(source)
        self.doc["evidence"].append({"id": "unused-proof", "content": "Unused retained content."})
        self.assertTrue(all(item["status"] == "passed" for item in self.gates(self.sibling["id"])))

    def test_referenced_authority_and_evidence_changes_stale_target(self):
        for kind in ("authority", "evidence"):
            doc = copy.deepcopy(self.doc)
            if kind == "authority":
                doc["authorities"][0]["authoritySource"] += " Revised registry basis."
            else:
                doc["evidence"][0]["content"]["method"] += " Modified result."
                doc["evidence"][0]["contentHash"] = qc.evidence_hash(doc["evidence"][0], ".")
            report = qc.Checker(self.catalogue, doc).run()
            self.assertTrue(all(item["status"] == "stale" for item in self.gates(self.sibling["id"], report)), kind)

    def test_legacy_global_fingerprint_cannot_pass_scoped_review(self):
        for review in self.doc["reviews"]:
            review.pop("bindingVersion")
            review["subjectFingerprint"] = qc.subject_fingerprint(self.doc, self.catalogue)
        report = self.report()
        self.assertNotIn(report["qualityState"]["status"], qc.SUCCESS_STATES)
        self.assertTrue(all(item["status"] == "stale" for item in self.gates(self.sibling["id"], report)))

    def test_changed_link_membership_reopens_alignment_and_target(self):
        self.sibling["parentId"] = self.story["parentId"]
        child = copy.deepcopy(next(item for item in self.doc["elements"] if item["elementType"] == "acceptance_criterion"))
        child["id"] = "new-criterion"
        child["parentId"] = self.sibling["id"]
        self.doc["elements"].append(child)
        self.assertEqual([item["checkId"] for item in self.gates(self.sibling["id"]) if item["status"] == "stale"], ["profile.planning.user_story.01"])

    def test_public_binding_helper_refuses_unknown_or_wrong_level_target(self):
        for target in (("missing", None, "profile.planning.user_story.00"), (self.story["id"], "vision.description", "vision.description.clear"), (None, None, "unknown-check")):
            with self.assertRaises(ValueError):
                qc.check_subject_fingerprint(self.doc, self.catalogue, *target)

    def test_current_failed_review_routes_to_repair_with_the_actual_finding(self):
        review = next(item for item in self.doc["reviews"] if item["elementId"] == self.story["id"])
        review["status"] = "failed"
        review["rationale"] = "The source requires a reservation limit, but the story leaves that limit undefined."
        result = next(item for item in self.report()["checks"] if item["checkId"] == review["checkId"] and item["elementId"] == self.story["id"])
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["resolutionKind"], "author_repair_or_owner_decision")
        self.assertIn(review["rationale"], result["reason"])


class TrustAndInputTests(unittest.TestCase):
    def test_real_advisory_receipt_survives_queue_bookkeeping_but_not_changed_verdict(self):
        catalogue, doc = fixture(profile_catalogue(), real=True, assessment_mode="profile")
        trust = trust_fixture(catalogue, doc)
        doc["revision"] += 1
        doc["changeReason"] = "Record an answered decision without modifying product content."
        doc["questionDecisionVersions"] = {"unrelated-owner-question": 2}
        report = qc.Checker(catalogue, doc, trust_store=trust).run()
        self.assertEqual(report["qualityState"]["status"], "stage_checks_satisfied")
        doc["reviews"][0]["status"] = "failed"
        report = qc.Checker(catalogue, doc, trust_store=trust).run()
        self.assertNotIn(report["qualityState"]["status"], qc.SUCCESS_STATES)
        self.assertTrue(any(item["checkId"] == "external_review_verification" and item["status"] == "missing" for item in report["checks"]))

    def test_hierarchy_reviewer_cannot_be_any_scoped_author_or_have_narrow_rights(self):
        catalogue, doc = fixture()
        story = next(item for item in doc["elements"] if item["elementType"] == "user_story")
        story["authorId"] = "story-author"
        doc["authorities"].append({"id": "story-author", "permissions": ["quality_review"], "elementIds": ["*"], "authoritySource": "Synthetic registry proof."})
        hierarchy = next(review for review in doc["reviews"] if review["elementId"] is None)
        hierarchy["reviewerId"] = "story-author"
        bind_scoped_reviews(catalogue, doc)
        report = qc.Checker(catalogue, doc).run()
        self.assertEqual(next(item for item in report["checks"] if item["checkId"] == "hierarchy.coherent")["status"], "invalid")
        hierarchy["reviewerId"] = "fixture-reviewer"
        doc["authorities"][0]["elementIds"] = [story["id"]]
        bind_scoped_reviews(catalogue, doc)
        report = qc.Checker(catalogue, doc).run()
        reason = next(item for item in report["checks"] if item["checkId"] == "hierarchy.coherent")["reason"]
        self.assertIn("every assessed element", reason)

    def test_approved_element_and_placeholder_approval_reference_are_refused(self):
        catalogue, doc = fixture(profile_catalogue(), assessment_mode="profile")
        doc["elements"][0]["approvalStatus"] = "approved"
        doc["elements"][0]["approvalReference"] = "TBD by owner"
        refresh_reviews(catalogue, doc)
        report = qc.Checker(catalogue, doc).run()
        self.assertNotIn(report["qualityState"]["status"], qc.SUCCESS_STATES)
        candidate = copy.deepcopy(doc)
        candidate["revision"] += 1
        candidate["changeReason"] = "Attempt approved content overwrite."
        candidate["elements"][0]["fields"]["vision.description"]["value"] += " Overwrite."
        with self.assertRaises(ValueError):
            qc.protect_revision(doc, candidate)

    def test_placeholder_checks_distinguish_unresolved_values_from_confirmed_absence(self):
        for value in ("TBD by product owner", "Owner: TBD", "Pending decision from accountable owner", "Approver: unknown", "None"):
            self.assertFalse(qc.resolved(value), value)
        self.assertTrue(qc.resolved("None — no external dependencies (confirmed with platform team)"))

    def test_exact_blocking_cycle_path_and_nonblocking_design_references(self):
        catalogue, doc = fixture(profile_catalogue(), assessment_mode="profile")
        first, second = doc["elements"][:2]
        first["dependencyIds"], second["dependencyIds"] = [second["id"]], [first["id"]]
        refresh_reviews(catalogue, doc)
        report = qc.Checker(catalogue, doc).run()
        result = next(item for item in report["checks"] if item["checkId"] == "acyclic_dependencyIds")
        self.assertEqual(result["status"], "invalid")
        self.assertIn(first["id"] + " -> " + second["id"] + " -> " + first["id"], result["reason"])
        first["dependencyIds"], second["dependencyIds"] = [], []
        first["designDependencyIds"], second["designDependencyIds"] = [second["id"]], [first["id"]]
        refresh_reviews(catalogue, doc)
        self.assertEqual(qc.Checker(catalogue, doc).run()["qualityState"]["status"], "synthetic_checks_satisfied")

    def test_malformed_documents_fail_cli_with_exit_three_and_no_traceback(self):
        catalogue, doc = fixture(profile_catalogue(), assessment_mode="profile")
        malformed = [[], {**doc, "scope": "full"}, {**doc, "elements": "items"}, {**doc, "reviews": ["wrong"]}]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            qc.write_json(root / "catalogue.json", catalogue)
            for supplied in malformed:
                qc.write_json(root / "document.json", supplied)
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr):
                    code = qc.main(["--catalogue", str(root / "catalogue.json"), "check", "--document", str(root / "document.json"), "--report", str(root / "report.json"), "--allow-synthetic"])
                self.assertEqual(code, 3)
                self.assertNotIn("Traceback", stderr.getvalue())

    def test_synthetic_cli_requires_explicit_flag_and_uses_fixture_status(self):
        catalogue, doc = fixture(profile_catalogue(), assessment_mode="profile")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            qc.write_json(root / "catalogue.json", catalogue)
            qc.write_json(root / "document.json", doc)
            args = ["--catalogue", str(root / "catalogue.json"), "check", "--document", str(root / "document.json"), "--report", str(root / "report.json")]
            with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(qc.main(args), 3)
                self.assertEqual(qc.main(args + ["--allow-synthetic"]), 0)
            report = qc.read_json(root / "report.json")
            self.assertEqual(report["qualityState"]["status"], "synthetic_checks_satisfied")
            self.assertTrue(report["reviewerAuthentication"]["advisoryOnly"])
            self.assertFalse(report["qualityState"]["certificationGranted"])


if __name__ == "__main__":
    unittest.main()
