from pathlib import Path
import runpy
import unittest

predict = runpy.run_path(str(Path(__file__).with_name('combo_request_oracle.py')))['predicted_starts']


def presses(*ticks):
    return [(tick, 'press') for tick in ticks]


class ConsumedRequestsTest(unittest.TestCase):
    def test_early_requests_and_inclusive_ends(self):
        for ticks in ((1, 5, 10), (1, 2, 3), (1, 12, 25)):
            self.assertEqual(predict(presses(*ticks), True, 70), [(1, 1), (12, 2), (25, 3)])

    def test_grace_boundary_and_lapse(self):
        self.assertEqual(predict(presses(1, 18), True, 50), [(1, 1), (18, 2)])
        self.assertEqual(predict(presses(1, 19, 40), True, 70), [(1, 1), (19, 1), (40, 1)])

    def test_queue_cap_and_same_tick_duplicates(self):
        self.assertEqual(predict(presses(1, 2, 3, 4), True, 70), [(1, 1), (12, 2), (25, 3)])
        self.assertEqual(predict(presses(1, 1, 1), True, 50), [(1, 1)])

    def test_actual_legacy_gaps_not_nominal_schedule(self):
        self.assertEqual(predict(presses(3, 7, 9), False, 60), [(3, 1), (14, 2)])
        self.assertEqual(predict(presses(6, 9, 12), False, 60), [(6, 1), (17, 2), (30, 3)])
        self.assertEqual(predict(presses(1, 3, 5, 7, 10), False, 60), [(1, 1), (12, 2)])
        self.assertEqual(predict(presses(*range(1, 62, 2)), False, 100), [(1, 1)])

    def test_enhanced_repeat_and_release_never_request(self):
        events = [(1, 'press'), (10, 'repeat'), (20, 'repeat'), (21, 'release')]
        self.assertEqual(predict(events, True, 70), [(1, 1)])
        self.assertEqual(predict(events, False, 70), [(1, 1), (12, 2), (25, 3)])

    def test_first_delayed_legacy_repeat_is_a_request(self):
        for tick in (9, 16):
            events = [(1, 'press')] + [(t, 'repeat') for t in range(tick, tick + 20)]
            self.assertEqual(predict(events, False, 80), [(1, 1), (max(12, tick), 2)])
            self.assertEqual(predict(events, True, 80), [(1, 1)])

    def test_costs_refuse_queued_link_and_do_not_restart_automatically(self):
        events = presses(*range(1, 59, 3))
        expected = [(1, 1), (12, 2), (25, 3), (42, 1), (53, 2)]
        self.assertEqual(predict(events, False, 100), expected)
        self.assertEqual(predict(events + [(75, 'press')], False, 100), expected + [(75, 1)])
        self.assertEqual(predict(presses(1, 2, 3), True, 100, stamina=12), [(1, 1)])

    def test_each_bite_cost_has_an_independent_threshold(self):
        events = presses(1, 2, 3)
        for stamina, expected in ((11, []), (12, [(1, 1)]),
                                  (25, [(1, 1)]), (26, [(1, 1), (12, 2)]),
                                  (43, [(1, 1), (12, 2)]),
                                  (44, [(1, 1), (12, 2), (25, 3)])):
            # A single press pins cost12; the queued pair pins14 and18.
            data = presses(1) if stamina <= 12 else events
            self.assertEqual(predict(data, True, 60, stamina=stamina), expected)

    def test_idle_recovery_is_two_after_input_not_before_it(self):
        self.assertEqual(predict(presses(1, 6, 7), True, 40, stamina=0), [(7, 1)])

    def test_policy_mutation_controls_disagree(self):
        got = predict(presses(1, 12, 25), True, 70)
        for wrong in ([(1, 1), (25, 1)], [(1, 1), (12, 1), (23, 1)], [(1, 1), (13, 2), (26, 3)]):
            self.assertNotEqual(got, wrong)  # strict endpoint, all-left, delayed start mutants

    def test_invalid_or_unconsumed_event_data_is_rejected(self):
        for events in ([(2, 'press'), (1, 'press')], [(0, 'press')], [(2, 'unknown')], [(51, 'press')]):
            with self.assertRaises(AssertionError):
                predict(events, True, 50)


if __name__ == '__main__':
    unittest.main()
