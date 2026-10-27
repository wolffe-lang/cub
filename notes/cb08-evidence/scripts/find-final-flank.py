#!/usr/bin/env python3
"""Bounded real-key search for a flank witness in an existing boss journey.
Only truncates recorded keys and appends arrow/release/Space events; no
position, health, foe, timing or simulation-state injection is introduced.
"""
from pathlib import Path
import math
import subprocess

ROOT = Path('/work')
BIN = ROOT / 'target/release/cub'
OUT = ROOT / 'target/cb08-flank-search'
OUT.mkdir(exist_ok=True)
CASE = ROOT / 'tests/cases/boss-lynx-beaten.pk'
TRACE = ROOT / 'target/cb08-lynx.trace'


def parse(text):
    states, foes, tick = {}, {}, None
    for line in text.splitlines():
        w = line.split()
        if not w:
            continue
        if w[0] == 'tick':
            state = dict(zip(w[::2], map(int, w[1::2])))
            tick = state['tick']
            states[tick], foes[tick] = state, {}
        elif w[0] == 'foe':
            f = dict(zip(w[::2], map(int, w[1::2])))
            foes[tick][f['foe']] = f
    return states, foes


def witness(states, foes, first, expected_aim):
    for tick in sorted(states):
        if tick <= first or tick-1 not in foes:
            continue
        s = states[tick]
        if s['action'] != 1 or s['aim'] != expected_aim or s['combo'] != 1:
            continue
        for i, f in foes[tick].items():
            old = foes[tick-1].get(i)
            if not old or f['kind'] != 5 or f['health'] >= old['health'] or f['last_hit'] != s['started']:
                continue
            angle = s['cone'] * math.tau / 256
            sn, cs = round(256*math.sin(angle)), round(256*math.cos(angle))
            committed = states.get(s['started'])
            if committed is None:
                continue
            margins = []
            for origin in (s, committed):
                dx, dy = old['x']-origin['x'], old['y']-origin['y']
                dot, cross = dx*sn-dy*cs, dx*cs+dy*sn
                margins.append(max(-dot, abs(cross)-dot))
            # Both of cb07's former centre-cone endpoints must miss,
            # well clear of any floating/lookup rounding boundary.
            if min(margins) > 10000:
                return tick, s['aim'], s['cone'], old['health'], f['health'], min(margins)
    return None


states, foes = parse(TRACE.read_text())
starts, seen = [], set()
for tick, s in states.items():
    for f in foes[tick].values():
        if f['kind'] == 5 and f['health'] > 0 and f['phase'] == 4 and s['action'] == 0 and tick-f['since'] <= 14 and f['since'] not in seen:
            starts.append(tick)
            seen.add(f['since'])
starts = starts[:4]
assert starts, 'no real stagger/idle windows'
original = CASE.read_text().splitlines()
arrows = [('up',), ('up','right'), ('right',), ('down','right'), ('down',), ('down','left'), ('left',), ('up','left')]
releases = ('release', 'ctrl-up', 'shift-up', 'up-release', 'down-release', 'left-release', 'right-release')
trial = 0
for start in starts:
    prefix = [line for line in original if not line.startswith('#') and not (line.startswith('t ') and int(line.split()[1]) >= start)]
    moves = [((), 0)] + [(direction, length) for direction in (('up',),('down',),('left',),('right',)) for length in (4,8,12,16)]
    for move, length in moves:
        for aim in (1,3,5,7,0,2,4,6):
            trial += 1
            assert trial <= 544, 'bounded search exceeded'
            events = prefix.copy()
            events += [f't {start} {key}' for key in releases]
            for t in range(start, start+length):
                events += [f't {t} {key}' for key in move]
            strike = start+length
            events += [f't {strike} {key}' for key in releases]
            events += [f't {strike} {key}' for key in arrows[aim]]
            events.append(f't {strike} bite')
            end = strike+7
            events.append(f'# frames {end} every 1 from {max(start,strike-1)}')
            candidate = OUT/'candidate.pk'
            candidate.write_text('\n'.join(events)+'\n')
            result = subprocess.run([str(BIN),'--headless','--script',str(candidate),'--frames',str(end),'--every',str(end),'--tier','plain','--trace','--dump',str(OUT/'trial')], capture_output=True, text=True, check=True)
            ss, ff = parse(result.stderr)
            hit = witness(ss, ff, strike, aim*32)
            if hit:
                recipe = f'prefix {start} move {move} ticks {length} aim {aim*32} result {hit} trials {trial}'
                (OUT/'whisper-flank.pk').write_text('# cb08 real-key flank: '+recipe+'\n'+'\n'.join(events)+'\n')
                (OUT/'winner.trace').write_text(result.stderr)
                (OUT/'recipe.txt').write_text(recipe+'\n')
                print('FLANK FOUND '+recipe, flush=True)
                raise SystemExit(0)
            if trial % 16 == 0:
                print(f'flank search {trial}/544; prefix {start}', flush=True)
print('FLANK NOT FOUND in bounded real-key candidates', flush=True)
raise SystemExit(1)
