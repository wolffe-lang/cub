"""Game-owned live witnesses, using lair's pty and restore checks unchanged.

Rows that do not test the music pass --mute (cb03): a sound-on start spends
about a second rendering the WAVs before the terminal opens, and keys typed
in that second sit in the canonical line discipline. The sound rows below
start the game with music on deliberately."""
import os
from pathlib import Path
import subprocess


def den_keys(binary, ctx):
    home = Path(ctx.ROOT) / 'target' / 'pty' / 'home'
    home.mkdir(parents=True, exist_ok=True)
    env = ctx.env_for()
    env['HOME'] = str(home)
    s = ctx.Session([binary, '--seed', '7', '--save', str(home / 'den.save'), '--tier', 'plain', '--mute', '--no-title'], 24, 80, env)
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
    if b'a den ahead' not in s.out:
        problems.append('the den was not marked before resting')
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
            session = ctx.Session([binary, '--seed', '7', '--tier', tier, '--trace', '--mute', '--no-title'], 24, 80, env)
            session.type(b'?', settle=.15)
            session.type(chord + b' ', settle=.45)
            session.type(b'q')
            session.finish()
            ctx.common_checks(session, 0, problems)
            (root / (tier + '-' + name + '.trace')).write_bytes(session.err)
            if not re.search(rb'action 1 aim ' + str(aim).encode() + rb' combo 1', session.err):
                problems.append(tier + ' ' + name + ' did not commit the injected aim')
        session = ctx.Session([binary, '--seed', '7', '--tier', tier, '--trace', '--mute', '--no-title'], 24, 80, env)
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
        session = ctx.Session([binary, '--seed', '7', '--tier', tier, '--trace', '--mute', '--no-title'], 24, 80, env)
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
                               '--tier', 'plain', '--mute', '--no-title'], 24, 80, ctx.env_for())
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
    session = ctx.Session([binary, '--save', str(path), '--tier', 'plain', '--mute', '--no-title'],
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
                           '--tier', 'plain', '--no-truecolor', '--ticks', '30', '--mute', '--no-title'],
                          24, 80, ctx.env_for())
    session.type(b'?', settle=.2)
    session.finish()
    problems = []
    ctx.common_checks(session, 0, problems)
    if 'journey 4' not in record.read_text():
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


def _sound_session(binary, ctx, args, env_extra=None, keys=b'q', settle=1.2):
    root = Path(ctx.ROOT) / 'target/pty/sound'
    root.mkdir(parents=True, exist_ok=True)
    env = ctx.env_for()
    env['HOME'] = str(root)
    if env_extra:
        env.update(env_extra)
    sound_dir = root / 'wavs'
    s = ctx.Session([binary, '--seed', '7', '--save', str(root / 'sound.save'),
                     '--sound-dir', str(sound_dir), '--tier', 'plain'] + args, 24, 80, env)
    s.pump(settle)
    players = subprocess.run(['ps', '-axo', 'ppid=,comm='], capture_output=True, text=True).stdout
    mine = [l for l in players.splitlines() if l.split()[0] == str(s.job)]
    wavs = sorted(p.name for p in sound_dir.glob('*.wav')) if sound_dir.exists() else []
    s.type(keys)
    s.finish()
    after = subprocess.run(['ps', '-axo', 'ppid=,comm='], capture_output=True, text=True).stdout
    left = [l for l in after.splitlines() if l.split()[0] == str(s.job)]
    return s, mine, wavs, left, sound_dir


def sound_live(binary, ctx):
    """Sound on (cb03): the parts render to WAVs under --sound-dir, the
    backend is probed before the terminal, and on macOS the title plays
    through /usr/bin/afplay, a child of the game that is gone with it; on
    Linux without paplay the refusal is named once and the WAVs are the sink."""
    import sys
    s, mine, wavs, left, sound_dir = _sound_session(binary, ctx, [])
    problems = []
    ctx.common_checks(s, 0, problems)
    want = ['boss-alpha.wav', 'boss-boar.wav', 'boss-elk.wav', 'boss-lynx.wav', 'bramblehold.wav',
            'crack.wav', 'death.wav', 'den.wav', 'larkmeadow.wav', 'shingle.wav', 'silence.wav', 'title.wav']
    if wavs != want:
        problems.append('the WAVs under --sound-dir during the run: %r' % wavs)
    if sound_dir.exists() and list(sound_dir.glob('*.wav')):
        problems.append('WAVs left behind after the exit')
    if b'sound on backend' not in s.err:
        problems.append('the closing line does not report the sound: %r' % s.err[-300:])
    if sys.platform == 'darwin':
        if not any('afplay' in l for l in mine):
            problems.append('no afplay child of the game while it ran: %r' % mine)
        if b'answers 1' not in s.err or b'cue title' not in s.err:
            problems.append('afplay did not answer the probe or the title was not cued: %r' % s.err[-300:])
    else:
        if s.err.count(b'player_missing: paplay') != 1:
            problems.append('paplay missing was not named exactly once: %r' % s.err[-300:])
        if b'answers 0' not in s.err:
            problems.append('a missing player must leave the sink silent')
    if left:
        problems.append('a player child outlived the game: %r' % left)
    s.evidence = 'children during the run %r; %d WAVs' % ([l.split()[1] for l in mine], len(wavs))
    return s, problems


