"""Compact helpers and explicit evidence bindings do not manufacture reviews."""
import argparse
import copy
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

CHECKER = Path(__file__).resolve().parents[1]
if str(CHECKER) not in sys.path:
    sys.path.insert(0, str(CHECKER))
import quality_tools as qt
from test_checker import fixture, qc


class ToolTests(unittest.TestCase):
    def test_compact_summary_preserves_honest_status_without_criteria_dump(self):
        catalogue, document = fixture()
        report = qc.Checker(catalogue, document).run()
        result = qt.summary_report(report)
        self.assertEqual(result['qualityState'], report['qualityState'])
        self.assertNotIn('checks', result)
        self.assertTrue(result['inspectionOnly'])
        self.assertLess(len(qc.canonical(result)), 12000)

    def test_next_inspection_does_not_acknowledge_batch(self):
        packet = {'loopStatus': 'needs_input', 'currentBatchId': 'batch-1', 'pendingQuestionCount': 1,
                  'nextBatch': [{'id': 'Q-1', 'question': 'Which population is in scope?', 'status': 'pending'}],
                  'reviewerQueue': [{'id': 'R-1', 'checkId': 'gate-1', 'reason': 'Missing review'}], 'repairQueue': []}
        previous = copy.deepcopy(packet)
        result = qt.inspect_next(packet)
        self.assertEqual(result['ownerQueue'][0]['id'], 'Q-1')
        self.assertEqual(result['reviewerQueue'][0]['id'], 'R-1')
        self.assertEqual(packet, previous)

    def test_explain_requires_exact_target_when_ambiguous(self):
        report = {'checks': [{'id': 'story-1:same', 'checkId': 'same', 'elementId': 'story-1', 'status': 'stale'},
                             {'id': 'story-2:same', 'checkId': 'same', 'elementId': 'story-2', 'status': 'passed'}]}
        with self.assertRaises(ValueError):
            qt.explain_check(report, 'same')
        self.assertEqual(qt.explain_check(report, 'same', 'story-1')['status'], 'stale')
        self.assertEqual(qt.explain_check(report, 'story-2:same')['status'], 'passed')

    def test_hash_and_trust_helpers_never_create_a_favorable_receipt(self):
        catalogue, document = fixture()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'document.json'; qc.write_json(source, document)
            before = source.read_bytes()
            result = qt.dispatch(argparse.Namespace(command='review-hashes', document=str(source), output=None), catalogue, qc)
            self.assertEqual(result['reviewHashes'], sorted(qc.digest(row) for row in document['reviews']))
            target = root / 'registry.json'
            intake = qt.dispatch(argparse.Namespace(command='trust-template', document=str(source), output=str(target)), catalogue, qc)
            self.assertFalse(intake['certificationGranted'])
            self.assertFalse(intake['authorityCreatedByThisHelper'])
            self.assertEqual(qc.read_json(target)['reviewVerifications'], [])
            self.assertEqual(source.read_bytes(), before)

    def test_review_hash_output_cannot_overwrite_product_document(self):
        catalogue, document = fixture()
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'document.json'; qc.write_json(source, document)
            before = source.read_bytes()
            with self.assertRaises(ValueError):
                qt.dispatch(argparse.Namespace(command='review-hashes', document=str(source), output=str(source)), catalogue, qc)
            self.assertEqual(source.read_bytes(), before)

    def test_bind_one_evidence_target_preserves_original_and_review_verdicts(self):
        catalogue, document = fixture()
        review = document['reviews'][0]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'document.json'; target = root / 'candidate.json'
            qc.write_json(source, document); before = source.read_bytes()
            args = argparse.Namespace(command='bind-evidence', document=str(source), output=str(target),
                evidence_id=document['evidence'][0]['id'], element_id=review['elementId'],
                field_id=review['fieldId'], check_id=review['checkId'], allow_synthetic=True)
            result = qt.dispatch(args, catalogue, qc)
            candidate = qc.read_json(target)
            bindings = candidate['evidence'][0]['bindings']
            binding = next(row for row in bindings if row.get('elementId') == review['elementId'] and row.get('fieldId') == review['fieldId'] and row.get('checkId') == review['checkId'])
            self.assertEqual(binding['subjectFingerprint'], qc.check_subject_fingerprint(candidate, catalogue,
                review['elementId'], review['fieldId'], review['checkId'], root))
            self.assertEqual(candidate['reviews'], document['reviews'])
            self.assertEqual(result['reviewsCreated'], 0)
            self.assertEqual(source.read_bytes(), before)
            args.allow_synthetic = False
            with self.assertRaises(ValueError):
                qt.dispatch(args, catalogue, qc)

    def test_binding_helper_refuses_unknown_target_and_asset_relocation(self):
        catalogue, document = fixture()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); source = root / 'document.json'
            qc.write_json(source, document)
            args = argparse.Namespace(command='bind-evidence', document=str(source), output=str(root / 'candidate.json'),
                evidence_id=document['evidence'][0]['id'], element_id=document['elements'][0]['id'],
                field_id=None, check_id='nonexistent-check', allow_synthetic=True)
            with self.assertRaises(ValueError):
                qt.dispatch(args, catalogue, qc)
            args.output = str(root / 'elsewhere' / 'candidate.json')
            with self.assertRaises(ValueError):
                qt.dispatch(args, catalogue, qc)

    def test_rulebook_unicode_roundtrip_under_ascii_default(self):
        specification = importlib.util.spec_from_file_location('rulebook_fixture', CHECKER / 'render_rulebooks.py')
        renderer = importlib.util.module_from_spec(specification); specification.loader.exec_module(renderer)
        from unittest.mock import patch
        actual_read, actual_write = Path.read_text, Path.write_text
        def ascii_read(path, *args, **kwargs):
            if kwargs.get('encoding') != 'utf-8':
                raise UnicodeError('Simulated Windows non-UTF default requires explicit UTF-8.')
            return actual_read(path, *args, **kwargs)
        def ascii_write(path, text, *args, **kwargs):
            if kwargs.get('encoding') != 'utf-8':
                raise UnicodeError('Simulated Windows non-UTF default requires explicit UTF-8.')
            return actual_write(path, text, *args, **kwargs)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); catalogue = qc.read_json(CHECKER / 'catalogue.json')
            catalogue['fields'][0]['purpose'] += ' Unicode Ω café हिन्दी.'
            qc.write_json(root / 'catalogue.json', catalogue); renderer.ROOT = root
            with patch.object(Path, 'read_text', ascii_read), patch.object(Path, 'write_text', ascii_write), patch('builtins.print'):
                renderer.main()
            self.assertIn('Unicode Ω café हिन्दी.', qc.read_json(root / 'publication/common.json')['content'])


if __name__ == '__main__':
    unittest.main()
