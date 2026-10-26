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
that is the expectation the columns above measure against. The ground's glyphs are pack's (its
`docs/GLYPHS.md`) with the Ashwater's `≈` and the reeds' `⠇`; the creatures and the bundle are cub's pixel
silhouettes (`src/silhouette/silhouette.lu`, cb02b): every cell of a silhouette is the full block where all
eight of its pixels are lit, a half block where exactly one half is, and otherwise the braille pattern of
its lit pixels, so the braille rows below are the set every drawing produces in each of its four facings,
not a hand-picked few. The list is generated from `sprites.rich_code_points()` (the test holds it).

| code point | glyph | name | block | UTF-8 | used for |
|---|---|---|---|---|---|
| U+00B7 | · | MIDDLE DOT | Latin-1 Supplement | C2 B7 | a gravel mark |
| U+2024 | ․ | ONE DOT LEADER | General Punctuation | E2 80 A4 | a gravel mark |
| U+2248 | ≈ | ALMOST EQUAL TO | Mathematical Operators | E2 89 88 | a ripple on the Ashwater |
| U+2503 | ┃ | BOX DRAWINGS HEAVY VERTICAL | Box Drawing | E2 94 83 | a trunk |
| U+2580 | ▀ | UPPER HALF BLOCK | Block Elements | E2 96 80 | a silhouette cell lit above |
| U+2584 | ▄ | LOWER HALF BLOCK | Block Elements | E2 96 84 | a silhouette cell lit below |
| U+2588 | █ | FULL BLOCK | Block Elements | E2 96 88 | a silhouette cell lit through; a jetty face |
| U+258C | ▌ | LEFT HALF BLOCK | Block Elements | E2 96 8C | a silhouette cell lit on the left |
| U+2590 | ▐ | RIGHT HALF BLOCK | Block Elements | E2 96 90 | a silhouette cell lit on the right |
| U+2591 | ░ | LIGHT SHADE | Block Elements | E2 96 91 | a gravel mark, a jetty face, a log grain |
| U+2801 | ⠁ | BRAILLE PATTERN DOTS-1 | Braille Patterns | E2 A0 81 | a silhouette cell (braille of its lit pixels) |
| U+2802 | ⠂ | BRAILLE PATTERN DOTS-2 | Braille Patterns | E2 A0 82 | a silhouette cell (braille of its lit pixels) |
| U+2803 | ⠃ | BRAILLE PATTERN DOTS-12 | Braille Patterns | E2 A0 83 | a silhouette cell (braille of its lit pixels) |
| U+2804 | ⠄ | BRAILLE PATTERN DOTS-3 | Braille Patterns | E2 A0 84 | a silhouette cell (braille of its lit pixels) |
| U+2806 | ⠆ | BRAILLE PATTERN DOTS-23 | Braille Patterns | E2 A0 86 | a silhouette cell (braille of its lit pixels) |
| U+2807 | ⠇ | BRAILLE PATTERN DOTS-123 | Braille Patterns | E2 A0 87 | reeds |
| U+2808 | ⠈ | BRAILLE PATTERN DOTS-4 | Braille Patterns | E2 A0 88 | a silhouette cell (braille of its lit pixels) |
| U+2809 | ⠉ | BRAILLE PATTERN DOTS-14 | Braille Patterns | E2 A0 89 | a silhouette cell (braille of its lit pixels) |
| U+280A | ⠊ | BRAILLE PATTERN DOTS-24 | Braille Patterns | E2 A0 8A | a silhouette cell (braille of its lit pixels) |
| U+280B | ⠋ | BRAILLE PATTERN DOTS-124 | Braille Patterns | E2 A0 8B | a silhouette cell (braille of its lit pixels) |
| U+280F | ⠏ | BRAILLE PATTERN DOTS-1234 | Braille Patterns | E2 A0 8F | a silhouette cell (braille of its lit pixels) |
| U+2810 | ⠐ | BRAILLE PATTERN DOTS-5 | Braille Patterns | E2 A0 90 | a silhouette cell (braille of its lit pixels) |
| U+2811 | ⠑ | BRAILLE PATTERN DOTS-15 | Braille Patterns | E2 A0 91 | a silhouette cell (braille of its lit pixels) |
| U+2812 | ⠒ | BRAILLE PATTERN DOTS-25 | Braille Patterns | E2 A0 92 | a silhouette cell (braille of its lit pixels) |
| U+2813 | ⠓ | BRAILLE PATTERN DOTS-125 | Braille Patterns | E2 A0 93 | a silhouette cell (braille of its lit pixels) |
| U+2814 | ⠔ | BRAILLE PATTERN DOTS-35 | Braille Patterns | E2 A0 94 | a silhouette cell (braille of its lit pixels) |
| U+2815 | ⠕ | BRAILLE PATTERN DOTS-135 | Braille Patterns | E2 A0 95 | a silhouette cell (braille of its lit pixels) |
| U+2816 | ⠖ | BRAILLE PATTERN DOTS-235 | Braille Patterns | E2 A0 96 | grass, reeds |
| U+2818 | ⠘ | BRAILLE PATTERN DOTS-45 | Braille Patterns | E2 A0 98 | a silhouette cell (braille of its lit pixels) |
| U+2819 | ⠙ | BRAILLE PATTERN DOTS-145 | Braille Patterns | E2 A0 99 | a silhouette cell (braille of its lit pixels) |
| U+281A | ⠚ | BRAILLE PATTERN DOTS-245 | Braille Patterns | E2 A0 9A | a silhouette cell (braille of its lit pixels) |
| U+281C | ⠜ | BRAILLE PATTERN DOTS-345 | Braille Patterns | E2 A0 9C | a silhouette cell (braille of its lit pixels) |
| U+281E | ⠞ | BRAILLE PATTERN DOTS-2345 | Braille Patterns | E2 A0 9E | a silhouette cell (braille of its lit pixels) |
| U+281F | ⠟ | BRAILLE PATTERN DOTS-12345 | Braille Patterns | E2 A0 9F | a silhouette cell (braille of its lit pixels) |
| U+2820 | ⠠ | BRAILLE PATTERN DOTS-6 | Braille Patterns | E2 A0 A0 | a silhouette cell (braille of its lit pixels) |
| U+2822 | ⠢ | BRAILLE PATTERN DOTS-26 | Braille Patterns | E2 A0 A2 | a silhouette cell (braille of its lit pixels) |
| U+2823 | ⠣ | BRAILLE PATTERN DOTS-126 | Braille Patterns | E2 A0 A3 | a silhouette cell (braille of its lit pixels) |
| U+2824 | ⠤ | BRAILLE PATTERN DOTS-36 | Braille Patterns | E2 A0 A4 | a silhouette cell (braille of its lit pixels) |
| U+2827 | ⠧ | BRAILLE PATTERN DOTS-1236 | Braille Patterns | E2 A0 A7 | a silhouette cell (braille of its lit pixels) |
| U+282A | ⠪ | BRAILLE PATTERN DOTS-246 | Braille Patterns | E2 A0 AA | a silhouette cell (braille of its lit pixels) |
| U+282B | ⠫ | BRAILLE PATTERN DOTS-1246 | Braille Patterns | E2 A0 AB | a silhouette cell (braille of its lit pixels) |
| U+282E | ⠮ | BRAILLE PATTERN DOTS-2346 | Braille Patterns | E2 A0 AE | a silhouette cell (braille of its lit pixels) |
| U+2830 | ⠰ | BRAILLE PATTERN DOTS-56 | Braille Patterns | E2 A0 B0 | a silhouette cell (braille of its lit pixels) |
| U+2833 | ⠳ | BRAILLE PATTERN DOTS-1256 | Braille Patterns | E2 A0 B3 | a silhouette cell (braille of its lit pixels) |
| U+2835 | ⠵ | BRAILLE PATTERN DOTS-1356 | Braille Patterns | E2 A0 B5 | a silhouette cell (braille of its lit pixels) |
| U+2836 | ⠶ | BRAILLE PATTERN DOTS-2356 | Braille Patterns | E2 A0 B6 | grass, thin canopy, deep forest |
| U+2837 | ⠷ | BRAILLE PATTERN DOTS-12356 | Braille Patterns | E2 A0 B7 | a silhouette cell (braille of its lit pixels) |
| U+2838 | ⠸ | BRAILLE PATTERN DOTS-456 | Braille Patterns | E2 A0 B8 | a silhouette cell (braille of its lit pixels) |
| U+2839 | ⠹ | BRAILLE PATTERN DOTS-1456 | Braille Patterns | E2 A0 B9 | a silhouette cell (braille of its lit pixels) |
| U+283B | ⠻ | BRAILLE PATTERN DOTS-12456 | Braille Patterns | E2 A0 BB | a silhouette cell (braille of its lit pixels) |
| U+283C | ⠼ | BRAILLE PATTERN DOTS-3456 | Braille Patterns | E2 A0 BC | a silhouette cell (braille of its lit pixels) |
| U+283E | ⠾ | BRAILLE PATTERN DOTS-23456 | Braille Patterns | E2 A0 BE | a silhouette cell (braille of its lit pixels) |
| U+283F | ⠿ | BRAILLE PATTERN DOTS-123456 | Braille Patterns | E2 A0 BF | a silhouette cell (braille of its lit pixels) |
| U+2840 | ⡀ | BRAILLE PATTERN DOTS-7 | Braille Patterns | E2 A1 80 | a silhouette cell (braille of its lit pixels) |
| U+2841 | ⡁ | BRAILLE PATTERN DOTS-17 | Braille Patterns | E2 A1 81 | a silhouette cell (braille of its lit pixels) |
| U+2843 | ⡃ | BRAILLE PATTERN DOTS-127 | Braille Patterns | E2 A1 83 | a silhouette cell (braille of its lit pixels) |
| U+2844 | ⡄ | BRAILLE PATTERN DOTS-37 | Braille Patterns | E2 A1 84 | a silhouette cell (braille of its lit pixels) |
| U+2845 | ⡅ | BRAILLE PATTERN DOTS-137 | Braille Patterns | E2 A1 85 | a silhouette cell (braille of its lit pixels) |
| U+2846 | ⡆ | BRAILLE PATTERN DOTS-237 | Braille Patterns | E2 A1 86 | a silhouette cell (braille of its lit pixels) |
| U+284B | ⡋ | BRAILLE PATTERN DOTS-1247 | Braille Patterns | E2 A1 8B | a silhouette cell (braille of its lit pixels) |
| U+284C | ⡌ | BRAILLE PATTERN DOTS-347 | Braille Patterns | E2 A1 8C | a silhouette cell (braille of its lit pixels) |
| U+284E | ⡎ | BRAILLE PATTERN DOTS-2347 | Braille Patterns | E2 A1 8E | a silhouette cell (braille of its lit pixels) |
| U+284F | ⡏ | BRAILLE PATTERN DOTS-12347 | Braille Patterns | E2 A1 8F | a silhouette cell (braille of its lit pixels) |
| U+2853 | ⡓ | BRAILLE PATTERN DOTS-1257 | Braille Patterns | E2 A1 93 | a silhouette cell (braille of its lit pixels) |
| U+2854 | ⡔ | BRAILLE PATTERN DOTS-357 | Braille Patterns | E2 A1 94 | a silhouette cell (braille of its lit pixels) |
| U+2855 | ⡕ | BRAILLE PATTERN DOTS-1357 | Braille Patterns | E2 A1 95 | a silhouette cell (braille of its lit pixels) |
| U+2856 | ⡖ | BRAILLE PATTERN DOTS-2357 | Braille Patterns | E2 A1 96 | a silhouette cell (braille of its lit pixels) |
| U+2857 | ⡗ | BRAILLE PATTERN DOTS-12357 | Braille Patterns | E2 A1 97 | a silhouette cell (braille of its lit pixels) |
| U+2858 | ⡘ | BRAILLE PATTERN DOTS-457 | Braille Patterns | E2 A1 98 | a silhouette cell (braille of its lit pixels) |
| U+2859 | ⡙ | BRAILLE PATTERN DOTS-1457 | Braille Patterns | E2 A1 99 | a silhouette cell (braille of its lit pixels) |
| U+285A | ⡚ | BRAILLE PATTERN DOTS-2457 | Braille Patterns | E2 A1 9A | a silhouette cell (braille of its lit pixels) |
| U+285B | ⡛ | BRAILLE PATTERN DOTS-12457 | Braille Patterns | E2 A1 9B | a silhouette cell (braille of its lit pixels) |
| U+285C | ⡜ | BRAILLE PATTERN DOTS-3457 | Braille Patterns | E2 A1 9C | a silhouette cell (braille of its lit pixels) |
| U+285F | ⡟ | BRAILLE PATTERN DOTS-123457 | Braille Patterns | E2 A1 9F | a silhouette cell (braille of its lit pixels) |
| U+2860 | ⡠ | BRAILLE PATTERN DOTS-67 | Braille Patterns | E2 A1 A0 | a silhouette cell (braille of its lit pixels) |
| U+2862 | ⡢ | BRAILLE PATTERN DOTS-267 | Braille Patterns | E2 A1 A2 | a silhouette cell (braille of its lit pixels) |
| U+2863 | ⡣ | BRAILLE PATTERN DOTS-1267 | Braille Patterns | E2 A1 A3 | a silhouette cell (braille of its lit pixels) |
| U+2864 | ⡤ | BRAILLE PATTERN DOTS-367 | Braille Patterns | E2 A1 A4 | a silhouette cell (braille of its lit pixels) |
| U+2865 | ⡥ | BRAILLE PATTERN DOTS-1367 | Braille Patterns | E2 A1 A5 | a silhouette cell (braille of its lit pixels) |
| U+2867 | ⡧ | BRAILLE PATTERN DOTS-12367 | Braille Patterns | E2 A1 A7 | a silhouette cell (braille of its lit pixels) |
| U+286A | ⡪ | BRAILLE PATTERN DOTS-2467 | Braille Patterns | E2 A1 AA | a silhouette cell (braille of its lit pixels) |
| U+286B | ⡫ | BRAILLE PATTERN DOTS-12467 | Braille Patterns | E2 A1 AB | a silhouette cell (braille of its lit pixels) |
| U+286C | ⡬ | BRAILLE PATTERN DOTS-3467 | Braille Patterns | E2 A1 AC | a silhouette cell (braille of its lit pixels) |
| U+286D | ⡭ | BRAILLE PATTERN DOTS-13467 | Braille Patterns | E2 A1 AD | a silhouette cell (braille of its lit pixels) |
| U+2871 | ⡱ | BRAILLE PATTERN DOTS-1567 | Braille Patterns | E2 A1 B1 | a silhouette cell (braille of its lit pixels) |
| U+2872 | ⡲ | BRAILLE PATTERN DOTS-2567 | Braille Patterns | E2 A1 B2 | a silhouette cell (braille of its lit pixels) |
| U+2873 | ⡳ | BRAILLE PATTERN DOTS-12567 | Braille Patterns | E2 A1 B3 | a silhouette cell (braille of its lit pixels) |
| U+2874 | ⡴ | BRAILLE PATTERN DOTS-3567 | Braille Patterns | E2 A1 B4 | a silhouette cell (braille of its lit pixels) |
| U+2875 | ⡵ | BRAILLE PATTERN DOTS-13567 | Braille Patterns | E2 A1 B5 | a silhouette cell (braille of its lit pixels) |
| U+2876 | ⡶ | BRAILLE PATTERN DOTS-23567 | Braille Patterns | E2 A1 B6 | a silhouette cell (braille of its lit pixels) |
| U+2877 | ⡷ | BRAILLE PATTERN DOTS-123567 | Braille Patterns | E2 A1 B7 | a silhouette cell (braille of its lit pixels) |
| U+2878 | ⡸ | BRAILLE PATTERN DOTS-4567 | Braille Patterns | E2 A1 B8 | a silhouette cell (braille of its lit pixels) |
| U+287B | ⡻ | BRAILLE PATTERN DOTS-124567 | Braille Patterns | E2 A1 BB | a silhouette cell (braille of its lit pixels) |
| U+287D | ⡽ | BRAILLE PATTERN DOTS-134567 | Braille Patterns | E2 A1 BD | a silhouette cell (braille of its lit pixels) |
| U+287E | ⡾ | BRAILLE PATTERN DOTS-234567 | Braille Patterns | E2 A1 BE | a silhouette cell (braille of its lit pixels) |
| U+287F | ⡿ | BRAILLE PATTERN DOTS-1234567 | Braille Patterns | E2 A1 BF | a silhouette cell (braille of its lit pixels) |
| U+2880 | ⢀ | BRAILLE PATTERN DOTS-8 | Braille Patterns | E2 A2 80 | a silhouette cell (braille of its lit pixels) |
| U+2883 | ⢃ | BRAILLE PATTERN DOTS-128 | Braille Patterns | E2 A2 83 | a silhouette cell (braille of its lit pixels) |
| U+2884 | ⢄ | BRAILLE PATTERN DOTS-38 | Braille Patterns | E2 A2 84 | a silhouette cell (braille of its lit pixels) |
| U+2887 | ⢇ | BRAILLE PATTERN DOTS-1238 | Braille Patterns | E2 A2 87 | a silhouette cell (braille of its lit pixels) |
| U+2888 | ⢈ | BRAILLE PATTERN DOTS-48 | Braille Patterns | E2 A2 88 | a silhouette cell (braille of its lit pixels) |
| U+288B | ⢋ | BRAILLE PATTERN DOTS-1248 | Braille Patterns | E2 A2 8B | a silhouette cell (braille of its lit pixels) |
| U+288E | ⢎ | BRAILLE PATTERN DOTS-2348 | Braille Patterns | E2 A2 8E | a silhouette cell (braille of its lit pixels) |
| U+2893 | ⢓ | BRAILLE PATTERN DOTS-1258 | Braille Patterns | E2 A2 93 | a silhouette cell (braille of its lit pixels) |
| U+2894 | ⢔ | BRAILLE PATTERN DOTS-358 | Braille Patterns | E2 A2 94 | a silhouette cell (braille of its lit pixels) |
| U+2895 | ⢕ | BRAILLE PATTERN DOTS-1358 | Braille Patterns | E2 A2 95 | a silhouette cell (braille of its lit pixels) |
| U+2896 | ⢖ | BRAILLE PATTERN DOTS-2358 | Braille Patterns | E2 A2 96 | a silhouette cell (braille of its lit pixels) |
| U+2898 | ⢘ | BRAILLE PATTERN DOTS-458 | Braille Patterns | E2 A2 98 | a silhouette cell (braille of its lit pixels) |
| U+2899 | ⢙ | BRAILLE PATTERN DOTS-1458 | Braille Patterns | E2 A2 99 | a silhouette cell (braille of its lit pixels) |
| U+289A | ⢚ | BRAILLE PATTERN DOTS-2458 | Braille Patterns | E2 A2 9A | a silhouette cell (braille of its lit pixels) |
| U+289B | ⢛ | BRAILLE PATTERN DOTS-12458 | Braille Patterns | E2 A2 9B | a silhouette cell (braille of its lit pixels) |
| U+289C | ⢜ | BRAILLE PATTERN DOTS-3458 | Braille Patterns | E2 A2 9C | a silhouette cell (braille of its lit pixels) |
| U+289D | ⢝ | BRAILLE PATTERN DOTS-13458 | Braille Patterns | E2 A2 9D | a silhouette cell (braille of its lit pixels) |
| U+289E | ⢞ | BRAILLE PATTERN DOTS-23458 | Braille Patterns | E2 A2 9E | a silhouette cell (braille of its lit pixels) |
| U+289F | ⢟ | BRAILLE PATTERN DOTS-123458 | Braille Patterns | E2 A2 9F | a silhouette cell (braille of its lit pixels) |
| U+28A0 | ⢠ | BRAILLE PATTERN DOTS-68 | Braille Patterns | E2 A2 A0 | a silhouette cell (braille of its lit pixels) |
| U+28A1 | ⢡ | BRAILLE PATTERN DOTS-168 | Braille Patterns | E2 A2 A1 | a silhouette cell (braille of its lit pixels) |
| U+28A2 | ⢢ | BRAILLE PATTERN DOTS-268 | Braille Patterns | E2 A2 A2 | a silhouette cell (braille of its lit pixels) |
| U+28A3 | ⢣ | BRAILLE PATTERN DOTS-1268 | Braille Patterns | E2 A2 A3 | a silhouette cell (braille of its lit pixels) |
| U+28A4 | ⢤ | BRAILLE PATTERN DOTS-368 | Braille Patterns | E2 A2 A4 | a silhouette cell (braille of its lit pixels) |
| U+28A5 | ⢥ | BRAILLE PATTERN DOTS-1368 | Braille Patterns | E2 A2 A5 | a silhouette cell (braille of its lit pixels) |
| U+28A6 | ⢦ | BRAILLE PATTERN DOTS-2368 | Braille Patterns | E2 A2 A6 | a silhouette cell (braille of its lit pixels) |
| U+28A8 | ⢨ | BRAILLE PATTERN DOTS-468 | Braille Patterns | E2 A2 A8 | a silhouette cell (braille of its lit pixels) |
| U+28AA | ⢪ | BRAILLE PATTERN DOTS-2468 | Braille Patterns | E2 A2 AA | a silhouette cell (braille of its lit pixels) |
| U+28AC | ⢬ | BRAILLE PATTERN DOTS-3468 | Braille Patterns | E2 A2 AC | a silhouette cell (braille of its lit pixels) |
| U+28AE | ⢮ | BRAILLE PATTERN DOTS-23468 | Braille Patterns | E2 A2 AE | a silhouette cell (braille of its lit pixels) |
| U+28AF | ⢯ | BRAILLE PATTERN DOTS-123468 | Braille Patterns | E2 A2 AF | a silhouette cell (braille of its lit pixels) |
| U+28B0 | ⢰ | BRAILLE PATTERN DOTS-568 | Braille Patterns | E2 A2 B0 | a silhouette cell (braille of its lit pixels) |
| U+28B1 | ⢱ | BRAILLE PATTERN DOTS-1568 | Braille Patterns | E2 A2 B1 | a silhouette cell (braille of its lit pixels) |
| U+28B2 | ⢲ | BRAILLE PATTERN DOTS-2568 | Braille Patterns | E2 A2 B2 | a silhouette cell (braille of its lit pixels) |
| U+28B6 | ⢶ | BRAILLE PATTERN DOTS-23568 | Braille Patterns | E2 A2 B6 | a silhouette cell (braille of its lit pixels) |
| U+28B7 | ⢷ | BRAILLE PATTERN DOTS-123568 | Braille Patterns | E2 A2 B7 | a silhouette cell (braille of its lit pixels) |
| U+28B9 | ⢹ | BRAILLE PATTERN DOTS-14568 | Braille Patterns | E2 A2 B9 | a silhouette cell (braille of its lit pixels) |
| U+28BA | ⢺ | BRAILLE PATTERN DOTS-24568 | Braille Patterns | E2 A2 BA | a silhouette cell (braille of its lit pixels) |
| U+28BB | ⢻ | BRAILLE PATTERN DOTS-124568 | Braille Patterns | E2 A2 BB | a silhouette cell (braille of its lit pixels) |
| U+28BC | ⢼ | BRAILLE PATTERN DOTS-34568 | Braille Patterns | E2 A2 BC | a silhouette cell (braille of its lit pixels) |
| U+28BE | ⢾ | BRAILLE PATTERN DOTS-234568 | Braille Patterns | E2 A2 BE | a silhouette cell (braille of its lit pixels) |
| U+28BF | ⢿ | BRAILLE PATTERN DOTS-1234568 | Braille Patterns | E2 A2 BF | a silhouette cell (braille of its lit pixels) |
| U+28C0 | ⣀ | BRAILLE PATTERN DOTS-78 | Braille Patterns | E2 A3 80 | a silhouette cell (braille of its lit pixels) |
| U+28C4 | ⣄ | BRAILLE PATTERN DOTS-378 | Braille Patterns | E2 A3 84 | a silhouette cell (braille of its lit pixels) |
| U+28C5 | ⣅ | BRAILLE PATTERN DOTS-1378 | Braille Patterns | E2 A3 85 | a silhouette cell (braille of its lit pixels) |
| U+28C6 | ⣆ | BRAILLE PATTERN DOTS-2378 | Braille Patterns | E2 A3 86 | a silhouette cell (braille of its lit pixels) |
| U+28C7 | ⣇ | BRAILLE PATTERN DOTS-12378 | Braille Patterns | E2 A3 87 | a silhouette cell (braille of its lit pixels) |
| U+28C9 | ⣉ | BRAILLE PATTERN DOTS-1478 | Braille Patterns | E2 A3 89 | a silhouette cell (braille of its lit pixels) |
| U+28CC | ⣌ | BRAILLE PATTERN DOTS-3478 | Braille Patterns | E2 A3 8C | a silhouette cell (braille of its lit pixels) |
| U+28CF | ⣏ | BRAILLE PATTERN DOTS-123478 | Braille Patterns | E2 A3 8F | a silhouette cell (braille of its lit pixels) |
| U+28D5 | ⣕ | BRAILLE PATTERN DOTS-13578 | Braille Patterns | E2 A3 95 | a silhouette cell (braille of its lit pixels) |
| U+28DA | ⣚ | BRAILLE PATTERN DOTS-24578 | Braille Patterns | E2 A3 9A | a silhouette cell (braille of its lit pixels) |
| U+28DE | ⣞ | BRAILLE PATTERN DOTS-234578 | Braille Patterns | E2 A3 9E | a silhouette cell (braille of its lit pixels) |
| U+28E0 | ⣠ | BRAILLE PATTERN DOTS-678 | Braille Patterns | E2 A3 A0 | a silhouette cell (braille of its lit pixels) |
| U+28E1 | ⣡ | BRAILLE PATTERN DOTS-1678 | Braille Patterns | E2 A3 A1 | a silhouette cell (braille of its lit pixels) |
| U+28E2 | ⣢ | BRAILLE PATTERN DOTS-2678 | Braille Patterns | E2 A3 A2 | a silhouette cell (braille of its lit pixels) |
| U+28E5 | ⣥ | BRAILLE PATTERN DOTS-13678 | Braille Patterns | E2 A3 A5 | a silhouette cell (braille of its lit pixels) |
| U+28E6 | ⣦ | BRAILLE PATTERN DOTS-23678 | Braille Patterns | E2 A3 A6 | a silhouette cell (braille of its lit pixels) |
| U+28E7 | ⣧ | BRAILLE PATTERN DOTS-123678 | Braille Patterns | E2 A3 A7 | a silhouette cell (braille of its lit pixels) |
| U+28E8 | ⣨ | BRAILLE PATTERN DOTS-4678 | Braille Patterns | E2 A3 A8 | a silhouette cell (braille of its lit pixels) |
| U+28EA | ⣪ | BRAILLE PATTERN DOTS-24678 | Braille Patterns | E2 A3 AA | a silhouette cell (braille of its lit pixels) |
| U+28EC | ⣬ | BRAILLE PATTERN DOTS-34678 | Braille Patterns | E2 A3 AC | a silhouette cell (braille of its lit pixels) |
| U+28EE | ⣮ | BRAILLE PATTERN DOTS-234678 | Braille Patterns | E2 A3 AE | canopy, deep forest |
| U+28F0 | ⣰ | BRAILLE PATTERN DOTS-5678 | Braille Patterns | E2 A3 B0 | a silhouette cell (braille of its lit pixels) |
| U+28F3 | ⣳ | BRAILLE PATTERN DOTS-125678 | Braille Patterns | E2 A3 B3 | a silhouette cell (braille of its lit pixels) |
| U+28F4 | ⣴ | BRAILLE PATTERN DOTS-35678 | Braille Patterns | E2 A3 B4 | a silhouette cell (braille of its lit pixels) |
| U+28F5 | ⣵ | BRAILLE PATTERN DOTS-135678 | Braille Patterns | E2 A3 B5 | a silhouette cell (braille of its lit pixels) |
| U+28F6 | ⣶ | BRAILLE PATTERN DOTS-235678 | Braille Patterns | E2 A3 B6 | canopy, deep forest |
| U+28F7 | ⣷ | BRAILLE PATTERN DOTS-1235678 | Braille Patterns | E2 A3 B7 | a silhouette cell (braille of its lit pixels) |
| U+28F8 | ⣸ | BRAILLE PATTERN DOTS-45678 | Braille Patterns | E2 A3 B8 | a silhouette cell (braille of its lit pixels) |
| U+28F9 | ⣹ | BRAILLE PATTERN DOTS-145678 | Braille Patterns | E2 A3 B9 | a silhouette cell (braille of its lit pixels) |
| U+28FC | ⣼ | BRAILLE PATTERN DOTS-345678 | Braille Patterns | E2 A3 BC | a silhouette cell (braille of its lit pixels) |
| U+28FE | ⣾ | BRAILLE PATTERN DOTS-2345678 | Braille Patterns | E2 A3 BE | a silhouette cell (braille of its lit pixels) |
| U+28FF | ⣿ | BRAILLE PATTERN DOTS-12345678 | Braille Patterns | E2 A3 BF | dense canopy, deep forest |

154 code points in six blocks: one each in Latin-1 Supplement, General Punctuation, Mathematical Operators
and Box Drawing, six Block Elements (the gravel's light shade and the five silhouette fills) and 144 Braille
Patterns (the ground's seven and the silhouettes' rest; cb02c's tail frames added U+287D and U+28DE). The ground is pack's forest and the Shingle's
marks; the creatures are one drawing each, turned.
