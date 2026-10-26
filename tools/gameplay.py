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
            assert states[1]['action'] == 1, 'aim fixture did not attack'
        _, locked, _ = run(binary, 'aim-lock', tier)
        last = locked[max(locked)]
        assert any(v['action'] == 1 and v['lock'] >= 0 and v['aim'] != 64 for v in locked.values()), 'nearby lock failed to override right arrow'
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
        # The two scratch archives (an empty one, another world's) live only
        # for their runs: mkdtemp makes them owner-only, and a directory the
        # runner cannot scan breaks the artifact upload, so they are world
        # readable while they exist and gone after, on success or failure.
        empty = Path(tempfile.mkdtemp(prefix='cub-no-ghosts-', dir=OUT))
        other = Path(tempfile.mkdtemp(prefix='cub-other-world-', dir=OUT))
        try:
            for d in (empty, other):
                d.chmod(0o755)
            none, states_b, _ = run(binary, 'ghost', tier, ghosts=empty, label='-none')
            (other / files[0].name).write_text(text.replace('seed 1\n', 'seed 2\n', 1))
            foreign, states_c, _ = run(binary, 'ghost', tier, ghosts=other, label='-foreign')
        finally:
            for d in (empty, other):
                shutil.rmtree(d, ignore_errors=True)
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

def feel(binary):
    for option, columns in [('--feel-audit', 8), ('--chase-audit', 8)]:
        p = subprocess.run([str(binary), option], capture_output=True, text=True, check=True)
        (OUT / (Path(binary).parent.name + option + '.txt')).write_text(p.stdout)
        rows = [list(map(int, line.split())) for line in p.stdout.splitlines()[1:]]
        assert len(rows) == 150 and all(len(row) == columns for row in rows), option
        if option == '--feel-audit':
            assert {(r[0], r[1]) for r in rows} == {(s, a) for s in range(50) for a in range(3)}
            assert all(r[2] == (1, 3, 4)[r[1]] for r in rows), 'den census accepted missing dens'
            assert all(r[5] >= 4 and r[6] == 6 and r[7] > 260 for r in rows if r[1] == 1)
        else:
            assert {(r[0], r[1]) for r in rows} == {(s, k) for s in range(50) for k in (0, 1, 3)}
            assert all(r[4] == 1 and r[3] <= 30 * 256 and r[5:] == [0, 0, 0] for r in rows)
    mouths = subprocess.run([str(binary), '--mouth-audit'], capture_output=True, text=True, check=True)
    (OUT / (Path(binary).parent.name + '-mouth-audit.txt')).write_text(mouths.stdout)
    rows = [list(map(int, line.split())) for line in mouths.stdout.splitlines()[1:]]
    assert len(rows) == 400 and {(r[0], r[1], r[2]) for r in rows} == {(s, f, k) for s in range(50) for f in (80, 200) for k in (4, 5, 6, 7)}
    assert all(r[3] == 1 and r[5] > 0 and r[6] == 0 for r in rows), 'den-to-mouth route failed'
    _, states, foes = run(binary, 'sprint-hit')
    assert any(v['action'] == 8 and any(f['last_hit'] == v['started'] for f in foes[t])
               for t, v in states.items()), 'sprinting attack did not land'
    for size in ('80x24', '120x40'):
        _, states, _ = run(binary, 'sprint-' + size)
        values = [v['stamina'] for v in states.values() if v['sprint']]
        assert len(values) > 1 and min(values) < max(values), 'sprint did not cost stamina'
    retired = subprocess.run([str(binary), '--hud'], capture_output=True)
    assert retired.returncode == 2, '--hud was not retired'
    print('gameplay: den/path/chase censuses, sprint costs, real-key hit and retired HUD flag: green')


def level_look(binary):
    p = subprocess.run([str(binary), '--look-audit'], capture_output=True, text=True, check=True)
    (OUT / (Path(binary).parent.name + '-look-audit.txt')).write_text(p.stdout)
    assert len([line for line in p.stdout.splitlines() if line.startswith('look: seed ')]) == 50
    assert 'look: green seeds 50 frames ' in p.stdout
    for tier in ('rich', 'plain'):
        for size in ('80x24', '120x40'):
            dest, states, _ = run(binary, 'hud-after-c-' + size, tier)
            assert any(v['action'] == 4 for v in states.values()), 'c never dodged'
            assert all(line[22] == ' ' for line in (dest / 'final.txt').read_text().splitlines()[:5]), 'stamina edge leak'
            _, states, _ = run(binary, 'scent-recover-' + size, tier)
            assert any(v['mark'] and v['mark_scent'] == 28 for v in states.values()), 'no death mark'
            assert states[max(states)]['mark'] == 0 and states[max(states)]['scent'] == 28, 'recovery lost scent'
    print('gameplay: fifty-seed world labels, after-c padding, scent recovery: green')


