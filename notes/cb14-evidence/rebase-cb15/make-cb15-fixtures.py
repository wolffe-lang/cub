#!/usr/bin/env python3
"""cb14 (lane tooling, not committed): the CUB 6 save and the journey 5
recording a binary built at cub 60890a49 writes, for cb14's CUB 7 / journey
6 migration witnesses. Three real runs of that binary, nothing edited:

1. live in a pty with `--save <dir>/birch_7.save` (a new path: the name is
   the file's, played_ms the session's wall time), the opening skipped,
   then quit;
2. headless `--script tests/cases/pouch-inventory.pk --save` that file:
   the case's journey 5 checkpoint (pine, ice, tuft, two found lore lines)
   played two ticks, the save rewritten with the wrapper's name and time
   kept;
3. live in a pty again with `--record <dir>/journey5.pk`: the recording's
   initial journey 5 snapshot is the loaded save; quit (played_ms grows).

    python3 -I make-cb15-fixtures.py <trunk binary> <trunk worktree> <out dir>
"""
import fcntl
import os
import pathlib
import pty
import select
import struct
import subprocess
import sys
import termios
import time

binary, tree, out = sys.argv[1], pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
home = out / 'home'
home.mkdir(exist_ok=True)
env = {'HOME': str(home), 'TERM': 'xterm-256color', 'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8'}
save = out / 'birch_7.save'


def live(args, keys, name):
    master, slave = pty.openpty()
    fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack('HHHH', 24, 80, 0, 0))
    err = open(out / (name + '.err'), 'wb')
    p = subprocess.Popen([binary] + args, stdin=slave, stdout=slave, stderr=err, env=env,
                         start_new_session=True, close_fds=True)
    os.close(slave)
    captured = bytearray()

    def pump(seconds):
        end = time.time() + seconds
        while time.time() < end:
            ready, _, _ = select.select([master], [], [], 0.05)
            if ready:
                try:
                    chunk = os.read(master, 65536)
                except OSError:
                    return
                if not chunk:
                    return
                captured.extend(chunk)

    pump(1.5)
    for key, settle in keys:
        os.write(master, key)
        pump(settle)
    deadline = time.time() + 10
    while p.poll() is None and time.time() < deadline:
        pump(0.2)
    status = p.poll()
    if status is None:
        p.terminate()
        status = p.wait()
    os.close(master)
    err.close()
    (out / (name + '.out')).write_bytes(bytes(captured))
    print(name, 'exit', status, flush=True)
    return status


save.unlink(missing_ok=True)
s1 = live(['--no-title', '--mute', '--tier', 'plain', '--seed', '7', '--save', str(save)],
          [(b' ', 1.0), (b' ', 1.5), (b'q', 1.0)], 'stage1-live')
print('stage1', save.read_bytes().decode().splitlines()[0] if save.exists() else 'no save', flush=True)
h = subprocess.run([binary, '--headless', '--script', str(tree / 'tests/cases/pouch-inventory.pk'),
                    '--save', str(save), '--frames', '2', '--every', '2', '--dump', str(out / 'stage2')],
                   capture_output=True, text=True, env=env)
(out / 'stage2.err').write_text(h.stdout + h.stderr)
print('stage2-headless exit', h.returncode, flush=True)
(out / 'cb15-v6-stage2.save').write_bytes(save.read_bytes())
record = out / 'journey5.pk'
record.unlink(missing_ok=True)
s3 = live(['--no-title', '--mute', '--tier', 'plain', '--save', str(save), '--record', str(record)],
          [(b' ', 1.5), (b'q', 1.0)], 'stage3-live')
print('stage3 record', record.exists(), flush=True)
print('CB14_FIXTURES_DONE', s1, h.returncode, s3, flush=True)
