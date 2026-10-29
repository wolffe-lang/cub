#!/usr/bin/env python3
"""cb16 lane tooling: classify the golden directories that differ between
tests/goldens (committed) and target/goldens (this run): which files moved,
whether final.state moved, and the first differing state words.

    python3 -I golden-diff.py <cub checkout>
"""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
old = root / 'tests' / 'goldens'
new = root / 'target' / 'goldens'
rows = []
for d in sorted(p for p in new.iterdir() if p.is_dir()):
    o = old / d.name
    if not o.exists():
        rows.append((d.name, 'NEW', '', ''))
        continue
    names = sorted(set(p.name for p in d.iterdir()) | set(p.name for p in o.iterdir()))
    moved = [n for n in names if not (d / n).exists() or not (o / n).exists()
             or (d / n).read_bytes() != (o / n).read_bytes()]
    if not moved:
        continue
    state = 'final.state' in moved
    detail = ''
    if state and (d / 'final.state').exists() and (o / 'final.state').exists():
        a = (o / 'final.state').read_text().split('\n')[0].split()
        b = (d / 'final.state').read_text().split('\n')[0].split()
        diffs = [f'{a[i]} {a[i+1]}->{b[i+1]}' for i in range(0, min(len(a), len(b)) - 1, 2)
                 if a[i + 1] != b[i + 1]]
        detail = '; '.join(diffs[:8])
    rows.append((d.name, 'STATE' if state else 'frames', f'{len(moved)} files', detail))
for r in rows:
    print('\t'.join(r))
print('total', len(rows), 'state', sum(1 for r in rows if r[1] == 'STATE'))
