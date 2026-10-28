#!/usr/bin/env python3
"""Bounded real-loop resident-growth probe; terminal output is drained, not retained.

macOS ps reports KiB; Linux /proc reports pages (the pinned image needs no
procps package). Trace supplies actual simulation ticks;
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
import sys
import tempfile
import termios
import time


LINUX = sys.platform.startswith('linux')


def rss_bytes(pid):
    if LINUX:
        # The pinned image has no procps dependency; statm is pages, not KiB.
        fields = Path(f'/proc/{pid}/statm').read_text().split()
        return int(fields[1]) * os.sysconf('SC_PAGE_SIZE')
    result = subprocess.run(['ps', '-o', 'rss=', '-p', str(pid)],
                            capture_output=True, text=True, check=True)
    return int(result.stdout.strip()) * 1024


def evaluate(samples, budget=None, estimated=False):
    if len(samples) < 2:
        raise ValueError('missing samples')
    first, last = samples[0], samples[-1]
    ticks = last['tick'] - first['tick']
    if estimated:
        ticks = (last['seconds'] - first['seconds']) * 30
    growth = last['rss_bytes'] - first['rss_bytes']
    slope = growth / ticks if ticks > 0 else float('inf')
    red = ticks <= 0 or (budget is not None and slope > budget)
    return {'status': 'RED' if red else 'GREEN', 'start': first, 'end': last,
            'ticks': ticks, 'growth_bytes': growth, 'bytes_per_tick': slope,
            'tick_source': 'estimated-30Hz' if estimated else 'trace',
            'budget_bytes_per_tick': budget}


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
    if a.sample_seconds <= 0 or a.ceiling <= 0 or a.timeout <= 0:
        p.error('sample interval, ceiling and timeout must be positive')
    if a.budget is not None and (a.budget < 0 or a.no_trace):
        p.error('a budget requires exact ticks and a nonnegative value')
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
               '--sound-dir', str(work / 'sound'),
               '--ticks', str(a.ticks + int(a.sample_seconds * 30) + 60)]
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
        fall_tick = None
        skipped_fall = False
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
                            if re.search(rb' action 6 ', line):
                                if fall_tick is None:
                                    fall_tick = tick
                                if tick - fall_tick >= 50 and not skipped_fall:
                                    os.write(fd, b' ')
                                    skipped_fall = True
                            else:
                                fall_tick = None
                                skipped_fall = False
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
        result = evaluate(samples, a.budget, a.no_trace)
        print(json.dumps(result), flush=True)
        return int(result['status'] == 'RED')


if __name__ == '__main__':
    raise SystemExit(main())
