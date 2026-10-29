"""cb16's NPC rows on each shipping binary, with owned save paths (never HOME).

The npc census (`--npc-audit`): every place an NPC stands on open ground the
area's flood reaches, fifty seeds at both fields. The three witnesses run
through the binary with a save: the conversation (Quill's first line in the
frame, the forest paused under it, Esc closing it), the purchase (pine and
yarrow bought, 100 - 50 - 20 = 30 scent, the pouch and the NPCs' line in the
save), the toll (sixty paid, the cub landed on the far causeway). The trunk
writer's CUB 7 migrates to CUB 8 at file level, the sett counted dug.
"""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent.parent
LINE = 'You are small for a wolf. That is not an insult; small things live.'


def state(path):
    words = path.read_text().splitlines()[0].split()
    return dict(zip(words[::2], map(int, words[1::2])))


def check(binary):
    binary = Path(binary).resolve()
    out = ROOT / 'target' / 'npcs' / binary.parent.name
    out.mkdir(parents=True, exist_ok=True)
    audit = subprocess.run([str(binary), '--npc-audit'], capture_output=True, text=True)
    (out / 'npc-audit.txt').write_text(audit.stdout)
    assert audit.returncode == 0, ('npc census', audit.returncode, audit.stdout[-400:])
    rows = [r.split() for r in audit.stdout.splitlines()[1:-1]]
    assert len(rows) == 2200 and all(r[8] == '1' and r[9] == '1' for r in rows), 'an NPC place shut or cut off'
    assert {(int(r[0]), int(r[1])) for r in rows} == {(s, f) for s in range(50) for f in (80, 200)}, 'incomplete npc census'
    assert re.search(r'^npc-audit: green, 2200 places', audit.stdout, re.M), 'npc census verdict'

    def run(case, tier, label, frames=None, every=None, start=None):
        text = (ROOT / 'tests/cases' / (case + '.pk')).read_text()
        m = re.search(r'# frames (\d+) every (\d+) from (\d+)', text)
        frames = frames or int(m[1])
        dest = out / (label + '-' + tier)
        save = out / (label + '-' + tier + '.save')
        save.unlink(missing_ok=True)
        Path(str(save) + '.pending').unlink(missing_ok=True)
        args = [str(binary), '--headless', '--script', str(ROOT / 'tests/cases' / (case + '.pk')),
                '--frames', str(frames), '--every', str(every or m[2]), '--from', str(start or m[3]),
                '--tier', tier, '--save', str(save), '--dump', str(dest)]
        p = subprocess.run(args, capture_output=True, text=True)
        assert p.returncode == 0, (case, tier, p.returncode, p.stderr)
        return dest, save

    for tier in ('rich', 'plain'):
        dest, _ = run('npc-talk', tier, 'talk')
        frames = sorted(dest.glob('frame-*.txt'))
        assert any(LINE in f.read_text() and 'Quill' in f.read_text() for f in frames), 'the frame never showed Quill\'s line'
        assert any('Quill\'s wares' in f.read_text() for f in frames), 'Space never opened the wares'
        final = state(dest / 'final.state')
        assert LINE not in (dest / 'final.txt').read_text() and 'wares' not in (dest / 'final.txt').read_text(), 'Esc left the frame open'
        assert final['scent'] == 0 and final['action'] == 0, 'the conversation moved the cub\'s numbers'
        dest, save = run('npc-trade', tier, 'trade')
        text = save.read_text()
        assert re.search(r'^water \d+ scent 30$', text, re.M), 'pine 50 and yarrow 20 from 100'
        assert re.search(r'^cache \d+ pouch 1 0 ', text, re.M), 'one yarrow bought'
        assert re.search(r'^items 1 ', text, re.M), 'one pine bought'
        assert re.search(r'^npcs 1 0 0 0 0 0 0 0 0 dead 0 perch -1 flags 0$', text, re.M), 'Quill said one line'
        dest, save = run('npc-toll', tier, 'toll')
        final = state(dest / 'final.state')
        assert final['scent'] == 10 and final['area'] == 9, 'sixty paid in the Mere'
        assert final['y'] // 256 == 168, ('the far causeway', final['y'])
    print('gameplay: npc census green (2200 places) and the conversation, purchase and toll witnesses on both tiers')

    # The trunk writer's CUB 7 (cub ed180ef5; tests/saves/provenance.json):
    # the next write is CUB 8, the sett's open shortcut counted dug.
    trunk7 = out / 'cb14-v7.save'
    trunk7.write_bytes((ROOT / 'tests/saves/cb14-v7.save').read_bytes())
    p = subprocess.run([str(binary), '--headless', '--save', str(trunk7), '--frames', '1', '--every', '1',
                        '--dump', str(out / 'migrate-cb14-v7')], capture_output=True, text=True)
    assert p.returncode == 0, ('the trunk CUB 7', p.returncode, p.stderr)
    migrated = trunk7.read_bytes()
    assert migrated.startswith(b'CUB 8\n') and b'\nname sett_1\nplayed_ms 7135\nitems 0 0 0 0 1024 0 0\nnpcs 0 0 0 0 0 0 0 0 0 dead 0 perch -1 flags 1\n' in migrated, 'the trunk CUB 7 lost state on migration'
    p = subprocess.run([str(binary), '--headless', '--save', str(trunk7), '--frames', '1', '--every', '1',
                        '--dump', str(out / 'resume-cb14-v7')], capture_output=True, text=True)
    assert p.returncode == 0 and trunk7.read_bytes() == migrated, 'a CUB 8 resume changed the migrated bytes'
    print('gameplay: the trunk CUB 7 migrates to CUB 8 with the sett dug, and resumes byte-exact')
