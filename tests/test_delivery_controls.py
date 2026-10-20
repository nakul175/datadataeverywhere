"""Delivery control tests, separate from the 33 application tests."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ReportGateTests(unittest.TestCase):
    def check_report(self, nodes, expected):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'report.xml'
            # Deliberately untrustworthy summary count must not override actual nodes.
            path.write_text('<testsuite tests="999">' + ''.join(nodes) + '</testsuite>')
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/check-test-report.py'), str(path)], capture_output=True)
            self.assertEqual(result.returncode, expected, result.stdout.decode())

    def test_fabricated_nonzero_summary_with_zero_cases_is_rejected(self):
        self.check_report([], 1)

    def test_skipped_required_cases_are_rejected(self):
        self.check_report(['<testcase><skipped/></testcase>'] * 33, 1)

    def test_actual_failure_is_rejected(self):
        self.check_report(['<testcase/>'] * 32 + ['<testcase><failure/></testcase>'], 1)

    def test_nonempty_passing_report_is_accepted(self):
        self.check_report(['<testcase/>'] * 33, 0)

if __name__ == '__main__':
    unittest.main()