def sound_oss(binary, ctx):
    """CUB_SOUND_BACKEND=oss: the engine's OSS stub refuses by name before
    the terminal is entered; the game plays on in silence."""
    s, mine, wavs, left, _ = _sound_session(binary, ctx, [], {'CUB_SOUND_BACKEND': 'oss'}, settle=.8)
    problems = []
    ctx.common_checks(s, 0, problems)
    if s.err.count(b'oss_ioctl_unsupported') != 1:
        problems.append('the OSS stub was not refused by name exactly once: %r' % s.err[-300:])
    if b'backend oss answers 0' not in s.err:
        problems.append('the closing line does not name the silent oss backend')
    if mine or left:
        problems.append('a player child under the oss backend: %r %r' % (mine, left))
    return s, problems


def sound_mute(binary, ctx):
    """--mute and CUB_SOUND=0: no WAV written, no child, no probe."""
    problems = []
    for args, env in (['--mute'], None), ([], {'CUB_SOUND': '0'}):
        s, mine, wavs, left, sound_dir = _sound_session(binary, ctx, args, env, settle=.5)
        ctx.common_checks(s, 0, problems)
        if wavs or mine or left:
            problems.append('muted, yet %r %r %r' % (wavs, mine, left))
        if b'sound off' not in s.err:
            problems.append('the closing line does not say the sound is off: %r' % s.err[-200:])
    return s, problems


def mute_key(binary, ctx):
    """m during play: the music stops (the child ends) and m again cues the
    scene's part afresh; the key is recorded like every key."""
    import sys
    root = Path(ctx.ROOT) / 'target/pty/sound'
    root.mkdir(parents=True, exist_ok=True)
    env = ctx.env_for()
    env['HOME'] = str(root)
    record = root / 'mute.pk'
    s = ctx.Session([binary, '--seed', '7', '--save', str(root / 'mute.save'), '--sound-dir',
                     str(root / 'wavs-m'), '--record', str(record), '--tier', 'plain'], 24, 80, env)
    s.pump(.9)
    s.type(b'm', settle=.6)
    players = subprocess.run(['ps', '-axo', 'ppid=,comm='], capture_output=True, text=True).stdout
    muted = [l for l in players.splitlines() if l.split()[0] == str(s.job)]
    s.type(b'm', settle=.6)
    s.type(b'q')
    s.finish()
    problems = []
    ctx.common_checks(s, 0, problems)
    if 'mute' not in record.read_text():
        problems.append('the mute key was not recorded')
    if sys.platform == 'darwin':
        if any('afplay' in l for l in muted):
            problems.append('afplay still ran while muted: %r' % muted)
        if b'starts 2 ' not in s.err:
            problems.append('the second m did not cue the part afresh: %r' % s.err[-300:])
    return s, problems


ROWS.update({'sound-live': sound_live, 'sound-oss': sound_oss, 'sound-mute': sound_mute, 'mute-key': mute_key})
def title(binary, ctx):
    """The title (cb04): drawn first with the four silhouettes and the
    keys; any key begins the opening; `--no-title` starts the game."""
    import re
    root = Path(ctx.ROOT) / 'target/pty/title'
    root.mkdir(parents=True, exist_ok=True)
    env = ctx.env_for()
    env['HOME'] = str(root)
    problems = []
    session = ctx.Session([binary, '--seed', '7', '--tier', 'plain', '--trace', '--mute'], 24, 80, env)
    session.pump(0.5)
    session.type(b'x', settle=.4)
    session.type(b'q')
    session.finish()
    ctx.common_checks(session, 0, problems)
    (root / 'title.trace').write_bytes(session.err)
    for text in (b'any key begins', b'Old Snag', b'Whisper', b'Alder', b'Ashgrim', b'z parry'):
        if text not in session.out:
            problems.append('title lacks %r' % text)
    if not re.search(rb'trace tick \d+ .* scene 2 ', session.err):
        problems.append('no title scene in the trace')
    if not re.search(rb'trace tick \d+ .* scene 1 ', session.err):
        problems.append('a key did not begin the opening')
    session = ctx.Session([binary, '--seed', '7', '--tier', 'plain', '--trace', '--mute', '--no-title'], 24, 80, env)
    session.pump(0.4)
    session.type(b'q')
    session.finish()
    ctx.common_checks(session, 0, problems)
    if b'any key begins' in session.out or re.search(rb'scene 2 ', session.err):
        problems.append('--no-title still drew the title')
    return session, problems


def title_demo(binary, ctx):
    """Ten idle seconds on the title start the committed demo replay."""
    import re
    root = Path(ctx.ROOT) / 'target/pty/title-demo'
    root.mkdir(parents=True, exist_ok=True)
    env = ctx.env_for()
    env['HOME'] = str(root)
    problems = []
    session = ctx.Session([binary, '--seed', '7', '--tier', 'plain', '--trace', '--mute'], 24, 80, env)
    session.pump(11.5)
    session.type(b'q')
    session.finish()
    ctx.common_checks(session, 0, problems)
    (root / 'title-demo.trace').write_bytes(session.err)
    if re.search(rb'trace tick (\d|[1-9]\d|[12]\d\d) .* demo 1 ', session.err):
        problems.append('the demo played before the idle time')
    if not re.search(rb'trace tick 3[1-9]\d .* scene 2 demo 1 ', session.err):
        problems.append('no demo after ten idle seconds on the title')
    return session, problems


ROWS.update({'title': title, 'title-demo': title_demo})



