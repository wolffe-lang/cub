#!/usr/bin/env python3
"""The fox-contact oracle must reject water theft and incorrect scent."""
from pathlib import Path
import runpy
import unittest

ROOT = Path(__file__).resolve().parent.parent
check_fox_contact = runpy.run_path(str(ROOT / 'tools/gameplay.py'))['check_fox_contact']


class FoxContactOracle(unittest.TestCase):
    def before(self, scent=16):
        return {'health': 52, 'flasks': 2, 'scent': scent}

    def after(self, scent=11):
        return {'health': 36, 'flasks': 2, 'scent': scent}

    def test_landed_hit_preserves_water_and_takes_five_scent(self):
        check_fox_contact(self.before(), self.after())

    def test_zero_and_partial_scent_clamp_at_zero(self):
        for scent in (0, 1, 4, 5):
            with self.subTest(scent=scent):
                check_fox_contact(self.before(scent), self.after(0))

    def test_old_water_theft_and_wrong_scent_are_rejected(self):
        cases = {
            'old-water-theft': {'health': 36, 'flasks': 1, 'scent': 16},
            'water-theft-even-with-scent': {'health': 36, 'flasks': 1, 'scent': 11},
            'no-scent-stolen': self.after(16),
            'too-much-stolen': self.after(10),
            'no-landed-hit': {'health': 52, 'flasks': 2, 'scent': 11},
        }
        for name, after in cases.items():
            with self.subTest(case=name), self.assertRaises(AssertionError):
                check_fox_contact(self.before(), after)

    def test_scent_underflow_is_rejected(self):
        with self.assertRaises(AssertionError):
            check_fox_contact(self.before(1), self.after(-4))


if __name__ == '__main__':
    unittest.main()
