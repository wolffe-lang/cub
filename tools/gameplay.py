#!/usr/bin/env python3
"""Assert gameplay semantics on the actual binaries, not just rendered snapshots."""
import argparse
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'target' / 'gameplay'


def run(binary, name, tier='rich', frames=None, ghosts=None, label=''):
    case = ROOT / 'tests' / 'cases' / (name + '.pk')
    if frames is None:
        frames = int(re.search(r'# frames (\d+)', case.read_text())[1])
    dest = OUT / (Path(binary).parent.name + '-' + name + '-' + tier + label)
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
        # The last game event (the trailer's ghost words stand at the death tick itself).
        last = max(int(m) for m in re.findall(r'^t (\d+) (?!ghost-)', text, re.M)) + 1
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


BOSSES = {4: 'boar', 5: 'lynx', 6: 'elk', 7: 'alpha'}
BOSS_HEALTH = {4: 240, 5: 140, 6: 400, 7: 300}
BOSS_BIT = {4: 1, 5: 2, 6: 4, 7: 8}
BOSS_SHORTCUT = {4: 1, 5: 4, 6: 8, 7: 0}
BOSS_AREA = {4: 1, 5: 3, 6: 4, 7: 5}
# Parryable attacks by boss (sim.boss_move); the howl (alpha 2) does no damage.
PARRYABLE = {4: {0}, 5: {0, 1}, 6: {0, 2}, 7: {0}}
PARRY_WINDOW = 9


def boss_rows(foes, kind):
    """The boss's row at every tick of a trace."""
    return {t: next(f for f in fs if f['kind'] == kind) for t, fs in foes.items()
            if any(f['kind'] == kind for f in fs)}


def tells(rows):
    """(start, strike, attack) of every windup that reached its strike."""
    out, start = [], None
    for t in sorted(rows):
        f = rows[t]
        if f['phase'] == 1 and start is None:
            start = f['since']
        elif f['phase'] == 2 and start is not None:
            out.append((start, f['since'], f['attack']))
            start = None
        elif f['phase'] not in (1, 2):
            start = None
    return out


def bosses(binary):
    """cb04: the four bosses on their real-key scripts, in both tiers: every
    parryable telegraph at least the parry window, phase two at half health,
    the beaten bit and shortcut in the state, the end after the alpha."""
    for tier in ('rich', 'plain'):
        for kind, name in BOSSES.items():
            _, states, foes = run(binary, 'boss-%s-windup' % name, tier)
            rows = boss_rows(foes, kind)
            final = states[max(states)]
            assert rows[max(rows)]['phase'] == 1, (name, 'windup case ends outside a windup')
            assert final['bosses'] & BOSS_BIT[kind] == 0 and final['area'] == BOSS_AREA[kind]
            _, states, foes = run(binary, 'boss-%s-phase2' % name, tier)
            rows = boss_rows(foes, kind)
            last = rows[max(rows)]
            assert 0 < last['health'] <= BOSS_HEALTH[kind] // 2, (name, 'phase two not reached', last)
            _, states, foes = run(binary, 'boss-%s-beaten' % name, tier)
            rows = boss_rows(foes, kind)
            final = states[max(states)]
            assert final['bosses'] & BOSS_BIT[kind], (name, 'beaten bit missing')
            assert final['shortcuts'] & BOSS_SHORTCUT[kind] == BOSS_SHORTCUT[kind], (name, 'shortcut closed')
            assert any(f['health'] <= 0 for f in rows.values()), (name, 'boss never fell')
            seen = tells(rows)
            assert seen, (name, 'no telegraph reached its strike')
            for start, strike, attack in seen:
                if attack in PARRYABLE[kind]:
                    assert strike - start >= PARRY_WINDOW, (name, 'telegraph under the parry window', start, strike, attack)
            assert final['deaths'] == 0, (name, 'the fighter fell')
            print('gameplay:', Path(binary).parent.name, name, tier, 'windup/phase2/beaten ok,',
                  len(seen), 'telegraphs, shortest', min(s - a for a, s, _ in seen))
        _, states, _ = run(binary, 'end', tier)
        final = states[max(states)]
        card = next(t for t, s in states.items() if s['scene'] == 3)
        assert final['end'] == 1 and final['bosses'] == 15, final
        assert final['scene'] == 0 and max(states) > card, 'r did not keep the game playing'
        # Foe kinds: 1 fox, 2 hawk, 5 lynx, 6 elk, 7 alpha.
        for name, area, kinds in (('crags', 3, {1, 5}), ('river', 4, {2, 6}), ('old-den', 5, {1, 7})):
            _, states, foes = run(binary, name, tier)
            final = states[max(states)]
            assert final['area'] == area, (name, final['area'])
            assert kinds <= {f['kind'] for f in foes[max(foes)] if f['health'] > 0}, (name, 'foes missing')
        _, states, _ = run(binary, 'title', tier)
        assert states[1]['scene'] == 2 and states[2]['scene'] == 2
        _, states, _ = run(binary, 'title-demo', tier)
        assert states[331]['scene'] == 2, 'the title did not hold through the idle time'
        print('gameplay: end, the three new areas, the title', tier, 'ok')