def sprint_live(binary, ctx):
    """Actual repeated Ctrl+arrow bytes drain stamina; Space chooses the snapping attack."""
    import re
    root = Path(ctx.ROOT) / 'target/pty/cb03a'
    root.mkdir(parents=True, exist_ok=True)
    env = ctx.env_for()
    env['HOME'] = str(root)
    s = ctx.Session([binary, '--seed', '7', '--save', str(root / 'sprint.save'),
                     '--trace', '--mute', '--no-title', '--tier', 'plain'], 24, 80, env)
    s.type(b'?', settle=.15)
    for _ in range(12):
        s.type(b'\x1b[1;5C', settle=.09)
    s.type(b' ', settle=.2)
    s.type(b'q')
    s.finish()
    problems = []
    ctx.common_checks(s, 0, problems)
    values = [int(m[0]) for m in re.findall(rb'stamina (\d+) sprint (1)', s.err)]
    if len(values) < 2 or min(values) >= max(values):
        problems.append('held sprint did not visibly drain stamina')
    if not re.search(rb'action 8 aim ', s.err):
        problems.append('Space while sprinting never became the snapping attack')
    if b'a den ahead' not in s.out:
        problems.append('entry den was not discoverable')
    return s, problems


def sprint_lands(binary, ctx):
    """Replay ordinary keys through the live loop and require the actual hit."""
    import re
    root = Path(ctx.ROOT)
    case = root / 'tests/cases/sprint-hit.pk'
    ticks = re.search(r'# frames (\d+)', case.read_text())[1]
    s = ctx.Session([binary, '--replay', str(case), '--ticks', ticks, '--trace', '--mute', '--no-title',
                     '--tier', 'plain'], 24, 80, ctx.env_for())
    s.finish()
    problems = []
    ctx.common_checks(s, 0, problems)
    if not re.search(rb'action 8 .*dash_hits [1-9]', s.err):
        problems.append('sprint hit replay never landed on a foe')
    return s, problems

ROWS.update({'sprint-live': sprint_live, 'sprint-lands': sprint_lands})


def level_look_after_c(binary, ctx):
    """A literal 0x63 goes through the live terminal, not a synthetic event.
    Compare its recorded run with headless output and inspect the bar's
    reserved edge; sample ECHO while the game owns the terminal."""
    import termios
    root = Path(ctx.ROOT) / 'target/pty/level-look'
    root.mkdir(parents=True, exist_ok=True)
    problems = []
    for tier in ('rich', 'plain'):
        for cols, rows in ((80, 24), (120, 40)):
            name = f'{tier}-{cols}x{rows}'
            save = root / (name + '.save')
            save.unlink(missing_ok=True)
            record = root / (name + '.pk')
            session = ctx.Session([binary, '--seed', '7', '--save', str(save),
                                   '--record', str(record), '--tier', tier,
                                   '--mute', '--no-title', '--no-truecolor', '--ticks', '24'],
                                  rows, cols, ctx.env_for())
            if termios.tcgetattr(session.master)[3] & termios.ECHO:
                problems.append(name + ': terminal echo is enabled during play')
            session.type(b'c', settle=.2)
            session.finish()
            ctx.common_checks(session, 0, problems)
            capture = root / (name + '.bin')
            capture.write_bytes(session.out)
            applied = subprocess.run([binary, '--apply', str(capture), '--size', f'{cols}x{rows}'],
                                     capture_output=True, check=True)
            text, sty, _ = applied.stdout.decode().split('--\n')
            dest = root / (name + '-headless')
            subprocess.run([binary, '--headless', '--script', str(record), '--frames', '24',
                            '--every', '24', '--tier', tier, '--dump', str(dest)], check=True)
            if text != (dest / 'final.txt').read_text() or sty != (dest / 'final.sty').read_text():
                problems.append(name + ': byte-c live/headless frame mismatch')
            if any(line[22] != ' ' for line in text.splitlines()[:5]):
                problems.append(name + ': world glyph leaked into the stamina edge')
            if 'dodge' not in record.read_text():
                problems.append(name + ': literal c never recorded the action')
    session.evidence = 'byte 63, ECHO clear, 80x24/120x40 rich/plain, replay agreement and HUD edge'
    return session, problems


def level_look_recovery(binary, ctx):
    root = Path(ctx.ROOT) / 'target/pty/level-recovery'
    root.mkdir(parents=True, exist_ok=True)
    problems = []
    case = Path(ctx.ROOT) / 'tests/cases/scent-recover-80x24.pk'
    for tier in ('rich', 'plain'):
        session = ctx.Session([binary, '--replay', str(case), '--ticks', '120',
                               '--tier', tier, '--mute', '--no-title', '--no-truecolor'],
                              24, 80, ctx.env_for())
        session.finish()
        ctx.common_checks(session, 0, problems)
        capture = root / (tier + '.bin')
        capture.write_bytes(session.out)
        applied = subprocess.run([binary, '--apply', str(capture), '--size', '80x24'],
                                 capture_output=True, check=True)
        text, sty, _ = applied.stdout.decode().split('--\n')
        dest = root / tier
        subprocess.run([binary, '--headless', '--script', str(case), '--frames', '120',
                        '--every', '120', '--tier', tier, '--dump', str(dest)], check=True)
        if text != (dest / 'final.txt').read_text() or sty != (dest / 'final.sty').read_text():
            problems.append(tier + ': scent recovery live/headless mismatch')
        words = (dest / 'final.state').read_text().splitlines()[0].split()
        state = dict(zip(words[::2], map(int, words[1::2])))
        if state['mark'] != 0 or state['scent'] != 28:
            problems.append(tier + ': death scent was not recovered exactly')
    return session, problems


ROWS.update({'level-look-after-c': level_look_after_c,
             'level-look-recovery': level_look_recovery})

