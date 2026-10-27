import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    'memory_probe', Path(__file__).resolve().parents[1] / 'tools/memory-probe.py')
probe = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(probe)


class MemoryProbeTests(unittest.TestCase):
    def samples(self, growth, ticks=900):
        return [{'seconds': 10, 'tick': 300, 'rss_bytes': 10000000},
                {'seconds': 40, 'tick': 300 + ticks, 'rss_bytes': 10000000 + growth}]

    def test_budget_boundary_is_in_bytes_per_actual_tick(self):
        self.assertEqual(probe.evaluate(self.samples(4096 * 900), 4096)['status'], 'GREEN')
        self.assertEqual(probe.evaluate(self.samples(4096 * 900 + 1), 4096)['status'], 'RED')

    def test_stalled_or_backward_tick_is_red(self):
        for ticks in [0, -1]:
            self.assertEqual(probe.evaluate(self.samples(0, ticks), 4096)['status'], 'RED')

    def test_empty_or_single_sample_is_not_a_pass(self):
        for rows in [[], self.samples(0)[:1]]:
            with self.assertRaises(ValueError):
                probe.evaluate(rows, 4096)

    def test_flat_or_reclaimed_residency_passes(self):
        for growth in [0, -1000000]:
            self.assertEqual(probe.evaluate(self.samples(growth), 4096)['status'], 'GREEN')

    def test_ps_kib_is_converted_to_bytes(self):
        with patch.object(probe, 'LINUX', False), patch.object(probe.subprocess, 'run') as run:
            run.return_value.stdout = ' 12345\n'
            self.assertEqual(probe.rss_bytes(123), 12345 * 1024)
            self.assertTrue(run.call_args.kwargs['check'])

    def test_bad_ps_output_fails_closed(self):
        with patch.object(probe, 'LINUX', False), patch.object(probe.subprocess, 'run') as run:
            run.return_value.stdout = ''
            with self.assertRaises(ValueError):
                probe.rss_bytes(123)

    def test_linux_proc_pages_use_the_actual_page_size(self):
        with patch.object(probe, 'LINUX', True), \
                patch.object(probe.Path, 'read_text', return_value='1000 123 90 0 0 0 0'), \
                patch.object(probe.os, 'sysconf', return_value=4096):
            self.assertEqual(probe.rss_bytes(123), 123 * 4096)

    def test_trunk_fresh_slope_is_red(self):
        self.assertEqual(probe.evaluate(self.samples(41118 * 900), 4096)['status'], 'RED')

    def test_both_platform_entrypoints_call_the_gate(self):
        root = Path(__file__).resolve().parents[1]
        for name in ['check', 'check-linux']:
            self.assertIn('sh tools/check-memory target/release/cub', (root / 'tools' / name).read_text())
