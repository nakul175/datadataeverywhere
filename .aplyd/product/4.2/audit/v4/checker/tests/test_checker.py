"""Synthetic behavioural tests: these results do not certify actual product records."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / "quality_checker.py"
sys.path.insert(0, str(MODULE.parent))
spec = importlib.util.spec_from_file_location("quality_checker", MODULE)
qc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qc)


def small_catalogue():
    fields = []
    for kind in ("common", *qc.ELEMENT_TYPES):
        field_id = kind + ".description"
        checks = [{"id": field_id + ".present", "dimension": "completeness", "mode": "structural", "structuralRule": "nonempty", "passCriterion": "Explicit nonempty detail.", "evidenceRequirement": "Current field content."},
                  {"id": field_id + ".clear", "dimension": "clarity", "mode": "review", "passCriterion": "Specific, unambiguous description backed by cited source.", "evidenceRequirement": "Independent rationale and current evidence snapshot."}]
        fields.append({"id": field_id, "element": kind, "label": "Description", "requiredness": {"policy": "always"}, "checks": checks})
    return {"schemaVersion": "1.0", "fields": fields, "elementChecks": [{"id": "element.traceable", "element": "all", "mode": "review", "dimension": "traceability", "passCriterion": "Every field traces to this item's actual source.", "evidenceRequirement": "Explicit field-to-source matrix."}],
            "hierarchyChecks": [{"id": "hierarchy.coherent", "mode": "review", "dimension": "consistency", "passCriterion": "Parent goals, children and scope are consistent.", "evidenceRequirement": "Review of the complete scoped hierarchy."}]}


def profile_catalogue():
    catalogue = small_catalogue()
    catalogue["fields"].append({"id": "user_story.delivery_evidence", "element": "user_story", "label": "Operational delivery evidence", "valueType": "text", "requiredness": {"policy": "always"}, "checks": [{"id": "user_story.delivery_evidence.present", "mode": "structural", "passCriterion": "Retained observed evidence.", "evidenceRequirement": "Observed release record."}]})
    catalogue["profileChecks"] = []
    stages = {}
    for stage in qc.REVIEW_STAGES:
        types = {}
        for kind in qc.ELEMENT_TYPES:
            ids = []
            for index in range(7):
                check_id = "profile.%s.%s.%02d" % (stage, kind, index)
                fields = ["common.description", kind + ".description"]
                if stage == "delivery" and kind == "user_story" and index == 0:
                    fields.append("user_story.delivery_evidence")
                catalogue["profileChecks"].append({"id": check_id, "mode": "review", "dimension": "semantic", "severity": "critical", "scope": "profile", "profile_stage": stage, "applicable_types": [kind], "requiredFieldIds": fields, "passCriterion": "Current %s %s gate %s matches scope and retained evidence, including every applicable protected safety obligation." % (stage, kind, index), "evidenceRequirement": "Independent source comparison and current retained stage evidence."})
                ids.append(check_id)
            types[kind] = ids
        stages[stage] = {"types": types}
    catalogue["review_profiles"] = {"version": "1.0", "default_stage": "planning", "sample_limit": 2, "stages": stages}
    return catalogue


def fixture(catalogue=None, real=False, assessment_mode="exhaustive", stage="planning"):
    catalogue = catalogue or small_catalogue()
    doc = qc.scaffold(catalogue, "SYNTHETIC-WORKSHOP", "fixture-author", "real" if real else "synthetic_fixture", assessment_mode, stage)
    source = doc["sources"][0]
    source.update(text="Synthetic workshop plan: participants register, reserve a session and receive a confirmation within the controlled fixture environment. No actual users or recipients.", version="fixture-1", originality="original", protected=True)
    doc["sourcePins"] = {source["id"]: qc.source_hash(source)}
    doc["productProfile"] = {branch: {"applicability": "no", "sourceIds": [source["id"]], "rationale": "Synthetic mechanics fixture excludes product-runtime AI and actual personal data; test labels are generated identifiers, not actual participants."} for branch in ("ai", "personalData")}
    doc["authorities"] = [{"id": "fixture-reviewer", "kind": "independent_ai", "permissions": ["quality_review"], "elementIds": ["*"], "authoritySource": "Synthetic test harness registry, not an actual identity or approval."}]
    for element in doc["elements"]:
        for field_id in element["fields"]:
            element["fields"][field_id]["value"] = element["id"] if field_id == "common.id" else "Synthetic %s %s: workshop registration scope, existing fixture session identifiers, source fixture-1 and explicit observable outcome." % (element["elementType"], field_id)
    artifact = {"id": "fixture-audit", "kind": "independent_review_snapshot", "description": "Synthetic audit matrix exercising checker mechanics. Its verdicts are deliberately generated test fixtures and do not assess real quality.", "origin": "Local synthetic fixture generator", "syntheticFixture": not real,
                "content": {"label": "SYNTHETIC TEST ONLY", "coveredElements": [element["id"] for element in doc["elements"]], "method": "This fixture tests schema validation, fingerprints, evidence and gates, not semantic truth."}}
    artifact["contentHash"] = qc.evidence_hash(artifact, ".")
    doc["evidence"] = [artifact]
    refresh_reviews(catalogue, doc)
    return catalogue, doc


def refresh_reviews(catalogue, doc):
    doc["catalogueHash"] = qc.digest(catalogue)
    fingerprint = qc.subject_fingerprint(doc, catalogue)
    for item in doc["evidence"]:
        item["boundTo"] = fingerprint
    reviews = []
    def add(element, field, check):
        reviews.append({"id": "fixture-review-%04d" % len(reviews), "elementId": element["id"] if element else None, "fieldId": field["id"] if field else None, "checkId": check["id"],
                        "status": "passed", "reviewerId": "fixture-reviewer", "independent": True, "subjectFingerprint": fingerprint,
                        "evidenceIds": ["fixture-audit"], "rationale": "SYNTHETIC generated verdict for gate tests; not a real semantic review. Criterion: " + check["passCriterion"]})
    selection = qc.assessment_selection(catalogue, doc)
    if selection["mode"] == "profile":
        for element in doc["elements"]:
            for check in selection["checks"][element["elementType"]]:
                add(element, None, check)
        doc["reviews"] = reviews
        bind_scoped_reviews(catalogue, doc)
        return
    for element in doc["elements"]:
        for field in catalogue["fields"]:
            if field["element"] in {"common", element["elementType"]}:
                for check in field["checks"]:
                    if check["mode"] == "review":
                        add(element, field, check)
        for check in catalogue.get("elementChecks", []):
            if check.get("element", "all") in {"all", "common", element["elementType"]}:
                add(element, None, check)
    for check in catalogue.get("hierarchyChecks", []):
        add(None, None, check)
    doc["reviews"] = reviews
    bind_scoped_reviews(catalogue, doc)


def bind_scoped_reviews(catalogue, doc):
    """Synthetic harness binding only; deliberately not a production auto-review."""
    for item in doc["evidence"]:
        item["bindings"] = []
    checker = qc.Checker(catalogue, doc)
    for review in doc["reviews"]:
        target = (review.get("elementId"), review.get("fieldId"), review.get("checkId"))
        fingerprint = qc.digest(checker.scoped_payload(target))
        review["bindingVersion"] = "scoped-v1"
        review["subjectFingerprint"] = fingerprint
        for evidence_id in review.get("evidenceIds", []):
            item = next(item for item in doc["evidence"] if item["id"] == evidence_id)
            item["bindings"].append({"bindingVersion": "scoped-v1", "elementId": target[0], "fieldId": target[1], "checkId": target[2], "subjectFingerprint": fingerprint})


def trust_fixture(catalogue, doc):
    return {"catalogueHash": qc.digest(catalogue), "sourcePins": copy.deepcopy(doc["sourcePins"]), "authorities": copy.deepcopy(doc["authorities"]),
            "reviewVerifications": [{"bindingVersion": "scoped-v1", "subjectFingerprint": qc.review_set_fingerprint(doc, catalogue), "verificationMethod": "independent_agent_review", "independent": True,
                                     "verifierId": "fixture-reviewer", "reviewHashes": sorted(qc.digest(review) for review in doc["reviews"]), "verificationRecord": "SYNTHETIC receipt testing external-import format only; no actual authority granted."}]}


class CheckerTests(unittest.TestCase):
    def setUp(self):
        self.catalogue, self.doc = fixture()

    def check(self, doc=None, catalogue=None, trust=None):
        return qc.Checker(catalogue or self.catalogue, doc or self.doc, trust_store=trust).run()

    def assertNotTop(self, report):
        self.assertNotIn(report["qualityState"]["status"], qc.SUCCESS_STATES)

    def test_complete_fixture_is_labelled_and_all_applicable_checks_pass(self):
        report = self.check()
        self.assertEqual(report["qualityState"]["status"], "synthetic_checks_satisfied")
        self.assertIn("SYNTHETIC", report["assurance"])
        self.assertIsNone(report["qualityState"]["score"])
        self.assertEqual(report["qualityState"]["passed"], report["qualityState"]["applicable"])

    def test_service_context_needs_no_software_delivery_claim_and_changes_reopen_review(self):
        source = self.doc["sources"][0]
        source["text"] += " Product context: facilitated workshop service, no software deliverable; launch requires rehearsal and pilot observations, currently not run."
        self.doc["sourcePins"][source["id"]] = qc.source_hash(source)
        self.doc["readinessState"] = {"status": "not_assessed", "reason": "Facilitator and venue readiness not assessed."}
        self.doc["deliveryState"] = {"status": "not_run", "launchRoute": "Controlled rehearsal and pilot observations."}
        refresh_reviews(self.catalogue, self.doc)
        report = self.check()
        self.assertEqual(report["qualityState"]["status"], "synthetic_checks_satisfied")
        self.assertFalse(report["deliveryState"]["deliveryObservedByChecker"])
        self.assertEqual(report["deliveryState"]["suppliedClaim"]["status"], "not_run")
        source["text"] += " Revised material requirement: participants must also reserve equipment."
        self.doc["sourcePins"][source["id"]] = qc.source_hash(source)
        report = self.check()
        self.assertNotTop(report)
        self.assertGreater(report["qualityState"]["counts"]["stale"], 0)

    def test_blank_whitespace_placeholder_never_pass(self):
        for value in ("", " \n\t", "Pending", "Pending: assigned owner", "[TBD]", None):
            doc = copy.deepcopy(self.doc)
            doc["elements"][0]["fields"]["vision.description"]["value"] = value
            refresh_reviews(self.catalogue, doc)
            self.assertNotTop(self.check(doc))

    def test_missing_semantic_review_cannot_be_replaced_by_structural_checks(self):
        self.doc["reviews"] = []
        self.assertNotTop(self.check())

    def test_self_review_rejected_even_when_passed(self):
        self.doc["reviews"][0]["reviewerId"] = self.doc["authorId"]
        self.assertNotTop(self.check())

    def test_reviewer_boolean_trusted_does_not_grant_registry_authority(self):
        self.doc["reviews"][0]["reviewerId"] = "made-up-person"
        self.doc["reviews"][0]["trusted"] = True
        self.assertNotTop(self.check())

    def test_one_failed_check_cannot_hide_in_average(self):
        self.doc["reviews"][0]["status"] = "failed"
        report = self.check()
        self.assertNotTop(report)
        self.assertGreater(report["qualityState"]["passed"], 20)

    def test_edit_invalidates_all_cross_hierarchy_reviews(self):
        self.doc["elements"][0]["fields"]["vision.description"]["value"] += " material additional scope"
        report = self.check()
        self.assertNotTop(report)
        self.assertGreater(report["qualityState"]["counts"]["stale"], 10)

    def test_source_or_approval_change_invalidates_evidence(self):
        for key, value in (("sources", "change"), ("approvalRecords", "change")):
            doc = copy.deepcopy(self.doc)
            if key == "sources":
                doc["sources"][0]["text"] += " changed scope"
            else:
                doc["approvalRecords"] = [{"id": "DEC-1", "status": "withdrawn"}]
            self.assertNotTop(self.check(doc))

    def test_catalogue_removal_or_new_threshold_requires_revision_and_review(self):
        catalogue = copy.deepcopy(self.catalogue)
        catalogue["fields"][0]["checks"].pop()
        self.assertNotTop(self.check(catalogue=catalogue))
        catalogue = copy.deepcopy(self.catalogue)
        catalogue["fields"][0]["checks"][1]["passCriterion"] += " with a revised approved target"
        self.assertNotTop(self.check(catalogue=catalogue))

    def test_duplicate_and_orphan_and_cycle_fail(self):
        duplicate = copy.deepcopy(self.doc)
        duplicate["elements"].append(copy.deepcopy(duplicate["elements"][0]))
        self.assertNotTop(self.check(duplicate))
        orphan = copy.deepcopy(self.doc)
        orphan["elements"][2]["parentId"] = "does-not-exist"
        self.assertNotTop(self.check(orphan))
        cyclic = copy.deepcopy(self.doc)
        cyclic["elements"][0]["dependencyIds"] = [cyclic["elements"][1]["id"]]
        cyclic["elements"][1]["dependencyIds"] = [cyclic["elements"][0]["id"]]
        self.assertNotTop(self.check(cyclic))

    def test_unknown_and_duplicate_reviews_fail(self):
        self.doc["reviews"].append(copy.deepcopy(self.doc["reviews"][0]))
        self.assertNotTop(self.check())
        _, self.doc = fixture()
        self.doc["reviews"][0]["checkId"] = "invented-check"
        self.assertNotTop(self.check())

    def test_wrong_level_field_is_rejected(self):
        self.doc["elements"][0]["fields"]["strategy.description"] = {"value": "A misplaced strategy field."}
        self.assertNotTop(self.check())

    def test_known_check_at_wrong_review_target_is_rejected(self):
        for modification in ({"fieldId": None}, {"checkId": "hierarchy.coherent", "fieldId": None}, {"elementId": None, "fieldId": None, "checkId": "element.traceable"}):
            doc = copy.deepcopy(self.doc)
            extra = copy.deepcopy(doc["reviews"][0])
            extra["id"] = "fixture-extra-invalid-target"
            extra.update(modification)
            doc["reviews"].append(extra)
            self.assertNotTop(self.check(doc))

    def test_text_value_type_cannot_be_faked_by_true_or_object(self):
        for value in (True, {"passed": True}):
            doc = copy.deepcopy(self.doc)
            doc["elements"][0]["fields"]["vision.description"]["value"] = value
            refresh_reviews(self.catalogue, doc)
            self.assertNotTop(self.check(doc))

    def test_real_input_local_names_or_fixture_evidence_not_enough(self):
        catalogue, doc = fixture(real=True)
        self.assertNotTop(qc.Checker(catalogue, doc).run())
        trust = trust_fixture(catalogue, doc)
        report = qc.Checker(catalogue, doc, trust_store=trust).run()
        self.assertEqual(report["qualityState"]["status"], "advisory_checks_satisfied")
        self.assertTrue(report["reviewerAuthentication"]["advisoryOnly"])
        self.assertFalse(report["qualityState"]["certificationGranted"])
        self.assertIn("does not authenticate", report["assurance"])
        doc["evidence"][0]["syntheticFixture"] = True
        self.assertNotTop(qc.Checker(catalogue, doc, trust_store=trust).run())

    def test_real_source_local_repin_not_external_baseline_proof(self):
        catalogue, doc = fixture(real=True)
        trust = trust_fixture(catalogue, doc)
        doc["sources"][0]["text"] += " changed original"
        doc["sourcePins"]["source-001"] = qc.source_hash(doc["sources"][0])
        refresh_reviews(catalogue, doc)
        trust["reviewVerifications"] = trust_fixture(catalogue, doc)["reviewVerifications"]
        self.assertNotTop(qc.Checker(catalogue, doc, trust_store=trust).run())

    def test_evidence_hash_mismatch_urls_only_and_traversal_fail(self):
        for alteration in ("mismatch", "url", "traversal"):
            doc = copy.deepcopy(self.doc)
            if alteration == "mismatch":
                doc["evidence"][0]["contentHash"] = "fabricated"
            elif alteration == "url":
                doc["evidence"][0].pop("content")
                doc["evidence"][0]["url"] = "https://example.invalid/no-retained-proof"
            else:
                doc["evidence"][0].pop("content")
                doc["evidence"][0]["assetPath"] = "../../secret"
            self.assertNotTop(self.check(doc))

    def test_na_not_a_bypass_for_always_required_or_unreviewed(self):
        self.doc["elements"][0]["fields"]["vision.description"]["applicability"] = "not_applicable"
        self.assertNotTop(self.check())
        self.catalogue["fields"][1]["requiredness"]["policy"] = "conditional"
        refresh_reviews(self.catalogue, self.doc)
        self.assertNotTop(self.check())

    def test_conditional_na_requires_exact_review_for_each_check(self):
        self.catalogue["fields"][1]["requiredness"]["policy"] = "conditional"
        self.doc["elements"][0]["fields"]["vision.description"]["applicability"] = "not_applicable"
        refresh_reviews(self.catalogue, self.doc)
        existing = next(review for review in self.doc["reviews"] if review["fieldId"] == "vision.description")
        existing.update(status="not_applicable", scopeJustification="This synthetic conditional field is out of declared fixture scope; source fixture-1 confirms it.")
        structural = copy.deepcopy(existing)
        structural["id"] = "fixture-na-structural"
        structural["checkId"] = "vision.description.present"
        self.doc["reviews"].append(structural)
        bind_scoped_reviews(self.catalogue, self.doc)
        self.assertEqual(self.check()["qualityState"]["status"], "synthetic_checks_satisfied")

    def test_no_scope_or_missing_level_is_not_full_hierarchy_pass(self):
        self.doc.pop("scope")
        self.assertNotTop(self.check())
        _, self.doc = fixture()
        self.doc["elements"].pop()
        self.assertNotTop(self.check())

    def test_readiness_and_delivery_claims_remain_unverified(self):
        self.doc["readinessState"] = {"status": "ready"}
        self.doc["deliveryState"] = {"status": "delivered", "deployment": "pretend-sha"}
        refresh_reviews(self.catalogue, self.doc)
        report = self.check()
        self.assertEqual(report["readinessState"]["status"], "supplied_unverified")
        self.assertEqual(report["deliveryState"]["status"], "supplied_unverified")
        self.assertFalse(report["readinessState"]["authorizationGranted"])

    def test_unanswered_questions_dedupe_and_field_factors_consolidate(self):
        # An absent fact creates a clarification; an absent review creates work
        # for a reviewer. A generated packet is not a shown/answered packet.
        self.doc["elements"][0]["fields"]["vision.description"]["value"] = ""
        refresh_reviews(self.catalogue, self.doc)
        report = self.check()
        first, state = qc.question_packet(report, self.doc, batch_size=100)
        second, state = qc.question_packet(report, self.doc, state, batch_size=100)
        self.assertEqual(first["newQuestionCount"], 1)
        self.assertEqual(second["newQuestionCount"], 0)
        self.assertEqual(first["currentBatchId"], second["currentBatchId"])
        self.assertEqual([item["id"] for item in first["nextBatch"]], [item["id"] for item in second["nextBatch"]])
        self.assertEqual(len(first["nextBatch"][0]["checksToResolve"]), 2)
        self.assertEqual(first["nextBatch"][0]["presentedCount"], 0)
        self.assertEqual(first["pendingQuestionCount"], second["pendingQuestionCount"])
        _, present_facts = fixture()
        present_facts["reviews"] = []
        review_packet, _ = qc.question_packet(self.check(present_facts), present_facts)
        self.assertEqual(review_packet["nextBatch"], [])
        self.assertGreater(review_packet["reviewerQueueCount"], 0)
        self.assertEqual(review_packet["loopStatus"], "needs_review")

    def test_cosmetic_rewrite_does_not_create_new_question(self):
        self.doc["elements"][0]["fields"]["vision.description"]["value"] = "Pending: the workshop's exclusion boundary is unspecified."
        refresh_reviews(self.catalogue, self.doc)
        first, state = qc.question_packet(self.check(), self.doc, batch_size=100)
        self.assertGreater(first["pendingQuestionCount"], 0)
        self.doc["elements"][0]["fields"]["vision.description"]["value"] = "Pending: equivalent editorial wording of the same missing workshop exclusion boundary."
        second, state = qc.question_packet(self.check(), self.doc, state, batch_size=100)
        self.assertEqual(second["newQuestionCount"], 0)
        self.assertEqual(first["nextBatch"][0]["id"], second["nextBatch"][0]["id"])

    def test_unrelated_source_change_does_not_reissue_same_decision(self):
        self.doc["elements"][0]["fields"]["vision.description"]["value"] = "Pending: actual workshop exclusion boundary."
        refresh_reviews(self.catalogue, self.doc)
        first, state = qc.question_packet(self.check(), self.doc, batch_size=100)
        self.assertGreater(first["pendingQuestionCount"], 0)
        source = {"id": "unrelated-source", "text": "Synthetic unrelated context; not an authority or policy for the existing workshop decision.", "version": "fixture-1", "originality": "original", "approvalStatus": "draft", "protected": True}
        self.doc["sources"].append(source)
        self.doc["sourcePins"][source["id"]] = qc.source_hash(source)
        packet, state = qc.question_packet(self.check(), self.doc, state, batch_size=100)
        self.assertEqual(packet["newQuestionCount"], 0)
        self.assertEqual(first["nextBatch"][0]["id"], packet["nextBatch"][0]["id"])

    def test_answer_not_quality_pass_and_unlimited_followup_rounds(self):
        from quality_loop import write_state
        self.doc["elements"][0]["fields"]["vision.description"]["value"] = "Pending: actual workshop scope boundary."
        refresh_reviews(self.catalogue, self.doc)
        report = self.check()
        packet, state = qc.question_packet(report, self.doc, batch_size=100)
        current = packet["nextBatch"][0]["id"]
        with tempfile.TemporaryDirectory() as directory:
            for round_number in range(7):
                write_state(directory, state, api=qc)
                qc.record_answer(directory, current, "We need another specific detail from the fixture decision owner.", "fixture-respondent", "needs_clarification", "The scope boundary is still unspecified.")
                state = qc.read_json(Path(directory) / "loop-state.json")
                packet, state = qc.question_packet(report, self.doc, state, batch_size=100)
                self.assertEqual(packet["loopStatus"], "needs_input")
                followups = [item for item in packet["nextBatch"] if item.get("followUpTo") == current]
                self.assertEqual(len(followups), 1)
                current = followups[0]["id"]
            self.assertEqual(len(state["answers"]), 7)

    def test_resolved_and_superseded_question_history_retained(self):
        original = copy.deepcopy(self.doc)
        self.doc["elements"][0]["fields"]["vision.description"]["value"] = "Pending: actual workshop scope boundary."
        refresh_reviews(self.catalogue, self.doc)
        packet, state = qc.question_packet(self.check(), self.doc, batch_size=100)
        field_question = next(item for item in packet["nextBatch"] if item["fieldId"] == "vision.description")
        self.doc["elements"][0]["fields"]["vision.description"]["value"] = "Pending: revised material scope boundary decision."
        self.doc["questionDecisionVersions"] = {field_question["groupId"]: 2}
        _, state = qc.question_packet(self.check(), self.doc, state, batch_size=100)
        self.assertEqual(state["questions"][field_question["id"]]["status"], "superseded")
        final, state = qc.question_packet(self.check(original), original, state)
        self.assertEqual(final["loopStatus"], "synthetic_complete")
        self.assertTrue(any(item["status"] == "resolved" for item in state["questions"].values()))
        regressed, state = qc.question_packet(self.check(), self.doc, state, batch_size=100)
        self.assertGreater(regressed["pendingQuestionCount"], 0)
        self.assertTrue(any(item.get("regressionOf") for item in regressed["nextBatch"]))

    def test_protected_source_frozen_element_and_protected_field_cannot_change(self):
        for kind in ("source", "frozen", "field"):
            old = copy.deepcopy(self.doc)
            if kind == "frozen":
                old["elements"][0]["approvalStatus"] = "frozen"
            if kind == "field":
                old["elements"][0]["fields"]["vision.description"]["protected"] = True
            candidate = copy.deepcopy(old)
            candidate["revision"] += 1
            candidate["changeReason"] = "Attempt a protected rewrite; it must be refused."
            if kind == "source":
                candidate["sources"][0]["text"] += " overwrite"
                candidate["sourcePins"]["source-001"] = qc.source_hash(candidate["sources"][0])
            else:
                candidate["elements"][0]["fields"]["vision.description"]["value"] += " overwrite"
            with self.assertRaises(ValueError):
                qc.protect_revision(old, candidate)

    def test_revision_helper_preserves_snapshot_and_invalidates_review(self):
        with tempfile.TemporaryDirectory() as directory:
            current, candidate = Path(directory) / "current.json", Path(directory) / "candidate.json"
            qc.write_json(current, self.doc)
            changed = copy.deepcopy(self.doc)
            changed["revision"] += 1
            changed["changeReason"] = "Clarify the synthetic workshop capacity boundary."
            changed["elements"][0]["fields"]["vision.description"]["value"] += " revised scope"
            qc.write_json(candidate, changed)
            result = qc.apply_revision(current, candidate, Path(directory) / "history")
            self.assertTrue(Path(result["preservedSnapshot"]).exists())
            self.assertEqual(qc.read_json(result["preservedSnapshot"])["revision"], 1)
            self.assertNotTop(self.check(qc.read_json(current)))

    def test_unsupported_catalogue_rule_is_blocked_not_fallback_pass(self):
        self.catalogue["fields"][0]["checks"][0]["structuralRule"] = "imaginary-semantic-autocertify"
        self.assertTrue(qc.catalogue_errors(self.catalogue))
        self.assertNotTop(self.check())


class StageProfileTests(unittest.TestCase):
    def setUp(self):
        self.catalogue, self.doc = fixture(profile_catalogue(), assessment_mode="profile")

    def report(self):
        return qc.Checker(self.catalogue, self.doc).run()

    def test_default_workload_is_56_verdicts_and_at_most_16_advisory_samples(self):
        self.assertEqual(len(self.doc["reviews"]), 56)
        report = self.report()
        self.assertEqual(report["qualityState"]["status"], "synthetic_checks_satisfied")
        self.assertEqual(report["assessmentCoverage"]["selectedMandatoryReviewCount"], 56)
        self.assertLessEqual(report["assessmentCoverage"]["advisorySampleCount"], 16)
        self.assertFalse(report["assessmentCoverage"]["referenceChecksFullyAssessed"])
        self.assertGreater(report["assessmentCoverage"]["referenceInstancesDeferred"], 0)

    def test_blank_initial_profile_has_bounded_questions_and_no_future_stage_questions(self):
        doc = qc.scaffold(self.catalogue, "SYNTHETIC-PENDING", "fixture-author", "synthetic_fixture")
        report = qc.Checker(self.catalogue, doc).run()
        packet, _ = qc.question_packet(report, doc, batch_size=100)
        self.assertLessEqual(packet["newQuestionCount"], 64)
        self.assertTrue(all("profile.delivery." not in item["checkId"] and "profile.learning." not in item["checkId"] for item in packet["nextBatch"]))

    def test_planning_does_not_require_future_operational_evidence(self):
        story = next(element for element in self.doc["elements"] if element["elementType"] == "user_story")
        story["fields"].pop("user_story.delivery_evidence")
        refresh_reviews(self.catalogue, self.doc)
        self.assertEqual(self.report()["qualityState"]["status"], "synthetic_checks_satisfied")
        self.doc["assessment"]["stage"] = "delivery"
        refresh_reviews(self.catalogue, self.doc)
        self.assertNotIn(self.report()["qualityState"]["status"], qc.SUCCESS_STATES)

    def test_unknown_profile_is_blocked_never_falls_back_to_reference_pass(self):
        self.doc["assessment"]["stage"] = "pretend-ready"
        report = self.report()
        self.assertEqual(report["qualityState"]["status"], "blocked")

    def test_legacy_document_defaults_to_planning_with_explicit_coverage_warning(self):
        self.doc.pop("assessment")
        refresh_reviews(self.catalogue, self.doc)
        report = self.report()
        self.assertEqual(report["qualityState"]["status"], "synthetic_checks_satisfied")
        self.assertIn("not a full-reference", report["assessmentCoverage"]["legacyDefaultWarning"])

    def test_sample_can_never_substitute_for_missing_or_failed_mandatory_gate(self):
        target = self.report()["advisorySamples"][0]
        sample = copy.deepcopy(self.doc["reviews"][0])
        sample.update(id="sample-verdict", elementId=target["elementId"], fieldId=target["fieldId"], checkId=target["checkId"])
        self.doc["reviews"].pop(0)
        self.doc["reviews"].append(sample)
        self.assertNotIn(self.report()["qualityState"]["status"], qc.SUCCESS_STATES)
        refresh_reviews(self.catalogue, self.doc)
        self.doc["reviews"][0]["status"] = "failed"
        self.assertNotIn(self.report()["qualityState"]["status"], qc.SUCCESS_STATES)

    def test_advisory_missing_not_owner_questions_but_mandatory_defect_escalates(self):
        first = self.report()
        packet, _ = qc.question_packet(first, self.doc)
        self.assertEqual(packet["newQuestionCount"], 0)
        self.assertGreater(first["assessmentCoverage"]["advisoryUnreviewedCount"], 0)
        target = first["advisorySamples"][0]
        sample = copy.deepcopy(self.doc["reviews"][0])
        sample.update(id="critical-sample", elementId=target["elementId"], fieldId=target["fieldId"], checkId=target["checkId"], status="failed", mandatoryDefect=True)
        self.doc["reviews"].append(sample)
        report = self.report()
        self.assertNotIn(report["qualityState"]["status"], qc.SUCCESS_STATES)
        self.assertTrue(any(item["checkId"].startswith("sample_escalation_") for item in report["checks"]))

    def test_sample_selection_deterministic_and_at_most_two_per_level(self):
        first = self.report()["advisorySamples"]
        self.assertEqual(first, self.report()["advisorySamples"])
        story = next(element for element in self.doc["elements"] if element["elementType"] == "user_story")
        for index in range(20):
            extra = copy.deepcopy(story)
            extra["id"] = "user-story-extra-" + str(index)
            self.doc["elements"].append(extra)
        refresh_reviews(self.catalogue, self.doc)
        report = self.report()
        self.assertEqual(report["assessmentCoverage"]["selectedMandatoryReviewCount"], 56 + 20 * 7)
        self.assertLessEqual(report["assessmentCoverage"]["advisorySampleCount"], 16)

    def test_runtime_ai_unknown_and_unsourced_no_are_unsampled_blockers(self):
        for decision in ({"applicability": "unknown"}, {"applicability": "no", "sourceIds": [], "rationale": "No evidence supplied."}):
            self.doc["productProfile"]["ai"] = decision
            refresh_reviews(self.catalogue, self.doc)
            self.assertNotIn(self.report()["qualityState"]["status"], qc.SUCCESS_STATES)

    def test_ai_no_cannot_contradict_pinned_required_branch_or_rewrite_protected_metadata(self):
        source = self.doc["sources"][0]
        source["requiredBranches"] = {"ai": True}
        self.doc["sourcePins"][source["id"]] = qc.source_hash(source)
        refresh_reviews(self.catalogue, self.doc)
        self.assertEqual(self.report()["qualityState"]["status"], "blocked")
        changed = copy.deepcopy(self.doc)
        changed["revision"] += 1
        changed["changeReason"] = "Attempt to remove protected AI requirement."
        changed["sources"][0]["requiredBranches"] = {}
        with self.assertRaises(ValueError):
            qc.protect_revision(self.doc, changed)

    def test_ai_yes_activates_unsampled_required_details(self):
        gate = next(check for check in self.catalogue["profileChecks"] if check["profile_stage"] == "planning" and check["applicable_types"] == ["user_story"])
        gate["conditionalFieldIds"] = {"ai": ["user_story.delivery_evidence"]}
        self.doc["productProfile"]["ai"]["applicability"] = "yes"
        story = next(element for element in self.doc["elements"] if element["elementType"] == "user_story")
        story["fields"].pop("user_story.delivery_evidence")
        refresh_reviews(self.catalogue, self.doc)
        self.assertNotIn(self.report()["qualityState"]["status"], qc.SUCCESS_STATES)

    def test_actual_catalogue_exhaustive_does_not_bypass_required_ai_or_active_na(self):
        actual = qc.read_json(MODULE.with_name("catalogue.json"))
        for malformed in (None, "yes", True):
            catalogue, doc = fixture(actual, assessment_mode="profile")
            doc["productProfile"]["ai"] = malformed
            self.assertEqual(qc.Checker(catalogue, doc).run()["qualityState"]["status"], "blocked")
        for choice in ("no", "unknown"):
            catalogue, doc = fixture(actual, assessment_mode="exhaustive")
            doc["sources"][0]["requiredBranches"] = {"ai": True}
            doc["sourcePins"]["source-001"] = qc.source_hash(doc["sources"][0])
            doc["productProfile"]["ai"]["applicability"] = choice
            refresh_reviews(catalogue, doc)
            self.assertNotIn(qc.Checker(catalogue, doc).run()["qualityState"]["status"], qc.SUCCESS_STATES)
        catalogue, doc = fixture(actual, assessment_mode="exhaustive")
        doc["productProfile"]["ai"]["applicability"] = "yes"
        element = doc["elements"][0]
        field_id = "common.ai_assurance_reference"
        element["fields"][field_id].update(applicability="not_applicable", scopeJustification="An attempted blanket exemption for active AI; it must fail.")
        refresh_reviews(catalogue, doc)
        field = next(field for field in catalogue["fields"] if field["id"] == field_id)
        for check in field["checks"]:
            review = next((review for review in doc["reviews"] if review["elementId"] == element["id"] and review["fieldId"] == field_id and review["checkId"] == check["id"]), None)
            if review is None:
                review = copy.deepcopy(doc["reviews"][0])
                review.update(id="attempt-active-na-" + check["id"], elementId=element["id"], fieldId=field_id, checkId=check["id"])
                doc["reviews"].append(review)
            review.update(status="not_applicable", scopeJustification="Attempt to waive all active assurance obligations.")
        self.assertNotIn(qc.Checker(catalogue, doc).run()["qualityState"]["status"], qc.SUCCESS_STATES)

    def test_discovery_unknown_needs_sourced_resolution_plan_and_then_later_stage_reopens(self):
        self.doc["assessment"]["stage"] = "discovery"
        self.doc["productProfile"]["ai"] = {"applicability": "unknown", "resolutionPlan": "Investigate runtime AI need without consequential evaluation."}
        refresh_reviews(self.catalogue, self.doc)
        self.assertNotIn(self.report()["qualityState"]["status"], qc.SUCCESS_STATES)
        self.doc["productProfile"]["ai"].update(sourceIds=["source-001"], rationale="The retained synthetic research scope requires resolving AI feasibility before commitment.")
        refresh_reviews(self.catalogue, self.doc)
        self.assertEqual(self.report()["qualityState"]["status"], "synthetic_checks_satisfied")
        self.doc["assessment"]["stage"] = "ready"
        refresh_reviews(self.catalogue, self.doc)
        self.assertNotIn(self.report()["qualityState"]["status"], qc.SUCCESS_STATES)

    def test_fabricated_offline_registry_never_authenticates_independence(self):
        catalogue, doc = fixture(profile_catalogue(), real=True, assessment_mode="profile")
        trust = trust_fixture(catalogue, doc)
        report = qc.Checker(catalogue, doc, trust_store=trust).run()
        self.assertEqual(report["qualityState"]["status"], "stage_checks_satisfied")
        self.assertTrue(report["reviewerAuthentication"]["advisoryOnly"])
        self.assertEqual(report["reviewerAuthentication"]["status"], "not_authenticated_offline")
        self.assertFalse(report["qualityState"]["certificationGranted"])
        self.assertIn("author can create", report["assurance"])

    def test_aliases_preserve_legacy_values_conflicts_block_and_migration_retires_verdicts(self):
        self.catalogue["fieldAliases"] = {"user_story.merge_sha": "user_story.delivery_evidence"}
        story = next(element for element in self.doc["elements"] if element["elementType"] == "user_story")
        story["fields"]["user_story.merge_sha"] = story["fields"].pop("user_story.delivery_evidence")
        refresh_reviews(self.catalogue, self.doc)
        self.assertEqual(self.report()["qualityState"]["status"], "synthetic_checks_satisfied")
        story["fields"]["user_story.delivery_evidence"] = {"value": "Conflicting release identifier."}
        self.assertEqual(self.report()["qualityState"]["status"], "blocked")
        story["fields"].pop("user_story.delivery_evidence")
        story["fields"]["user_story.merge_sha"]["protected"] = True
        original = copy.deepcopy(self.doc)
        with tempfile.TemporaryDirectory() as directory:
            old, new = Path(directory) / "legacy.json", Path(directory) / "current.json"
            qc.write_json(old, self.doc)
            result = qc.migrate_document(self.catalogue, old, new, Path(directory) / "history", reason="Adopt generic field mappings and stage review without changing protected content.")
            migrated = qc.read_json(new)
            self.assertEqual(qc.read_json(old), original)
            self.assertEqual(migrated["sourcePins"], original["sourcePins"])
            self.assertEqual(migrated["reviews"], [])
            self.assertEqual(next(element for element in migrated["elements"] if element["elementType"] == "user_story")["fields"]["user_story.merge_sha"], story["fields"]["user_story.merge_sha"])
            self.assertFalse(result["reviewReuseAllowed"])
            self.assertNotIn(qc.Checker(self.catalogue, migrated).run()["qualityState"]["status"], qc.SUCCESS_STATES)


if __name__ == "__main__":
    unittest.main()
