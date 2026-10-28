#!/usr/bin/env python3
"""Reuse cb08's bounded ordinary-key flank search against the new journey.
The witness predicate and candidate order are unchanged; only output paths
are namespaced to cb11. The source recipe is retained in cb08's evidence.
"""
from pathlib import Path
import re
import subprocess

root = Path(__file__).resolve().parents[2]
binary = root / 'target/release/cub'
case = root / 'tests/cases/boss-lynx-beaten.pk'
frames = re.search(r'# frames (\d+)', case.read_text())[1]
trace = root / 'target/cb11-lynx.trace'
p = subprocess.run([str(binary), '--headless', '--script', str(case),
                    '--frames', frames, '--every', frames, '--trace', '--dump',
                    str(root / 'target/cb11-lynx')], capture_output=True, text=True, check=True)
trace.write_text(p.stderr)
recipe = root / 'notes/cb08-evidence/scripts/find-final-flank.py'
source = recipe.read_text().replace("Path('/work')", f'Path({str(root)!r})').replace('target/cb08-', 'target/cb11-')
exec(compile(source, str(recipe), 'exec'), {'__name__': '__main__'})
