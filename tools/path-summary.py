#!/usr/bin/env python3
"""Summarize route samples, not generator promises. No graphics libraries."""
import collections
import csv
import sys

routes = collections.defaultdict(list)
widths = collections.defaultdict(collections.Counter)
with open(sys.argv[1]) as stream:
    for row in csv.DictReader(stream):
        r = {k: int(v) for k, v in row.items()}
        key = tuple(r[k] for k in ('seed', 'field', 'area', 'path'))
        routes[key].append(r)
        widths[r['area']][r['width']] += 1
scores = []
for key, points in routes.items():
    turns = 0
    last = 0
    last_at = -100
    for p in points:
        sign = (p['delta'] > 0) - (p['delta'] < 0)
        if sign:
            if last and sign != last and p['at'] - last_at <= 3:
                turns += 1
            last, last_at = sign, p['at']
    scores.append((turns * 10 / len(points), key, turns, len(points)))
for area in range(6):
    rows = [r for r in scores if r[1][2] == area]
    turns, samples = sum(r[2] for r in rows), sum(r[3] for r in rows)
    print(f'area {area}: reversals {turns}/{samples}; per10 {turns * 10 / samples:.6f}; widths {dict(sorted(widths[area].items()))}')
print('Three worst unique routes (field duplication excluded):')
seen = set()
for score, key, turns, count in sorted(scores, reverse=True):
    seed, field, area, path = key
    identity = seed, area, path
    if identity in seen:
        continue
    seen.add(identity)
    print(f'seed {seed} field {field} area {area} path {path}: {turns}/{count} = {score:.6f} per10')
    if len(seen) == 3:
        break
