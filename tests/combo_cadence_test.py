from pathlib import Path
import runpy
import unittest

MOD = runpy.run_path(str(Path(__file__).with_name('combo_pty.py')))


def event(key, kind=1, mods=1):
    return f'\x1b[{ord(key)};{mods}:{kind}u'.encode()


class Session:
    def __init__(self, tick=0, step=1, drop=False):
        self.trace = [dict(tick=tick, **{'in': 0})]
        self.step = step
        self.drop = drop
        self.pending = b''
        self.writes = []

    def type(self, data, settle=0):
        self.writes.append((self.trace[-1]['tick'], data))
        self.pending = data

    def pump(self, seconds):
        self.trace.append(dict(tick=self.trace[-1]['tick'] + self.step,
                               **{'in': 0 if self.drop else len(self.pending)}))
        self.pending = b''


def traces(session):
    return session.trace


class ObservedCadenceTest(unittest.TestCase):
    def test_press_after_observed_tick_is_acknowledged_at_requested_tick(self):
        s = Session()
        self.assertEqual(MOD['send_at_tick'](s, traces, b' ', 3), 3)
        self.assertEqual(s.writes, [(2, b' ')])
        self.assertEqual(MOD['send_at_tick'](s, traces, b' ', 6), 6)
        self.assertEqual(s.writes[-1], (5, b' '))

    def test_missed_predecessor_fails_before_writing(self):
        s = Session(tick=4)
        with self.assertRaisesRegex(MOD['DeliveryError'], 'late before write'):
            MOD['send_at_tick'](s, traces, b' ', 3)
        self.assertEqual(s.writes, [])

    def test_late_ack_is_not_silently_accepted(self):
        s = Session(step=2)
        with self.assertRaisesRegex(MOD['DeliveryError'], 'late delivery'):
            MOD['send_at_tick'](s, traces, b' ', 1)

    def test_dropped_input_is_not_a_strike_verdict(self):
        s = Session(drop=True)
        with self.assertRaisesRegex(MOD['DeliveryError'], 'missing input'):
            MOD['send_at_tick'](s, traces, b' ', 1)

    def test_missing_trace_times_out(self):
        with self.assertRaisesRegex(MOD['DeliveryError'], 'trace timeout'):
            MOD['wait_tick'](Session(), lambda _: [], 1, timeout=0)

    def test_hand_schedule_preserves_cumulative_tick_quantization(self):
        for ms, ticks in ((100, [0, 3, 6]), (150, [0, 4, 9]), (200, [0, 6, 12]),
                          (250, [0, 7, 15]), (330, [0, 9, 19])):
            for enhanced in (False, True):
                events, expected = MOD['schedule'](ms, enhanced, event)
                planned = MOD['tick_schedule'](events, ms)
                self.assertEqual([t for t, _, role, _ in planned if role == 'press'], ticks)
                self.assertEqual(expected, [1, 2, 3])

    def test_repeat_ticks_and_legacy_delay_limit_are_explicit(self):
        for ms, step in ((30, 1), (60, 2)):
            events, expected = MOD['schedule'](ms, False, event)
            ticks = [t for t, _, _, _ in MOD['tick_schedule'](events, ms)]
            self.assertEqual(set(MOD['gaps'](ticks)), {step})
            self.assertEqual(expected, [1])
        for interval, delay in (('held250', 8), ('held500', 15)):
            for enhanced in (False, True):
                events, expected = MOD['schedule'](interval, enhanced, event)
                planned = MOD['tick_schedule'](events, interval)
                repeats = [t for t, _, role, _ in planned if role == 'repeat']
                self.assertEqual(repeats[0], delay)
                self.assertEqual(set(MOD['gaps'](repeats)), {1})
                self.assertEqual(expected, [1] if enhanced else [1, 2])
                self.assertEqual(len({t for t, _, _, _ in planned}), len(planned))

    def test_wall_clock_measurement_is_not_in_default_rows(self):
        registered = MOD['rows']({'cb04b_event': event, 'cb04b_traces': traces,
                                  'fresh_save': lambda root: root / 'save'})
        self.assertEqual(list(registered), ['cb11-hand-reader'])


if __name__ == '__main__':
    unittest.main()
