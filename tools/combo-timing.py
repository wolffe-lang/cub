#!/usr/bin/env python3
"""Hand-spaced requests through production replay, independent hold-sign oracle."""
import argparse
import math
from pathlib import Path
import runpy
import subprocess

ROOT = Path(__file__).resolve().parent.parent
FACINGS = [('n', ('up',)), ('ne', ('up', 'right')), ('e', ('right',)),
           ('se', ('down', 'right')), ('s', ('down',)),
           ('sw', ('down', 'left')), ('w', ('left',)), ('nw', ('up', 'left'))]


def cases():
    for eighth, (name, arrows) in enumerate(FACINGS):
        # 367ms lands on age11 exactly: the real-reader all-left boundary.
        for ms in ((150, 200, 250, 330, 367) if eighth == 0 else (150,)):
            yield f'cb11-hand-{name}-{ms}', eighth * 32, arrows, ms


def write_cases():
    for name, _, arrows, ms in cases():
        every = 1 if name == 'cb11-hand-n-150' else 44
        lines = [f'# frames 44 every {every}', '# cb11: three hand presses; arena is an explicit fixture',
                 'pk 1', 'seed 7', 'tier rich', 'size 80x24', 't 0 combat-witness 1', 't 0 exact']
        for ordinal in range(3):
            tick = 2 + ordinal * ms * 30 // 1000
            lines += [f't {tick} {arrow}' for arrow in arrows]
            lines += [f't {tick} bite']
            lines += [f't {tick} {arrow}-release' for arrow in arrows]
        (ROOT / 'tests/cases' / (name + '.pk')).write_text('\n'.join(lines) + '\n')


def states_of(trace):
    result = {}
    for line in trace.splitlines():
        words = line.split()
        if words[:1] == ['tick']:
            state = dict(zip(words[::2], map(int, words[1::2])))
            result[state['tick']] = state
    return result


def holds(states, aim, expected=(1, 2, 3)):
    """Require predicted actions and each hold; deterministic rows stay1/2/3."""
    expected = tuple(expected)
    bites = {}
    for state in states.values():
        if state['action'] == 1:
            bites.setdefault(state['started'], []).append(state)
    sequence = [rows[0]['combo'] for rows in bites.values()]
    assert sequence == list(expected), f'hold sequence {sequence}, expected {list(expected)}'
    sine, cosine = math.sin(aim * math.tau / 256), math.cos(aim * math.tau / 256)
    result = []
    for combo, (start, rows) in zip(expected, bites.items()):
        assert combo in (1, 2, 3), ('invalid expected strike', combo)
        origin = states[start]
        assert origin['aim'] == aim, (combo, 'wrong commitment', origin['aim'], aim)
        held = [row for row in rows if 3 <= row['tick'] - start <= (8 if combo == 3 else 6)]
        assert len(held) == (6 if combo == 3 else 4), (combo, 'missing hold ticks')
        for row in held:
            assert row['combo'] == combo and row['aim'] == aim, (combo, 'hold changed strike or aim')
            dx, dy = row['x'] - origin['x'], row['y'] - origin['y']
            forward, left = (dx * sine - dy * cosine) / 256, (-dx * cosine - dy * sine) / 256
            assert forward >= (1.99 if combo == 3 else .99), (combo, 'forward', forward)
            assert (left >= .99 if combo == 1 else left <= -.99 if combo == 2 else abs(left) < .01), (combo, 'left', left)
        result.append((combo, held[0]['tick'], round(forward, 3), round(left, 3)))
    return result


def north_pixels(states, frames, tier):
    """Check rendered fur relative to each commitment, including head swings."""
    centroid = runpy.run_path(str(ROOT / 'tests/pty_rows.py'))['cb07_fur_centroid']
    samples = {}
    for tick in states:
        frame = frames / f'frame-{tick:04d}'
        if not frame.with_suffix('.txt').exists():
            continue
        samples[tick] = centroid(frame.with_suffix('.txt').read_text(),
                                 frame.with_suffix('.sty').read_text(),
                                 range(6, 19), range(29, 52), tier == 'rich')
    bites = {}
    for row in states.values():
        if row['action'] == 1:
            bites.setdefault(row['started'], []).append(row)
    assert bites, 'no drawn strikes'
    for start, rows in bites.items():
        hit = rows[0]['combo']
        base = samples[start]
        assert base[2], 'empty standing drawing'
        swings = []
        for row in rows:
            age = row['tick'] - start
            c = samples[row['tick']]
            assert c[2], 'empty bite drawing'
            left, forward = -(c[0] - base[0]) / 2, -(c[1] - base[1]) / 4
            if 3 <= age <= (8 if hit == 3 else 6):
                # Standing and snapping plain glyphs have different occupied-cell
                # centroids (north loses about 0.23 cell); measure the visible
                # direction here, the exact whole-cell displacement in holds().
                assert forward > (0 if hit != 3 else 1), (hit, age, forward)
                if hit != 3:
                    assert left > 0 if hit == 1 else left < 0, (hit, age, left)
            if hit == 3 and 5 <= age <= 12:
                swings.append((age, left))
        if hit == 3:
            lefts = [v for a, v in swings if (a - 5) // 2 % 2 == 0]
            rights = [v for a, v in swings if (a - 5) // 2 % 2 == 1]
            assert len(lefts) == len(rights) == 4 and min(lefts) > max(rights), ('head shake', swings)


def check(binary, out=None):
    out = Path(out or ROOT / 'target' / 'combo-timing' / Path(binary).parent.name)
    failures = []
    for name, aim, _, ms in cases():
        for tier in ('rich', 'plain'):
            dest = out / f'{name}-{tier}'
            p = subprocess.run([str(binary), '--headless', '--script', str(ROOT / 'tests/cases' / (name + '.pk')),
                                '--frames', '44', '--every', '1', '--tier', tier, '--trace', '--dump', str(dest)],
                               capture_output=True, text=True)
            dest.mkdir(parents=True, exist_ok=True)
            (dest / 'trace.txt').write_text(p.stderr)
            label = f'{name}-{tier}'
            try:
                assert p.returncode == 0, f'binary exit {p.returncode}'
                states = states_of(p.stderr)
                assert len(states) == 44, f'missing trace ticks: {len(states)}'
                observed = [(r['tick'], r['combo'], r['x'] - states[r['started']]['x'],
                             r['y'] - states[r['started']]['y']) for r in states.values()
                            if r['action'] == 1 and r['tick'] - r['started'] == 3]
                print(f'OBSERVED {label} (tick, strike, dx, dy)={observed}', flush=True)
                result = holds(states, aim)
                if aim == 0:
                    north_pixels(states, dest, tier)
                print(f'PASS {label} interval_ms={ms} holds={result}', flush=True)
            except AssertionError as error:
                print(f'FAIL {label}: {error}', flush=True)
                failures.append(label)
    assert not failures, f'hand-timing rows failed: {failures}'
    print(f'combo-timing: {2 * len(list(cases()))} rows green', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bin', default=str(ROOT / 'target/native/cub'))
    parser.add_argument('--out')
    parser.add_argument('--write-cases', action='store_true')
    args = parser.parse_args()
    if args.write_cases:
        write_cases()
    else:
        check(args.bin, args.out)
