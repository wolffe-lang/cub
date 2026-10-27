"""File-level journey witnesses on each shipping backend; never user HOME."""
from pathlib import Path
import subprocess
import re

ROOT = Path(__file__).resolve().parent.parent


def check_hitbox_rows(text):
    rows = [line.split() for line in text.splitlines() if line[:1].isdigit()]
    assert len(rows) == 16 and all(len(row) == 7 for row in rows), 'hitbox audit must report sixteen complete rows'
    expected = {(aim, gap) for aim in range(8) for gap in (0, 1)}
    assert {(int(row[0]), int(row[3])) for row in rows} == expected, 'hitbox audit omitted or duplicated an aim/gap'
    assert all(row[6] == 'true' for row in rows), 'a declared first bite did not land'


def check(binary):
    binary = Path(binary).resolve()
    out = ROOT / 'target' / 'world' / binary.parent.name
    out.mkdir(parents=True, exist_ok=True)
    audit = subprocess.run([str(binary), '--world-audit'], capture_output=True, text=True, check=True)
    (out / 'reachability.txt').write_text(audit.stdout)
    rows = [list(map(int, row.split())) for row in audit.stdout.splitlines()[1:]]
    assert len(rows) == 700 and {(r[0], r[1], r[2]) for r in rows} == {(s, f, a) for s in range(50) for f in (80, 200) for a in range(7)}
    # reached == required; straight <= 12; nearest foe >= 30; the caches per
    # area (three inland, four in the town, none in the last three; cb05); bank step <= 1; flat run <= 2; textured share >= 90 %; walk <= 200;
    # every path cell in its area's one path style (cb02c).
    assert all(len(r) == 13 for r in rows), 'world audit row has the wrong columns'
    assert all(r[3] == r[4] and r[5] <= 12 and r[6] >= 30 and r[7] == {0: 4, 1: 3, 2: 3, 6: 4}.get(r[2], 0) and r[8] <= 1
               and r[9] <= 2 and r[10] >= 90 and r[11] <= 200 and r[12] == 0 for r in rows), 'world audit row out of bounds'
    wide(binary, out)

    def run(name, path, frames=1, case=None, extra=(), want=0):
        args = [str(binary), '--headless', '--save', str(path), '--frames', str(frames),
                '--every', str(frames), '--dump', str(out / name)]
        if case:
            args += ['--script', str(ROOT / 'tests/cases' / (case + '.pk'))]
        p = subprocess.run(args + list(extra), capture_output=True, text=True)
        (out / (name + '.log')).write_text(p.stdout + p.stderr)
        assert p.returncode == want, (name, p.returncode, p.stderr)
        return p

    save = out / 'journey.save'
    save.unlink(missing_ok=True)
    Path(str(save) + '.pending').unlink(missing_ok=True)
    frames = int(re.search(r'# frames (\d+)', (ROOT / 'tests/cases/world-den.pk').read_text())[1])
    run('write-den', save, frames, 'world-den')
    before = save.read_bytes()
    assert before.startswith(b'CUB 5\n') and len(before) < 512
    run('resume-den', save)
    assert save.read_bytes() == before, 'write/resume changed persistent state'
    words = (out / 'resume-den/final.state').read_text().splitlines()[0].split()
    state = dict(zip(words[::2], map(int, words[1::2])))
    assert state['area'] == 1 and state['den_id'] == 1 and state['health'] == 160 and state['flasks'] == 2
    conflict = run('seed-conflict', save, extra=['--seed', '2'], want=2)
    assert 'save_seed_conflict' in conflict.stderr and save.read_bytes() == before
    conflict = subprocess.run([str(binary), '--headless', '--script', str(ROOT / 'tests/cases/saved-den.pk'),
                               '--seed', '2', '--frames', '1', '--dump', str(out / 'record-seed-conflict')],
                              capture_output=True, text=True)
    assert conflict.returncode == 2 and 'save_seed_conflict' in conflict.stderr, 'checkpoint seed override was silently ignored'
    cut = run('cut', save, extra=['--save-cut'], want=2)
    assert 'save_cut' in cut.stderr and save.read_bytes() == before, 'cut write lost old save'
    pending = Path(str(save) + '.pending')
    assert not pending.exists()
    pending.write_bytes(b'another writer owns this stage')
    busy = run('busy', save, want=2)
    assert 'save_busy' in busy.stderr and save.read_bytes() == before
    assert pending.read_bytes() == b'another writer owns this stage'
    pending.unlink()
    for name, data, diagnostic in [
        ('unknown', before.replace(b'CUB 5', b'CUB 9', 1), 'save_version'),
        ('schema-1', before.replace(b'CUB 5', b'CUB 1', 1), 'save_version'),
        ('schema-2', before.replace(b'CUB 5', b'CUB 2', 1), 'save_version'),
        ('schema-3', before.replace(b'CUB 5', b'CUB 3', 1), 'save_version'),
        ('corrupt', before[:-5], 'save_corrupt'),
        ('extra', before + b'junk\n', 'save_corrupt'),
    ]:
        path = out / (name + '.save')
        path.write_bytes(data)
        result = run(name, path, want=2)
        assert diagnostic in result.stderr and path.read_bytes() == data, 'invalid save silently reset'

    # File-level schema4 migration uses an independently recomputed old checksum.
    legacy = out / 'schema-4.save'
    payload = before.decode().split('check ')[0]
    payload = re.sub(r'^slain .*\n', '', payload, flags=re.M).replace('CUB 5\n', 'CUB 4\n', 1)
    h = 7
    for byte in payload.encode():
        h = (h * 31 + byte) % 1000000007
    legacy.write_text(payload + 'check ' + str(h) + '\n')
    run('migrate-schema-4', legacy)
    assert legacy.read_bytes().startswith(b'CUB 5\n') and b'slain 0 0 0 0 0 0 0\n' in legacy.read_bytes(), 'schema4 migration lost validation/state'

    memory = out / 'slain.save'
    memory.unlink(missing_ok=True)
    count = int(re.search(r'# frames (\d+)', (ROOT / 'tests/cases/den-memory.pk').read_text())[1])
    run('write-slain', memory, count, 'den-memory')
    masks = re.search(rb'^slain (.*)$', memory.read_bytes(), re.M)[1]
    assert int(masks.split()[0]) > 0, 'save never carried Shingle kills'
    run('resume-slain', memory)
    assert re.search(rb'^slain (.*)$', memory.read_bytes(), re.M)[1] == masks, 'resume revived slain foes'
    foe_lines = (out / 'resume-slain/final.state').read_text().splitlines()[1:]
    assert any('health 0 ' in row for row in foe_lines), 'restored mask not applied to encounter'

    fallen = out / 'fallen.save'
    fallen.unlink(missing_ok=True)
    death_tick = int(re.search(r'^t (\d+) health -1000$', (ROOT / 'tests/cases/world-return.pk').read_text(), re.M)[1]) + 1
    run('fallen', fallen, death_tick, 'world-return')
    mark = fallen.read_bytes()
    run('resume-mark', fallen)
    assert fallen.read_bytes() == mark, 'mark did not survive resume'
    w = (out / 'resume-mark/final.state').read_text().splitlines()[0].split()
    st = dict(zip(w[::2], map(int, w[1::2])))
    assert st['area'] == 1 and st['mark_area'] == 2 and st['mark'] == 1 and st['mark_scent'] > 0
    print('world: 50 seeds, all dens/exits/caches, meanders, density, save roundtrip/cut/busy/corrupt/mark: green')


