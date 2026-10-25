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

2026-10-25 — the maintainer's word: "The sprite when moving sideways should look the same as its north-south orientation."

The cub keeps two body cells on the lower row and two ear cells above in
all four headings. Only ear glyphs turn; east and west never rotate the
body into a vertical strip. Plain uses the same two-by-two footprint:
two `C` body cells and two facing ears. Rich uses quadrant ears and blocks.
Stand, alternating walk foot, lowered sneak ears and flat-eared pant share
this footprint. The sheet shows every heading crossed with all four poses
on both tiers. Health tails and stamina colours remain in game frames.

## The Shingle

From the north: the Ashwater (blue, ripples `≈` here and there; plain `~`), two rows of reeds at the edge
(`⠇` and `⠖` in reed green on the water; plain `|` and `!`), five rows of gravel (grey 240 with the odd
mark `·` `․` `░`; plain bright black with `.` `,` `:`), then grass and Thornmere's woods from pack's forest
texture (grass `⠖⠶`, trunks `┃`, canopy `⣿⣶⣮⠶`, deep forest blank) on the forest floor. Trunks, deep forest
and water stop the cub; grass, gravel, reeds and canopy are open ground.

Sheet rows 0-2 the water, 3-4 the reeds, 5-10 the gravel, 11-14 the grass, 15-19 the woods, 20-23 the
deep forest.

## What is owed

Dusk and night palettes follow with the other areas. Combat posture, foes and the den are covered by the game-frame goldens below.

## Combat sheet vocabulary (2026-10-25)

The game frames now draw the weasel as `w` and the fox as `f`, followed by
`^` hunting, `_` crouching, `~` feinting, `>` striking, `<` retreating or `!`
staggered. `[]` beneath a foe is the lock. The same tells appear on both
tiers; a raised apostrophe during a strike is a presentation arc over its
ground body, never a collision displacement.

The cub's adjacent move mark is `>` bite, `>>` lunge, `]` parry, `o` dodge,
`~` water or `_` fall. A spent cub pants `:`. Ears dim as stamina drops; the
plain ears change `^`, `<`, `_`. The tail is `/`, `-`, `_` through health
bands. Each band spans a third; the lowest health band also limps.

Scent is a dim `:` then `.`, the dropped mark a bright `*`; the hollow log
is labelled, and the thorn row is `#X#X#` until broken. Only the den shows
numbers. Every action and encounter has a replay golden on both tiers.