def den_contact(binary, ctx):
    """Walk from the den centre to its visible edge, enter, pause, leave.

    No snapshot, teleports or numeric fixture: these bytes also run on trunk.
    """
    import re
    root = Path(ctx.ROOT) / 'target/pty/den-contact'
    root.mkdir(parents=True, exist_ok=True)
    path = root / 'journey.save'
    path.unlink(missing_ok=True)
    Path(str(path) + '.pending').unlink(missing_ok=True)
    s = ctx.Session([binary, '--seed', '7', '--save', str(path), '--tier', 'plain',
                     '--trace', '--mute', '--no-title'], 24, 80, ctx.env_for())
    s.type(b'?', settle=.15)
    s.type(b'\x1b[C', settle=.35)
    s.type(b'r', settle=.25)
    # A resting cub must ignore movement/combat, not queue a held arrow.
    s.type(b'\x1b[B ', settle=.25)
    s.type(b'\x1b', settle=.20)
    s.type(b'q')
    s.finish()
    problems = []
    ctx.common_checks(s, 0, problems)
    if b'Esc discard' not in s.out:
        problems.append('visible den edge: r never entered the rest scene')
    states = []
    for line in s.err.decode().splitlines():
        words = line.split()
        if words[:2] == ['trace', 'tick']:
            words = words[1:]
            states.append(dict(zip(words[::2], map(int, words[1::2]))))
    # New trace adds resting; the menu assertion above is baseline-compatible.
    rested = [v for v in states if v.get('resting') == 1]
    if rested and (len({(v['x'], v['y'], v['health'], v['action']) for v in rested}) != 1
                   or states[-1].get('resting') != 0):
        problems.append('rest did not pause, or Esc did not leave')
    return s, problems


def den_checkpoint(binary, ctx):
    """Live replay of the ordinary den8 -> den2 walk/rest/leave and fatal hit."""
    import re
    root = Path(ctx.ROOT)
    case = root / 'tests/cases/den-checkpoint.pk'
    ticks = re.search(r'# frames (\d+)', case.read_text())[1]
    session = ctx.Session([binary, '--replay', str(case), '--ticks', ticks,
                           '--tier', 'plain', '--trace', '--mute', '--no-title'],
                          24, 80, ctx.env_for())
    session.finish()
    problems = []
    ctx.common_checks(session, 0, problems)
    states = []
    for line in session.err.decode().splitlines():
        words = line.split()
        if words[:2] == ['trace', 'tick']:
            words = words[1:]
            states.append(dict(zip(words[::2], map(int, words[1::2]))))
    if not states:
        problems.append('checkpoint trace missing')
    else:
        final = states[-1]
        if not any(v.get('resting') == 1 and v['den_id'] == 2 for v in states):
            problems.append('did not rest at den2')
        if (final['area'], final['den_id'], final['x'], final['y'], final['deaths'], final['mark_area']) != (1, 2, -2688, 26240, 1, 1):
            problems.append('death failed to wake at den2 with its mark in the death area')
        if final['mark'] != 1 or final['health'] != 52:
            problems.append('death mark or rest healing missing')
    return session, problems


ROWS['den-contact'] = den_contact
ROWS['den-checkpoint'] = den_checkpoint


def rest_allocate(binary, ctx):
    """Actual arrow/Enter bytes: stage two stats, refuse, lower, confirm, discard."""
    root = Path(ctx.ROOT) / 'target/pty/cb04d-rest'
    root.mkdir(parents=True, exist_ok=True)
    problems = []
    for tier in ('rich', 'plain'):
        save = root / (tier + '.save')
        save.unlink(missing_ok=True)
        subprocess.run([binary, '--headless', '--script', str(Path(ctx.ROOT) / 'tests/cases/rest-menu-empty-80x24.pk'),
                        '--frames', '1', '--save', str(save), '--dump', str(root / ('setup-' + tier))], check=True, capture_output=True)
        session = ctx.Session([binary, '--save', str(save), '--tier', tier, '--trace', '--mute', '--no-title'], 24, 80, ctx.env_for())
        session.type(b'?', settle=.15)
        for key in (b'r', b'\x1b[C', b'\x1b[B', b'\x1b[C', b'\x1b[C', b'\x1b[D', b'\x1b[A', b'\x1b[A', b'\r'):
            session.type(key, settle=.12)
        session.type(b'\x1b[C', settle=.12)  # pending heart at row zero; still affordable
        session.type(b'\x1b', settle=.2)
        session.type(b'q')
        session.finish()
        ctx.common_checks(session, 0, problems)
        states = trace_states(session)
        if not any(v.get('pending') == 2 and v.get('needed') == 75 for v in states):
            problems.append(tier + ': second stat/refused third purchase not witnessed')
        if b'Not enough scent' not in session.out:
            problems.append(tier + ': refusal not shown')
        if not any(v.get('level') == 2 and v.get('scent') == 25 for v in states):
            problems.append(tier + ': lower then confirm did not spend exactly 24')
        if not states or states[-1].get('resting') != 0 or states[-1].get('level') != 2 or states[-1].get('scent') != 25:
            problems.append(tier + ': Esc failed to discard next pending level')
        (root / (tier + '.trace')).write_bytes(session.err)
    return session, problems


def trace_states(session):
    states = []
    for line in session.err.decode().splitlines():
        words = line.split()
        if words[:2] == ['trace', 'tick']:
            words = words[1:]
            states.append(dict(zip(words[::2], map(int, words[1::2]))))
    return states