def readable(root):
    """Nothing the gate leaves under target/gameplay may be unreadable: the
    CI artifact upload scans every path, and an owner-only directory from a
    container run fails it after every gate was green."""
    bad = []
    for path in root.rglob('*'):
        mode = path.stat().st_mode & 0o777
        need = 0o555 if path.is_dir() else 0o444
        if mode & need != need:
            bad.append('%s %o' % (path, mode))
    assert not bad, 'unreadable under target/gameplay: ' + ', '.join(bad[:10])
    print('gameplay: every path under', root, 'readable')


def den_progression(binary):
    census = subprocess.run([str(binary), '--den-census'], capture_output=True, text=True, check=True)
    (OUT / 'den-census.txt').write_text(census.stdout)
    assert '100 den paths, 400 gate-face-tier rows, 0 skips' in census.stdout
    for tier in ('rich', 'plain'):
        _, states, _ = run(binary, 'den-checkpoint', tier)
        final = states[max(states)]
        assert any(v['resting'] == 1 and v['den_id'] == 2 for v in states.values()), 'den2 not entered'
        assert (final['area'], final['den_id'], final['x'], final['y'], final['deaths']) == (1, 2, 3968, 23680, 1), 'wrong death checkpoint'
        assert final['mark'] == 1 and final['mark_area'] == 1 and final['health'] == 52
        _, spring, _ = run(binary, 'spring-found', tier)
        assert spring[max(spring)]['capacity'] == 2, 'first spring not found through real keys'
        assert any(v['capacity'] == 0 for v in spring.values()), 'spring fixture started already equipped'
        _, drink, _ = run(binary, 'spring-drink', tier)
        last = drink[max(drink)]
        assert last['capacity'] == 2 and last['flasks'] == 1 and last['health'] == 52
        assert any(v['action'] == 5 for v in drink.values()), 'water never animated'
        _, refill, _ = run(binary, 'water-refill', tier)
        last = refill[max(refill)]
        assert last['resting'] == 1 and last['flasks'] == 2
    print('gameplay: den entry, checkpoint, spring/drink/refill and 50-seed censuses green')



def paths_doors_rest(binary):
    import collections
    import csv
    import io
    import statistics
    census = subprocess.run([str(binary), '--paths-audit'], capture_output=True, text=True, check=True)
    (OUT / (Path(binary).parent.name + '-paths.csv')).write_text(census.stdout)
    widths = collections.defaultdict(list)
    routes = collections.defaultdict(list)
    for row in csv.DictReader(io.StringIO(census.stdout)):
        r = {k: int(v) for k, v in row.items()}
        widths[r['area']].append(r['width'])
        routes[tuple(r[k] for k in ('seed', 'field', 'area', 'path'))].append(r)
    for area, minimum in enumerate((7, 9, 9, 7, 9, 9)):
        assert statistics.median(widths[area]) >= minimum, ('path median lost two-cell widening', area)
        turns = samples = 0
        for key, rows in routes.items():
            if key[2] != area:
                continue
            sign, last_at = 0, -100
            samples += len(rows)
            for row in rows:
                direction = (row['delta'] > 0) - (row['delta'] < 0)
                if direction:
                    turns += bool(sign and direction != sign and row['at'] - last_at <= 3)
                    sign, last_at = direction, row['at']
        assert turns * 40 <= samples, ('jaggedness exceeds 0.25 reversals per ten samples', area)
    for flag, marker in (('--doorways-audit', 'total 806400 misses 0'),
                         ('--foes-audit', 'frames 193200 omitted_frames 0')):
        p = subprocess.run([str(binary), flag], capture_output=True, text=True, check=True)
        (OUT / (Path(binary).parent.name + flag + '.txt')).write_text(p.stdout)
        assert marker in p.stdout, (flag, 'incomplete census')
    for tier in ('rich', 'plain'):
        for size in ('80x24', '120x40'):
            for name in ('empty', 'pending', 'refused'):
                dest, states, _ = run(binary, 'rest-menu-' + name + '-' + size, tier)
                assert all(v['level'] == 1 and v['scent'] == 49 for v in states.values()), 'pending spent early'
                text = (dest / 'final.txt').read_text()
                assert 'Scent after' in text and 'Confirm' in text and 'Esc discard' in text
                if name == 'refused':
                    assert 'Not enough scent' in text, 'unaffordable raise not shown'
    print('gameplay: door shadows, clipped foe walk, staged rest panels green')


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
    den_progression(Path(args.bin).resolve())
    paths_doors_rest(Path(args.bin).resolve())

    feel(Path(args.bin).resolve())
    level_look(Path(args.bin).resolve())
    import runpy
    world = runpy.run_path(str(ROOT / 'tools/world_checks.py'))
    world['check'](Path(args.bin).resolve())
    readable(OUT)
    print('gameplay: green (0 skips)')

if __name__ == '__main__':
    main()
