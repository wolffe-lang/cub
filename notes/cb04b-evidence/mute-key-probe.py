"""Controlled real-pty timing reproduction and fixed-row checks; no game mutation."""
import importlib.machinery
import importlib.util
from pathlib import Path
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[2]

def load(name, path):
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module

ctx = load('mute_pty', ROOT / '.lair/tools/pty')
rows = load('mute_rows', ROOT / 'tests/pty_rows.py')
binary, mode = sys.argv[1:]
if mode == 'suite':
    import subprocess
    for case in ('startup', 'fixed', 'delay', 'drop-second'):
        subprocess.run([sys.executable, __file__, binary, case], check=True)
    raise SystemExit(0)
dest = ROOT / 'target/pty' / ('cb04b-mute-' + mode)
dest.mkdir(parents=True, exist_ok=True)
ctx.ROOT = str(dest)
if mode == 'startup':
    record = dest / 'record.pk'
    env = ctx.env_for()
    env['HOME'] = str(dest)
    session = ctx.Session([binary, '--seed', '7', '--save', str(dest / 'save'),
                           '--record', str(record), '--sound-dir', str(dest / 'wavs'),
                           '--tier', 'plain', '--trace', '--ticks', '180'], 24, 80, env,
                          replies=[(b'\x1b[?u', b'm')])
    deadline = time.monotonic() + 10
    while not rows.trace_states(session) and not session.eof and time.monotonic() < deadline:
        session.pump(.02)
    session.pump(.6)
    session.type(b'm', settle=.6)
    session.type(b'q')
    session.finish()
    problems = []
    ctx.common_checks(session, 0, problems)
    ticks = [int(t) for t in re.findall(r'^t (\d+) mute$', record.read_text(), re.M)]
    if len(ticks) != 2 or ticks[0] != 0 or ticks[1] <= 0:
        problems.append('controlled startup did not record two m keys, first at tick zero')
    if b'starts 1 ' not in session.err or b'stops 2 ' not in session.err:
        problems.append('startup prediction starts1/stops2 did not hold')
    print('controlled query-time first m; mute ticks', ticks)
else:
    if mode == 'delay':
        wrapper = dest / 'delayed-game'
        wrapper.write_text('#!' + sys.executable + '\nimport os, sys, time\ntime.sleep(2)\nos.execv(' + repr(binary) + ', [' + repr(binary) + '] + sys.argv[1:])\n')
        wrapper.chmod(0o755)
        binary = str(wrapper)
    if mode == 'drop-second':
        original = ctx.Session
        class DropSecond(original):
            count = 0
            def type(self, data, settle=.08):
                if data == b'm':
                    self.count += 1
                    if self.count == 2:
                        self.pump(settle)
                        return
                super().type(data, settle)
        ctx.Session = DropSecond
    session, problems = rows.mute_key(binary, ctx)
    if mode == 'drop-second':
        print('negative driver: second key omitted, NOT a score.restart code mutation')
        print('expected row failures', problems)
        assert len(problems) == 2, problems
        assert any('second m did not cue' in p for p in problems), problems
        assert any('two ordered mute keys' in p for p in problems), problems
        assert b'starts 1 ' in session.err
        problems = []
(dest / 'capture.bin').write_bytes(session.out)
(dest / 'stderr.txt').write_bytes(session.err)
print(session.err.decode().splitlines()[-1])
print('problems', problems)
assert not problems, problems
