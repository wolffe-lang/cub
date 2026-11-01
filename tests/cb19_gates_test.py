"""cb19: negative controls for the spacing census and theft witness gates."""
from pathlib import Path
import runpy
import unittest

ROOT = Path(__file__).resolve().parent.parent
GAMEPLAY = runpy.run_path(str(ROOT / 'tools/gameplay.py'))
EVIDENCE = ROOT / 'notes/cb19-evidence/spacing'


def green():
    rows = ['foe-npc-world seed field nearest']
    rows += ['foe-npc-world %d %d 5' % (s, f) for s in range(50) for f in (80, 200)]
    rows += ['foe-moved 0 80 5 ordinal 0 kind 1 from -11 40 gap -4 to -1 49 gap 5']
    rows += ['foe-npc-gap: green, 16600 foes over 50 seeds at both fields in 13 areas, '
             '574 moved by the gap, the nearest 5 clear cells from an NPC (talk radius 4)']
    return rows


class SpacingCensusGate(unittest.TestCase):
    def test_a_green_census_passes(self):
        self.assertEqual(len(GAMEPLAY['validate_foe_npc_census']('\n'.join(green()))), 100)

    def test_the_base_placements_are_red(self):
        # The census over cub c8669f2c's placements, the Hush's foxes and
        # weasels by the lost: 560 rows inside the gap.
        text = (EVIDENCE / 'census-red-at-base.txt').read_text()
        self.assertEqual(text.count('\nfoe-near-npc '), 560)
        with self.assertRaises(AssertionError):
            GAMEPLAY['validate_foe_npc_census'](text)

    def test_a_foe_in_the_gap_a_short_world_or_a_bad_move_is_red(self):
        rows = green()
        for bad in ([*rows[:3], 'foe-near-npc 0 80 5 1 -11 40 -4', *rows[3:]],
                    [rows[0], rows[1].replace(' 5', ' 4'), *rows[2:]],
                    [*rows[:1], *rows[2:]],
                    [*rows[:-2], rows[-2].replace('gap 5', 'gap 3'), rows[-1]],
                    rows[:-1],
                    [*rows[:-1], rows[-1].replace('nearest 5', 'nearest 6')]):
            with self.assertRaises(AssertionError):
                GAMEPLAY['validate_foe_npc_census']('\n'.join(bad))


class TheftWitnessGate(unittest.TestCase):
    GOOD = ('theft-proof: slot 1 theft 300 death 340 wake 721 held 1 returned 900 recovered 980 final x 1 y 2 health 3 yarrow 1\n'
            'theft-replay: slot 1 theft 300 death 340 wake 721 held 1 returned 900 recovered 980 parity 1\n'
            'theft-proof: green, steal at 300, death at 340, wake at 721 holding it, bitten back at 900, recovered at 980, 990 ticks\n')

    def test_a_green_witness_passes(self):
        self.assertEqual(GAMEPLAY['validate_theft_proof'](self.GOOD)[0], '1')

    def test_a_lost_theft_a_broken_replay_or_a_missing_verdict_is_red(self):
        for bad in (self.GOOD.replace('held 1 returned 900 recovered 980 parity', 'held 0 returned 900 recovered 980 parity'),
                    self.GOOD.replace('parity 1', 'parity 0'),
                    self.GOOD.replace('returned 900 recovered 980 parity', 'returned 300 recovered 980 parity'),
                    '\n'.join(self.GOOD.splitlines()[:2])):
            with self.assertRaises(AssertionError):
                GAMEPLAY['validate_theft_proof'](bad)


if __name__ == '__main__':
    unittest.main()
