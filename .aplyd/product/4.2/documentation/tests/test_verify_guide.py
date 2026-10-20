"""Meaningful negative tests for the read-only actual-OOXML content verifier."""

import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("verify_guide", ROOT / "verify_guide.py")
VERIFIER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFIER)
DOCUMENT = ROOT / "Generic Product Management Operating Framework.docx"
CATALOGUE = ROOT.parent / "checker/catalogue.json"
SOURCE = ROOT.parent / "checker/source-standard.md"
AI = ROOT.parent / "AI-ASSURANCE.md"


class GuideVerificationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.catalogue = json.loads(CATALOGUE.read_text(encoding="utf-8"))

    def verify(self, document=DOCUMENT, source=SOURCE):
        return VERIFIER.verify(document, CATALOGUE, source, AI)

    def tamper_document(self, mutation):
        """Mutate a temporary copy's actual Word XML, never the bundled guide."""
        with zipfile.ZipFile(DOCUMENT) as archive:
            tree = ET.fromstring(archive.read("word/document.xml"))
            mutation(tree)
            result = io.BytesIO()
            with zipfile.ZipFile(result, "w") as candidate:
                for info in archive.infolist():
                    candidate.writestr(info, ET.tostring(tree, encoding="utf-8", xml_declaration=True)
                                      if info.filename == "word/document.xml" else archive.read(info))
        path = Path(self.directory.name) / "candidate.docx"
        path.write_bytes(result.getvalue())
        return path

    def alter_first(self, tree, predicate, replacement):
        for node in tree.iter(VERIFIER.W + "t"):
            if predicate(node.text or ""):
                node.text = replacement(node.text)
                return
        self.fail("Actual Word text selected for tampering was absent")

    def assert_failure(self, receipt, kind):
        self.assertEqual("failed", receipt["status"])
        self.assertIn(kind, [failure["kind"] for failure in receipt["failures"]])

    def test_actual_guide_complete_and_bound_to_input_bytes(self):
        receipt = self.verify()
        self.assertEqual("passed", receipt["status"])
        self.assertEqual([], receipt["failures"])
        self.assertEqual({
            "fieldIdsInTheirOwningRows": 189, "componentLabelsInTheirOwningRows": 587,
            "baseCriteriaInMappedParagraphs": 56, "sharedStageClauses": 5,
            "conditionalAssuranceClauses": 1, "exactStageCriteriaReconstructedFromWord": 280,
            "aiSourceHeadingsWithExactPunctuation": 14,
        }, receipt["verified"])
        for name, path in (("document", DOCUMENT), ("catalogue", CATALOGUE),
                           ("source", SOURCE), ("ai", AI)):
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), receipt["pins"][name]["sha256"])

    def test_field_id_elsewhere_cannot_substitute_for_owning_row(self):
        field_id = self.catalogue["fields"][0]["id"]
        def mutation(tree):
            for row in tree.iter(VERIFIER.W + "tr"):
                cells = row.findall(VERIFIER.W + "tc")
                if cells and field_id in VERIFIER.cell_text(cells[0]).splitlines():
                    self.alter_first(cells[0], lambda text: text == field_id, lambda _: "removed.field")
                    return
            self.fail("Owning field row was absent")
        candidate = self.tamper_document(mutation)
        self.assert_failure(self.verify(candidate), "field_row")

    def test_component_label_missing_from_its_own_row_is_refused(self):
        label = self.catalogue["fields"][0]["details"][0]["label"]
        candidate = self.tamper_document(lambda tree: self.alter_first(
            tree, lambda text: label in text, lambda text: text.replace(label, "Removed component", 1)))
        receipt = self.verify(candidate)
        self.assert_failure(receipt, "field_components_or_applicability")
        self.assert_failure(receipt, "component_label")

    def test_base_criterion_edit_reopens_its_five_stage_reconstructions(self):
        bases, _, _, _ = VERIFIER.expected_criteria(self.catalogue)
        key = ("vision", "01")
        original = bases[key]
        candidate = self.tamper_document(lambda tree: self.alter_first(
            tree, lambda text: text == original, lambda text: text + " Changed."))
        receipt = self.verify(candidate)
        self.assert_failure(receipt, "base_criterion")
        affected = {failure["checkId"] for failure in receipt["failures"]
                    if failure["kind"] == "stage_criterion_reconstruction"}
        self.assertEqual({"gate.vision." + stage + ".01" for stage in VERIFIER.STAGES}, affected)

    def test_shared_stage_edit_reopens_all_56_criteria_in_that_stage(self):
        _, stages, _, _ = VERIFIER.expected_criteria(self.catalogue)
        original = stages["ready"]
        candidate = self.tamper_document(lambda tree: self.alter_first(
            tree, lambda text: text == original, lambda text: text + " Changed."))
        receipt = self.verify(candidate)
        self.assert_failure(receipt, "stage_clause_text")
        affected = [failure["checkId"] for failure in receipt["failures"]
                    if failure["kind"] == "stage_criterion_reconstruction"]
        self.assertEqual(56, len(affected))
        self.assertTrue(all(".ready." in check_id for check_id in affected))

    def test_assurance_suffix_edit_reopens_only_all_40_gate_06_definitions(self):
        _, _, suffixes, _ = VERIFIER.expected_criteria(self.catalogue)
        original = next(iter(suffixes))
        candidate = self.tamper_document(lambda tree: self.alter_first(
            tree, lambda text: text == original, lambda text: text + " Changed."))
        receipt = self.verify(candidate)
        self.assert_failure(receipt, "conditional_assurance_clause")
        affected = [failure["checkId"] for failure in receipt["failures"]
                    if failure["kind"] == "stage_criterion_reconstruction"]
        self.assertEqual(40, len(affected))
        self.assertTrue(all(check_id.endswith(".06") for check_id in affected))

    def test_ai_heading_punctuation_must_be_exact_in_heading_paragraph(self):
        original = "AI-01 — Intended use, authority and risk"
        candidate = self.tamper_document(lambda tree: self.alter_first(
            tree, lambda text: text == original, lambda text: text.replace("—", "-")))
        self.assert_failure(self.verify(candidate), "ai_heading_exact_punctuation")

    def test_catalogue_source_pin_is_checked_against_actual_source(self):
        source = Path(self.directory.name) / "source-standard.md"
        source.write_bytes(SOURCE.read_bytes() + b"\nChanged source.\n")
        self.assert_failure(self.verify(source=source), "catalogue_source_pin")

    def test_cli_is_read_only_and_uses_actual_word_not_cached_document_text(self):
        inputs = (DOCUMENT, CATALOGUE, SOURCE, AI)
        before = {path: path.read_bytes() for path in inputs}
        completed = subprocess.run([sys.executable, str(ROOT / "verify_guide.py")],
                                   cwd=self.directory.name, capture_output=True, text=True)
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual("passed", json.loads(completed.stdout)["status"])
        self.assertEqual(before, {path: path.read_bytes() for path in inputs})
        self.assertEqual([], list(Path(self.directory.name).iterdir()))

    def test_malformed_word_cli_returns_3_without_traceback(self):
        candidate = Path(self.directory.name) / "invalid.docx"
        candidate.write_text("This is not a Word archive.", encoding="utf-8")
        completed = subprocess.run([sys.executable, str(ROOT / "verify_guide.py"),
                                    "--document", str(candidate)], capture_output=True, text=True)
        self.assertEqual(3, completed.returncode)
        self.assertEqual("malformed_input", json.loads(completed.stdout)["status"])
        self.assertNotIn("Traceback", completed.stdout + completed.stderr)

    def test_invalid_cli_flag_returns_3_without_traceback_or_file_write(self):
        completed = subprocess.run([sys.executable, str(ROOT / "verify_guide.py"),
                                    "--output", "unauthorized-output.json"],
                                   cwd=self.directory.name, capture_output=True, text=True)
        self.assertEqual(3, completed.returncode)
        self.assertEqual("malformed_input", json.loads(completed.stdout)["status"])
        self.assertNotIn("Traceback", completed.stdout + completed.stderr)
        self.assertEqual([], list(Path(self.directory.name).iterdir()))


if __name__ == "__main__":
    unittest.main()
