"""Retain startup-failure captures and obtain real predecessor-written saves."""
import errno
import importlib.machinery
import importlib.util
from pathlib import Path
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
loader = importlib.machinery.SourceFileLoader('save_probe_pty', str(ROOT / '.lair/tools/pty'))
spec = importlib.util.spec_from_loader('save_probe_pty', loader)
ctx = importlib.util.module_from_spec(spec)
loader.exec_module(ctx)
mode, binary, destination = sys.argv[1:]
destination = Path(destination)
destination.mkdir(parents=True, exist_ok=True)
if mode == 'startup':
    for name in ('quit', 'ctrl-c', 'trap'):
        argv = [binary, '--seed', '7'] + ctx.RUN_ARGS
        if name == 'trap':
            argv += ['--trap-at', ctx.TRAP_AT]
        session = ctx.Session(argv, 24, 80, ctx.env_for())
        error = None
        if name != 'trap':
            session.pump(.4)
            try:
                session.type(b'\x1b[B')
            except OSError as exc:
                error = exc.errno
        session.finish()
        (destination / (name + '.bin')).write_bytes(session.out)
        (destination / (name + '.err')).write_bytes(session.err)
        assert session.status == 2 and b'save_corrupt: target/pty/engine.save' in session.err
        assert not session.out
        if name != 'trap':
            assert error == errno.EIO, error
        print(name, 'status', session.status, 'write errno', error, session.err.decode().strip())
else:
    save = destination / ('trunk.save' if mode == 'trunk' else 'cb05.save')
    assert not save.exists(), 'preserve an existing writer fixture instead of overwriting it'
    env = ctx.env_for()
    env['HOME'] = str(destination)
    session = ctx.Session([binary, '--seed', '137', '--save', str(save), '--no-title',
                           '--mute', '--trace', '--ticks', '90'], 24, 80, env)
    deadline = time.monotonic() + 5
    while b'trace tick ' not in session.err and not session.eof and time.monotonic() < deadline:
        session.pump(.02)
    session.type(b'?', settle=.15)
    session.type(b'r', settle=.15)
    session.type(b'\x1b', settle=.15)
    session.type(b'q')
    session.finish()
    problems = []
    ctx.common_checks(session, 0, problems)
    assert not problems, problems
    assert re.search(rb'trace tick \d+ .* scene 0 ', session.err)
    text = save.read_text()
    assert 'seed 137 difficulty 0\n' in text and 'opening 1\n' in text
    assert len(next(line for line in text.splitlines() if line.startswith('slain ')).split()) == 8
    (destination / (mode + '-writer.bin')).write_bytes(session.out)
    (destination / (mode + '-writer.err')).write_bytes(session.err)
    print(mode, save, session.err.decode().splitlines()[-1])
    print(text)
