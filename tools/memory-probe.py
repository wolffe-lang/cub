#!/usr/bin/env python3
"""Bounded real-loop resident-growth probe; terminal output is drained, not retained.

ps reports KiB on both supported hosts. Trace supplies actual simulation ticks;
its cost is deliberately included. All saves/ghosts are private disposable copies.
"""
import argparse
import errno
import fcntl
import json
import os
from pathlib import Path
import pty
import re
import select
import shutil
import signal
import struct
import subprocess
import tempfile
import termios
import time


def rss_bytes(pid):
    result = subprocess.run(['ps', '-o', 'rss=', '-p', str(pid)],
                            capture_output=True, text=True, check=True)
    return int(result.stdout.strip()) * 1024


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--bin', required=True)
    p.add_argument('--save')
    p.add_argument('--ghost-dir')
    p.add_argument('--work', required=True)
    p.add_argument('--seed', type=int, default=7)
    p.add_argument('--warmup', type=int, default=60)
    p.add_argument('--ticks', type=int, default=600)
    p.add_argument('--sample-seconds', type=float, default=1)
    p.add_argument('--budget', type=float)
    p.add_argument('--ceiling', type=int, default=805306368)
    p.add_argument('--timeout', type=float, default=120)
    p.add_argument('--no-trace', action='store_true')
    a = p.parse_args()
    if a.ticks <= a.warmup or a.warmup < 1:
        p.error('ticks must exceed positive warmup')
    root = Path(a.work).resolve()
    root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='memory-', dir=root) as td:
        work = Path(td)
        if a.save:
            shutil.copyfile(a.save, work / 'save')
        if a.ghost_dir:
            shutil.copytree(a.ghost_dir, work / 'ghosts')
        cmd = [str(Path(a.bin).resolve()), '--mute', '--no-title',
               '--save', str(work / 'save'), '--ghost-dir', str(work / 'ghosts'),
               '--sound-dir', str(work / 'sound'), '--ticks', str(a.ticks + 30)]
        if not a.save:
            cmd += ['--seed', str(a.seed)]
        if not a.no_trace:
            cmd += ['--trace']
        pid, fd = pty.fork()
        if pid == 0:
            os.environ.update(TERM='xterm-256color', COLUMNS='120', LINES='40',
                              HOME=str(work))
            fcntl.ioctl(0, termios.TIOCSWINSZ, struct.pack('HHHH', 40, 120, 0, 0))
            os.execv(cmd[0], cmd)
        start = time.monotonic()
        next_sample = 0
        tick = 0
        pending = b''
        samples = []
        failure = None
        try:
            while True:
                elapsed = time.monotonic() - start
                ready, _, _ = select.select([fd], [], [], 0.05)
                if ready:
                    try:
                        data = os.read(fd, 65536)
                    except OSError as e:
                        if e.errno != errno.EIO:
                            raise
                        data = b''
                    if not data:
                        failure = 'child exited before measurement end'
                        break
                    pending += data
                    lines = pending.split(b'\n')
                    pending = lines.pop()[-16384:]
                    for line in lines:
                        matches = re.findall(rb'trace tick (\d+) ', line)
                        if matches:
                            tick = int(matches[-1])
                if elapsed >= next_sample:
                    next_sample = elapsed + a.sample_seconds
                    resident = rss_bytes(pid)
                    row = {'seconds': round(elapsed, 3), 'tick': tick,
                           'rss_bytes': resident}
                    print(json.dumps(row), flush=True)
                    if resident > a.ceiling:
                        failure = 'resident ceiling exceeded'
                        break
                    if tick >= a.warmup or (a.no_trace and elapsed >= a.warmup / 30):
                        samples.append(row)
                    if tick >= a.ticks or (a.no_trace and elapsed >= a.ticks / 30):
                        break
                if elapsed > a.timeout:
                    failure = 'timeout'
                    break
        finally:
            # The native game ignored SIGTERM in the original reproduction.
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            os.waitpid(pid, 0)
            os.close(fd)
        if failure or len(samples) < 2:
            print(json.dumps({'status': 'RED', 'reason': failure or 'missing samples'}))
            return 1
        first, last = samples[0], samples[-1]
        dt = last['tick'] - first['tick']
        if a.no_trace:
            dt = (last['seconds'] - first['seconds']) * 30
        growth = last['rss_bytes'] - first['rss_bytes']
        slope = growth / dt if dt > 0 else float('inf')
        red = dt <= 0 or (a.budget is not None and slope > a.budget)
        print(json.dumps({'status': 'RED' if red else 'GREEN',
                          'start': first, 'end': last, 'ticks': dt,
                          'growth_bytes': growth, 'bytes_per_tick': slope,
                          'tick_source': 'estimated-30Hz' if a.no_trace else 'trace',
                          'budget_bytes_per_tick': a.budget}), flush=True)
        return int(red)


if __name__ == '__main__':
    raise SystemExit(main())
