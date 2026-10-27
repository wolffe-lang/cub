import tempfile
import unittest
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parent.parent
check_directory = runpy.run_path(str(ROOT / 'tools/check-render-glyphs.py'))['check_directory']


class RenderedGlyphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_root = ROOT / 'target/rendered-glyph-tests'
        cls.temp_root.mkdir(parents=True, exist_ok=True)

    def fixture(self, root, cp):
        (root / 'frame.txt').write_text(chr(cp) + '\n')
        (root / 'frame.sty').write_text('style\n')
        (root / 'glyphs.txt').write_text('| U+2851 | declared |\n')

    def test_declared_rendered_cell_passes(self):
        with tempfile.TemporaryDirectory(dir=self.temp_root) as directory:
            root = Path(directory)
            self.fixture(root, 0x2851)
            frames, used = check_directory(root, root / 'glyphs.txt')
            self.assertEqual((frames, used), (1, {0x2851}))

    def test_unlisted_rendered_cell_fails(self):
        with tempfile.TemporaryDirectory(dir=self.temp_root) as directory:
            root = Path(directory)
            self.fixture(root, 0x2861)
            with self.assertRaisesRegex(AssertionError, 'unlisted rendered glyphs'):
                check_directory(root, root / 'glyphs.txt')

    def test_nested_replay_cell_is_checked(self):
        with tempfile.TemporaryDirectory(dir=self.temp_root) as directory:
            root = Path(directory)
            replay = root / 'case-rich'
            replay.mkdir()
            self.fixture(replay, 0x2861)
            with self.assertRaisesRegex(AssertionError, 'unlisted rendered glyphs'):
                check_directory(root, replay / 'glyphs.txt')

    def test_empty_rendered_audit_fails(self):
        with tempfile.TemporaryDirectory(dir=self.temp_root) as directory:
            root = Path(directory)
            (root / 'glyphs.txt').write_text('| U+2851 | declared |\n')
            with self.assertRaisesRegex(AssertionError, 'no frames'):
                check_directory(root, root / 'glyphs.txt')