def ghosts(binary):
    """cb04: a death's trailer matches the sim frame for frame; the committed
    archive draws a ghost; an empty archive, or another world's, draws none."""
    import shutil
    import tempfile
    for tier in ('rich', 'plain'):
        archive = OUT / (Path(binary).parent.name + '-ghost-archive-' + tier)
        shutil.rmtree(archive, ignore_errors=True)
        archive.mkdir(parents=True)
        _, states, _ = run(binary, 'ghost-death', tier, ghosts=archive)
        files = sorted(archive.glob('*.pk'))
        assert len(files) == 1, 'the death wrote %d archives' % len(files)
        text = files[0].read_text()
        frames = {}
        for m in re.finditer(r'^t (\d+) ghost-(x|y|area) (-?\d+)$', text, re.M):
            frames.setdefault(int(m[1]), {})[m[2]] = int(m[3])
        death = re.search(r'^t (\d+) ghost-death (\d+)$', text, re.M)
        assert frames and death, 'no trailer in the archive'
        assert len(frames) == 90 and max(frames) == int(death[1]), (len(frames), max(frames), death[1])
        assert states[int(death[1])]['deaths'] == int(death[2]) == 1
        for t, f in frames.items():
            assert (f['x'], f['y'], f['area']) == (states[t]['x'], states[t]['y'], states[t]['area']), (t, f, states[t])
        committed = ROOT / 'tests' / 'ghosts'
        assert [p.name for p in files] == [p.name for p in committed.glob('*.pk')]
        assert re.sub(r'^tier .*$', '', text, flags=re.M) == re.sub(r'^tier .*$', '', next(committed.glob('*.pk')).read_text(), flags=re.M), 'committed archive differs from a fresh death'
        shown, states_a, _ = run(binary, 'ghost', tier, ghosts=committed, label='-shown')
        empty = Path(tempfile.mkdtemp(prefix='cub-no-ghosts-', dir=OUT))
        none, states_b, _ = run(binary, 'ghost', tier, ghosts=empty, label='-none')
        other = Path(tempfile.mkdtemp(prefix='cub-other-world-', dir=OUT))
        (other / files[0].name).write_text(text.replace('seed 1\n', 'seed 2\n', 1))
        foreign, states_c, _ = run(binary, 'ghost', tier, ghosts=other, label='-foreign')
        assert states_a == states_b == states_c, 'ghosts changed the simulation'
        a, b, c = ((d / 'final.txt').read_text() for d in (shown, none, foreign))
        assert a != b, 'the archive drew no ghost'
        assert b == c, "another world's death drew a ghost"
        if tier == 'plain':
            # The plain mark is one `x` at the death spot, over the forest's own marks.
            assert a.count('x') == b.count('x') + 1, (a.count('x'), b.count('x'))
        print('gameplay: ghost trailer, display and absence', tier, 'ok')


def fairness(binary):
    """cb04: the census on the shipping binary, its summary kept for the note."""
    p = subprocess.run([str(binary), '--boss-census'], capture_output=True, text=True)
    (OUT / (Path(binary).parent.name + '-boss-census.txt')).write_text(p.stdout + p.stderr)
    assert p.returncode == 0, ('boss census', p.returncode, p.stdout[-600:])
    lines = [l for l in p.stdout.splitlines() if l.startswith('fairness ')]
    assert len(lines) == 4, lines
    for line in lines:
        words = line.split()
        assert 'unwon:0' in words and words[-1] == '0' and words[-2] == 'arena_breaches', line
        print('gameplay:', line)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--bin', required=True)
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    check(Path(args.bin).resolve())
    bodies(Path(args.bin).resolve())
    bosses(Path(args.bin).resolve())
    ghosts(Path(args.bin).resolve())
    fairness(Path(args.bin).resolve())
    import runpy
    world = runpy.run_path(str(ROOT / 'tools/world_checks.py'))
    world['check'](Path(args.bin).resolve())
    print('gameplay: green (0 skips)')

if __name__ == '__main__':
    main()
