#!/usr/bin/env python3
"""Independent by-gap oracle for cub --hit-census.

INTO: each axis separating jaws from the nearest foe-cell centre points
strictly inward. AWAY: that displacement has a negative dot with aim.
ALONG: the remaining tangent/mixed aims. No shipping hit predicate is used.
The complete north-facing ring supplies the foe rectangle's position;
its size and every expected position/aim pair are checked independently.
"""
import argparse
import collections
import csv
from pathlib import Path
import subprocess

VECTORS = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
PIXELS = {4: (12, 24), 5: (10, 20), 6: (14, 28), 7: (12, 24), 8: (4, 12)}


def body(x, y, aim, old):
    face = ((aim + 1) // 2) % 4 * 2 if old else aim
    w, h = ((4, 4) if face % 4 == 0 else (8, 2)) if face % 2 == 0 else (8, 4)
    x0, y0 = x - (w - 1) // 2, y - (h - 1) // 2
    return (x0, y0, x0 + w - 1, y0 + h - 1), face


def gap(a, b):
    return max(b[0] - a[2], a[0] - b[2], b[1] - a[3], a[1] - b[3]) - 1


def direction(rect, face, foe, aim):
    x0, y0, x1, y1 = rect
    vx, vy = VECTORS[face]
    # Doubled cell-centre coordinates keep half-cell midpoints exact.
    jx = 2 * (x1 if vx > 0 else x0) + 1 if vx else x0 + x1 + 1
    jy = 2 * (y1 if vy > 0 else y0) + 1 if vy else y0 + y1 + 1
    dx = min(max(jx, 2 * foe[0] + 1), 2 * foe[2] + 1) - jx
    dy = min(max(jy, 2 * foe[1] + 1), 2 * foe[3] + 1) - jy
    ax, ay = VECTORS[aim]
    into = (dx == 0 or dx * ax > 0) and (dy == 0 or dy * ay > 0)
    return 'into' if into else 'away' if dx * ax + dy * ay < 0 else 'along'


def audit(rows, old=False, enforce=False):
    kinds = sorted({r['kind'] for r in rows})
    if enforce:
        assert kinds == list(PIXELS), ('incomplete foe census', kinds)
    bounds, expected = {}, set()
    for kind in kinds:
        for q in range(4):
            north = [r for r in rows if (r['kind'], r['foe_quarter'], r['aim']) == (kind, q, 0)]
            assert north, ('missing north ring', kind, q)
            fb = (min(r['x'] for r in north) + 5, min(r['y'] for r in north) + 5,
                  max(r['x'] for r in north) - 4, max(r['y'] for r in north) - 4)
            pw, ph = PIXELS[kind]
            if q % 2:
                pw, ph = ph, pw
            assert (fb[2] - fb[0] + 1, fb[3] - fb[1] + 1) == ((pw + 1) // 2, (ph + 3) // 4)
            bounds[kind, q] = fb
            for aim in range(8):
                cb, _ = body(0, 0, aim, old)
                for y in range(fb[1] - 3 - cb[3], fb[3] + 4 - cb[1]):
                    for x in range(fb[0] - 3 - cb[2], fb[2] + 4 - cb[0]):
                        if 0 <= gap(body(x, y, aim, old)[0], fb) <= 2:
                            expected.add((kind, q, x, y, aim))
    observed = {(r['kind'], r['foe_quarter'], r['x'], r['y'], r['aim']) for r in rows}
    assert len(observed) == len(rows), 'duplicate census pairs'
    assert expected == observed, ('incomplete ring', len(expected - observed), len(observed - expected))
    counts = collections.defaultdict(lambda: [0, 0])
    misses = []
    for r in rows:
        fb = bounds[r['kind'], r['foe_quarter']]
        cb, face = body(r['x'], r['y'], r['aim'], old)
        assert r['gap'] == gap(cb, fb), ('wrong reported gap', r)
        assert r['hit'] in (0, 1)
        category = direction(cb, face, fb, r['aim'])
        counts[r['kind'], r['gap'], category][0] += r['hit']
        counts[r['kind'], r['gap'], category][1] += 1
        if category == 'into' and r['gap'] <= 1 and not r['hit']:
            misses.append(r)
        if enforce:
            assert not (category == 'away' and r['hit']), ('rear strike landed', r)
            assert not (r['gap'] == 2 and r['hit']), ('bite exceeded reach', r)
    if enforce:
        assert not misses, ('inward gap0/1 bite refused', misses[:5])
    lines = ['kind gap direction hits pairs percent']
    for (kind, distance, category), (hits, total) in sorted(counts.items()):
        lines.append(f'{kind} {distance} {category} {hits} {total} {100 * hits / total:.1f}')
    lines.append(f'inward-gap01 misses {len(misses)}')
    return '\n'.join(lines) + '\n'


def read_rows(path):
    with open(path) as handle:
        return [{k: int(v) for k, v in row.items()} for row in csv.DictReader(handle)]


def check(binary, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    name = Path(binary).parent.name
    result = subprocess.run([str(binary), '--hit-census'], text=True, capture_output=True, check=True)
    path = out / (name + '-hit-census.csv')
    path.write_text(result.stdout)
    table = audit(read_rows(path), enforce=True)
    (out / (name + '-hit-breakdown.txt')).write_text(table)
    print(table, end='')
    print('gameplay: complete hit rings, inward gap0/1 100%, away/gap2 zero')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--bin')
    ap.add_argument('--out', default='target/hit-census')
    ap.add_argument('--csv')
    ap.add_argument('--before', action='store_true')
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    if args.bin:
        check(Path(args.bin).resolve(), args.out)
    else:
        assert args.csv, '--bin or --csv required'
        print(audit(read_rows(args.csv), old=args.before, enforce=args.check), end='')
