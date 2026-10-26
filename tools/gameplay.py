#!/usr/bin/env python3
"""Assert gameplay semantics on the actual binaries, not just rendered snapshots."""
import argparse
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'target' / 'gameplay'


def run(binary, name, tier='rich', frames=None, ghosts=None):
    case = ROOT / 'tests' / 'cases' / (name + '.pk')
    if frames is None:
        frames = int(re.search(r'# frames (\d+)', case.read_text())[1])
    dest = OUT / (Path(binary).parent.name + '-' + name + '-' + tier)
    args = [str(binary), '--headless', '--script', str(case), '--frames', str(frames),
            '--every', str(frames), '--tier', tier, '--trace', '--dump', str(dest)]
    if ghosts:
        args += ['--ghost-dir', str(ghosts)]
    p = subprocess.run(args, capture_output=True, text=True, check=True)
    (dest / 'trace.txt').write_text(p.stderr)
    states, foes = {}, {}
    tick = None
    for line in p.stderr.splitlines():
        words = line.split()
        if words[:1] == ['tick']:
            state = dict(zip(words[::2], map(int, words[1::2])))
            tick = state['tick']
            states[tick] = state
            foes[tick] = []
        elif words[:1] == ['foe']:
            foes[tick].append(dict(zip(words[::2], map(int, words[1::2]))))
    assert len(states) == frames, (name, 'trace missing ticks')
    return dest, states, foes


def check(binary):
    expected = {}
    for tier in ('rich', 'plain'):
        for name in ('bite', 'parry', 'dodge', 'weasel-retreat', 'fox-feint',
                     'trail-fading', 'rest', 'death-recovery', 'thorn-gate'):
            dest, states, foes = run(binary, name, tier)
            final = states[max(states)]
            if name == 'bite':
                assert any(fs[0]['health'] <= 0 for fs in foes.values()), 'bite never killed'
                assert any(v['drops'] > 0 for v in states.values()), 'no visible scent pickup'
                assert final['scent'] >= 8, 'walking over scent did not collect it'
            elif name == 'parry':
                assert any(fs[0]['phase'] == 4 for fs in foes.values()), 'parry did not stagger'
                assert final['health'] == 52
            elif name == 'dodge':
                assert any(v['action'] == 4 for v in states.values()), 'no dodge'
                assert final['health'] == 52
            elif name == 'weasel-retreat':
                crouch = next(t for t, fs in foes.items() if fs[0]['phase'] == 1)
                active = next(t for t, fs in foes.items() if fs[0]['phase'] == 2)
                assert active - crouch == 12 and final['health'] < 52
                assert any(fs[0]['phase'] == 3 for fs in foes.values())
            elif name == 'fox-feint':
                false = next(t for t, fs in foes.items() if fs[2]['phase'] == 5)
                real = next(t for t, fs in foes.items() if fs[2]['phase'] == 1)
                active = next(t for t, fs in foes.items() if fs[2]['phase'] == 2)
                assert real - false == 16 and active - real == 12
                assert states[active]['flasks'] == states[active - 1]['flasks'] - 1
            elif name == 'trail-fading':
                assert states[60]['trail'] > 0 and final['trail'] == 0
            elif name == 'rest':
                assert final['health'] == 64 and final['stamina'] == 80 and final['scent'] == 0
            elif name == 'death-recovery':
                assert states[47]['mark_scent'] == 28 and states[47]['action'] == 6
                assert final['deaths'] == 1 and final['mark'] == 0 and final['scent'] == 28
            elif name == 'thorn-gate':
                assert any(v['gate'] == 0 for v in states.values()) and final['gate'] == 1
            state_bytes = (dest / 'final.state').read_bytes()
            if tier == 'rich':
                expected[name] = state_bytes
            else:
                assert expected[name] == state_bytes, (name, 'tier changed the simulation')
            print('gameplay:', Path(binary).parent.name, name, tier, 'ok')
    # The new controls must really commit their aim/action on shipping binaries.
    for tier in ('rich', 'plain'):
        for name, aim in [('n', 0), ('ne', 32), ('e', 64), ('se', 96), ('s', 128),
                          ('sw', 160), ('w', 192), ('nw', 224)]:
            _, states, _ = run(binary, 'aim-' + name, tier)
            assert all(state['aim'] == aim for state in states.values()), ('aim', name)
            assert states[1]['action'] == 2, 'aim fixture did not attack'
        _, locked, _ = run(binary, 'aim-lock', tier)
        last = locked[max(locked)]
        assert any(v['action'] == 2 and v['lock'] >= 0 and v['aim'] != 64 for v in locked.values()), 'nearby lock failed to override right arrow'
        dest, states, _ = run(binary, 'three-bites', tier)
        starts = [(n, v['combo']) for n, v in states.items()
                  if v['action'] == 1 and v['started'] == n]
        assert starts == [(1, 1), (12, 2), (23, 3)], starts
        assert states[34]['combo'] == 0, 'lapsed chain failed to reset'
        _, states, _ = run(binary, 'heavy', tier)
        assert states[1]['action'] == 7 and states[1]['stamina'] == 28
        assert states[39]['action'] == 7 and states[40]['action'] == 0
        print('gameplay:', Path(binary).parent.name, 'aim/combo/heavy', tier, 'ok')
    for tier in ('rich', 'plain'):
        _, opening, _ = run(binary, 'opening', tier)
        assert opening[90]['scene'] == 1 and opening[180]['scene'] == 1 and opening[269]['scene'] == 1
        _, skipped, _ = run(binary, 'opening-skip', tier)
        assert skipped[100]['scene'] == 1 and skipped[101]['scene'] == 0
        _, journey, enemies = run(binary, 'world-return', tier)
        assert {s['area'] for s in journey.values()} == {0, 1, 2}
        final = journey[max(journey)]
        assert final['area'] == 0 and final['shortcuts'] == 3 and final['deaths'] == 1 and not final['mark']
        assert any(s['area'] == 1 and s['mark_area'] == 2 and s['mark'] for s in journey.values()), 'no cross-area death'
        assert any(s['area'] == 2 and any(f['kind'] == 2 and f['health'] == 0 for f in enemies[t]) for t,s in journey.items()), 'hawk never fought'
        print('gameplay: connected journey, hawk, opening and recovery', tier, 'ok')
    for cache in (0, 1, 2, 3):
        _, states, _ = run(binary, 'coast-cache-' + str(cache))
        final = states[max(states)]
        assert final['area'] == 0 and final['caches'] & (1 << cache), 'coast bundle not collected'
    # A natural, unassisted death: approach and re-engage the fox after retreats.
    ghosts = OUT / (Path(binary).parent.name + '-ghosts')
    ghosts.mkdir(parents=True, exist_ok=True)
    before = set(ghosts.glob('*.pk'))
    _, states, _ = run(binary, 'natural-death', ghosts=ghosts)
    files = set(ghosts.glob('*.pk')) - before
    assert files, 'natural death did not write a ghost'
    preserved = {p: p.read_bytes() for p in ghosts.glob('*.pk')}
    run(binary, 'natural-death', ghosts=ghosts)
    assert all(p.read_bytes() == data for p, data in preserved.items()), 'archive was overwritten'
    assert len(set(ghosts.glob('*.pk')) - set(preserved)) == len(files), 'repeat death reused a filename'
    for path in sorted(files):
        text = path.read_text()
        last = max(int(m) for m in re.findall(r'^t (\d+)', text, re.M)) + 1
        assert states[last]['action'] == 6 and states[last]['health'] == 0
        dest = OUT / ('verify-' + path.stem)
        subprocess.run([str(binary), '--headless', '--script', str(path), '--frames', str(last),
                        '--every', str(last), '--dump', str(dest)], check=True)
        got = (dest / 'final.state').read_text().splitlines()[0].split()
        assert dict(zip(got[::2], map(int, got[1::2]))) == states[last], 'ghost replay state differs'
        print('gameplay: death archive replay-verified at tick', last)
    # Exercise a storage error without changing permissions or touching user data.
    invalid = OUT / 'not-a-directory'
    invalid.write_text('fixture')
    p = subprocess.run([str(binary), '--headless', '--script', str(ROOT / 'tests/cases/death-recovery.pk'),
                        '--frames', '48', '--every', '48', '--ghost-dir', str(invalid),
                        '--dump', str(OUT / 'write-error')], capture_output=True)
    assert p.returncode == 2, 'archive failure was hidden'


