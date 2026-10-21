#!/usr/bin/env python3
"""Archive/restore the stopped unified service. Never starts services or reads keys to stdout."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import pwd
import shutil
import tarfile
import tempfile
import sys

if sys.version_info < (3, 12):
    raise SystemExit('Python 3.12 or later is required for safe archive extraction.')


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for part in iter(lambda: f.read(1024 * 1024), b''):
            h.update(part)
    return h.hexdigest()


def inside(path, root):
    resolved = path.resolve(strict=True)
    if not resolved.is_relative_to(root.resolve(strict=True)):
        raise ValueError('A backup source resolves outside the application directory')
    return resolved


def account(user):
    p = pwd.getpwnam(user)
    return p, Path(p.pw_dir).resolve(strict=True)


def backup(root, user, output):
    p, home = account(user)
    root = root.resolve(strict=True)
    if not root.is_relative_to(home.resolve()):
        raise ValueError('Unified root must be inside the service account home')
    source = inside(root / 'current', root)
    for name in ['shared/runtime.env', 'shared/access.json', 'shared/data']:
        inside(root / name, root)
    if not (source / '.next/standalone/server.js').is_file():
        raise ValueError('Compiled standalone application is missing')
    service = home / '.config/systemd/user/datadataeverywhere.service'
    if not service.is_file() or service.is_symlink():
        raise ValueError('Expected regular service unit is missing')
    inside(service, home)
    output.mkdir(mode=0o700, parents=True, exist_ok=True)
    targets = [output / name for name in ['unified-shared.tgz', 'unified-app.tgz', 'unified-service.unit', 'unified.json']]
    if any(t.exists() for t in targets):
        raise ValueError('Refusing to overwrite an existing unified backup')
    # Caller has stopped the service. Include SQLite WAL/SHM, not only its main file.
    with tarfile.open(targets[0], 'w:gz') as tar:
        for name in ['runtime.env', 'access.json', 'data']:
            tar.add(root / 'shared' / name, arcname=name)
    with tarfile.open(targets[1], 'w:gz') as tar:
        tar.add(source / '.next/standalone', arcname='.next/standalone')
    shutil.copyfile(service, targets[2])
    targets[3].write_text(json.dumps({'formatVersion': 1, 'user': user, 'home': str(home), 'root': str(root), 'artifacts': {t.name: digest(t) for t in targets[:3]}}, indent=2))
    for target in targets:
        target.chmod(0o600)


def checked_manifest(folder):
    data = json.loads((folder / 'unified.json').read_text())
    if data.get('formatVersion') != 1:
        raise ValueError('Unsupported unified backup version')
    required = {'unified-shared.tgz', 'unified-app.tgz', 'unified-service.unit'}
    if set(data.get('artifacts', {})) != required:
        raise ValueError('Incomplete unified backup manifest')
    for name, expected in data['artifacts'].items():
        path = folder / name
        if path.is_symlink() or digest(path) != expected:
            raise ValueError('Unified backup checksum mismatch')
    return data


def restore(folder):
    data = checked_manifest(folder)
    p, home = account(data['user'])
    root = Path(data['root'])
    if str(home) != data['home'] or not root.is_absolute() or not root.resolve().is_relative_to(home) or root.resolve() == home:
        raise ValueError('Restore requires the original service user/home and application path')
    service = home / '.config/systemd/user/datadataeverywhere.service'
    if not service.parent.resolve().is_relative_to(home):
        raise ValueError('Service unit parent resolves outside the service account home')
    if root.exists() or root.is_symlink() or service.exists() or service.is_symlink():
        raise ValueError('Restore requires an absent unified directory and service unit')
    root.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.dde-restore-', dir=root.parent) as temp:
        stage = Path(temp) / 'application'
        stage.mkdir(mode=0o700)
        shared = stage / 'shared'
        release = stage / 'restored-release'
        shared.mkdir(mode=0o700)
        release.mkdir(mode=0o700)
        for name, dest in [('unified-shared.tgz', shared), ('unified-app.tgz', release)]:
            with tarfile.open(folder / name, 'r:gz') as tar:
                # Python 3.12 data filter rejects traversal, devices and escaping links.
                tar.extractall(dest, filter='data')
        for path in [shared/'runtime.env', shared/'access.json', release/'.next/standalone/server.js']:
            inside(path, stage)
            if not path.is_file():
                raise ValueError('Incomplete restored application')
        for path in [stage, *stage.rglob('*')]:
            os.chown(path, p.pw_uid, p.pw_gid, follow_symlinks=False)
        (stage / 'current').symlink_to(root / 'restored-release', target_is_directory=True)
        shared.chmod(0o700)
        for path in [shared/'runtime.env', shared/'access.json']:
            path.chmod(0o600)
        for directory in [home/'.config', home/'.config/systemd', service.parent]:
            if not directory.exists():
                directory.mkdir(mode=0o700)
                os.chown(directory, p.pw_uid, p.pw_gid)
        # Save the unit exclusively; do not replace or execute another service.
        with service.open('x') as f:
            f.write((folder / 'unified-service.unit').read_text())
        service.chmod(0o600)
        os.chown(service, p.pw_uid, p.pw_gid)
        stage.rename(root)
    print('Unified files restored. Review the unit/configuration, then enable and verify the user service separately.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    b = sub.add_parser('backup')
    b.add_argument('--root', type=Path, required=True)
    b.add_argument('--user', required=True)
    b.add_argument('--output', type=Path, required=True)
    r = sub.add_parser('restore')
    r.add_argument('--backup', type=Path, required=True)
    v = sub.add_parser('validate')
    v.add_argument('--backup', type=Path, required=True)
    args = parser.parse_args()
    if args.action == 'backup':
        backup(args.root, args.user, args.output)
    elif args.action == 'restore':
        restore(args.backup)
    else:
        checked_manifest(args.backup)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, tarfile.TarError):
        raise SystemExit('Unified backup/restore failed validation; inspect files privately. No service was started.')
