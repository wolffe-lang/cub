"""cb11 real-reader proof paced by observed ticks; optional wall-clock measurement."""
from pathlib import Path
import runpy
import subprocess
import time


class DeliveryError(AssertionError):
    """An event was never consumed; lateness is measured, not rejected."""


def wait_tick(session, traces, target, timeout=5):
    deadline = time.monotonic() + timeout
    while True:
        live = traces(session)
        if live and live[-1]['tick'] >= target:
            return live[-1]['tick']
        if time.monotonic() >= deadline:
            raise DeliveryError(f'trace timeout waiting for tick{target}')
        session.pump(.001)


def send_at_tick(session, traces, data, target, timeout=5, observer_stall_ms=0):
    """Aim for N, acknowledge actual consumption strictly after this write.

    The optional proof-driver stall models a descheduled observer. Default
    ROWS never enables it. An already-late write is still sent; older input
    traces cannot acknowledge it, and a late acknowledgement is valid data.
    """
    wait_tick(session, traces, target - 1, timeout)
    if observer_stall_ms:
        session.pump(observer_stall_ms / 1000)
    before = traces(session)[-1]['tick']
    session.type(data, settle=0)
    deadline = time.monotonic() + timeout
    while True:
        live = traces(session)
        carrying = next((r for r in live if r['tick'] > before and
                         r.get('in', 0) > 0 and r.get('keys', 0) > 0), None)
        if carrying is not None:
            return carrying['tick']
        if time.monotonic() >= deadline:
            raise DeliveryError(f'input never consumed after write at tick{before}; requested{target}')
        session.pump(.001)


def schedule(interval, enhanced, event):
    """(nominal milliseconds, role, bytes), plus the unchanged strike contract."""
    press = b'\x1b[32u' if enhanced else b' '
    repeat = event(' ', 2) if enhanced else b' '
    result = [(0, 'press', press)]
    if isinstance(interval, str):
        result += [(ms, 'repeat', repeat) for ms in range(int(interval[4:]), 851, 30)]
        if enhanced:
            result.append((870, 'release', event(' ', 3)))
        expected = [1] if enhanced else [1, 2]
    elif interval in (30, 60):
        result += [(ms, 'repeat', repeat) for ms in range(interval, 851, interval)]
        if enhanced:
            result.append((880, 'release', event(' ', 3)))
        expected = [1]
    else:
        result = []
        for n in range(3):
            result.append((n * interval, 'press', press))
            if enhanced:
                result.append((n * interval + 45, 'release', event(' ', 3)))
        expected = [1, 2, 3]
    return sorted(result), expected


def tick_schedule(events, interval):
    """Explicit 30Hz quantization, not a claim of exact physical milliseconds.

    Hand presses retain cumulative floor quantization (150ms -> gaps4,5).
    Nominal30/60ms repeat streams use1/2 ticks. Held repeats start after8/15
    ticks for nominal250/500ms and repeat every tick. Release follows the
    last repeat, never sharing a tick with it.
    """
    result, repeats, last = [], 0, -1
    for ms, role, data in events:
        tick = ms * 30 // 1000
        if role == 'repeat':
            if isinstance(interval, str):
                tick = (int(interval[4:]) * 30 + 999) // 1000 + repeats
            else:
                tick = (repeats + 1) * (1 if interval == 30 else 2)
            repeats += 1
        elif role == 'release':
            tick = max(tick, last + 1)
        assert tick > last, ('schedule must have distinct ordered ticks', tick, last)
        result.append((tick, ms, role, data))
        last = tick
    return result


def gaps(ticks):
    return [b - a for a, b in zip(ticks, ticks[1:])]


def recorded_bites(path):
    # Replay event tN is applied by sim.step at tickN+1.
    return [int(w[1]) + 1 for line in path.read_text().splitlines()
            if len(w := line.split()) == 3 and w[0] == 't' and w[2] == 'bite']


