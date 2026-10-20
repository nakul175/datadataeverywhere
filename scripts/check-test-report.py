#!/usr/bin/env python3
"""Reject empty/skipped/failed reports rather than trusting a summary count."""
import sys
import xml.etree.ElementTree as ET

root = ET.parse(sys.argv[1]).getroot()
cases = list(root.iter('testcase'))
failed = sum(c.find('failure') is not None or c.find('error') is not None for c in cases)
skipped = sum(c.find('skipped') is not None for c in cases)
executed = len(cases) - skipped
print(f'Test cases: {len(cases)}; executed: {executed}; skipped: {skipped}; failed: {failed}')
sys.exit(0 if executed >= 33 and skipped == 0 and failed == 0 else 1)
