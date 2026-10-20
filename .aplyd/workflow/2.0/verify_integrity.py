"""Byte-integrity check only; external provenance and semantic approval are separate."""
from pathlib import Path
import hashlib
import json
import sys

root = Path(__file__).resolve().parent
manifest = root / 'audit' / 'BUNDLE-MANIFEST.json'
data = json.loads(manifest.read_text())
failures = []
for relative, expected in data['files'].items():
    p = root / relative
    if p.is_symlink() or not p.resolve().is_relative_to(root) or not p.is_file():
        failures.append(relative + ': missing or unsafe path')
    elif hashlib.sha256(p.read_bytes()).hexdigest() != expected:
        failures.append(relative + ': hash mismatch')
actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
unexpected = actual - set(data['files']) - {'audit/BUNDLE-MANIFEST.json'}
failures.extend(p + ': unmanifested file' for p in sorted(unexpected))
print(json.dumps({'byteIntegrity': 'failed' if failures else 'passed',
                  'filesChecked': len(data['files']), 'failures': failures,
                  'externalTrustVerified': False, 'productTestsExecuted': False}, indent=2))
sys.exit(1 if failures else 0)
