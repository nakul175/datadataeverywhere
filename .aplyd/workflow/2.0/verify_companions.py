"""Verify exact companion archive pins without extracting or executing companion code."""
from pathlib import Path
import hashlib
import json
import sys

if len(sys.argv) != 2:
    raise SystemExit('Usage: python3 verify_companions.py /folder/containing/three/ZIPs')
root = Path(__file__).resolve().parent
folder = Path(sys.argv[1])
lock = json.loads((root / 'PACKAGE-LOCK.json').read_text())
results = []
for package in lock['companions']:
    p = folder / package['archive']
    matches = p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest() == package['sha256']
    results.append({'archive': package['archive'], 'pinnedBytesMatch': matches})
print(json.dumps({'results': results, 'nativeCompatibilityVerified': False,
                  'externalAuthorityVerified': False}, indent=2))
sys.exit(0 if all(x['pinnedBytesMatch'] for x in results) else 1)
