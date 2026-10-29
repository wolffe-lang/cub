#!/usr/bin/env python3
"""cb16 lane tooling: the pty runner's full row list (the engine's rows and
tests/pty_rows.py's ROWS, in the runner's own order) without sound-live and
mute-key, comma-joined for `--rows` (the-rules.md since planning 46518b2)."""
import importlib.util
import pathlib

root = pathlib.Path('/Users/mfwolffe/lanes/cb16/cub')
spec = importlib.util.spec_from_file_location('pty_rows', root / 'tests' / 'pty_rows.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
engine = ['quit', 'ctrl-c', 'trap', 'agree-rich', 'agree-plain']
rows = [r for r in engine + list(mod.ROWS) if r not in ('sound-live', 'mute-key')]
print(','.join(rows))
