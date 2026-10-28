#!/usr/bin/env python3
"""cb12: every integer is a real rendered HUD, and replay is deterministic."""
from pathlib import Path
import argparse
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent.parent
GLYPHS = (
    ('###', '#.#', '#.#', '#.#', '###'),
    ('.#.', '##.', '.#.', '.#.', '###'),
    ('###', '..#', '###', '#..', '###'),
    ('###', '..#', '.##', '..#', '###'),
    ('#.#', '#.#', '###', '..#', '..#'),
    ('###', '#..', '###', '..#', '###'),
    ('#..', '#..', '###', '#.#', '###'),
    ('###', '..#', '.#.', '.#.', '.#.'),
    ('###', '#.#', '###', '#.#', '###'),
    ('###', '#.#', '###', '..#', '..#'),
)
QUADS = ' ▘▝▀▖▌▞▛▗▚▐▜▄▙▟█'


def expected_digits(value, tier):
    ds = [int(c) for c in str(value)]
    def lit(y, x):
        d, col = divmod(x, 4)
        return 1 <= y <= 5 and d < len(ds) and col < 3 and GLYPHS[ds[d]][y - 1][col] == '#'
    result = {}
    if tier == 'plain':
        width = len(ds) * 4 - 1
        for y in range(5):
            for x in range(width):
                if lit(y + 1, x):
                    result[19 + y, 79 - width + x] = '#'
    else:
        width = len(ds) * 2
        for y in range(3):
            for x in range(width):
                bits = sum(1 << (dy * 2 + dx) for dy in range(2) for dx in range(2)
                           if lit(y * 2 + dy, x * 2 + dx))
                if bits:
                    result[21 + y, 79 - width + x] = QUADS[bits]
    return result


def frames(binary, name, tier, every, replay=False):
    parent = ROOT / 'target/cb12-check'
    parent.mkdir(parents=True, exist_ok=True)
    prefix = binary.parent.name + '-' + name + '-' + tier + '-' + str(every) + ('-replay' if replay else '') + '-'
    dest = Path(tempfile.mkdtemp(prefix=prefix, dir=parent))
    count = 50 if name.endswith('spend') else 20
    command = [str(binary), '--headless', '--replay' if replay else '--script',
               str(ROOT / 'tests/cases' / (name + '.pk')), '--frames', str(count),
               '--every', str(every), '--tier', tier, '--trace', '--dump', str(dest)]
    p = subprocess.run(command, text=True, capture_output=True, check=True)
    (dest / 'trace.txt').write_text(p.stderr)
    found = []
    for path in dest.glob('count-*.txt'):
        tick, index, value = map(int, re.fullmatch(r'count-(\d+)-(\d+)-(\d+)\.txt', path.name).groups())
        found.append((tick, index, value, path))
    return dest, sorted(found), p.stderr


def check(binary):
    binary = Path(binary).resolve()
    for tier in ('rich', 'plain'):
        for name, wanted in [('cb12-scent-gain', list(range(1, 31))),
                             ('cb12-scent-spend', list(range(1, 50)) + list(range(48, -1, -1)))]:
            first, batch, trace = frames(binary, name, tier, 50)
            second, again, _ = frames(binary, name, tier, 1, replay=True)
            assert [v for _, _, v, _ in batch] == wanted, (name, tier, 'skipped integer')
            assert [(t, i, v) for t, i, v, _ in batch] == [(t, i, v) for t, i, v, _ in again], 'replay batch schedule changed'
            assert (first / 'final.state').read_bytes() == (second / 'final.state').read_bytes(), 'replay state changed'
            for tick, index, value, path in batch:
                text = path.read_text().splitlines()
                expected = expected_digits(value, tier)
                styles = []
                for row in path.with_suffix('.sty').read_text().splitlines():
                    expanded = []
                    for chunk in row.split():
                        style, repeat = chunk.split('*')
                        expanded.extend([int(style.split(',')[0])] * int(repeat))
                    styles.append(expanded)
                width = len(str(value)) * (2 if tier == 'rich' else 4) - (0 if tier == 'rich' else 1)
                actual = {(y, x): text[y][x] for y in range(21 if tier == 'rich' else 19, 24)
                          for x in range(79 - width, 79) if styles[y][x] == (221 if tier == 'rich' else 11)}
                assert actual == expected, (name, tier, tick, value, 'HUD drew another number')
                for suffix in ('.txt', '.sty'):
                    assert path.with_suffix(suffix).read_bytes() == (second / path.with_suffix(suffix).name).read_bytes(), 'render frequency changed counter frame'
            if name.endswith('gain'):
                assert batch[-1][0] == 20 and 'scent 30 ' in trace.splitlines()[0], 'currency not immediate or count late'
            else:
                assert batch[-1][0] <= 46, 'spending took more than twenty ticks'
            print('cb12-counter:', binary.parent.name, name, tier, len(batch), 'integer frames, replay identical')
    print('cb12-counter: green (0 skips)')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--bin', required=True)
    check(p.parse_args().bin)