def doorway_edge(binary, ctx):
    """Resume at the meadow den, then inject north arrows along the shadow's east edge."""
    root = Path(ctx.ROOT) / 'target/pty/cb04d-door'
    root.mkdir(parents=True, exist_ok=True)
    problems = []
    for tier in ('rich', 'plain'):
        save = root / (tier + '.save')
        save.unlink(missing_ok=True)
        subprocess.run([binary, '--headless', '--script', str(Path(ctx.ROOT) / 'tests/cases/rest-larkmeadow-80x24.pk'),
                        '--frames', '1', '--save', str(save), '--dump', str(root / ('setup-' + tier))], check=True, capture_output=True)
        session = ctx.Session([binary, '--save', str(save), '--tier', tier, '--trace', '--mute', '--no-title'], 24, 80, ctx.env_for())
        session.type(b'\x1b[C', settle=.65)
        for _ in range(20):
            session.type(b'\x1b[A', settle=.06)
        session.type(b'q')
        session.finish()
        ctx.common_checks(session, 0, problems)
        states = trace_states(session)
        changes = [(a, b) for a, b in zip(states, states[1:]) if a['area'] == 2 and b['area'] == 1]
        if not changes:
            problems.append(tier + ': northward edge approach did not leave meadow')
        elif not any(a['x'] >= 3 * 256 and a['y'] > 2 * 256 for a, _ in changes):
            problems.append(tier + ': crossing was not outside the old centre trigger')
        (root / (tier + '.trace')).write_bytes(session.err)
    return session, problems

ROWS.update({'rest-allocate': rest_allocate, 'doorway-edge': doorway_edge})


def doorway_return(binary, ctx):
    """Enter the shadow from its side, then immediately return without leaving its band."""
    root = Path(ctx.ROOT) / 'target/pty/cb04d-return'
    root.mkdir(parents=True, exist_ok=True)
    problems = []
    for tier in ('rich', 'plain'):
        save = root / (tier + '.save')
        save.unlink(missing_ok=True)
        subprocess.run([binary, '--headless', '--script', str(Path(ctx.ROOT) / 'tests/cases/rest-larkmeadow-80x24.pk'),
                        '--frames', '1', '--save', str(save), '--dump', str(root / ('setup-' + tier))], check=True, capture_output=True)
        session = ctx.Session([binary, '--save', str(save), '--tier', tier, '--trace', '--mute', '--no-title'], 24, 80, ctx.env_for())
        # Approach from the east: a horizontal body still overlaps the far-end
        # arrival shadow, and turning south makes it taller, never briefly clear.
        for _ in range(50):
            session.type(b'\x1b[C', settle=.06)
            if trace_states(session)[-1]['x'] >= 9 * 256:
                break
        for _ in range(50):
            session.type(b'\x1b[A', settle=.06)
            if trace_states(session)[-1]['y'] <= 2 * 256 + 128:
                break
        arrived = False
        for _ in range(60):
            session.type(b'\x1b[D', settle=.06)
            if any(v['area'] == 1 for v in trace_states(session)):
                arrived = True
                break
        mark = len(trace_states(session))
        returned = False
        if arrived:
            for _ in range(40):
                session.type(b'\x1b[B', settle=.06)
                if any(v['area'] == 2 for v in trace_states(session)[mark:]):
                    returned = True
                    break
        session.type(b'q')
        session.finish()
        ctx.common_checks(session, 0, problems)
        if not arrived or not returned:
            problems.append(tier + ': arrival did not permit immediate reverse crossing')
        (root / (tier + '.trace')).write_bytes(session.err)
    return session, problems

ROWS['doorway-return'] = doorway_return


def den_world_memory(binary, ctx):
    """A killed Shingle encounter stays gone after a path and an open log return."""
    import re
    root = Path(ctx.ROOT)
    case = root / 'tests/cases/den-memory.pk'
    ticks = re.search(r'# frames (\d+)', case.read_text())[1]
    session = ctx.Session([binary, '--replay', str(case), '--ticks', ticks,
                           '--trace', '--mute', '--no-title', '--tier', 'plain'],
                          24, 80, ctx.env_for())
    # The case is longer since cb05 (the gate opens on Cinderwick and the log
    # mouth lies at the Shingle's other end: about 1,230 ticks, 21 s live).
    session.finish(timeout=60)
    problems = []
    ctx.common_checks(session, 0, problems)
    states = trace_states(session)
    # The gate opens on Cinderwick since cb05: a departure leaves the Shingle
    # for any area, a return comes back into it (the path from the town, the
    # log from Bramblehold).
    departure = next((a for a, b in zip(states, states[1:])
                      if a['area'] == 0 and b['area'] != 0), None)
    returns = [b for a, b in zip(states, states[1:]) if a['area'] != 0 and b['area'] == 0]
    if departure is None or departure['live_foes'] >= 9:
        problems.append('den-world-memory: witness never killed a Shingle foe')
    elif len(returns) != 2 or any(b['live_foes'] > departure['live_foes'] for b in returns):
        problems.append('den-world-memory: path/log return revived slain Shingle foes')
    if not states or any(v['deaths'] or v['resting'] for v in states):
        problems.append('den-world-memory: a death/rest invalidated the witness')
    (root / 'target/pty').mkdir(parents=True, exist_ok=True)
    (root / 'target/pty/den-world-memory.trace').write_bytes(session.err)
    return session, problems

ROWS['den-world-memory'] = den_world_memory
# cb06: the real opening, no injected scene age or shortened timer. Each
# skip is a real decoded arrow, recorded and compared with headless replay.
OPENING_SHOTS = [0, 210, 225, 300, 330, 360, 420, 480, 510, 600, 660, 720, 765, 789, 810, 840]