def make_row(helpers, observed_ticks=True, observer_stall_ms=0):
    event = helpers['cb04b_event']
    traces = helpers['cb04b_traces']
    fresh_save = helpers['fresh_save']

    def row(binary, ctx):
        problems = []
        root = Path(ctx.ROOT)
        oracle = runpy.run_path(str(root / 'tools/combo-timing.py'))
        predict = runpy.run_path(str(root / 'tests/combo_request_oracle.py'))['predicted_starts']
        late_deliveries = 0
        for enhanced in (True, False):
            protocol = 'enhanced' if enhanced else 'legacy'
            for interval in (150, 200, 250, 330, 100, 30, 60, 'held250', 'held500'):
                for tier in ('rich', 'plain'):
                    prefix = 'cb11-ticks' if observed_ticks else 'cb11-measure'
                    label = f'{prefix}-{protocol}-{interval}-{tier}'
                    dest = root / 'target/pty' / label
                    dest.mkdir(parents=True, exist_ok=True)
                    env = ctx.env_for()
                    env['HOME'] = str(dest)
                    s = ctx.Session([binary, '--seed', '7', '--tier', tier, '--trace', '--mute',
                                     '--no-title', '--combat-witness', '--save', str(fresh_save(dest)),
                                     '--record', str(dest / 'record.pk'), '--no-truecolor'],
                                    24, 80, env, replies=[(b'\x1b[?u', b'\x1b[?0u')] if enhanced else [])
                    events, expected = schedule(interval, enhanced, event)
                    planned = tick_schedule(events, interval)
                    sent, delivered = [], []
                    began = time.monotonic()
                    delivery_ok = True
                    first = None
                    try:
                        first = wait_tick(s, traces, 1) + 2
                        if enhanced and b'\x1b[>11u' not in s.out:
                            raise AssertionError('missing event-types/all-keys request ESC[>11u')
                        if observed_ticks:
                            for offset, ms, role, data in planned:
                                requested = first + offset
                                tick = send_at_tick(s, traces, data, requested,
                                                    observer_stall_ms=observer_stall_ms)
                                delivered.append((offset, role, tick))
                                late_deliveries += tick > requested
                                print(f'{label}: event={role} nominal_ms={ms} requested_tick={requested} '
                                      f'consumed_tick={tick} late_ticks={tick - requested}', flush=True)
                                sent.append((ms, round((time.monotonic() - began) * 1000, 3), data.hex()))
                            wait_tick(s, traces, delivered[-1][2] + 45)
                        else:
                            # Deliberately retained wall-clock measurement. It is
                            # NOT registered in ROWS or called by a correctness gate.
                            for ms, role, data in events:
                                remaining = began + ms / 1000 - time.monotonic()
                                if remaining > .025:
                                    s.pump(remaining - .025)
                                remaining = began + ms / 1000 - time.monotonic()
                                if remaining > 0:
                                    time.sleep(remaining)
                                sent.append((ms, round((time.monotonic() - began) * 1000, 3), data.hex()))
                                s.type(data, settle=0)
                            s.pump(1.5)
                    except (AssertionError, KeyError) as error:
                        delivery_ok = False
                        problems.append(f'{label}: DELIVERY {error}')
                    finally:
                        s.type(event('q') if enhanced else b'q', settle=0)
                        s.finish()
                    ctx.common_checks(s, 0, problems)
                    (dest / 'trace.txt').write_bytes(s.err)
                    (dest / 'sent.txt').write_text('\n'.join(map(str, sent)) + '\n')
                    (dest / 'delivered.txt').write_text('\n'.join(map(str, delivered)) + '\n')
                    live = traces(s)
                    starts, previous = {}, (0, 0)
                    for state in live:
                        current = (state['action'], state['combo'])
                        if state['action'] == 1 and current != previous:
                            starts[state['tick']] = state['combo']
                        previous = current
                    bite_ticks = recorded_bites(dest / 'record.pk')
                    nominal_ms = [ms for ms, role, _ in events if role != 'release' and (not enhanced or role == 'press')]
                    if observed_ticks and delivery_ok:
                        predicted = predict([(tick, role) for _, role, tick in delivered],
                                            enhanced, max(r['tick'] for r in live))
                        expected = [hit for _, hit in predicted]
                    else:
                        predicted = []
                    print(f'{label}: nominal_ms={nominal_ms} recorded_bite_ticks={bite_ticks} delivered_gaps={gaps(bite_ticks)} '
                          f'strike_starts={list(starts.items())} ' +
                          (f'predicted_starts={predicted}' if observed_ticks else f'MEASUREMENT_ONLY ideal={expected} sent={sent}'), flush=True)
                    if observed_ticks:
                        requested = [] if first is None else [first + offset for offset, _, role, _ in planned
                                     if role != 'release' and (not enhanced or role == 'press')]
                        consumed = [tick for _, role, tick in delivered
                                    if role != 'release' and (not enhanced or role == 'press')]
                        print(f'{label}: requested_bite_ticks={requested} consumed_bite_ticks={consumed} acknowledgements={delivered}', flush=True)
                        if delivery_ok and bite_ticks != consumed:
                            delivery_ok = False
                            problems.append(f'{label}: DELIVERY recorded{bite_ticks}, acknowledged consumption{consumed}')
                        if delivery_ok and list(starts.items()) != predicted:
                            problems.append(f'{label}: observed starts{list(starts.items())}, predicted{predicted} from consumed gaps{gaps(bite_ticks)}')
                    if observed_ticks and delivery_ok and interval == 150:
                        frames = dest / 'frames'
                        count = max(r['tick'] for r in live)
                        p = subprocess.run([binary, '--headless', '--script', str(dest / 'record.pk'),
                                            '--frames', str(count), '--every', '1', '--tier', tier,
                                            '--trace', '--dump', str(frames)], capture_output=True, text=True)
                        (dest / 'replayed-trace.txt').write_text(p.stderr)
                        try:
                            assert p.returncode == 0, ('replay exit', p.returncode)
                            replayed = oracle['states_of'](p.stderr)
                            for state in live:
                                for key in ('x', 'y', 'heading', 'action', 'aim', 'combo', 'health',
                                            'stamina', 'flasks', 'area'):
                                    assert replayed[state['tick']][key] == state[key], ('live/replay', state['tick'], key)
                            oracle['holds'](replayed, 0, expected)
                            oracle['north_pixels'](replayed, frames, tier)
                        except (AssertionError, KeyError) as error:
                            problems.append(f'{label}: {error}')
        print(f'cb11b reader observer_stall_ms={observer_stall_ms} late_deliveries={late_deliveries}', flush=True)
        if observer_stall_ms and not late_deliveries:
            problems.append('observer-stall proof produced no actual late consumption')
        return s, problems
    return row


def rows(helpers):
    return {'cb11-hand-reader': make_row(helpers)}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--measure-wall-clock', action='store_true')
    mode.add_argument('--observer-stall-ms', type=int, help='proof-only observer descheduling; default ROWS never enable it')
    parser.add_argument('--bin', required=True)
    args = parser.parse_args()
    if args.observer_stall_ms is not None and not 1 <= args.observer_stall_ms <= 500:
        parser.error('observer stall must be1..500ms')
    root = Path(__file__).resolve().parents[1]
    engine = runpy.run_path(str(root / '.lair/tools/pty'))
    helpers = runpy.run_path(str(root / 'tests/pty_rows.py'))
    _, problems = make_row(helpers, observed_ticks=not args.measure_wall_clock,
                           observer_stall_ms=args.observer_stall_ms or 0)(str(Path(args.bin).resolve()), engine['Ctx'])
    if args.measure_wall_clock:
        print('Wall-clock cadence is measurement only; no strike-sequence acceptance assertion.')
    for problem in problems:
        print('reader proof FAILED:', problem)
    raise SystemExit(bool(problems))
