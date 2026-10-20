import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import sqlite3
import tarfile
import tempfile
import types
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('unified_state', Path(__file__).parents[1]/'scripts/unified-state.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class UnifiedRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.home = Path(self.temp.name)/'account'
        self.root = self.home/'datadataeverywhere'
        self.output = Path(self.temp.name)/'backup'
        release = self.root/'releases/r1/sidecar/.next/standalone'
        release.mkdir(parents=True)
        (release/'server.js').write_text('test-only artifact')
        (self.root/'current').symlink_to(release.parents[1])
        shared = self.root/'shared'
        (shared/'data').mkdir(parents=True)
        (shared/'runtime.env').write_text('APP_ORIGIN=https://example.test\n')
        (shared/'access.json').write_text('{"tables":[],"users":{}}')
        with sqlite3.connect(shared/'data/budget.sqlite') as db:
            db.execute('CREATE TABLE usage(amount INTEGER)')
            db.execute('INSERT INTO usage VALUES (490000)')
        self.unit = self.home/'.config/systemd/user/datadataeverywhere.service'
        self.unit.parent.mkdir(parents=True)
        self.unit.write_text('[Service]\nExecStart=/test-only/server\n')
        p = types.SimpleNamespace(pw_dir=str(self.home),pw_uid=os.getuid(),pw_gid=os.getgid())
        self.account_patch = patch.object(mod.pwd, 'getpwnam', return_value=p)
        self.account_patch.start()

    def tearDown(self):
        self.account_patch.stop()
        self.temp.cleanup()

    def archive(self):
        mod.backup(self.root, 'fixture-user', self.output)

    def empty_target(self):
        shutil.rmtree(self.root)
        self.unit.unlink()

    def test_complete_round_trip_retains_budget_configuration_artifact_and_permissions(self):
        self.archive()
        self.empty_target()
        mod.restore(self.output)
        self.assertEqual((self.root/'current/.next/standalone/server.js').read_text(),'test-only artifact')
        self.assertEqual((self.root/'shared/access.json').stat().st_mode & 0o777,0o600)
        self.assertEqual((self.root/'shared').stat().st_mode & 0o777,0o700)
        with sqlite3.connect(self.root/'shared/data/budget.sqlite') as db:
            self.assertEqual(db.execute('SELECT amount FROM usage').fetchone()[0],490000)
        self.assertIn('ExecStart=/test-only/server',self.unit.read_text())

    def test_refuses_existing_application_or_unit(self):
        self.archive()
        with self.assertRaises(ValueError): mod.restore(self.output)
        shutil.rmtree(self.root)
        with self.assertRaises(ValueError): mod.restore(self.output)

    def test_corruption_is_refused_before_writing_a_restore(self):
        self.archive()
        self.empty_target()
        (self.output/'unified-app.tgz').write_bytes(b'corrupt')
        with self.assertRaises(ValueError): mod.restore(self.output)
        self.assertFalse(self.root.exists())
        self.assertFalse(self.unit.exists())

    def test_traversal_is_rejected_even_with_a_matching_archive_digest(self):
        self.archive()
        self.empty_target()
        archive = self.output/'unified-app.tgz'
        with tarfile.open(archive,'w:gz') as tar:
            info = tarfile.TarInfo('../escape')
            info.size=1
            tar.addfile(info,io.BytesIO(b'x'))
        metadata=json.loads((self.output/'unified.json').read_text())
        metadata['artifacts'][archive.name]=mod.digest(archive)
        (self.output/'unified.json').write_text(json.dumps(metadata))
        with self.assertRaises(tarfile.TarError): mod.restore(self.output)
        self.assertFalse(self.root.exists())
        self.assertFalse((self.home/'escape').exists())

    def test_refuses_current_symlink_outside_application(self):
        (self.root/'current').unlink()
        (self.root/'current').symlink_to(self.home)
        with self.assertRaises(ValueError): self.archive()

    def test_refuses_escaping_service_directory_on_restore(self):
        self.archive()
        self.empty_target()
        shutil.rmtree(self.home/'.config')
        outside=Path(self.temp.name)/'outside'
        (outside/'systemd/user').mkdir(parents=True)
        (self.home/'.config').symlink_to(outside,target_is_directory=True)
        with self.assertRaises(ValueError): mod.restore(self.output)
        self.assertFalse((outside/'systemd/user/datadataeverywhere.service').exists())


if __name__ == '__main__':
    unittest.main()
