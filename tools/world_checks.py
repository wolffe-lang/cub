"""File-level journey witnesses on each shipping backend; never user HOME."""
from pathlib import Path
import subprocess
import re

ROOT = Path(__file__).resolve().parent.parent


def check(binary):
    binary = Path(binary).resolve()
    out = ROOT / 'target' / 'world' / binary.parent.name
    out.mkdir(parents=True, exist_ok=True)
    audit = subprocess.run([str(binary), '--world-audit'], capture_output=True, text=True, check=True)
    (out / 'reachability.txt').write_text(audit.stdout)
    rows = [list(map(int, row.split())) for row in audit.stdout.splitlines()[1:]]
    assert len(rows) == 300 and {(r[0], r[1], r[2]) for r in rows} == {(s, f, a) for s in range(50) for f in (80, 200) for a in range(3)}
    # reached == required; straight <= 12; nearest foe >= 30; the caches per
    # area; bank step <= 1; flat run <= 2; textured share >= 90 %; walk <= 200;
    # every path cell in its area's one path style (cb02c).
    assert all(len(r) == 13 for r in rows), 'world audit row has the wrong columns'
    assert all(r[3] == r[4] and r[5] <= 12 and r[6] >= 30 and r[7] == (4 if r[2] == 0 else 2) and r[8] <= 1
               and r[9] <= 2 and r[10] >= 90 and r[11] <= 200 and r[12] == 0 for r in rows), 'world audit row out of bounds'

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
    assert before.startswith(b'CUB 2\n') and len(before) < 512
    run('resume-den', save)
    assert save.read_bytes() == before, 'write/resume changed persistent state'
    words = (out / 'resume-den/final.state').read_text().splitlines()[0].split()
    state = dict(zip(words[::2], map(int, words[1::2])))
    assert state['area'] == 1 and state['den_id'] == 1 and state['health'] == 160 and state['flasks'] == 3
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
        ('unknown', before.replace(b'CUB 2', b'CUB 9', 1), 'save_version'),
        ('schema-1', before.replace(b'CUB 2', b'CUB 1', 1), 'save_version'),
        ('corrupt', before[:-5], 'save_corrupt'),
        ('extra', before + b'junk\n', 'save_corrupt'),
    ]:
        path = out / (name + '.save')
        path.write_bytes(data)
        result = run(name, path, want=2)
        assert diagnostic in result.stderr and path.read_bytes() == data, 'invalid save silently reset'

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
