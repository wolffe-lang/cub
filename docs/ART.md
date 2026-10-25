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

Sheet rows 0-2 the water, 3-4 the reeds, 5-10 the gravel, 11-14 the grass, 15-19 the woods, 20 onward the
deep forest, with the foe study below the cub poses.

## What is owed

The thicket and meadow now have dusk palettes. Night and the later areas remain ahead. Combat posture, foes and dens are covered by game-frame goldens.

## Combat sheet vocabulary (2026-10-25)

2026-10-25 — the maintainer's word: "Enemies don't look like enemies; all enemies should have sprites."

Every foe has a sprite on both tiers, with its windup tell as a posture.
This rule applies to later foes and bosses, not just the weasel and fox.
Both current foes have a two-cell body, a readable head above and a tail
below: a narrow `==` weasel and a broad `##` fox. Crouch lowers the head
to `__`; a feint curls the tail `?`; flee trails `~`; stagger lifts `!!`.
Rich adds directional quadrant ears, plain keeps punctuation. Foe palette
roles are red/brown, distinct from cub fur and the dim scent trail.
A death sprite dims and erodes over 15 ticks (proposal), never disappearing
on the hit tick. The expanded 80×40 sheet covers each species × phase and
three fade stages, beside the cub's four headings × four postures.

The cub travels on its bite, lunge and heavy arcs, without a `>` attack
mark. Bite combos lean left/right then finish forward with shaking ears;
heavy back-steps and leaves a four-tick punctuation burst. Parry `]`, dodge
`o`, water `~`, fall `_`, pant `:` and the health tail remain readable.

Scent is a dim `:` then `.`, the dropped mark a bright `*`; the hollow log
is labelled, and the thorn row is `#X#X#` until broken. Scent is numeric in the top-row HUD at all times; other stat numbers remain
in the den. The death card shows scent lost. Every action and encounter has a replay golden on both tiers.

## Thorn hazards and exits (2026-10-25)

The thorn gate is a collision wall, not lettering. Rich thorns alternate
braille thorn clusters in hazard red 196; plain uses `%` and `&` in bright
red 12. Neither tier uses `#` or `/` for the wall. Their glyph/colour pairs
are disjoint from labels and terrain walls. A bite gives the line
“the thorns need a lunge”; an active lunge targets the nearest point of
the full five-cell collision rectangle, including fractional cell spans.
The old wall's target stopped at the rightmost cell's origin: an approach
inside that cell's right half could miss despite facing the wall.

Every area exit and shortcut mouth has a three-row dim ground band,
seven cells wide, not a label or a card. Rich uses middle dots in 238 on
232; plain uses dots in 8 on 0. This exit shadow says that the path leaves
the area. Closed gates retain their hazard colour over the route; opening
one leaves the shadow readable. The approach is a deliberately carved,
treeless path branch, never an accidental gap between tree glyphs.


## The connected forest and opening

The bank and path bend from seeded noise. Bramblehold's dense canopy and
short visibility contrast with the meadow's long, brown-gold dusk view.
A hollow and a burrow sit at the ends of side branches, with empty forms
after digging; guards remain ordinary creatures, never disguised caches.
The meadow hawk has its own seven-column posture/fade sheet on both tiers.
A scent pickup shares the death mark's star, fades to a dot, and disappears
on collection or expiry.

The opening uses three original compositions: the pack over broken bands
of river ice, the cub below the split crossing, and the gravel bank at dawn.
Each carries no more than two lines of story. Simulation ticks select the
frame; skipping is an ordinary recorded key. Later story scenes use the
named hooks documented in DESIGN.md, not borrowed art or text.
