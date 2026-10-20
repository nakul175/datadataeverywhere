"""Actual shipped-engine catalogue guard tests, without the old toy-model mock.

All reviews, evidence and external-looking trust below are generated negative
mechanics fixtures. They neither authenticate a reviewer nor assess a product.
The fresh engine and actual CLI subprocess retain the production literal pin.
"""

import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


CHECKER = Path(__file__).resolve().parents[1]
if str(CHECKER) not in sys.path:
    sys.path.insert(0, str(CHECKER))
SPEC = importlib.util.spec_from_file_location("actual_catalogue_guard_engine", CHECKER / "quality_checker.py")
actual = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(actual)
import quality_tools
from test_checker import fixture, trust_fixture


def raw_check_index(catalogue):
    checks = [check for field in catalogue["fields"] for check in field["checks"]]
    checks += catalogue.get("elementChecks", []) + catalogue.get("hierarchyChecks", []) + catalogue.get("profileChecks", [])
    return {check["id"]: check for check in checks}


def author_repin_for_negative_test(catalogue, document):
    """Fabricate matching declarations as an author could, without assessing them.

    The private serialization primitive is deliberately used only to construct
    the hostile test input. Every public assessment/binding entry point remains
    guarded and must reject this candidate before accepting any declaration.
    """
    document = copy.deepcopy(document)
    catalogue_hash = actual.digest(catalogue)
    document["catalogueHash"] = catalogue_hash
    check_index = raw_check_index(catalogue)
    for evidence in document["evidence"]:
        evidence["bindings"] = []
    for review in document["reviews"]:
        target = (review.get("elementId"), review.get("fieldId"), review["checkId"])
        fingerprint = actual.digest(actual._check_subject_payload(
            document, catalogue, *target, catalogue_hash=catalogue_hash, check_index=check_index))
        review["bindingVersion"] = "scoped-v1"
        review["subjectFingerprint"] = fingerprint
        for evidence_id in review["evidenceIds"]:
            record = next(item for item in document["evidence"] if item["id"] == evidence_id)
            record["bindings"].append({"bindingVersion": "scoped-v1", "elementId": target[0],
                                       "fieldId": target[1], "checkId": target[2], "subjectFingerprint": fingerprint})
    entries = [{"id": review["id"], "reviewHash": actual.digest(review),
                "currentSubjectFingerprint": review["subjectFingerprint"]} for review in document["reviews"]]
    review_set_hash = actual.digest({"bindingVersion": "scoped-v1", "catalogueHash": catalogue_hash,
                                    "documentId": document["documentId"],
                                    "entries": sorted(entries, key=lambda item: str(item["id"]))})
    trust = {"catalogueHash": catalogue_hash, "sourcePins": copy.deepcopy(document["sourcePins"]),
             "authorities": copy.deepcopy(document["authorities"]),
             "reviewVerifications": [{"bindingVersion": "scoped-v1", "subjectFingerprint": review_set_hash,
                 "verificationMethod": "independent_agent_review", "independent": True,
                 "verifierId": "fixture-reviewer", "reviewHashes": sorted(actual.digest(review) for review in document["reviews"]),
                 "verificationRecord": "SYNTHETIC hostile self-repinned receipt; not genuine independent authority."}]}
    return document, trust


class CatalogueIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalogue = actual.read_json(CHECKER / "catalogue.json")
        _, cls.document = fixture(cls.catalogue, real=True, assessment_mode="profile")
        cls.trust = trust_fixture(cls.catalogue, cls.document)

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def weak_catalogue(self):
        catalogue = copy.deepcopy(self.catalogue)
        for criterion in catalogue["profileChecks"]:
            criterion["requiredFieldIds"] = []
        return catalogue

    def write_inputs(self, catalogue, document=None, trust=None):
        paths = {"catalogue": self.root / "catalogue.json", "document": self.root / "document.json",
                 "trust": self.root / "trust.json", "report": self.root / "report.json"}
        actual.write_json(paths["catalogue"], catalogue)
        actual.write_json(paths["document"], document or self.document)
        actual.write_json(paths["trust"], trust or self.trust)
        return paths

    def cli(self, paths, command, arguments=(), engine=None, environment=None):
        return subprocess.run([sys.executable, str(engine or CHECKER / "quality_checker.py"),
                               "--catalogue", str(paths["catalogue"]), command, *arguments],
                              capture_output=True, text=True, env=environment)

    def assert_refusal(self, completed, catalogue):
        self.assertEqual(3, completed.returncode, completed.stdout + completed.stderr)
        self.assertEqual("", completed.stdout)
        self.assertNotIn("Traceback", completed.stderr)
        refusal = json.loads(completed.stderr)
        self.assertEqual("blocked", refusal["qualityState"]["status"])
        self.assertTrue(refusal["noPassGranted"])
        identity = refusal["catalogueIdentity"]
        self.assertEqual("mismatch", identity["status"])
        self.assertEqual(actual.EXPECTED_CATALOGUE_HASH, identity["expectedCanonicalHash"])
        self.assertEqual(actual.digest(catalogue), identity["actualCanonicalHash"])
        return refusal

    def test_fresh_actual_module_enforces_literal_shipped_identity_and_reports_match(self):
        self.assertEqual("actual_catalogue_guard_engine", actual.require_canonical_catalogue.__module__)
        self.assertEqual("3.0-generic", actual.EXPECTED_CATALOGUE_VERSION)
        self.assertEqual("a72502ce4dcfe5ec1e8537cd377f93e77ad32b9d998fdad62c252605089759fe", actual.EXPECTED_CATALOGUE_HASH)
        report = actual.Checker(self.catalogue, self.document, trust_store=self.trust).run()
        self.assertEqual("stage_checks_satisfied", report["qualityState"]["status"])
        self.assertEqual("matched", report["catalogueIdentity"]["status"])
        self.assertTrue(report["catalogueIdentity"]["enginePinned"])
        self.assertEqual(report["catalogueHash"], report["catalogueIdentity"]["expectedCanonicalHash"])
        self.assertEqual(report["catalogueIdentity"], quality_tools.summary_report(report)["catalogueIdentity"])
        self.assertFalse(report["qualityState"]["certificationGranted"])

    def test_all_required_fields_empty_and_real_self_repinned_trust_are_refused(self):
        catalogue = self.weak_catalogue()
        document = copy.deepcopy(self.document)
        for element in document["elements"]:
            for field in element["fields"].values():
                field["value"] = "Pending: required fact remains unresolved"
        document, trust = author_repin_for_negative_test(catalogue, document)
        self.assertEqual(0, sum(len(gate["requiredFieldIds"]) for gate in catalogue["profileChecks"]))
        self.assertEqual("real", document["mode"])
        self.assertEqual(actual.digest(catalogue), trust["catalogueHash"])
        with self.assertRaises(actual.CatalogueIntegrityError):
            actual.Checker(catalogue, document, trust_store=trust)
        paths = self.write_inputs(catalogue, document, trust)
        completed = self.cli(paths, "check", ["--document", str(paths["document"]), "--trust-store", str(paths["trust"]),
                                               "--report", str(paths["report"])])
        self.assert_refusal(completed, catalogue)
        self.assertFalse(paths["report"].exists())

    def test_one_removed_critical_field_is_refused_despite_matching_document_pin(self):
        catalogue = copy.deepcopy(self.catalogue)
        check = next(gate for gate in catalogue["profileChecks"] if gate["id"] == "gate.vision.planning.01")
        check["requiredFieldIds"].remove("vision.problem_evidence")
        document, trust = author_repin_for_negative_test(catalogue, self.document)
        with self.assertRaises(actual.CatalogueIntegrityError):
            actual.Checker(catalogue, document, trust_store=trust)
        self.assertTrue(actual.catalogue_errors(catalogue))

    def test_changed_criterion_requiredness_or_conditional_branch_is_refused(self):
        for change in ("criterion", "requiredness", "conditional"):
            with self.subTest(change=change):
                catalogue = copy.deepcopy(self.catalogue)
                if change == "criterion":
                    catalogue["profileChecks"][0]["passCriterion"] = "Any declaration suffices."
                    catalogue["profileChecks"][0]["pass_criteria"] = "Any declaration suffices."
                elif change == "requiredness":
                    catalogue["fields"][0]["requiredness"]["policy"] = "conditional"
                else:
                    check = next(gate for gate in catalogue["profileChecks"] if gate["conditionalFieldIds"])
                    check["conditionalFieldIds"] = {}
                with self.assertRaises(actual.CatalogueIntegrityError):
                    actual.require_canonical_catalogue(catalogue)

    def test_synthetic_flag_and_mode_cannot_exempt_altered_catalogue(self):
        catalogue = self.weak_catalogue()
        document = copy.deepcopy(self.document)
        document["mode"] = "synthetic_fixture"
        document, trust = author_repin_for_negative_test(catalogue, document)
        paths = self.write_inputs(catalogue, document, trust)
        completed = self.cli(paths, "check", ["--document", str(paths["document"]), "--report", str(paths["report"]), "--allow-synthetic"])
        self.assert_refusal(completed, catalogue)
        self.assertFalse(paths["report"].exists())

    def test_relocated_reformatted_key_reordered_ascii_escaped_copy_passes_actual_cli(self):
        paths = self.write_inputs(self.catalogue)
        paths["catalogue"].write_text(json.dumps(self.catalogue, ensure_ascii=True, sort_keys=True, indent=1), encoding="utf-8")
        self.assertNotEqual(hashlib.sha256(paths["catalogue"].read_bytes()).digest(), hashlib.sha256((CHECKER / "catalogue.json").read_bytes()).digest())
        completed = self.cli(paths, "check", ["--document", str(paths["document"]), "--trust-store", str(paths["trust"]), "--report", str(paths["report"])])
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        self.assertEqual("matched", actual.read_json(paths["report"])["catalogueIdentity"]["status"])

    def test_altered_default_catalogue_is_refused_by_copied_actual_cli(self):
        engine_directory = self.root / "copied-engine"
        engine_directory.mkdir()
        for name in ("quality_checker.py", "quality_tools.py", "quality_loop.py"):
            shutil.copy2(CHECKER / name, engine_directory / name)
        catalogue = self.weak_catalogue()
        actual.write_json(engine_directory / "catalogue.json", catalogue)
        output = self.root / "draft.json"
        completed = subprocess.run([sys.executable, str(engine_directory / "quality_checker.py"),
                                    "scaffold", "--output", str(output)], capture_output=True, text=True)
        self.assert_refusal(completed, catalogue)
        self.assertFalse(output.exists())

    def test_original_argument_mutation_cannot_change_checker_snapshot(self):
        supplied = copy.deepcopy(self.catalogue)
        checker = actual.Checker(supplied, self.document, trust_store=self.trust)
        supplied["profileChecks"][0]["requiredFieldIds"] = []
        report = checker.run()
        self.assertEqual("matched", report["catalogueIdentity"]["status"])
        self.assertEqual(actual.EXPECTED_CATALOGUE_HASH, actual.digest(checker.catalogue))
        self.assertNotEqual(actual.digest(supplied), actual.digest(checker.catalogue))

    def test_internal_catalogue_mutation_after_constructor_is_refused_at_run(self):
        checker = actual.Checker(self.catalogue, self.document, trust_store=self.trust)
        checker.catalogue["profileChecks"][0]["requiredFieldIds"] = []
        review = self.document["reviews"][0]
        with self.assertRaises(actual.CatalogueIntegrityError):
            checker.scoped_payload((review["elementId"], review["fieldId"], review["checkId"]))
        with self.assertRaises(actual.CatalogueIntegrityError):
            checker.run()
        self.assertEqual([], checker.results)

    def test_public_binding_and_selection_helpers_reject_altered_dictionary_and_cache_claim(self):
        catalogue = self.weak_catalogue()
        review = self.document["reviews"][0]
        target = (review["elementId"], review["fieldId"], review["checkId"])
        operations = [
            lambda: actual.subject_fingerprint(self.document, catalogue),
            lambda: actual.check_subject_payload(self.document, catalogue, *target,
                                                  catalogue_hash=actual.EXPECTED_CATALOGUE_HASH, check_index=raw_check_index(catalogue)),
            lambda: actual.check_subject_fingerprint(self.document, catalogue, *target),
            lambda: actual.validate_review_target(self.document, catalogue, *target),
            lambda: actual.review_set_fingerprint(self.document, catalogue),
            lambda: actual.assessment_selection(catalogue, self.document),
            lambda: list(actual.catalogue_checks(catalogue)),
            lambda: actual.scaffold(catalogue),
        ]
        for operation in operations:
            with self.subTest(operation=operations.index(operation)):
                with self.assertRaises(actual.CatalogueIntegrityError):
                    operation()

    def test_direct_migration_rejects_before_reading_or_writing_files(self):
        with self.assertRaises(actual.CatalogueIntegrityError):
            actual.migrate_document(self.weak_catalogue(), self.root / "absent-document.json",
                                    self.root / "candidate.json", self.root / "history",
                                    reason="Synthetic mechanics test of refusal before migration.")
        self.assertEqual([], list(self.root.iterdir()))

    def test_direct_tools_reject_before_evidence_mutation_or_outputs(self):
        catalogue = self.weak_catalogue()
        paths = self.write_inputs(catalogue)
        review = self.document["reviews"][0]
        for command in ("review-hashes", "trust-template", "bind-evidence"):
            output = self.root / (command + ".json")
            args = argparse.Namespace(command=command, document=str(paths["document"]), output=str(output),
                                      evidence_id=self.document["evidence"][0]["id"], element_id=review["elementId"],
                                      field_id=review["fieldId"], check_id=review["checkId"], allow_synthetic=True)
            with self.subTest(command=command):
                with self.assertRaises(actual.CatalogueIntegrityError):
                    quality_tools.dispatch(args, catalogue, actual)
                self.assertFalse(output.exists())
        document = copy.deepcopy(self.document)
        with self.assertRaises(actual.CatalogueIntegrityError):
            quality_tools.bind_evidence(args, document, catalogue, actual)
        self.assertEqual(self.document, document)

    def test_changed_catalogue_cli_paths_refuse_without_overwriting_report_or_creating_state(self):
        catalogue = self.weak_catalogue()
        paths = self.write_inputs(catalogue)
        paths["report"].write_text("Retained prior report bytes.\n", encoding="utf-8")
        before = {path: path.read_bytes() for path in self.root.iterdir()}
        common = ["--document", str(paths["document"])]
        output = self.root / "candidate.json"
        state = self.root / "state"
        review = self.document["reviews"][0]
        operations = {
            "check": common + ["--report", str(paths["report"])],
            "loop": common + ["--report", str(paths["report"]), "--state-dir", str(state)],
            "fingerprint": common,
            "scaffold": ["--output", str(output)],
            "migrate": common + ["--output", str(output), "--state-dir", str(state), "--change-reason", "Synthetic catalogue refusal test."],
            "review-hashes": common + ["--output", str(output)],
            "trust-template": common + ["--output", str(output)],
            "bind-evidence": common + ["--output", str(output), "--evidence-id", self.document["evidence"][0]["id"],
                                        "--element-id", review["elementId"], "--check-id", review["checkId"]],
            "summary": ["--report", str(paths["report"])],
        }
        for command, arguments in operations.items():
            with self.subTest(command=command):
                self.assert_refusal(self.cli(paths, command, arguments), catalogue)
                self.assertEqual(before, {path: path.read_bytes() for path in self.root.iterdir()})

    def test_expected_identity_in_document_trust_or_environment_is_not_an_override(self):
        catalogue = self.weak_catalogue()
        document, trust = author_repin_for_negative_test(catalogue, self.document)
        document["expectedCatalogueHash"] = actual.digest(catalogue)
        trust["expectedCatalogueHash"] = actual.digest(catalogue)
        paths = self.write_inputs(catalogue, document, trust)
        environment = dict(os.environ)
        environment["EXPECTED_CATALOGUE_HASH"] = actual.digest(catalogue)
        completed = self.cli(paths, "check", ["--document", str(paths["document"]), "--trust-store", str(paths["trust"]),
                                               "--report", str(paths["report"])], environment=environment)
        self.assert_refusal(completed, catalogue)
        self.assertFalse(paths["report"].exists())

    def test_catalogue_version_cannot_be_relabelled_as_new_authorized_standard(self):
        catalogue = copy.deepcopy(self.catalogue)
        catalogue["catalogueVersion"] = "99.0-self-approved"
        with self.assertRaises(actual.CatalogueIntegrityError) as refusal:
            actual.require_canonical_catalogue(catalogue)
        self.assertEqual("3.0-generic", refusal.exception.identity["expectedCatalogueVersion"])
        self.assertEqual("99.0-self-approved", refusal.exception.identity["actualCatalogueVersion"])


if __name__ == "__main__":
    unittest.main()
