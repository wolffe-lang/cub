#!/usr/bin/env python3
"""cb17 scratch: a game's peak resident set over a short sound-on run.

    peak.py BIN WORKDIR

Runs BIN under /usr/bin/time -l in a pty (the game needs a terminal), music
on through the OSS stub (silent: the stub refuses, no player starts), 90
ticks, a fresh seed-7 journey; prints the maximum resident set size line and
the game's closing sound line.
"""
import os
import pty
import re
import select
import shutil
import sys


def main():
    binary, work = sys.argv[1], sys.argv[2]
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    cmd = ["/usr/bin/time", "-l", binary, "--no-title", "--seed", "7", "--save", work + "/save",
           "--ghost-dir", work + "/ghosts", "--sound-dir", work + "/sound", "--ticks", "90"]
    pid, fd = pty.fork()
    if pid == 0:
        os.environ.update(TERM="xterm-256color", COLUMNS="120", LINES="40", HOME=work,
                          CUB_SOUND_BACKEND="oss")
        os.execv(cmd[0], cmd)
    out = b""
    while True:
        r, _, _ = select.select([fd], [], [], 30)
        if not r:
            break
        try:
            data = os.read(fd, 65536)
        except OSError:
            break
        if not data:
            break
        out += data
    _, status = os.waitpid(pid, 0)
    os.close(fd)
    text = out.decode("utf-8", "replace")
    m = re.search(r"(\d+)\s+maximum resident set size", text)
    s = re.search(r"sound on[^\r\n]*", text)
    print("exit %d peak_rss_bytes %s %s" % (os.waitstatus_to_exitcode(status), m.group(1) if m else "?", s.group(0) if s else "?"))


if __name__ == "__main__":
    main()
