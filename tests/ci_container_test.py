import contextlib
import hashlib
import importlib.util
import io
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('ci_container', ROOT / 'tools/ci-container.py')
cache = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cache)


class ContainerCacheTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / 'target/ci-container-tests'
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.recipe = self.root / '.lair/ci/Containerfile'
        self.recipe.parent.mkdir(parents=True)
        self.recipe.write_text('FROM example:fixture\n')
        self.archive = self.root / 'target/ci-container/image.tar'
        self.image = cache.image_name(self.root)
        self.calls = []
        self.present = False
        self.failure = None
        self.bad_load = False

    def engine(self, argv, **kwargs):
        self.calls.append((argv, kwargs))
        action = argv[1]
        if action == 'image':
            return subprocess.CompletedProcess(argv, 0 if self.present else 1)
        if action == self.failure:
            raise subprocess.CalledProcessError(17, argv)
        if action == 'build' or (action == 'load' and not self.bad_load):
            self.present = True
        if action == 'save':
            Path(argv[argv.index('--output') + 1]).write_bytes(b'fixture-image')
        return subprocess.CompletedProcess(argv, 0)

    def prepare(self):
        with mock.patch.object(cache.subprocess, 'run', side_effect=self.engine):
            cache.prepare(self.root, 'fixture-engine')

    def test_tag_matches_engine_recipe_hash_and_changes_with_recipe(self):
        self.assertEqual(self.image, 'localhost/pack-ci:' + hashlib.sha256(self.recipe.read_bytes()).hexdigest()[:16])
        self.recipe.write_text('FROM example:changed\n')
        self.assertNotEqual(self.image, cache.image_name(self.root))

    def test_cold_cache_builds_and_saves_exact_image(self):
        self.prepare()
        build = next(args for args, _ in self.calls if args[1] == 'build')
        self.assertEqual(build, ['fixture-engine', 'build', '--memory', '12g', '-t', self.image,
                                 '-f', str(self.recipe), str(self.recipe.parent)])
        self.assertEqual(self.archive.read_bytes(), b'fixture-image')
        self.assertFalse(self.archive.with_suffix('.partial').exists())

    def test_existing_local_image_is_saved_without_rebuilding(self):
        self.present = True
        self.prepare()
        self.assertNotIn('build', [args[1] for args, _ in self.calls])
        self.assertTrue(self.archive.is_file())

    def test_warm_cache_loads_without_build_or_save(self):
        self.archive.parent.mkdir(parents=True)
        self.archive.write_bytes(b'cached-image')
        self.prepare()
        self.assertEqual([args[1] for args, _ in self.calls], ['load', 'image'])
        self.assertEqual(self.archive.read_bytes(), b'cached-image')

    def test_wrong_image_in_cache_fails_closed(self):
        self.archive.parent.mkdir(parents=True)
        self.archive.write_bytes(b'wrong-image')
        self.bad_load = True
        with self.assertRaisesRegex(RuntimeError, 'exact Containerfile tag'):
            self.prepare()
        self.assertNotIn('build', [args[1] for args, _ in self.calls])

    def test_failed_build_never_creates_a_cache(self):
        self.failure = 'build'
        with self.assertRaises(subprocess.CalledProcessError):
            self.prepare()
        self.assertFalse(self.archive.exists())
        self.assertNotIn('save', [args[1] for args, _ in self.calls])

    def test_failed_save_never_promotes_a_partial_archive(self):
        self.present = True
        self.failure = 'save'
        with self.assertRaises(subprocess.CalledProcessError):
            self.prepare()
        self.assertFalse(self.archive.exists())
        self.assertFalse(self.archive.with_suffix('.partial').exists())

    def test_tests_require_a_prepared_image_and_use_engine_entrypoint(self):
        with mock.patch.object(cache.subprocess, 'run', side_effect=self.engine):
            with self.assertRaisesRegex(RuntimeError, 'provisioned'):
                cache.run_tests(self.root, 'fixture-engine', ['tools/check-linux'])
        self.present = True
        with mock.patch.object(cache.subprocess, 'run') as run:
            run.return_value.returncode = 0
            cache.run_tests(self.root, 'fixture-engine', ['tools/check-linux'])
        args, kwargs = run.call_args
        self.assertEqual(args[0], [str(self.root / '.lair/tools/in-container'), 'tools/check-linux'])
        self.assertEqual(kwargs['env']['LAIR_ENGINE'], 'fixture-engine')
        self.assertTrue(kwargs['check'])

    def test_timing_records_failure_and_reraises_it(self):
        out = io.StringIO()
        def fail():
            raise subprocess.CalledProcessError(23, ['fixture'])
        with contextlib.redirect_stdout(out), self.assertRaises(subprocess.CalledProcessError):
            cache.timed('fixture-stage', fail)
        self.assertIn('ci-stage fixture-stage START utc=', out.getvalue())
        self.assertRegex(out.getvalue(), r'END utc=.*elapsed_seconds=.*status=23')

    def test_workflow_saves_exact_cache_before_tests_without_raising_timeout(self):
        workflow = (ROOT / '.github/workflows/ci.yml').read_text()
        linux = workflow.split('\n  linux:', 1)[1].split('\n  macos:', 1)[0]
        markers = ['actions/cache/restore@v4', 'tools/ci-container.py prepare',
                   'actions/cache/save@v4', 'tools/ci-container.py run -- tools/check-linux']
        offsets = [linux.index(marker) for marker in markers]
        self.assertEqual(offsets, sorted(offsets))
        self.assertIn("hashFiles('.lair/ci/Containerfile')", linux)
        self.assertIn('${{ runner.arch }}', linux)
        self.assertIn('cache-primary-key', linux)
        self.assertNotIn('restore-keys:', linux)
        self.assertIn('timeout-minutes: 40', linux)

    def test_performance_leg_reuses_the_same_exact_image_cache(self):
        workflow = (ROOT / '.github/workflows/ci.yml').read_text()
        linux = workflow.split('\n  linux:', 1)[1].split('\n  macos:', 1)[0]
        perf = workflow.split('\n  perf:', 1)[1].split('\n  tier:', 1)[0]
        key = next(line.strip() for line in linux.splitlines() if 'key: lair-container-v1-' in line)
        self.assertIn(key, perf)
        self.assertIn('actions/cache/restore@v4', perf)
        self.assertLess(perf.index('actions/cache/save@v4'),
                        perf.index('tools/ci-container.py run -- tools/check-perf'))
        self.assertIn('timeout-minutes: 20', perf)

    def run_staged_gate(self, fail_score=False, fail_memory=False):
        tools = self.root / 'tools'
        tools.mkdir()
        (tools / 'check-linux').write_text((ROOT / 'tools/check-linux').read_text())
        (tools / 'check-memory').write_text((ROOT / 'tools/check-memory').read_text())
        engine_tools = self.root / '.lair/tools'
        engine_tools.mkdir()
        for name in ('check-linux', 'goldens'):
            script = engine_tools / name
            script.write_text('#!/bin/sh\nexit 0\n')
            script.chmod(0o755)
        binaries = self.root / 'bin'
        binaries.mkdir()
        python = binaries / 'python3'
        python.write_text('#!/bin/sh\ncase "$*" in *tools/score-check*) exit "${FAIL_SCORE:-0}";; *tools/memory-probe.py*) exit "${FAIL_MEMORY:-0}";; esac\nexit 0\n')
        python.chmod(0o755)
        env = dict(os.environ, PATH=str(binaries) + os.pathsep + os.environ['PATH'],
                   FAIL_SCORE='23' if fail_score else '0',
                   FAIL_MEMORY='23' if fail_memory else '0')
        return subprocess.run(['sh', str(tools / 'check-linux')], env=env,
                              capture_output=True, text=True)

    def test_stage_markers_keep_every_gate(self):
        result = self.run_staged_gate()
        self.assertEqual(result.returncode, 0, result.stderr)
        names = ['python-tests', 'pty-fixtures', 'engine-check', 'native-goldens',
                 'score-check', 'native-gameplay', 'release-gameplay', 'memory-gate']
        offsets = []
        for name in names:
            offsets.extend([result.stdout.index('ci-stage ' + name + ' START'),
                            result.stdout.index('ci-stage ' + name + ' END')])
        self.assertEqual(offsets, sorted(offsets))
        self.assertEqual(result.stdout.count('status=0'), len(names))
        self.assertIn('cub check-linux: green', result.stdout)

    def test_memory_budget_failure_is_not_a_green_stage(self):
        result = self.run_staged_gate(fail_memory=True)
        self.assertEqual(result.returncode, 23)
        self.assertRegex(result.stdout, r'ci-stage memory-gate END .*status=23')
        self.assertNotIn('memory gate: green', result.stdout)
        self.assertNotIn('cub check-linux: green', result.stdout)

    def test_stage_failure_keeps_status_and_stops_before_later_gates(self):
        result = self.run_staged_gate(fail_score=True)
        self.assertEqual(result.returncode, 23)
        self.assertRegex(result.stdout, r'ci-stage score-check END .*status=23')
        self.assertNotIn('ci-stage native-gameplay', result.stdout)
        self.assertNotIn('cub check-linux: green', result.stdout)

