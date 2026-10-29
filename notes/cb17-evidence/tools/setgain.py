#!/usr/bin/env python3
"""cb17 scratch: set `gain` on a part file's `part` lines.

    setgain.py FILE NAME=DB [NAME=DB ...]
"""
import re
import sys


def main():
    path = sys.argv[1]
    want = dict(a.split("=") for a in sys.argv[2:])
    out = []
    for line in open(path, encoding="utf-8").read().split("\n"):
        w = line.split()
        if len(w) >= 3 and w[0] == "part" and w[1] in want:
            line = re.sub(r" gain -?\d+", "", line)
            g = int(want.pop(w[1]))
            if g != 0:
                line = line + " gain %d" % g
        out.append(line)
    if want:
        raise SystemExit("no part line for %s" % sorted(want))
    open(path, "w", encoding="utf-8").write("\n".join(out))


if __name__ == "__main__":
    main()