def opening_live(binary, ctx, shot=None):
    import re
    import time
    label = 'complete' if shot is None else 'skip-%02d' % shot
    root = Path(ctx.ROOT) / 'target/pty' / ('opening-' + label)
    root.mkdir(parents=True, exist_ok=True)
    save = root / 'fresh.save'
    for suffix in ('', '.pending'):
        path = Path(str(save) + suffix)
        if path.exists():
            path.unlink()
    record = root / 'record.pk'
    env = ctx.env_for()
    env['HOME'] = str(root)
    session = ctx.Session([binary, '--seed', '1', '--save', str(save), '--record', str(record),
                           '--no-title', '--mute', '--trace', '--tier', 'plain',
                           '--no-truecolor', '--ticks', '920'], 24, 80, env)
    problems = []
    target = 902 if shot is None else max(12, OPENING_SHOTS[shot] + 3)
    deadline = time.monotonic() + 40
    tick = 0
    while tick < target and time.monotonic() < deadline:
        session.pump(.02)
        seen = re.findall(rb'trace tick (\d+)', session.err)
        if seen:
            tick = int(seen[-1])
    if tick < target:
        problems.append('opening did not reach tick %s' % target)
    if shot is not None:
        before = re.findall(rb'trace tick \d+ .*? x (-?\d+) y (-?\d+) .*? scene (\d+)', session.err)
        if not before or before[-1][2] != b'1':
            problems.append('skip was not in opening shot %d' % shot)
        session.type(b'\x1b[C', settle=.05)
        after = re.findall(rb'trace tick \d+ .*? x (-?\d+) y (-?\d+) .*? scene (\d+)', session.err)
        if not after or after[-1][2] != b'0' or before[-1][:2] != after[-1][:2]:
            problems.append('skip did not end scene without moving')
    elif not re.search(rb'trace tick 900 .*? area 0 .*? scene 0 ', session.err):
        problems.append('unskipped opening did not reach the Shingle at tick 900')
    session.type(b'q')
    session.finish()
    ctx.common_checks(session, 0, problems)
    (root / 'opening.trace').write_bytes(session.err)
    text = record.read_text()
    if text.count('opening 1') != 1:
        problems.append('record must hold exactly one opening event')
    if 'opening 1' not in save.read_text():
        problems.append('seen flag did not persist')
    # Read the actual completed tick from the closing line, then reproduce
    # the terminal's last frame from the recording, not a parallel script.
    ended = re.search(rb'; (\d+) ticks,', session.err)
    if ended:
        dest = root / 'replay'
        subprocess.run([binary, '--headless', '--script', str(record), '--frames', ended[1].decode(),
                        '--every', ended[1].decode(), '--tier', 'plain', '--dump', str(dest)], check=True)
        capture = root / 'capture.bin'
        capture.write_bytes(session.out)
        applied = subprocess.run([binary, '--apply', str(capture), '--size', '80x24'], capture_output=True, check=True)
        text, sty, _ = applied.stdout.decode().split('--\n')
        if (dest / 'final.txt').read_text() != text:
            problems.append('recorded opening does not reproduce the final terminal frame')
        if (dest / 'final.sty').read_text() != sty:
            problems.append('recorded opening does not reproduce terminal styles')
    else:
        problems.append('no final tick count')
    if shot is None:
        samples = {'crossing': 120, 'crack': 210, 'freeze': 260, 'spread': 315,
                   'plate': 345, 'fall': 390, 'underwater': 440, 'black': 495,
                   'blink1-open': 555, 'blink1-close': 630, 'blink1-peak': 600,
                   'blink1-shut': 660, 'blink2-open': 690, 'blink2-close': 744,
                   'blink2-shut': 765, 'blink3-open': 777, 'blink3-close': 800,
                   'blink3-shut': 810, 'clear-open': 825, 'clear': 870}
        for tier in ('plain', 'rich'):
            for name, age in samples.items():
                dest = root / ('recorded-' + name + '-' + tier)
                subprocess.run([binary, '--headless', '--script', str(record),
                                '--frames', str(age), '--every', str(age),
                                '--tier', tier, '--dump', str(dest)], check=True)
                golden = Path(ctx.ROOT) / ('tests/goldens/opening-%s-80x24-%s' % (name, tier))
                for extension in ('txt', 'sty'):
                    if (dest / ('final.' + extension)).read_bytes() != (golden / ('final.' + extension)).read_bytes():
                        problems.append('recorded shot %s/%s differs from %s golden' % (name, tier, extension))
    return session, problems


ROWS['opening-complete'] = opening_live
for _shot in range(len(OPENING_SHOTS)):
    ROWS['opening-skip-%02d' % _shot] = lambda binary, ctx, shot=_shot: opening_live(binary, ctx, shot)


def _opening_evidence_readable(home):
    """Publish only this synthetic fixture's evidence to the artifact reader.

    mkdtemp uses0700. Docker creates it as root, while the host uploader
    runs as another uid; rootless podman hides that ownership mismatch.
    Keep failure traces rather than deleting them, including partial output.
    """
    home.chmod(0o755)
    for directory, dirs, files in os.walk(home):
        for name in dirs:
            path = Path(directory) / name
            if not path.is_symlink():
                path.chmod(0o755)  # before os.walk descends into this child
        for name in files:
            path = Path(directory) / name
            if not path.is_symlink():
                path.chmod(0o644)


