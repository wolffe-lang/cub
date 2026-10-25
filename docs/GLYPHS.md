# The rich tier's glyphs

Every code point cub's rich tier can draw, each once. This list is the specification for PAX's console font
row for cub (the cub track's M-CB5, with pack's pk04): once PAX's font draws each of these at one cell, PAX
runs the rich tier unchanged. The plain tier uses nothing above U+00FF, so it needs no row.

The list is held to the code by a test: `src/glyphs_test.lu` reads this file and compares the `U+` entries
with `sprites.rich_code_points()`, both ways. Add a glyph to `src/sprites/sprites.lu` and this table must
gain it in the same commit.

## How a width is measured

A photo is not evidence. `cub --probe-glyphs` (the engine's probe) writes each glyph on an empty line and
asks the terminal where the cursor landed (`CSI 6 n`); the column it answers, less one, is the cells the
glyph took on that terminal. Run it in the terminal you want to know about and paste the table into the
matching column below with the date. A pseudo-terminal has no font, so the pty runner cannot measure this.

| | Terminal.app | iTerm2 | Linux VT (kasumi's kernel) | PAX's console |
|---|---|---|---|---|
| measured | owed: run `cub --probe-glyphs` here and record the date | owed, the same way | owed | draws `?` for every code point at or above U+0100 today; the font row |

## The glyphs

Unicode's East Asian Width is `N` (neutral) for every entry, so a conforming terminal gives each one cell;
that is the expectation the columns above measure against. Thirteen of the sixteen are pack's (its
`docs/GLYPHS.md`); the three cub adds are the Ashwater's `≈`, the reeds' `⠇` and the cub's fourth ear
quadrant `▖`.

| code point | glyph | name | block | UTF-8 | used for |
|---|---|---|---|---|---|
| U+00B7 | · | MIDDLE DOT | Latin-1 Supplement | C2 B7 | a gravel mark |
| U+2024 | ․ | ONE DOT LEADER | General Punctuation | E2 80 A4 | a gravel mark |
| U+2248 | ≈ | ALMOST EQUAL TO | Mathematical Operators | E2 89 88 | a ripple on the Ashwater |
| U+2503 | ┃ | BOX DRAWINGS HEAVY VERTICAL | Box Drawing | E2 94 83 | a trunk |
| U+2588 | █ | FULL BLOCK | Block Elements | E2 96 88 | the cub's body |
| U+2591 | ░ | LIGHT SHADE | Block Elements | E2 96 91 | a gravel mark |
| U+2596 | ▖ | QUADRANT LOWER LEFT | Block Elements | E2 96 96 | an ear (facing south or west) |
| U+2597 | ▗ | QUADRANT LOWER RIGHT | Block Elements | E2 96 97 | an ear (facing south or east) |
| U+2598 | ▘ | QUADRANT UPPER LEFT | Block Elements | E2 96 98 | an ear (facing north or west) |
| U+259D | ▝ | QUADRANT UPPER RIGHT | Block Elements | E2 96 9D | an ear (facing north or east) |
| U+2807 | ⠇ | BRAILLE PATTERN DOTS-123 | Braille Patterns | E2 A0 87 | reeds |
| U+2816 | ⠖ | BRAILLE PATTERN DOTS-235 | Braille Patterns | E2 A0 96 | grass, reeds |
| U+2836 | ⠶ | BRAILLE PATTERN DOTS-2356 | Braille Patterns | E2 A0 B6 | grass, thin canopy |
| U+28EE | ⣮ | BRAILLE PATTERN DOTS-234678 | Braille Patterns | E2 A3 AE | canopy |
| U+28F6 | ⣶ | BRAILLE PATTERN DOTS-2345678 | Braille Patterns | E2 A3 B6 | canopy |
| U+28FF | ⣿ | BRAILLE PATTERN DOTS-12345678 | Braille Patterns | E2 A3 BF | dense canopy |

Sixteen code points in six blocks. The cub's four ears are the four quadrant blocks, so a facing is read
from which two are lit; the body is the full block; the ground is pack's forest and the Shingle's marks.
