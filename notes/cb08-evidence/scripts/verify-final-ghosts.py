#!/usr/bin/env python3
from pathlib import Path
import runpy
import sys

root = Path(sys.argv[1]).resolve()
gameplay = runpy.run_path(str(root / 'tools/gameplay.py'))
gameplay['OUT'].mkdir(parents=True, exist_ok=True)
for backend in ('native', 'release'):
    binary = root / 'target' / backend / 'cub'
    print('ghost verification backend ' + backend, flush=True)
    gameplay['ghosts'](binary)
print('ghost verification: both backends, both tiers green', flush=True)
