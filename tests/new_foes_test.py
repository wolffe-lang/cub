"""Negative controls for the six-foe shipping-binary gate and ring oracle."""
import copy
import csv
import gzip
import io
from pathlib import Path
import runpy
import unittest

ROOT = Path(__file__).resolve().parent.parent
GAMEPLAY = runpy.run_path(str(ROOT / 'tools/gameplay.py'))
HIT = runpy.run_path(str(ROOT / 'tools/hit-census.py'))


def arena_fixture():
    header = ('foe seed cols resolved ticks health recovery travel_fp '
              'contacts overlaps unreachable dodges')
    rows = [[kind, seed, cols, 1, 100, 40, 24, 1000, 4, 0, 0,
             2 if kind == 12 else 0]
            for kind in range(9, 15) for seed in range(50) for cols in (80, 200)]
    return header, rows


def arena_text(header, rows):
    return header + '\n' + '\n'.join(' '.join(map(str, row)) for row in rows) + '\n'


def encounter_fixture():
    return '\n'.join(
        f'encounter {kind} ticks 100 done 1 parity 1 bites 2 dodges {2 if kind == 12 else 0} '
        f'theft {int(kind == 9)} returned {int(kind == 9)} dim {int(kind == 11)} '
        f'flash {int(kind == 13)} health 40 foe_health {int(kind == 14)} '
        f'phase {10 if kind == 14 else 3} died {-1 if kind in (12, 14) else 99}'
        for kind in range(9, 15))


class NewFoeGateTests(unittest.TestCase):
    def test_complete_arena_fixture(self):
        header, rows = arena_fixture()
        self.assertEqual(len(GAMEPLAY['validate_new_foe_rows'](arena_text(header, rows))), 600)

    def test_reject_missing_and_duplicate_worlds(self):
        header, rows = arena_fixture()
        for bad in (rows[:-1], rows[:-1] + rows[:1]):
            with self.assertRaises(AssertionError):
                GAMEPLAY['validate_new_foe_rows'](arena_text(header, bad))

    def test_reject_no_recovery_unresolved_contact_fault_and_undodged_heron(self):
        header, rows = arena_fixture()
        for column, value in ((6, 0), (3, 0), (9, 1), (10, 1)):
            bad = copy.deepcopy(rows)
            bad[0][column] = value
            with self.assertRaises(AssertionError):
                GAMEPLAY['validate_new_foe_rows'](arena_text(header, bad))
        bad = copy.deepcopy(rows)
        next(row for row in bad if row[0] == 12)[11] = 0
        with self.assertRaises(AssertionError):
            GAMEPLAY['validate_new_foe_rows'](arena_text(header, bad))

    def test_six_explicit_nonkill_encounters(self):
        self.assertEqual(set(GAMEPLAY['validate_new_foe_encounters'](encounter_fixture())), set(range(9, 15)))

    def test_reject_missing_returns_dimming_flash_and_replay_parity(self):
        text = encounter_fixture()
        for old, new in (('returned 1', 'returned 0'), ('dim 1', 'dim 0'),
                         ('flash 1', 'flash 0'), ('parity 1', 'parity 0')):
            with self.assertRaises(AssertionError):
                GAMEPLAY['validate_new_foe_encounters'](text.replace(old, new, 1))

    def test_reject_killed_wisp_and_killed_rather_than_passed_heron(self):
        lines = encounter_fixture().splitlines()
        for index, old, new in ((5, 'foe_health 1', 'foe_health 0'), (3, 'died -1', 'died 99')):
            bad = list(lines)
            bad[index] = bad[index].replace(old, new)
            with self.assertRaises(AssertionError):
                GAMEPLAY['validate_new_foe_encounters']('\n'.join(bad))


class NewSpawnTests(unittest.TestCase):
    def fixture(self):
        header = 'new-foes seed field area martens adders moth_swarms herons glow_worms wisps'
        values = {7: (3, 0, 0, 0, 0, 0), 8: (0, 2, 2, 0, 0, 0), 9: (0, 0, 0, 1, 0, 0),
                  10: (0, 0, 0, 0, 24, 0), 11: (0, 0, 0, 0, 0, 2)}
        return header + '\n' + '\n'.join('new-foes ' + ' '.join(map(str, (seed, field, area, *count)))
          for seed in range(50) for field in (80, 200) for area, count in values.items()) + '\n' + self.VERDICT

    VERDICT = ('new-foe-npc-gap: green, 3400 spawns over 50 seeds at both fields, '
               'the nearest 5 clear cells from an NPC (talk radius 4)')

    def test_complete_distribution(self):
        self.assertEqual(len(GAMEPLAY['validate_new_foe_spawns'](self.fixture())), 500)

    def test_missing_world_and_missing_kind_are_red(self):
        lines = self.fixture().splitlines()
        for bad in ([*lines[:-2], lines[-1]], [*lines[:1], lines[1].replace('3 0 0 0 0 0', '0 0 0 0 0 0'), *lines[2:]]):
            with self.assertRaises(AssertionError):
                GAMEPLAY['validate_new_foe_spawns']('\n'.join(bad))

    def test_a_spawn_in_an_npc_talk_radius_is_red(self):
        # cb16's NPCs: the verdict line is required, and a near row or a
        # red verdict (the Stand's last marten by the Hermit) fails it.
        lines = self.fixture().splitlines()
        near = 'new-foe-near-npc 0 80 7 9 20 192 2'
        red = 'new-foe-npc-gap: RED, 94 of 3400 spawns within 4 clear cells of an NPC'
        for bad in (lines[:-1], [*lines[:-1], red], [*lines[:2], near, *lines[2:]]):
            with self.assertRaises(AssertionError):
                GAMEPLAY['validate_new_foe_spawns']('\n'.join(bad))


class NewFoeRingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = gzip.decompress((ROOT / 'notes/cb18-evidence/new-hit-pre-merge.csv.gz').read_bytes()).decode()
        cls.rows = [{k: int(v) for k, v in row.items()} for row in csv.DictReader(io.StringIO(raw))]

    def test_complete_measured_new_rings(self):
        table = HIT['audit'](self.rows, enforce=True, pixels=HIT['NEW_PIXELS'])
        self.assertIn('inward-gap01 misses 0', table)
        self.assertEqual(len(self.rows), 22752)

    def test_reject_missing_new_kind(self):
        with self.assertRaises(AssertionError):
            HIT['audit']([row for row in self.rows if row['kind'] != 14],
                         enforce=True, pixels=HIT['NEW_PIXELS'])

    def test_reject_inward_wisp_snuff_refused(self):
        bad = copy.deepcopy(self.rows)
        for row in bad:
            if row['kind'] == 14:
                row['hit'] = 0
        with self.assertRaises(AssertionError):
            HIT['audit'](bad, enforce=True, pixels=HIT['NEW_PIXELS'])

    def test_reject_excess_reach(self):
        bad = copy.deepcopy(self.rows)
        next(row for row in bad if row['gap'] == 2)['hit'] = 1
        with self.assertRaises(AssertionError):
            HIT['audit'](bad, enforce=True, pixels=HIT['NEW_PIXELS'])


if __name__ == '__main__':
    unittest.main()
