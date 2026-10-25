"""Flat-fill measurement over a headless frame (final.txt + final.sty).

A forest cell is a cell whose glyph is one of the forest glyphs (rich
braille canopy, the trunk; plain & % * ; |). A flat run is a maximal
horizontal run of forest cells identical in glyph, colours and attributes.
Prints: forest cells, the longest flat run, the share of forest cells
inside a run longer than FLAT_MAX (the "flat share") and its complement.
Usage: python3 -I flatness.py FRAME_DIR [FLAT_MAX]
"""
import sys
from pathlib import Path

FOREST = set('⣿⣶⣮⠶┃&%*;|')


def cells(frame):
    text = (frame / 'final.txt').read_text().split('\n')
    sty = (frame / 'final.sty').read_text().split('\n')
    rows = []
    for row, line in enumerate(text):
        if row >= len(sty) or not sty[row].strip():
            continue
        styles = []
        for run in sty[row].split():
            style, count = run.rsplit('*', 1)
            styles += [style] * int(count)
        rows.append([(ch, styles[i] if i < len(styles) else '') for i, ch in enumerate(line)])
    return rows


def measure(frame, flat_max):
    rows = cells(frame)
    forest = flat = longest = 0
    for row in rows[1:]:  # row 0 carries the HUD
        run = []
        for cell in row + [(None, None)]:
            if cell[0] in FOREST and run and cell == run[-1]:
                run.append(cell)
                continue
            if run:
                longest = max(longest, len(run))
                if len(run) > flat_max:
                    flat += len(run)
            run = [cell] if cell[0] in FOREST else []
        forest += sum(1 for c in row if c[0] in FOREST)
    return forest, longest, flat


if __name__ == '__main__':
    flat_max = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    frame = Path(sys.argv[1])
    forest, longest, flat = measure(frame, flat_max)
    share = 100.0 * flat / forest if forest else 0.0
    print(f'{frame.name}: forest {forest} longest_flat_run {longest} flat_share {share:.1f}% textured_share {100 - share:.1f}%')
