"""Consumable replay semantics on each shipping binary, with owned save paths."""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent.parent


def saved(path):
    text = path.read_text()
    match = re.search(r'^cache (\d+) pouch (\d+) (\d+) opening (\d+)$', text, re.M)
    assert match, 'missing canonical pouch counts'
    words = list(map(int, re.search(r'^items (.*)$', text, re.M)[1].split()))
    assert len(words) == 7 + words[5] + words[6], 'truncated variable world data'
    return dict(yarrow=int(match[2]), marrow=int(match[3]), pine=words[0], ice=words[1],
                tuft=words[2], uses=words[3], seeded=words[4],
                lore=words[7:7 + words[5]], ground=words[7 + words[5]:])


def check(binary):
    binary = Path(binary).resolve()
    out = ROOT / 'target' / 'pouch-proof' / binary.parent.name
    out.mkdir(parents=True, exist_ok=True)

    def run(case, frames, tier, label):
        dest = out / (label + '-' + tier)
        save = out / (label + '-' + tier + '.save')
        save.unlink(missing_ok=True)
        Path(str(save) + '.pending').unlink(missing_ok=True)
        result = subprocess.run([str(binary), '--headless', '--script', str(ROOT / 'tests/cases' / (case + '.pk')),
                                 '--frames', str(frames), '--every', str(frames), '--tier', tier,
                                 '--save', str(save), '--dump', str(dest)], capture_output=True, text=True)
        assert result.returncode == 0, (case, result.returncode, result.stderr)
        text = (dest / 'final.state').read_text().splitlines()[0].split()
        state = dict(zip(text[::2], map(int, text[1::2])))
        return saved(save), state, (dest / 'final.txt').read_text(), save

    for tier in ('rich', 'plain'):
        pouch, state, frame, _ = run('pouch-inventory', 2, tier, 'list')
        assert 'The pouch' in frame and "The mother's tuft" in frame and pouch['yarrow'] == 2
        assert state['health'] == 52 and state['action'] == 0, 'menu advanced combat'
        dropped, ds, _, path = run('pouch-drop-repickup', 27, tier, 'drop')
        assert dropped['yarrow'] == 0 and len(dropped['ground']) == 1 and ds['resting'] == 0, 'drop did not happen away from den'
        taken, ts, _, _ = run('pouch-drop-repickup', 29, tier, 'take')
        assert taken['yarrow'] == 1 and not taken['ground'] and ts['resting'] == 0, 'r did not re-pickup'
        gone, _, _, _ = run('pouch-drop-repickup', 35, tier, 'discard')
        assert gone['yarrow'] == 0 and not gone['ground'], 'discard did not destroy'
        consumed, cs, _, _ = run('pouch-consume', 8, tier, 'consume')
        assert consumed['yarrow'] == 0 and cs['health'] == 32, 'tooltip consume did not heal ten'
        aimed, _, af, _ = run('pouch-aim', 4, tier, 'aim')
        assert aimed['ice'] == 1 and 'No foe within 6 cells' in af, 'aim refusal spent ice'
        lore, _, lf, _ = run('pouch-lore', 4, tier, 'lore')
        assert lore['lore'] == [1, 2] and '2 / 2' in lf and 'doorway' in lf, 'Lore path not scrolled'
        sprites, _, _, _ = run('pouch-pickups', 2, tier, 'sprites')
        assert len(sprites['ground']) == 5, 'pickup sprite fixture lost a kind'
        # Reopen a real dropped-item save without its fixture: item position/order
        # survive last-den waking and the first ordinary replay tick unchanged.
        result = subprocess.run([str(binary), '--headless', '--save', str(path),
                                 '--script', str(ROOT / 'tests/cases/walk-north.pk'), '--frames', '1',
                                 '--every', '1', '--tier', tier, '--dump', str(out / ('reload-' + tier))],
                                capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
        assert saved(path)['ground'] == dropped['ground'], 'reload lost or duplicated the dropped item'
    print('gameplay: pouch pickup/drop/re-pickup, consume/discard/aim/Lore, reload; both tiers green')
