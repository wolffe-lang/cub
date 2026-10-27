#!/usr/bin/env python3
"""Synthetic audit-output mutations must not pass the completeness check."""
from pathlib import Path
import runpy
import unittest

ROOT = Path(__file__).resolve().parent.parent
check_hitbox_rows = runpy.run_path(str(ROOT / 'tools/world_checks.py'))['check_hitbox_rows']


class HitboxCompleteness(unittest.TestCase):
    def rows(self):
        return [f'{aim} 0 0 {gap} true true true' for gap in (0, 1) for aim in range(8)]

    def test_all_sixteen_distinct_contacts_are_required(self):
        check_hitbox_rows('\n'.join(self.rows()) + '\nhitbox: green\n')

    def test_missing_duplicate_miss_and_empty_outputs_fail(self):
        rows = self.rows()
        cases = {
            'missing': rows[:-1],
            'duplicate': rows[:-1] + [rows[0]],
            'miss': rows[:-1] + [rows[-1].rsplit(' ', 1)[0] + ' false'],
            'empty': [],
        }
        for name, lines in cases.items():
            with self.subTest(name=name), self.assertRaises(AssertionError):
                check_hitbox_rows('\n'.join(lines) + '\nhitbox: green\n')


if __name__ == '__main__':
    unittest.main()
