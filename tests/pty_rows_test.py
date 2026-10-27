"""The opening row leaves uploadable evidence even when setup raises."""
import importlib.util
from pathlib import Path
import stat
import tempfile
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('cub_pty_rows', ROOT / 'tests/pty_rows.py')
rows = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rows)


class OpeningArtifactPermissions(unittest.TestCase):
    def check_failed_attempt(self, partial):
        scratch = ROOT / 'target/fixture-permissions'
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as directory:
            root = Path(directory)

            def fail_session(argv, height, width, env):
                if partial:
                    child = Path(env['HOME']) / 'partial'
                    child.mkdir(mode=0o700)
                    record = child / 'trace'
                    record.write_text('synthetic partial evidence\n')
                    record.chmod(0o600)
                raise RuntimeError('planted session setup failure')

            ctx = SimpleNamespace(ROOT=str(root), env_for=lambda: {}, Session=fail_session)
            with self.assertRaisesRegex(RuntimeError, 'planted session setup failure'):
                rows.opening_quit_due('/unused', ctx)
            homes = list((root / 'target/pty/opening-quit-due').glob('fresh-*'))
            self.assertEqual(len(homes), 1, 'the failed attempt must leave evidence')
            for path in [homes[0], *homes[0].rglob('*')]:
                mode = stat.S_IMODE(path.stat().st_mode)
                required = 0o005 if path.is_dir() else 0o004
                self.assertEqual(mode & required, required,
                                 '%s is not readable by the artifact uploader: %03o' % (path, mode))

    def test_setup_failure_releases_private_mkdtemp_directory(self):
        self.check_failed_attempt(False)

    def test_partial_failure_releases_nested_directories_and_files(self):
        self.check_failed_attempt(True)


if __name__ == '__main__':
    unittest.main()
