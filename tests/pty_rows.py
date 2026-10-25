"""Game-owned live witnesses, using lair's pty and restore checks unchanged."""
import os
from pathlib import Path
import subprocess


def den_keys(binary, ctx):
    home = Path(ctx.ROOT) / 'target' / 'pty' / 'home'
    home.mkdir(parents=True, exist_ok=True)
    env = ctx.env_for()
    env['HOME'] = str(home)
    s = ctx.Session([binary, '--seed', '7', '--save', str(home / 'den.save'), '--tier', 'plain'], 24, 80, env)
    s.type(b'?', settle=.15)
    s.type(b'r', settle=.2)
    s.type(b'12345', settle=.2)
    s.type(b'\x1b', settle=.2)
    s.type(b'\t', settle=.2)
    s.type(b'\x1b', settle=.2)
    s.type(b'q')
    s.finish()
    problems = []
    ctx.common_checks(s, 0, problems)
    if b'The hollow log' not in s.out:
        problems.append('rest never drew the den')
    if b'ended by the quit key' not in s.err:
        problems.append('Esc quit instead of releasing')
    return s, problems


def death_agree(binary, ctx):
    root = Path(ctx.ROOT)
    home = root / 'target' / 'pty' / 'home'
    home.mkdir(parents=True, exist_ok=True)
    env = ctx.env_for()
    env['HOME'] = str(home)
    case = root / 'tests' / 'cases' / 'death-recovery.pk'
    s = ctx.Session([binary, '--replay', str(case), '--ticks', '120', '--tier', 'plain', '--no-truecolor'], 24, 80, env)
    s.finish()
    problems = []
    ctx.common_checks(s, 0, problems)
    dest = root / 'target' / 'pty' / 'death-agree'
    dest.mkdir(parents=True, exist_ok=True)
    cap = dest / 'capture.bin'
    cap.write_bytes(s.out)
    applied = subprocess.run([binary, '--apply', str(cap), '--size', '80x24'], capture_output=True, check=True)
    subprocess.run([binary, '--headless', '--script', str(case), '--frames', '120', '--every', '120', '--tier', 'plain', '--dump', str(dest)], check=True)
    text, sty, _ = applied.stdout.decode().split('--\n')
    if text != (dest / 'final.txt').read_text() or sty != (dest / 'final.sty').read_text():
        problems.append('death and recovery differ between live and headless paths')
    return s, problems

def archive_failure(binary, ctx):
    root = Path(ctx.ROOT)
    dest = root / 'target' / 'pty'
    dest.mkdir(parents=True, exist_ok=True)
    invalid = dest / 'archive-not-a-directory'
    invalid.write_text('fixture')
    s = ctx.Session([binary, '--replay', str(root / 'tests/cases/death-recovery.pk'),
                     '--ghost-dir', str(invalid), '--ticks', '120'], 24, 80, ctx.env_for())
    s.finish()
    problems = []
    ctx.common_checks(s, 2, problems)
    if b'failed death archive' not in s.err:
        problems.append('archive failure was not reported after restoring the terminal')
    return s, problems

ROWS = {'den-keys': den_keys, 'death-agree': death_agree, 'archive-failure': archive_failure}


def feel_controls(binary, ctx):
    """Real decoder/loop path; injected bytes are not physical-key measurements."""
    import re
    root = Path(ctx.ROOT) / 'target' / 'pty' / 'feel'
    root.mkdir(parents=True, exist_ok=True)
    env = ctx.env_for()
    env['HOME'] = str(root)
    problems = []
    arrows = [('n', b'\x1b[A', 0), ('ne', b'\x1b[A\x1b[C', 32),
              ('e', b'\x1b[C', 64), ('se', b'\x1b[B\x1b[C', 96),
              ('s', b'\x1b[B', 128), ('sw', b'\x1b[B\x1b[D', 160),
              ('w', b'\x1b[D', 192), ('nw', b'\x1b[A\x1b[D', 224),
              ('lock-empty', b'\x1b[D\t', 192)]
    for tier in ('rich', 'plain'):
        for name, chord, aim in arrows:
            session = ctx.Session([binary, '--seed', '7', '--tier', tier, '--trace'], 24, 80, env)
            session.type(b'?', settle=.15)
            session.type(chord + b'x', settle=.45)
            session.type(b'q')
            session.finish()
            ctx.common_checks(session, 0, problems)
            (root / (tier + '-' + name + '.trace')).write_bytes(session.err)
            if not re.search(rb'action 2 aim ' + str(aim).encode() + rb' combo 0', session.err):
                problems.append(tier + ' ' + name + ' did not commit the injected aim')
        session = ctx.Session([binary, '--seed', '7', '--tier', tier, '--trace'], 24, 80, env)
        session.type(b'?', settle=.15)
        session.type(b'\x1b[C ', settle=.25)
        session.type(b' ', settle=.37)
        session.type(b' ', settle=.60)
        session.type(b'q')
        session.finish()
        ctx.common_checks(session, 0, problems)
        (root / (tier + '-combo.trace')).write_bytes(session.err)
        for combo in (1, 2, 3):
            if not re.search(rb'action 1 aim 64 combo ' + str(combo).encode(), session.err):
                problems.append(tier + ' live combo missing ' + str(combo))
        session = ctx.Session([binary, '--seed', '7', '--tier', tier, '--trace'], 24, 80, env)
        session.type(b'?', settle=.15)
        session.type(b'\x1b[Cs', settle=.75)
        session.type(b'q')
        session.finish()
        ctx.common_checks(session, 0, problems)
        (root / (tier + '-heavy.trace')).write_bytes(session.err)
        if not re.search(rb'action 7 aim 64 combo 0', session.err):
            problems.append(tier + ' s did not start heavy')
    return session, problems

