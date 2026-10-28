"""cb11 real-reader hand timing, enhanced events and legacy byte streams."""
from pathlib import Path
import runpy
import subprocess
import time


def rows(helpers):
    event = helpers['cb04b_event']
    traces = helpers['cb04b_traces']
    fresh_save = helpers['fresh_save']

    def row(binary, ctx):
        problems = []
        root = Path(ctx.ROOT)
        oracle = runpy.run_path(str(root / 'tools/combo-timing.py'))
        for enhanced in (True, False):
            protocol = 'enhanced' if enhanced else 'legacy'
            for interval in (150, 200, 250, 330, 100, 30, 60, 'held250', 'held500'):
                for tier in ('rich', 'plain'):
                    label = f'cb11-{protocol}-{interval}-{tier}'
                    dest = root / 'target/pty' / label
                    dest.mkdir(parents=True, exist_ok=True)
                    env = ctx.env_for()
                    env['HOME'] = str(dest)
                    s = ctx.Session([binary, '--seed', '7', '--tier', tier, '--trace', '--mute',
                                     '--no-title', '--combat-witness', '--save', str(fresh_save(dest)),
                                     '--record', str(dest / 'record.pk'), '--no-truecolor'],
                                    24, 80, env, replies=[(b'\x1b[?u', b'\x1b[?0u')] if enhanced else [])
                    deadline = time.monotonic() + 3
                    while not traces(s) and time.monotonic() < deadline:
                        s.pump(.01)
                    schedule = []
                    # Ghostty-compatible kitty sequences: flags 1|2|8 request
                    # event types AND all keys. PRESS may omit default fields.
                    press = b'\x1b[32u' if enhanced else b' '
                    if enhanced and b'\x1b[>11u' not in s.out:
                        problems.append(f'{label}: missing event-types/all-keys request ESC[>11u')
                    if isinstance(interval, str):
                        delay = int(interval[4:])
                        schedule.append((0, press))
                        for ms in range(delay, 851, 30):
                            schedule.append((ms, event(' ', 2) if enhanced else b' '))
                        if enhanced:
                            schedule.append((870, event(' ', 3)))
                        # The legacy heuristic cannot identify the first delayed
                        # repeat: its 250ms gap is indistinguishable from a tap.
                        expected = [1] if enhanced else [1, 2]
                    elif interval in (30, 60):
                        schedule.append((0, press))
                        for ms in range(interval, 851, interval):
                            schedule.append((ms, event(' ', 2) if enhanced else b' '))
                        if enhanced:
                            schedule.append((880, event(' ', 3)))
                        expected = [1]
                    else:
                        for n in range(3):
                            schedule.append((n * interval, press))
                            if enhanced:
                                schedule.append((n * interval + 45, event(' ', 3)))
                        expected = [1, 2, 3]
                    began = time.monotonic()
                    sent = []
                    for ms, data in sorted(schedule):
                        remaining = began + ms / 1000 - time.monotonic()
                        if remaining > .025:
                            s.pump(remaining - .025)
                        # Session.pump polls in 20ms quanta; do not let that
                        # polling cadence turn a requested 60ms gap into 80ms.
                        remaining = began + ms / 1000 - time.monotonic()
                        if remaining > 0:
                            time.sleep(remaining)
                        sent.append((ms, round((time.monotonic() - began) * 1000, 3), data.hex()))
                        s.type(data, settle=0)
                    s.pump(1.5)
                    s.type(event('q') if enhanced else b'q', settle=0)
                    s.finish()
                    ctx.common_checks(s, 0, problems)
                    (dest / 'trace.txt').write_bytes(s.err)
                    (dest / 'sent.txt').write_text('\n'.join(map(str, sent)) + '\n')
                    live = traces(s)
                    starts = {}
                    previous = (0, 0)
                    for state in live:
                        current = (state['action'], state['combo'])
                        if state['action'] == 1 and current != previous:
                            starts[state['tick']] = state['combo']
                        previous = current
                    sequence = list(starts.values())
                    print(f'{label}: strike_starts={list(starts.items())} expected={expected}', flush=True)
                    if sequence != expected:
                        problems.append(f'{label}: strike sequence {sequence}, expected {expected}')
                    if interval == 150:
                        frames = dest / 'frames'
                        count = max(r['tick'] for r in live)
                        p = subprocess.run([binary, '--headless', '--script', str(dest / 'record.pk'),
                                            '--frames', str(count), '--every', '1', '--tier', tier,
                                            '--trace', '--dump', str(frames)], capture_output=True, text=True)
                        (dest / 'replayed-trace.txt').write_text(p.stderr)
                        try:
                            assert p.returncode == 0, ('replay exit', p.returncode)
                            replayed = oracle['states_of'](p.stderr)
                            # Inputs are logged before sim.step; compare actual
                            # common ticks, never assume wall-clock exactness.
                            for state in live:
                                for key in ('x', 'y', 'heading', 'action', 'aim', 'combo', 'health',
                                            'stamina', 'flasks', 'area'):
                                    assert replayed[state['tick']][key] == state[key], ('live/replay', state['tick'], key)
                            oracle['holds'](replayed, 0)
                            oracle['north_pixels'](replayed, frames, tier)
                        except (AssertionError, KeyError) as error:
                            problems.append(f'{label}: {error}')
        return s, problems

    return {'cb11-hand-reader': row}