def opening_quit_due(binary, ctx):
    """A quit on the commit tick must not cancel an already-due seen flag.

    Keep opening-skip-01 unchanged. This drives its losing interleaving
    deliberately, then relaunches from the actual file, not a fixture.
    """
    import re
    import tempfile
    import time
    root = Path(ctx.ROOT) / 'target/pty/opening-quit-due'
    root.mkdir(parents=True, exist_ok=True)
    problems = []
    adjacent = 0
    for explicit in (False, True):
        for attempt in range(2):
            home = Path(tempfile.mkdtemp(prefix='fresh-', dir=root))
            try:
                env = ctx.env_for()
                env['HOME'] = str(home)
                path = home / ('missing/explicit.save' if explicit else '.cub/save')
                record = home / 'record.pk'
                args = [binary, '--seed', '1', '--no-title', '--mute', '--trace', '--tier', 'plain']
                if explicit:
                    args += ['--save', str(path)]
                session = ctx.Session(args + ['--record', str(record)], 24, 80, env)
                session.type(b'\x1b[C', settle=0)
                deadline = time.monotonic() + 3
                while time.monotonic() < deadline:
                    session.pump(.001)
                    if re.search(rb'trace tick \d+ .*? scene 0 ', session.err):
                        break
                else:
                    problems.append('opening never acknowledged the skip')
                session.type(b'q', settle=0)
                session.finish()
                ctx.common_checks(session, 0, problems)
                (home / 'first.trace').write_bytes(session.err)
                text = record.read_text()
                skipped = re.search(r'^t (\d+) right$', text, re.M)
                quit_at = re.search(r'^t (\d+) quit$', text, re.M)
                if skipped and quit_at and int(quit_at[1]) == int(skipped[1]) + 1:
                    adjacent += 1
                if 'opening 1' not in path.read_text():
                    problems.append('due seen flag lost on quit (%s attempt%d)' % ('explicit' if explicit else 'default', attempt))
                if Path(str(path) + '.pending').exists():
                    problems.append('owned stage survived quit')
                resumed = ctx.Session(args + ['--ticks', '2'], 24, 80, env)
                resumed.finish()
                ctx.common_checks(resumed, 0, problems)
                (home / 'resumed.trace').write_bytes(resumed.err)
                if re.search(rb'trace tick \d+ .*? scene 1 ', resumed.err):
                    problems.append('relaunch replayed an opening already seen')
            finally:
                _opening_evidence_readable(home)
    if adjacent == 0:
        problems.append('no adjacent skip/quit interleaving witnessed')
    resumed.evidence = '%d adjacent skip/quit pairs; fresh HOME and explicit path; relaunch checked' % adjacent
    return resumed, problems


ROWS['opening-quit-due'] = opening_quit_due




def _agree(binary, ctx, case_name, ticks, check):
    """cb05: a real-key witness replayed through the pty, its capture applied
    and compared with the headless frame, and its trace checked for the event
    the row names (a town passage, an Ashen parried, an ember touched, a
    yard's cache dug)."""
    root = Path(ctx.ROOT)
    case = root / 'tests' / 'cases' / (case_name + '.pk')
    s = ctx.Session([binary, '--replay', str(case), '--ticks', str(ticks), '--tier', 'plain', '--no-truecolor', '--mute'], 24, 80, ctx.env_for())
    s.finish()
    problems = []
    ctx.common_checks(s, 0, problems)
    dest = root / 'target' / 'pty' / case_name
    dest.mkdir(parents=True, exist_ok=True)
    cap = dest / 'capture.bin'
    cap.write_bytes(s.out)
    applied = subprocess.run([binary, '--apply', str(cap), '--size', '80x24'], capture_output=True, check=True)
    traced = subprocess.run([binary, '--headless', '--script', str(case), '--frames', str(ticks), '--every', str(ticks), '--tier', 'plain', '--trace', '--dump', str(dest)], capture_output=True, text=True, check=True)
    text, sty, _ = applied.stdout.decode().split('--\n')
    if text != (dest / 'final.txt').read_text() or sty != (dest / 'final.sty').read_text():
        problems.append(case_name + ': the live frame differs from the headless frame')
    states, foes, tick = {}, {}, None
    for line in traced.stderr.splitlines():
        words = line.split()
        if words[:1] == ['tick']:
            st = dict(zip(words[::2], map(int, words[1::2])))
            tick = st['tick']
            states[tick] = st
            foes[tick] = []
        elif words[:1] == ['foe']:
            foes[tick].append(dict(zip(words[::2], map(int, words[1::2]))))
    problem = check(states, foes)
    if problem:
        problems.append(problem)
    return s, problems


def _ticks_of(ctx, case_name):
    import re
    text = (Path(ctx.ROOT) / 'tests' / 'cases' / (case_name + '.pk')).read_text()
    return int(re.search(r'# frames (\d+)', text)[1])


def town_passage(binary, ctx):
    def check(states, foes):
        if not any(v['area'] == 6 for v in states.values()):
            return 'the passage row never stood in Cinderwick'
        return None
    return _agree(binary, ctx, 'town-passage', _ticks_of(ctx, 'town-passage'), check)


def ashen_parry(binary, ctx):
    def check(states, foes):
        wound = [t for t, fs in foes.items() if any(f['kind'] == 8 and f['phase'] == 1 for f in fs)]
        staggered = [t for t, fs in foes.items() if any(f['kind'] == 8 and f['phase'] == 4 for f in fs)]
        if not wound or not staggered or min(staggered) <= min(wound):
            return 'no Ashen wound up and was staggered'
        return None
    return _agree(binary, ctx, 'ashen-parry', _ticks_of(ctx, 'ashen-parry'), check)


def ember_touch(binary, ctx):
    def check(states, foes):
        healths = [v['health'] for t, v in sorted(states.items())]
        if not healths or min(healths) >= healths[0]:
            return 'the ember did not burn'
        return None
    return _agree(binary, ctx, 'ember-touch', _ticks_of(ctx, 'ember-touch'), check)


def yard_cache(binary, ctx):
    def check(states, foes):
        final = states[max(states)]
        if not final['caches'] & (1 << 8):
            return "the yard's cache was not dug"
        if not any(f['kind'] == 8 and f['health'] <= 0 for f in foes[max(foes)]):
            return 'the guard was not fought down'
        return None
    return _agree(binary, ctx, 'yard-cache', _ticks_of(ctx, 'yard-cache'), check)


