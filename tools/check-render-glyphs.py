#!/usr/bin/env python3
"""Check actual rendered art cells against GLYPHS, including composited heads."""
import argparse
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent.parent


def check_directory(directory, document):
    declared = {int(cp, 16) for cp in re.findall(r'^\| U\+([0-9A-Fa-f]+)', Path(document).read_text(), re.M)}
    frames = [p for p in Path(directory).rglob('*.txt') if p.with_suffix('.sty').is_file()]
    assert frames, 'rendered glyph audit contains no frames'
    used = set()
    for frame in frames:
        cps = {ord(c) for c in frame.read_text() if ord(c) > 255}
        missing = cps - declared
        assert not missing, (frame.name, 'unlisted rendered glyphs', [f'U+{c:04X}' for c in sorted(missing)])
        used.update(cps)
    return len(frames), used


def check(binary, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='rendered-glyphs-', dir=out) as directory:
        subprocess.run([str(binary), '--art-study', '--dump', directory], check=True)
        frames, used = check_directory(directory, ROOT / 'docs/GLYPHS.md')
    golden_frames, golden_used = check_directory(ROOT / 'tests/goldens', ROOT / 'docs/GLYPHS.md')
    used.update(golden_used)
    text = f'rendered-glyphs art_frames {frames} golden_frames {golden_frames} nonbyte_codepoints {len(used)} unlisted 0\n'
    text += ' '.join(f'{cp:04X}' for cp in sorted(used)) + '\n'
    (out / (Path(binary).parent.name + '-rendered-glyphs.txt')).write_text(text)
    print(text.splitlines()[0])


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--bin', required=True)
    ap.add_argument('--out', default=str(ROOT / 'target/rendered-glyphs'))
    args = ap.parse_args()
    check(Path(args.bin).resolve(), args.out)
