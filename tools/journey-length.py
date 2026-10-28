#!/usr/bin/env python3
"""The journey's length (cb14, the contract's item 4): from `cub --paths-audit`'s
CSV on standard input, per area at one seed and field, the cells of spine
(the route's rows plus its lateral travel, path 0), and the totals along the
way on; the dens and the bosses per area from the arguments' tables.

    cub --paths-audit | python3 -I tools/journey-length.py [--seed N] [--field F]

The same script reads cb05's binary and cb14's, so the before and after
tables in the note come from one instrument.
"""
import argparse
import csv
import sys

ap = argparse.ArgumentParser()
ap.add_argument('--seed', type=int, default=1)
ap.add_argument('--field', type=int, default=80)
args = ap.parse_args()

NAMES = {0: 'the Shingle', 1: 'Bramblehold', 2: 'Larkmeadow', 3: 'the Teeth', 4: 'the Shallows',
         5: 'the Hush (area 5)', 6: 'Cinderwick', 7: 'the Stand', 8: 'the Burn', 9: 'the Mere',
         10: 'the Underteeth', 11: 'the Howe', 12: 'Gravehollow'}
# Dens and bosses per area, before (cb05's seven) and after (cb14's thirteen).
DENS = {0: 1, 1: 2, 2: 2, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 0, 12: 0}
BOSSES_BEFORE = {1: 'Old Snag', 3: 'Whisper', 4: 'Alder', 5: 'Ashgrim'}
BOSSES_AFTER = {1: 'Old Snag', 3: 'Whisper', 4: 'Alder', 12: 'Ashgrim'}
LINE_BEFORE = [0, 6, 1, 2, 3, 4, 5]
LINE_AFTER = [0, 6, 1, 7, 2, 8, 3, 9, 4, 5, 11, 12]

rows = {}
for row in csv.DictReader(sys.stdin):
    r = {k: int(v) for k, v in row.items()}
    if r['seed'] != args.seed or r['field'] != args.field or r['path'] != 0:
        continue
    rows.setdefault(r['area'], []).append(r)
areas = sorted(rows)
after = max(areas) >= 7
line = LINE_AFTER if after else LINE_BEFORE
bosses = BOSSES_AFTER if after else BOSSES_BEFORE
print('journey-length seed %d field %d (%s)' % (args.seed, args.field, 'after' if after else 'before'))
print('area name rows lateral spine_cells dens boss')
total_rows = total_cells = total_dens = 0
for area in line:
    samples = sorted(rows.get(area, []), key=lambda r: r['at'])
    length = max(r['at'] for r in samples) if samples else 0
    lateral = sum(abs(r['delta']) for r in samples)
    cells = length + lateral
    dens = DENS[area] if after or area <= 6 else 0
    print('%d %s %d %d %d %d %s' % (area, NAMES[area].replace(' ', '_'), length, lateral, cells, dens, bosses.get(area, '-')))
    total_rows += length
    total_cells += cells
    total_dens += dens
branch = ''
if after and 10 in rows:
    samples = sorted(rows[10], key=lambda r: r['at'])
    branch = ' underteeth_off_the_line %d' % (max(r['at'] for r in samples) + sum(abs(r['delta']) for r in samples))
print('total rows %d spine_cells %d dens %d bosses %d%s' % (total_rows, total_cells, total_dens, len(bosses), branch))
