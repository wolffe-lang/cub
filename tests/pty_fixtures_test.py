#!/usr/bin/env python3
"""Fresh fixtures preserve old evidence; persistent compatibility has its own row."""
from pathlib import Path
import runpy
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
prepare = runpy.run_path(str(ROOT / 'tools/prepare-pty'))['prepare']
fresh_save = runpy.run_path(str(ROOT / 'tests/pty_rows.py'))['fresh_save']


class Fixtures(unittest.TestCase):
    def setUp(self):
        parent = ROOT / 'target/pty-fixture-tests'
        parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=parent)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_engine_state_is_archived_without_touching_capture(self):
        saved = {'engine.save': b'old save\n', 'engine.save.pending': b'old stage\n'}
        for name, data in saved.items():
            (self.root / name).write_bytes(data)
        (self.root / 'quit.bin').write_bytes(b'capture')
        archive = prepare(self.root)
        self.assertEqual(archive.stat().st_mode & 0o777, 0o755)
        for name, data in saved.items():
            self.assertFalse((self.root / name).exists())
            self.assertEqual((archive / name).read_bytes(), data)
        self.assertEqual((self.root / 'quit.bin').read_bytes(), b'capture')
        self.assertIsNone(prepare(self.root))
        self.assertEqual(len(list(self.root.glob('engine-previous-*'))), 1)

    def test_fresh_sessions_never_reuse_or_delete_prior_journeys(self):
        old = self.root / 'den.save'
        old.write_bytes(b'previous generation')
        first, second = fresh_save(self.root), fresh_save(self.root)
        self.assertNotEqual(first, second)
        self.assertFalse(first.exists())
        self.assertFalse(second.exists())
        self.assertEqual(first.parent.stat().st_mode & 0o777, 0o755)
        self.assertEqual(second.parent.stat().st_mode & 0o777, 0o755)
        self.assertEqual(old.read_bytes(), b'previous generation')


if __name__ == '__main__':
    unittest.main()
