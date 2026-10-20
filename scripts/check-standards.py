#!/usr/bin/env python3
"""Verify immutable supplied standards, not product approval or release readiness."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
lock = json.loads((root / '.aplyd/delivery-lock.json').read_text())
failures = []
count = 0
for package in lock['packages']:
    folder = root / package['path']
    actual = {p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()
              and '__pycache__' not in p.parts}
    if actual != set(package['files']):
        failures.append(package['role'] + ': file inventory changed')
    for name, digest in package['files'].items():
        path = folder / name
        if path.is_symlink() or not path.resolve().is_relative_to(folder.resolve()) or not path.is_file():
            failures.append(package['role'] + ': unsafe or missing ' + name)
        elif hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            failures.append(package['role'] + ': modified ' + name)
        count += 1
print(json.dumps({'reference_files_checked': count, 'failures': failures,
                  'meaning': 'Byte integrity only; no product, review or release approval.'}, indent=2))
if failures:
    sys.exit(1)
sys.exit(subprocess.call([sys.executable, '-B', str(root / lock['engineering_path'] / '06-enforcement/scripts/engctl.py'),
                         'verify-package', '--package', str(root / lock['engineering_path'])], cwd=root))
