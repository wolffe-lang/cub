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
                assert final['health'] == 52 and final['scent'] == 8 and foes[50][0]['health'] <= 0
            elif name == 'parry':
                assert states[54]['health'] == 52 and foes[54][0]['phase'] == 4
                assert final['scent'] == 8
            elif name == 'dodge':
                assert states[54]['health'] == 52 and states[54]['action'] == 4
                assert final['health'] == 52
            elif name == 'weasel-retreat':
                assert foes[42][0]['phase'] == 1 and states[53]['health'] == 52
                assert states[54]['health'] == 42 and foes[56][0]['phase'] == 3
            elif name == 'fox-feint':
                false = next(t for t, fs in foes.items() if fs[2]['phase'] == 5)
                real = next(t for t, fs in foes.items() if fs[2]['phase'] == 1)
                active = next(t for t, fs in foes.items() if fs[2]['phase'] == 2)
                assert real - false == 16 and active - real == 12
                assert states[active - 1]['health'] == 52 and states[active]['flasks'] == 2
            elif name == 'trail-fading':
                assert states[60]['trail'] > 0 and final['trail'] == 0
            elif name == 'rest':
                assert final['health'] == 64 and final['stamina'] == 80 and final['scent'] == 0
            elif name == 'death-recovery':
                assert states[47]['mark_scent'] == 28 and states[47]['action'] == 6
                assert final['deaths'] == 1 and final['mark'] == 0 and final['scent'] == 28
            elif name == 'thorn-gate':
                assert states[74]['gate'] == 0 and states[75]['gate'] == 1
            state_bytes = (dest / 'final.state').read_bytes()
            if tier == 'rich':
                expected[name] = state_bytes
            else:
                assert expected[name] == state_bytes, (name, 'tier changed the simulation')
            print('gameplay:', Path(binary).parent.name, name, tier, 'ok')
    # A natural, unassisted death: the player approaches then stands still.
    ghosts = OUT / (Path(binary).parent.name + '-ghosts')
    ghosts.mkdir(parents=True, exist_ok=True)
    before = set(ghosts.glob('*.pk'))
    _, states, _ = run(binary, 'fox-feint', frames=600, ghosts=ghosts)
    files = set(ghosts.glob('*.pk')) - before
    assert files, 'natural death did not write a ghost'
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--bin', required=True)
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    check(Path(args.bin).resolve())
    print('gameplay: green (0 skips)')

if __name__ == '__main__':
    main()
