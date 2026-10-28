"""The opening row leaves uploadable evidence even when setup raises."""
import importlib.util
from pathlib import Path
import stat
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

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


class OpeningSkipSynchronization(unittest.TestCase):
    def check_transition(self, events):
        class Session:
            def __init__(self):
                self.clock = 0.0
                self.err = self.trace(12, 0, 0, 1)
                self.events = list(events)
                self.typed = []

            def trace(self, tick, keys, x, scene):
                return (f'trace tick {tick} in {keys} keys {keys} queue 3 '
                        f'x {x} y 640 held -1 body 0 scene {scene} demo 0\n').encode()

            def type(self, data, settle):
                self.typed.append(data)
                self.pump(settle)

            def pump(self, seconds):
                self.clock += seconds
                while self.events and self.events[0][0] <= self.clock:
                    _, tick, keys, x, scene = self.events.pop(0)
                    self.err += self.trace(tick, keys, x, scene)

        session = Session()
        with mock.patch('time.monotonic', side_effect=lambda: session.clock):
            result = rows._opening_skip_without_moving(session, timeout=.2)
        self.assertEqual(session.typed, [b'\x1b[C'])
        return result

    def test_delayed_post_input_tick_is_not_a_failed_skip(self):
        self.assertTrue(self.check_transition([(0.081, 13, 3, 0, 0), (.1, 14, 0, 0, 0)]))

    def test_moving_skip_still_fails(self):
        self.assertFalse(self.check_transition([(.02, 13, 3, 16, 0), (.04, 14, 0, 16, 0)]))

    def test_unskipped_input_still_fails(self):
        self.assertFalse(self.check_transition([(.02, 13, 3, 0, 1), (.04, 14, 0, 0, 1)]))

    def test_absent_transition_still_fails(self):
        self.assertFalse(self.check_transition([]))

    def test_held_movement_after_skip_still_fails(self):
        self.assertFalse(self.check_transition([(.02, 13, 3, 0, 0), (.04, 14, 0, 16, 0)]))

    def test_natural_completion_does_not_count_as_input(self):
        self.assertFalse(self.check_transition([(.02, 13, 0, 0, 0), (.04, 14, 0, 0, 0)]))


class SoundRowsSkipStartupMenu(unittest.TestCase):
    def test_sound_helper_enters_play_before_typing_quit(self):
        class Session:
            def __init__(self, argv, height, width, env):
                self.argv = argv
                self.job = 1234567
                self.typed = []

            def pump(self, seconds):
                pass

            def type(self, data):
                self.typed.append(data)

            def finish(self):
                pass

        scratch = ROOT / 'target/sound-entry-tests'
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as directory:
            ctx = SimpleNamespace(ROOT=directory, env_for=lambda: {}, Session=Session)
            with mock.patch.object(rows.subprocess, 'run', return_value=SimpleNamespace(stdout='')):
                session, _, _, _, _ = rows._sound_session('/unused', ctx, ['--mute'], settle=0)
        self.assertEqual(session.argv.count('--no-title'), 1,
                         'sound rows must reach run_live, not quit from the fire menu')
        self.assertEqual(session.typed, [b'q'])


if __name__ == '__main__':
    unittest.main()
