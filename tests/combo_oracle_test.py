import copy
from pathlib import Path
import runpy
import unittest

ORACLE = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'tools/combo-timing.py'))


def north():
    result = {}
    for tick in range(1, 45):
        state = dict(tick=tick, action=0, started=0, combo=0, aim=0, x=0, y=0)
        for start, hit, duration in ((3, 1, 11), (14, 2, 13), (27, 3, 17)):
            age = tick - start
            if 0 <= age < duration:
                state.update(action=1, started=start, combo=hit)
                if 3 <= age <= (8 if hit == 3 else 6):
                    state.update(x=(-256 if hit == 1 else 256 if hit == 2 else 0),
                                 y=(-512 if hit == 3 else -256))
        result[tick] = state
    return result


class ComboOracleTest(unittest.TestCase):
    def test_north_sequence(self):
        self.assertEqual(ORACLE['holds'](north(), 0),
                         [(1, 6, 1.0, 1.0), (2, 17, 1.0, -1.0), (3, 30, 2.0, 0.0)])

    def test_empty_trace_is_not_green(self):
        with self.assertRaises(AssertionError):
            ORACLE['holds']({}, 0)

    def test_two_strikes_is_not_three(self):
        states = north()
        for state in states.values():
            if state['combo'] == 3:
                state['action'] = 0
        with self.assertRaises(AssertionError):
            ORACLE['holds'](states, 0)

    def test_all_left_is_red(self):
        states = north()
        for state in states.values():
            state['x'] = -abs(state['x'])
        with self.assertRaises(AssertionError):
            ORACLE['holds'](states, 0)

    def test_wrong_number_wrong_aim_and_one_missing_hold_each_fail(self):
        for field, value in (('combo', 1), ('aim', 64), ('action', 0)):
            states = copy.deepcopy(north())
            states[17][field] = value
            with self.assertRaises(AssertionError, msg=field):
                ORACLE['holds'](states, 0)

    def test_reader_can_require_two_first_strikes_after_real_grace_lapses(self):
        states = {}
        for tick in range(1, 40):
            row = dict(tick=tick, action=0, started=0, combo=0, aim=0, x=0, y=0)
            for start in (3, 25):
                if 0 <= tick - start < 11:
                    row.update(action=1, started=start, combo=1)
                    if 3 <= tick - start <= 6:
                        row.update(x=-256, y=-256)
            states[tick] = row
        self.assertEqual(ORACLE['holds'](states, 0, [1, 1]), [(1, 6, 1.0, 1.0), (1, 28, 1.0, 1.0)])
        with self.assertRaises(AssertionError):
            ORACLE['holds'](states, 0)  # deterministic three-press contract is unchanged
        states[28]['x'] = 256
        with self.assertRaises(AssertionError):
            ORACLE['holds'](states, 0, [1, 1])

    def test_backward_third_and_sideways_third_fail(self):
        for field, value in (('x', 256), ('y', 256)):
            states = north()
            states[30][field] = value
            with self.assertRaises(AssertionError, msg=field):
                ORACLE['holds'](states, 0)


if __name__ == '__main__':
    unittest.main()