ENCOUNTERS = ('bite', 'parry', 'dodge', 'weasel-retreat', 'fox-feint', 'natural-death', 'aim-lock')


def bodies(binary):
    """cb02c: no body inside another's drawing, no foe touching the cub out
    of a bite's reach, no foe inside another; over every real-key script as
    recorded, then fifty seeds at both sizes (a swarm from behind and the
    encounter scripts' keys in each world)."""
    cases = sorted(str(p) for p in (ROOT / 'tests' / 'cases').glob('*.pk'))
    p = subprocess.run([str(binary), '--measure'] + cases, capture_output=True, text=True, check=True)
    (OUT / (Path(binary).parent.name + '-measure.txt')).write_text(p.stdout)
    total = [l for l in p.stdout.splitlines() if l.startswith('census total ')]
    assert len(total) == 1, 'no census total'
    words = total[0].split()[2:]
    census = dict(zip(words[::2], map(int, words[1::2])))
    assert census['ticks'] > 40000 and census['contact'] > 0, census
    assert census['overlap'] == 0 and census['contact_unreachable'] == 0 and census['foe_overlap'] == 0, census
    print('gameplay:', Path(binary).parent.name, 'body census over', len(cases), 'scripts:', total[0])
    scripts = [str(ROOT / 'tests' / 'cases' / (n + '.pk')) for n in ENCOUNTERS]
    p = subprocess.run([str(binary), '--body-audit'] + scripts, capture_output=True, text=True)
    (OUT / (Path(binary).parent.name + '-body-audit.txt')).write_text(p.stdout + p.stderr)
    assert p.returncode == 0, ('body audit', p.returncode, p.stdout[-400:])
    rows = [l.split() for l in p.stdout.splitlines()[1:] if not l.startswith('total')]
    assert len(rows) == 100 and all(int(r[2]) > 0 and int(r[4]) > 0 for r in rows), 'a swarm was not fought'
    print('gameplay:', Path(binary).parent.name, 'body audit, 100 worlds:', p.stdout.splitlines()[-1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--bin', required=True)
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    check(Path(args.bin).resolve())
    bodies(Path(args.bin).resolve())
    import runpy
    world = runpy.run_path(str(ROOT / 'tools/world_checks.py'))
    world['check'](Path(args.bin).resolve())
    print('gameplay: green (0 skips)')

if __name__ == '__main__':
    main()
