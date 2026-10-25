# The art study

What cub draws, on both tiers, and why. Every sprite here is a mock frame committed as a golden:
`tests/goldens/art/sheet-rich.txt` and `sheet-plain.txt` (with their `.sty` style files) are the sheets
`cub --art-study --dump DIR` writes, and the engine's `.lair/tools/goldens` keeps them current. Change a
sprite and the sheet's golden moves with it; the diff shows exactly which cells.

The rule for the tiers (pack's campaign R-PK-4, the lair's): one cell model, two glyph sets. The rich tier
may use any code point in `docs/GLYPHS.md`; the plain tier uses code points 0-255 and the sixteen colours,
what PAX's console font draws today. The sheet's plain half is held to that by `sprites_test` and `art_test`.

## The viewpoint

Top down, the camera on the cub (ruling #130, R-CB-3): the cub is always the centre cell and the world
scrolls under it in every direction. North is up the screen; the Ashwater lies to the north of the Shingle,
Thornmere's woods to the south and the sides.

## The cub

Rich: two cells wide, two tall, the ears on the side it faces as quadrant blocks over or beside a full-block
body. Smaller than pack's three-cell wolves, as a cub is.

```
▝▘   facing north: the ears up and out, the body below
██

██   facing south: the body, the ears below pointing down and out
▗▖

▘█   facing west: the two left quadrants beside the body
▖█

█▝   facing east: the two right quadrants
█▗
```

The facing is the nearest quarter of the heading, which turns at the turn rate (`docs/DESIGN.md`), so the
sprite turns a quarter at a time while the motion underneath is smooth. Fur is 180 (a tawny sand) on the
gravel's 240.

**Posture is the HUD** (the design bible's section 3): the ears carry the stamina band (fresh, tired, spent)
and the tail the health band, a limp under a third of health, panting when spent. The scaffold draws the
fresh band; the ear sprite's variant already carries the band (`8 × band`) and cb01 draws the other two with
the tail.

The plain cub is a bold `C` in bright yellow with a facing mark in the cell to its left: `^` north, `>`
east, `v` south, `<` west.

Sheet row 7: the cub facing N, E, S, W on the gravel.

## The Shingle

From the north: the Ashwater (blue, ripples `≈` here and there; plain `~`), two rows of reeds at the edge
(`⠇` and `⠖` in reed green on the water; plain `|` and `!`), five rows of gravel (grey 240 with the odd
mark `·` `․` `░`; plain bright black with `.` `,` `:`), then grass and Thornmere's woods from pack's forest
texture (grass `⠖⠶`, trunks `┃`, canopy `⣿⣶⣮⠶`, deep forest blank) on the forest floor. Trunks, deep forest
and water stop the cub; grass, gravel, reeds and canopy are open ground.

Sheet rows 0-2 the water, 3-4 the reeds, 5-10 the gravel, 11-14 the grass, 15-19 the woods, 20-23 the
deep forest.

## What is owed

The dusk and night palettes (pack's keyframes shape, per area); the posture bands and the tail; the foes'
sprites and their windup glyphs (the bible's section 8); the den. Each arrives with its lane and moves the
sheet's golden.
