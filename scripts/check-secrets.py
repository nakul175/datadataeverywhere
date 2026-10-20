#!/usr/bin/env python3
"""Scan publishable files without printing matching credentials; defense in depth."""
from pathlib import Path
import re
import subprocess
import sys
from zipfile import ZipFile, BadZipFile

root = Path(__file__).resolve().parents[1]
names = set(subprocess.check_output(['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'], cwd=root).decode().split('\0')) - {''}
patterns = {
    'private-key': r'-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----',
    'github-token': r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b',
    'provider-key': r'\bsk-(?:proj-|ant-api\d+-)?[A-Za-z0-9_-]{24,}\b',
    'aws-key': r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b',
    'password-hash': r'\$2[aby]\$\d{2}\$[./A-Za-z0-9]{53}',
    'url-credential': r'(?:postgres(?:ql)?|redis|https?)://[^\s/:@]+:[^\s/@$\{]+@',
}
findings = []
def scan(name, data):
    text = data.decode('utf-8', errors='replace')
    for kind, pattern in patterns.items():
        for match in re.finditer(pattern, text):
            findings.append((name, text.count('\n', 0, match.start()) + 1, kind))
for name in sorted(names):
    path = root / name
    if not path.is_file():
        continue
    if path.is_symlink():
        findings.append((name, 0, 'publishable-symlink')); continue
    if path.name in {'.env', 'runtime.env', 'access.json', 'users.caddy'} or path.suffix in {'.pem', '.key', '.sqlite', '.db'}:
        findings.append((name, 0, 'private-runtime-file')); continue
    if path.suffix in {'.png', '.ttf', '.woff', '.woff2'}:
        continue
    if path.suffix in {'.docx', '.zip'}:
        try:
            with ZipFile(path) as archive:
                for member in archive.infolist():
                    if not member.is_dir() and member.file_size < 5_000_000:
                        scan(name + ':' + member.filename, archive.read(member))
        except BadZipFile:
            findings.append((name, 0, 'unreadable-archive'))
    else:
        scan(name, path.read_bytes())
for name, line, kind in findings:
    print(f'{name}:{line}: {kind} (value redacted)')
print(f'Scanned {len(names)} publishable files; findings: {len(findings)}. Pattern checks are not proof of absence.')
sys.exit(bool(findings))
