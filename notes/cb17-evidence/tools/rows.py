#!/usr/bin/env python3
"""cb17: the pty rows the Mac gauntlet runs, comma-joined: the engine's five
and every game row except the two that start afplay on macOS (sound-live,
mute-key), because no audio is played aloud on the Mac (the orchestrator's
rule, cb17's contract); Linux and CI run them all (paplay is missing there,
so they are silent).

    rows.py GAME_ROOT
"""
import importlib.machinery
import importlib.util
import os
import sys

ENGINE_ROWS = ["quit", "ctrl-c", "trap", "agree-rich", "agree-plain"]
AUDIBLE = {"sound-live", "mute-key"}


def main():
    path = os.path.join(sys.argv[1], "tests", "pty_rows.py")
    loader = importlib.machinery.SourceFileLoader("pty_rows", path)
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader("pty_rows", loader))
    loader.exec_module(mod)
    rows = ENGINE_ROWS + [r for r in mod.ROWS if r not in AUDIBLE]
    print(",".join(rows))


if __name__ == "__main__":
    main()