def wide(binary, out):
    """The wide forest's censuses (cb05), fifty seeds at both fields: at most
    two dens an area and no two within 110 route cells (R-cb05-3), no
    reversal within eight cells on any route or branch, the foes per area in
    their bands (R-cb05-4), every dead-end spur rewarded, every area
    generated under 50 ms at field 200."""
    for flag, green in (('--den-spacing', 'den-spacing: green'), ('--bends-audit', 'bends: green'),
                        ('--foe-census', 'foe-census: green'), ('--spurs-audit', 'spurs: green'),
                        ('--gen-bench', 'gen-bench: green'),
                        # Item 8: a scripted cub crosses Cinderwick in nine of ten seeds at both
                        # fields (R-cb05-5), and a bite in reach lands on the Ashen from every aim.
                        ('--crossing-census', 'crossing: green'), ('--hitbox-audit', 'hitbox: green')):
        p = subprocess.run([str(binary), flag], capture_output=True, text=True)
        (out / (flag[2:] + '.txt')).write_text(p.stdout + p.stderr)
        if flag == '--gen-bench' and binary.parent.name != 'release':
            # A timing bar, like the perf gate's, is the release build's; the
            # native build records its figures without a verdict.
            continue
        assert p.returncode == 0 and green in p.stdout, (flag, p.returncode, p.stdout[-400:], p.stderr[-400:])
        if flag == '--hitbox-audit':
            check_hitbox_rows(p.stdout)
        if flag == '--den-spacing':
            least = [int(n) for n in re.findall(r'least \w+(?: an area)? (\d+)', p.stdout)]
            assert least and min(least) >= 110, ('den spacing under the bar', p.stdout[-200:])
        if flag == '--bends-audit':
            rows = [list(map(int, r.split())) for r in p.stdout.splitlines() if r[:1].isdigit()]
            assert rows and all(r[-1] == 0 for r in rows), 'a reversal within eight cells'
        if flag == '--crossing-census':
            survived = [int(n) for n in re.findall(r'survived (\d+) of 10', p.stdout)]
            assert len(survived) == 2 and min(survived) >= 9, ('the crossing', survived)
            assert ' lane' not in p.stdout.replace('crossing: green, at least 9 of 10 seeds cross at each field, no death on the lane', ''), 'a death on the lane'