ROWS['feel-controls'] = feel_controls


def pending_save(binary, ctx):
    """q and a typed 03 each cut a real staged write before its rename."""
    root = Path(ctx.ROOT) / 'target/pty/save-cancel'
    root.mkdir(parents=True, exist_ok=True)
    problems = []
    for name, ending in [('quit', b'q'), ('interrupt', b'\x03')]:
        path = root / (name + '.save')
        path.unlink(missing_ok=True)
        stage = Path(str(path) + '.pending')
        stage.unlink(missing_ok=True)
        subprocess.run([binary, '--headless', '--save', str(path), '--frames', '1',
                        '--dump', str(root / (name + '-initial'))], check=True)
        before = path.read_bytes()
        session = ctx.Session([binary, '--save', str(path), '--save-delay', '60',
                               '--tier', 'plain'], 24, 80, ctx.env_for())
        session.type(b'?', settle=.25)
        if not stage.is_file():
            problems.append(name + ': no pending write existed before the exit')
        session.type(ending)
        session.finish()
        ctx.common_checks(session, 0, problems)
        if path.read_bytes() != before or stage.exists():
            problems.append(name + ': previous save changed or owned stage survived')
        if b'pending save cancelled' not in session.err:
            problems.append(name + ': cancellation was not reported')
    return session, problems


def save_failure(binary, ctx):
    root = Path(ctx.ROOT) / 'target/pty/save-error'
    root.mkdir(parents=True, exist_ok=True)
    path = root / 'journey.save'
    path.unlink(missing_ok=True)
    stage = Path(str(path) + '.pending')
    stage.unlink(missing_ok=True)
    subprocess.run([binary, '--headless', '--save', str(path), '--frames', '1',
                    '--dump', str(root / 'initial')], check=True)
    before = path.read_bytes()
    stage.write_bytes(b'another writer owns this stage')
    session = ctx.Session([binary, '--save', str(path), '--tier', 'plain'],
                          24, 80, ctx.env_for())
    session.type(b'?', settle=.2)
    session.finish()
    problems = []
    ctx.common_checks(session, 2, problems)
    if b'save_busy' not in session.err or path.read_bytes() != before:
        problems.append('failed staged save was not named or damaged previous save')
    if stage.read_bytes() != b'another writer owns this stage':
        problems.append('another writer stage was removed or overwritten')
    stage.unlink()
    return session, problems


def resumed_record(binary, ctx):
    """A resumed game records its initial journey; playback needs no save."""
    import re
    root = Path(ctx.ROOT) / 'target/pty/resumed-record'
    root.mkdir(parents=True, exist_ok=True)
    path = root / 'journey.save'
    path.unlink(missing_ok=True)
    case = Path(ctx.ROOT) / 'tests/cases/world-den.pk'
    frames = re.search(r'# frames (\d+)', case.read_text())[1]
    subprocess.run([binary, '--headless', '--script', str(case), '--save', str(path),
                    '--frames', frames, '--every', frames, '--dump', str(root / 'initial')], check=True)
    record = root / 'resumed.pk'
    session = ctx.Session([binary, '--save', str(path), '--record', str(record),
                           '--tier', 'plain', '--no-truecolor', '--ticks', '30'],
                          24, 80, ctx.env_for())
    session.type(b'?', settle=.2)
    session.finish()
    problems = []
    ctx.common_checks(session, 0, problems)
    if 'journey 1' not in record.read_text():
        problems.append('resumed recording lacks initial journey')
    cap = root / 'capture.bin'
    cap.write_bytes(session.out)
    applied = subprocess.run([binary, '--apply', str(cap), '--size', '80x24'], capture_output=True, check=True)
    subprocess.run([binary, '--headless', '--script', str(record), '--frames', '30',
                    '--every', '30', '--tier', 'plain', '--dump', str(root / 'replayed')], check=True)
    text, sty, _ = applied.stdout.decode().split('--\n')
    if text != (root / 'replayed/final.txt').read_text() or sty != (root / 'replayed/final.sty').read_text():
        problems.append('resumed recording differs from live frame without the save file')
    return session, problems


ROWS.update({'pending-save': pending_save, 'save-failure': save_failure,
             'resumed-record': resumed_record})
