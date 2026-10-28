#!/usr/bin/env python3
"""cb14's flank search over cb11's bite chain, the third tried: the first
two (the lane's prefix-and-aim search over the lynx fight's keys, and
cb08's recipe at its own stagger windows) found none (flank-searches.txt).
Over cb11's queued bite requests (e41c23ae) the lynx fight's keys moved;
a fresh bite is combo 1 (its cone slanted 11 left of the aim) and starts
the tick after the press, so a bite from where the fighter stands either
turns into the lynx's centre or lunges away from its body (probed at
ticks 805 and 808).
This is cb08's real-key recipe (notes/cb08-evidence/scripts/
find-final-flank.py: truncate the recorded keys at a start, hold one or
two arrows for a few ticks, release everything, then an aim and Space)
widened to every tick of the lynx fight where Whisper stands idle within
three cells of the lynx, eight move directions, and judged by
tests/pty_rows.py's own cb08 predicate. Candidates run in a fixed order on
a few workers; the first in that order that passes is written.

    python3 -I flank-search-moves.py <cub binary> <repo root> <out case path> <workers>
"""
import math
import multiprocessing
import pathlib
import subprocess
import sys
import tempfile

binary, root, out = sys.argv[1], pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3])
workers = int(sys.argv[4])
SOURCE = 'tests/cases/boss-lynx-beaten.pk'
source = (root / SOURCE).read_text().splitlines()
header = [l for l in source if not l.startswith('t ') and not l.startswith('#') and l.strip()]
header_t0 = [l for l in source if l.startswith('t 0 ')]
keys = [(int(l.split()[1]), l) for l in source if l.startswith('t ') and not l.startswith('t 0 ')]
RELEASES = ['release', 'ctrl-up', 'shift-up', 'up-release', 'down-release', 'left-release', 'right-release']
AIMS = [['down', 'left'], ['left'], ['up', 'left'], ['down'], ['up'], ['down', 'right'], ['right'], ['up', 'right']]
MOVES = [([], 0)]
for length in (4, 8, 12, 16):
    for move in (['down'], ['left'], ['up'], ['right'], ['down', 'left'], ['up', 'left'], ['down', 'right'], ['up', 'right']):
        MOVES.append((move, length))


def parse(text):
    states, foes, tick = {}, {}, None
    for line in text.splitlines():
        words = line.split()
        if words[:1] == ['tick']:
            st = dict(zip(words[::2], map(int, words[1::2])))
            tick = st['tick']
            states[tick] = st
            foes[tick] = []
        elif words[:1] == ['foe'] and tick is not None:
            foes[tick].append(dict(zip(words[::2], map(int, words[1::2]))))
    return states, foes


def check(states, foes):
    """tests/pty_rows.py's cb08_whisper_flank predicate, with the margin."""
    for tick, state in states.items():
        if tick - 1 not in foes or state['action'] != 1:
            continue
        before = {f['foe']: f for f in foes[tick - 1]}
        for foe in foes[tick]:
            old = before.get(foe['foe'])
            if foe['kind'] != 5 or old is None or foe['health'] >= old['health']:
                continue
            angle = state['cone'] * math.tau / 256
            sine, cosine = round(256 * math.sin(angle)), round(256 * math.cos(angle))
            committed = states.get(state['started'])
            if committed is None:
                continue
            misses, margins = [], []
            for origin in (state, committed):
                dx, dy = old['x'] - origin['x'], old['y'] - origin['y']
                dot, cross = dx * sine - dy * cosine, dx * cosine + dy * sine
                misses.append(dot < 0 or abs(cross) > dot)
                margins.append(max(-dot, abs(cross) - dot))
            if all(misses) and foe['last_hit'] == state['started']:
                return (tick, state['started'], state['cone'], old['health'], foe['health'], min(margins))
    return None


def case_text(start, move, length, aim):
    lines = list(header) + list(header_t0)
    lines += [l for t, l in keys if t < start]
    lines += ['t %d %s' % (start, k) for k in RELEASES]
    for t in range(start, start + length):
        lines += ['t %d %s' % (t, k) for k in move]
    strike = start + length
    lines += ['t %d %s' % (strike, k) for k in RELEASES + aim + ['bite']]
    end = strike + 7
    return '\n'.join(lines) + '\n\n# frames %d every 1 from %d\n' % (end, strike), end


def trial(candidate):
    start, move, length, aim = candidate
    text, end = case_text(start, move, length, aim)
    work = pathlib.Path(tempfile.mkdtemp(prefix='cb14-flank-moves-'))
    case = work / 'try.pk'
    case.write_text(text)
    p = subprocess.run([binary, '--headless', '--script', str(case), '--frames', str(end), '--every', str(end),
                        '--tier', 'plain', '--trace', '--dump', str(work / 'dump')], capture_output=True, text=True)
    subprocess.run(['rm', '-rf', str(work)])
    if p.returncode != 0:
        return None
    return check(*parse(p.stderr))


def starts():
    with tempfile.TemporaryDirectory(prefix='cb14-flank-trace-') as work:
        frames = [l for l in source if l.startswith('# frames ')][0].split()[2]
        p = subprocess.run([binary, '--headless', '--script', str(root / SOURCE), '--frames', frames, '--every', frames,
                            '--tier', 'plain', '--trace', '--dump', work + '/dump'], capture_output=True, text=True, check=True)
    states, foes = parse(p.stderr)
    found = []
    for tick in sorted(states):
        if states[tick]['action'] != 0:
            continue
        if any(f['kind'] == 5 and f['health'] > 0 and f['gap'] <= 3 for f in foes[tick]):
            found.append(tick)
    return found


if __name__ == '__main__':
    ticks = starts()
    print('starts %d: %s' % (len(ticks), ' '.join(map(str, ticks))), flush=True)
    candidates = [(s, m, n, a) for (m, n) in MOVES for s in ticks for a in AIMS]
    print('candidates %d' % len(candidates), flush=True)
    with multiprocessing.Pool(workers) as pool:
        for index, result in enumerate(pool.imap(trial, candidates, chunksize=4), 1):
            if result:
                start, move, length, aim = candidates[index - 1]
                recipe = 'start %d move %s ticks %d aim %s result %s trials %d' % (
                    start, '+'.join(move) or 'none', length, '+'.join(aim), result, index)
                text, _ = case_text(start, move, length, aim)
                out.write_text('# cb14 real-key flank over the grown bowl (boss-lynx-beaten keys): %s\n' % recipe + text)
                print('FLANK FOUND ' + recipe, flush=True)
                pool.terminate()
                sys.exit(0)
            if index % 400 == 0:
                print('flank search %d/%d' % (index, len(candidates)), flush=True)
    print('no flank found in %d trials' % len(candidates), flush=True)
    sys.exit(1)
