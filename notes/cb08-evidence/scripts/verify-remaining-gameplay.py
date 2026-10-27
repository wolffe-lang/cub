#!/usr/bin/env python3
from pathlib import Path
import runpy
import sys

root = Path(sys.argv[1]).resolve()
gameplay = runpy.run_path(str(root / 'tools/gameplay.py'))
gameplay['OUT'].mkdir(parents=True, exist_ok=True)
for backend in ('native', 'release'):
    binary = root / 'target' / backend / 'cub'
    for name in ('ghosts', 'fairness', 'den_progression', 'paths_doors_rest', 'feel', 'level_look'):
        print('remaining gate ' + backend + ' ' + name, flush=True)
        gameplay[name](binary)
    world = runpy.run_path(str(root / 'tools/world_checks.py'))
    world['check'](binary)
gameplay['readable'](gameplay['OUT'])
print('remaining gameplay: both backends green', flush=True)