ROWS.update({'town-passage': town_passage, 'ashen-parry': ashen_parry,
             'ember-touch': ember_touch, 'yard-cache': yard_cache})


def cb04b_traces(session):
    import re
    rows = []
    for line in session.err.decode(errors='replace').splitlines():
        if line.startswith('trace tick '):
            rows.append({k: int(v) for k, v in re.findall(r'(\w+) (-?\d+)', line)})
    return rows


def cb04b_event(key, kind=1, mods=1):
    if key in 'ABCD':
        return f'\x1b[1;{mods}:{kind}{key}'.encode()
    return f'\x1b[{ord(key)};{mods}:{kind}u'.encode()


def cb04b_session(binary, ctx, name, tier):
    dest = Path(ctx.ROOT) / 'target' / 'pty' / ('cb04b-' + name + '-' + tier)
    dest.mkdir(parents=True, exist_ok=True)
    save = dest / 'save'
    if save.exists():
        save.unlink()
    env = ctx.env_for()
    env['HOME'] = str(dest)
    s = ctx.Session([binary, '--seed', '1', '--tier', tier, '--trace', '--mute',
                     '--no-title', '--combat-witness', '--save', str(save),
                     '--record', str(dest / 'record.pk')], 40, 120, env,
                    replies=[(b'\x1b[?u', b'\x1b[?0u')])
    return s, dest


def cb04b_direction_row(aim, arrows, action, hold=0):
    def row(binary, ctx):
        problems = []
        for tier in ('rich', 'plain'):
            s, dest = cb04b_session(binary, ctx, f'{action}-{aim}-{hold}', tier)
            if hold:
                s.type(b''.join(cb04b_event(k) for k in arrows), settle=hold / 30 + .05)
                before = cb04b_traces(s)[-1]
                s.type(cb04b_event(action), settle=.62)
            else:
                before = cb04b_traces(s)[-1]
                s.type(b''.join(cb04b_event(k) for k in arrows) + cb04b_event(action), settle=.62)
            s.type(cb04b_event('q'))
            s.finish()
            ctx.common_checks(s, 0, problems)
            rows = cb04b_traces(s)
            active = [r for r in rows if r.get('action') == (4 if action == 'c' else 1)
                      and r['tick'] > before['tick']]
            if not active or any(r['aim'] != aim for r in active):
                problems.append(f'{tier}: held aim {aim} did not latch')
            if not any(r.get('exact') == 1 for r in rows):
                problems.append(f'{tier}: no negotiated exact state')
            if b'\x1b[>11u' not in s.out or b'\x1b[<u' not in s.out:
                problems.append(f'{tier}: missing keyboard push/pop')
            if active and action == 'c':
                last = active[-1]
                dx, dy = last['x'] - before['x'], last['y'] - before['y']
                print(f'cb04b roll tier={tier} aim={aim} hold={hold} dx={dx} dy={dy} heading={last["heading"]} blocked={last["blocked"]}')
                if last['heading'] != aim:
                    problems.append(f'{tier}: roll did not keep facing {aim}')
                if not hold and aim in (0, 64, 128, 192):
                    expected = {0: (0, -2560), 64: (2560, 0), 128: (0, 2560), 192: (-2560, 0)}[aim]
                    if (dx, dy) != expected:
                        problems.append(f'{tier}: clear cardinal distance {(dx, dy)} != {expected}')
            (dest / 'trace.txt').write_bytes(s.err)
        return s, problems
    return row


def cb04b_held_resume(binary, ctx):
    problems = []
    for tier in ('rich', 'plain'):
        s, dest = cb04b_session(binary, ctx, 'resume', tier)
        s.type(cb04b_event('B'), settle=.12)
        s.type(cb04b_event('D'), settle=.12)
        s.type(cb04b_event('D', 3), settle=.18)
        rows = cb04b_traces(s)
        if rows[-1].get('held') != 128:
            problems.append(f'{tier}: releasing Left lost still-held Down')
        s.type(cb04b_event('B', 3) + cb04b_event('C', mods=5), settle=.15)
        if cb04b_traces(s)[-1].get('sprint') != 1:
            problems.append(f'{tier}: Ctrl+Right did not sprint')
        # Modifier mask on a physical Control release, Right stays held.
        s.type(b'\x1b[57442;1:3u', settle=.15)
        last = cb04b_traces(s)[-1]
        if last.get('sprint') != 0 or last.get('held') != 64:
            problems.append(f'{tier}: Control release stopped the arrow or kept sprinting')
        s.type(cb04b_event('q'))
        s.finish()
        ctx.common_checks(s, 0, problems)
        (dest / 'trace.txt').write_bytes(s.err)
    return s, problems


ROWS['cb04b-held-resume'] = cb04b_held_resume
for _aim, _arrows in [(0, 'A'), (32, 'AC'), (64, 'C'), (96, 'BC'),
                     (128, 'B'), (160, 'BD'), (192, 'D'), (224, 'AD')]:
    ROWS[f'cb04b-roll-{_aim}'] = cb04b_direction_row(_aim, _arrows, 'c')
    ROWS[f'cb04b-bite-{_aim}'] = cb04b_direction_row(_aim, _arrows, ' ')
ROWS['cb04b-roll-none'] = cb04b_direction_row(0, '', 'c')
ROWS['cb04b-roll-held30-right'] = cb04b_direction_row(64, 'C', 'c', 30)
ROWS['cb04b-roll-held30-diagonal'] = cb04b_direction_row(224, 'AD', 'c', 30)
