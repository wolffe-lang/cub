#!/usr/bin/env python3
"""cb02c: bring docs/GLYPHS.md's table to the code points `cub --measure`
prints on its `glyphs` line (sprites.rich_code_points()). New braille rows
take the existing silhouette rows' wording; a row whose code point the tier
no longer draws is removed. Usage: glyphs-rows.py GLYPHS.md MEASURE.txt"""
import sys
import unicodedata

doc, measure = sys.argv[1], sys.argv[2]
want = None
for line in open(measure, encoding='utf-8'):
    if line.startswith('glyphs '):
        words = line.split()
        want = [int(w, 16) for w in words[2:]]
        assert len(want) == int(words[1])
assert want, 'no glyphs line'
lines = open(doc, encoding='utf-8').read().split('\n')
rows = {}
first = last = None
for i, line in enumerate(lines):
    if line.startswith('| U+'):
        cp = int(line[4:line.index(' ', 4)], 16)
        rows[cp] = line
        first = i if first is None else first
        last = i
for cp in want:
    if cp not in rows:
        assert 0x2800 <= cp <= 0x28FF, hex(cp)
        ch = chr(cp)
        name = unicodedata.name(ch)
        utf8 = ' '.join('%02X' % b for b in ch.encode('utf-8'))
        rows[cp] = f'| U+{cp:04X} | {ch} | {name} | Braille Patterns | {utf8} | a silhouette cell (braille of its lit pixels) |'
        print('added', f'U+{cp:04X}')
for cp in sorted(rows):
    if cp not in want:
        print('removed', f'U+{cp:04X}')
table = [rows[cp] for cp in want]
lines[first:last + 1] = table
open(doc, 'w', encoding='utf-8').write('\n'.join(lines))
print(len(table), 'rows')
