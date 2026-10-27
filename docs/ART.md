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
2026-10-25 (cb02b) — the maintainer's word: "make the wolf cub sprite more shaped like a wolf — currently it looks like a guy
holding a sword — and changing to left/right motion still distorts the sprite past recognizability from the north/south
orientation; it should look the same, just rotated."

The cub is one drawing: a pixel silhouette eight pixels across and sixteen down at the rich tier's finest
grain (two pixels across and four down a cell, the braille grid, square pixels at a 1:2 cell), a wolf from
above facing north: the nose, the muzzle, the head with an ear out each side, the neck, the shoulders, a
long body, the haunches and a tail trailing south (`src/silhouette/silhouette.lu`, `cub`). Facing east,
south or west the frame draws the same bitmap turned a quarter, a half or three quarters, pixel for pixel:
four cells by four north and south, eight by two east and west, the cub's own cell the second row and
column of the four (R-cb02b-2 A; `grove_test` holds the east drawing to the north one pixel by pixel).
Each cell becomes the full block where all eight pixels are lit, a half block where exactly one half is,
and the braille pattern of its lit pixels otherwise, so the silhouette is solid where it is thick and
drawn where it is thin; the ground shows through its unlit cells. The poses are frames of the same
drawing: a walk sets the paws out, a sneak tucks the muzzle and lays the ears back, a pant lays them flat
and opens the mouth.

2026-10-25 (cb02c) — the maintainer's word: "its tail oscillates too quickly. Make it natural." The tail and
the paws follow the gait, the ground the cub covers, never the tick (R-cb02c-2 A): the paws step twice a
stride, the tail wags once in two strides, through five frames walking (the tip two pixels either side of
the middle, the root one) and three standing, sneaking or panting (one pixel each side, a slow sway). At the
trot a wag is 0.9 s, at a grown paw's trot 0.6 s, standing 2 s. `silhouette.wag` holds the eight steps of a
wag; the frames are still the one drawing, turned. The sheet's `wag` row draws the walking cub north with its
tail at each offset; `docs/GLYPHS.md` gained two braille cells for them. The plain tier's tail `,` swings to
the side the rich tail swings to, and its walking paw `'` steps at the haunches' corners, inside the
footprint. Stamina is the fur: fresh, dim when tired or spent. The plain
tier keeps the footprints in ASCII (`.^^.` over `####` over `.,..` north; `.=####^.` over `,=####>.`
east). The posture marks sit clear of the silhouette in every facing.

2026-10-26 (cb03) — posture as HUD (campaign innovation 5; pack's idea, cub's drawing): the numbers leave
the running HUD, and health is read from the cub as one reads a dog. The one silhouette gains a hurt set
(`silhouette.cub_posed`, R-cb03-2 A), four bands by health:

| band | the drawing, facing north |
|---|---|
| full (3/4 and above) | as above: the ears out (`#.####.#`), the tail's full wag, both paws out a step |
| hurt (1/2 and above) | the ears back along the head (`.######.` over `.######.`), the tail's wag halved |
| badly hurt (1/4 and above) | the ears laid back at the neck (`..####..` over `#.####.#`), the tail hanging still down the middle, one paw out a step |
| dying (under 1/4) | the ears flat, the head dropped like the sneak's, the tail still, the trot a stand |

Stamina is the breath: standing, the shoulders (`.######.` → `########`) and the haunches (`..####..` →
`.######.`) widen a pixel each side on the in-breath, every two seconds fresh and every 1.2 s tired
(`sim.breath`); spent, the pant's mouth (`..#..#..`) opens and closes every four ticks. Every frame is the
same 8 by 16 drawing, so what is drawn is still what collides. The sheet's `hurt` row draws the four bands
walking north, its `breath` row the out-breath, the in-breath and the pant's two frames; `docs/GLYPHS.md`
gained sixteen braille cells for them. The plain tier shows the hurt set (the ears' low row from hurt on,
the tail `,` still on the left from badly hurt on) and the pant; it has no breath. cb01's health tail
mark (`/ - _`) is gone with the bars; the numbers show at a den and on the death card (R-cb03-3 A).

## Bodies (cb02c)

2026-10-25 — the maintainer's word: "Enemies should never overlap with the cub. They should have collision
to prevent weird attack moments where the enemy is behind the cub and can't be hit." What is drawn is what
collides: a body is its drawing's rectangle (`silhouette.footprint`, held to the bitmaps by `gait_test`),
the cub's turned the way the frame draws it. No two bodies share a cell; the leaps stop at a body, drawn or
fading; the head shake holds against one. The frame draws the cub's body facing (`sim.Sim.body_facing`):
its turn's or its attack's, held for a tick when a foe in the way has no room to step aside.

## The foes and the bundle

Every foe is the same kind of drawing: the weasel four pixels across (two cells by three north, six by
one east), the fox eight by twelve (four by three, six by two), the deer eight by sixteen; the hawk's
ground shadow eight by four, wings out while it circles, spread wide at the stop, folded in the stoop. The
tell is a posture of the one drawing: a crouch tucks the head (fewer pixels), a strike thrusts it, a
flight streams the tail, a stagger splits the body, a feint curls the tail; a death erodes the head at
five ticks and the body at ten. The wrapped bundle, which read as an enemy in ASCII, is a silhouette too
(ten by twelve pixels: a knot above a round parcel with its cord crossing; opened, the loose binding).
The plain tier keeps a head, body and tail in ASCII with the same footprints and the same tells
(`_` crouch, `!` stagger, `~` flight, `?` feint, `'` strike).

## The Shingle

From the north: the Ashwater (blue, ripples `≈` here and there; plain `~`), one row of reeds at the edge
(`⠇` and `⠖` in reed green on the water; plain `|` and `!`), five rows of gravel (grey 240 with the odd
mark `·` `․` `░`; plain bright black with `.` `,` `:`), then grass and Thornmere's woods from pack's forest
texture (grass `⠖⠶`, trunks `┃`, canopy `⣿⣶⣮⠶` in two greens) on the forest floor. The deep forest is the
same four glyphs in the deep green alone, with the same trunks among them (plain `& % * ;` and `|`),
everywhere: beyond an area's bounds, beyond the jetties, in the thicket's dense patches, so there is no
flat fill anywhere on the screen (cb02b; the maintainer's word: "fix the forest to use the forest
texture throughout"). Two adjacent foliage cells are never the same glyph: the variant alternates its
glyph set by the cell's parity (`art.terrain_row`), which the census holds (`coast.texture`, FLAT_MAX 2,
TEXTURED_MIN 90 %). Trunks, deep forest and water stop the cub; grass, gravel, reeds and canopy are open
ground. The coast runs a screen past the initial view each way to its jetties (`docs/DESIGN.md`), and four
branches leave it for their alcoves, two each side of the thorn path.

Sheet rows 0-2 the water, 3-4 the reeds, 5-10 the gravel, 11-14 the grass, 15-24 the woods, 25-27 the
deep forest, with the cub's four poses by four facings over them and the foe study (every phase and fade
facing north, the east form of each) on gravel below; the sheet is 56 rows.

## What is owed

The thicket and meadow now have dusk palettes. Night and the later areas remain ahead. Combat posture, foes and dens are covered by game-frame goldens.

## Combat sheet vocabulary (2026-10-25)

2026-10-25 — the maintainer's word: "Enemies don't look like enemies; all enemies should have sprites."

Every foe has a sprite on both tiers, with its windup tell as a posture.
This rule applies to later foes and bosses, not just the weasel and fox.
Both tiers give every foe a head, body and tail; the plain tier in ASCII (a
narrow `==` weasel, a `####` fox under `/^^\`): crouch lowers the head to
`_`, a feint curls the tail `?`, flight trails `~`, stagger lifts `!`. The
rich tier draws the silhouettes above. Foe palette roles are red/brown,
distinct from cub fur and the dim scent trail.
A death sprite dims and erodes over 15 ticks (proposal), never disappearing
on the hit tick. The expanded 80×40 sheet covers each species × phase and
three fade stages, beside the cub's four headings × four postures.

The cub travels on its bite, lunge and heavy arcs, without a `>` attack
mark. Bite combos lean left/right then finish forward with shaking ears;
heavy back-steps and leaves a four-tick punctuation burst. Parry `]`, dodge
`o`, water `~`, fall `_`, pant `:` and the health tail remain readable.

Scent is a dim `:` then `.`, the dropped mark a bright `*`; the hollow log
has a cut-timber sprite, and the thorn row uses the hazard glyphs below. Scent is numeric in the top-row HUD at all times; other stat numbers remain
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


## Coast sprites

`coast-rich` and `coast-plain` in the art goldens show the hollow log's
open end grain, a fallen log's lengthwise passage and direction marks,
a wrapped treasure bundle and its loose opened binding. The hollow log
remains the first den; the fallen log remains the Bramblehold shortcut.
The interaction hints still name their roles.

Five original two-row shore finds—driftwood, a broken crate, kelp, a
bottle and a net—are placed from the seed only where their complete
footprint is gravel. They are decoration, not collision or pickups.
Rich grain/folds use scalar grid cells; the engine text helper is ASCII.
The rocky texture belongs to the jetties, never the ordinary bank.

Deep forest keeps visible, textured foliage beyond collision bounds and
through dense patches. The plain tier uses green on black, not black on
black. Bramblehold keeps its limited AI sight, but every in-view foe sprite is
drawn cell by cell; terrain no longer culls a whole foe by its centre. The texture census uses the same terrain renderer as the
actual frame, before deliberate HUD/actor overlays, over every camera
position of every area at both fields and on both tiers.

## The bosses, the wolf and the ghosts (cb04, 2026-10-26)

`boss-rich`, `boss-plain`, `wolf-rich` and `wolf-plain` in the art goldens are the sheets. Each boss is an
original bitmap at two by four pixels a cell (the silhouette rule, R-cb02b-2 A), drawn facing north and
turned for the other facings, its body the drawing's rectangle: the boar 12×24 (six cells by six), the
lynx 10×20, the elk 14×28, the shadow alpha 12×24. Postures by phase: hunting, the windup (the body
drawn back, the boar's head down, the lynx flat, the elk's rack lowered, the alpha's hackles up), the
strike (stretched along its line), the recovery and the stagger (the body sagging); phase two marks the
posture (the boar's foam, the lynx's bared teeth, the elk's lowered rack held, the alpha's eyes). The alpha
alone has eyes: `●` U+25CF in red 196, dark the rest of it. A beaten boss fades over 45 ticks in two
stages (15, 30) that clear whole cell rows from the top, so a fading boss draws no glyph its postures do
not (the glyph table needs no fade rows for it). Colours: the boar 130, the lynx 179, the elk 145, the alpha 244
(plain 1, 3, 7, 8). The bar on row 1 is text in the HUD's ink with the filled cells in the boss's colour.

The wolf is the cub grown one size (12×24): the end's three frames draw it crossing the ford on the far
bank's side, the pack's four silhouettes waiting above the water, and after the end the cub is drawn as
the wolf everywhere, with the cub's poses.

A ghost is the cub's own silhouette in a dim grey by rank (251, 248, 245, 242, 239 with the dim
attribute; plain `x`, 7 for the newest then 8), standing at the death spot in the death's facing; within
eight cells it is drawn frame by frame from the archive's trailer (the recorded facing and pose, the
legs alternating), through the same `draw_pose_in` as the cub, so a ghost never draws a glyph the cub
cannot. No ghost is drawn where no death was: an empty archive, or another world's, draws nothing
(`tools/gameplay.py`, `ghosts`).

The title is a composition of its own: the name, the four boss silhouettes in a row (dim until beaten,
lit in their colours after), their names, the key rows and "any key begins"; the river's `≈` scatter is its
border. The end card is text alone, centred.

## Larkmeadow landmarks (cb03a)

Original three-cell trees, dark against the gold grass, share a thin root
and sparse bent limbs. Singletons and three-root copses use the seed's
14-cell lattice, never the route. Rich trunks use `┃`; plain uses `|`.

```
Y .'       /|    o}{o     __    vvvv     .     *::*
 |Y       [__]    ==     [xx]          oo
 |                                  oooo
```

The atlas `meadow-rich`/`meadow-plain` draws all eight seeded forms.
Standing stones and burnt stumps have solid roots. Bones are a pale
non-solid old kill, placed in the same quiet ground as deer forage.
Crows lift to `v^v^` within five cells and warn hunters within twelve,
including behind them. Cairns mark sheltered off-route patches, not
loot. Scent grass leaves trails 150 ticks longer. A creek at row106–107
is water outside the carved route; the path itself is its guaranteed
ford. These rules add no respawning currency or save field.

## World landmark legend

World names are drawings, not floating labels. The `props-rich` and
`props-plain` atlas rows read left to right as follows. Rich strokes use
blocks, ruled timber, circular stones and ripples; plain keeps the same
three-row clusters in ASCII. These are original drawings.

| drawing | meaning |
|---|---|
| crossed thorn stems | the way into Bramblehold |
| six-rayed flower above grass | Larkmeadow |
| tusked, broad head | Old Snag's clearing |
| pointed ears, narrow muzzle, curled tail | Ember, the speaking fox |
| paired bone ends and a shaft | old bones without scent |
| forked trunk with scent dots | the marked tree |
| three joined peaks | the Teeth |
| broken ripple bands | the Shallows |
| dark opening under an arched roof | Gravehollow |
| alternating paired tracks | the old pack's marks |
| woven stems, an opening after digging | the hedge shortcut |
| ascending rock steps | the ledge shortcut |
| stepping stones in ripples | the shallows shortcut |
| ringed log with a bright centre; empty ring after | inland hollow cache |
| rooted mound with a bright centre; empty mouth after | herb burrow cache |

The already-drawn log and coast bundle stay sprites. HUD area names,
interaction hints, the den/death cards and dialogue remain text. In
particular, `Ember:` on the bottom dialogue line is a speaker, not a world
label. There are no separate lever-name draw calls in this build.

## Scent and pickups

The scent left by a death is a white core between bright curved rims,
with a soft violet halo and four upward-drifting motes. It stays visible
inside the camera and the cub's nose range (`sim.scent_reach`). The
halo breathes over 96 simulation ticks. Seed, death cell and tick alone
place the motes: no emitter allocation, random wall clock or growing list.
The entire orb stays within seven columns and eight rows: three cells
left/right, five above and two below its centre. Its plain form is `(*)`
with dots, stars and the same halo and drift in console colours.

Ordinary scent uses the same light. Closed bundles are pale and bold,
with slowly alternating glints that widen their visible footprint to
nine cells. Inland hollows and burrows have their own bright contents
and glints; opened forms keep only the dark empty container. Collection
leaves eight sparks expanding to at most three cells and gone after
12 ticks. Successive collections replace that one burst; there is no
unbounded effect queue. Empty/foreign-area death marks draw no orb.

`meat-rich/plain` shows a bright salmon cut on a white bone, nine columns
by three rows, with a glint moving slowly across the flesh. `spring-rich/plain`
shows the seven-column pale stone basin, cyan spout and ripples in both
idle phases, then the dim empty basin after learning. These pure helpers
are `art.draw_meat(mut g, tier, row, col, tick)` and
`art.draw_spring(mut g, tier, row, col, tick, available)`, taking screen
cells, not simulation fields. Their 24-tick highlights never move the
pickup's logical position. Meat and spring logic now calls these helpers
directly, using the shared body-ring pickup predicate and recovery burst.
Fresh meat, like ordinary scent, survives its first rendered tick. Learned
springs keep their empty basin. `art.draw_water` fills row3, columns24–48
after the HUD's background clear on both tiers.

## Rest interiors (cb04a)

A den replaces the scrolling field with an original side view of the cub
lying toward a small fire. Its long back, haunch, lowered muzzle, pointed
ears, closed eye and extended forepaws are a separate drawing, not a scaled
map sprite. `restscene.cub_pixel` samples volume into half/quadrant cells;
`fur_light` shades the fire-facing muzzle brighter than the rump and the
underside. The shoulder follows `sim.breath`, the field posture's phase.
The fire has four seven-tick frames and a small rising ember. Plain mode
uses a simpler ASCII contour with the same breath and fire phases.

Surroundings are region-specific: a low rock overhang with blue water for
the Shingle; an enclosing thorn hollow for Bramblehold; gold hillside and
thin gangly trees against the sky for Larkmeadow; cold angled ledges in the
Teeth; reeds and blue river light in the Shallows; dark old roots and scent
marks in Gravehollow. Sea colour is visual atmosphere, not a new sound loop.
The same cub and fire sit in all six. The right-hand panel holds the stat choices, their effects, scent, pending
cost and save state; the whole cub and fire remain visible to its left.

`rest-{shingle,bramblehold,larkmeadow,teeth,shallows,old-den}-{80x24,120x40}`
are the twelve case names, each rendered rich/plain. Seven-tick samples pin
fire animation as well as the thirty-sixth tick's inhale. The rich glyph
repertoire adds the side-view quadrants and vertical half blocks.

The thorn gate now remains visible when opened: dim torn flanks either side
of a five-cell passage. Both faces of edge0 draw the same boundary; the
opening never draws a closed collision glyph across the passage.


## Allocation panel (cb04d)

A double frame of existing rule glyphs, muted gold179 on near-black232,
contains bone-white230 labels and aligned current/pending columns. Plain
uses doubled ASCII rules, gold3 and white15 on black0. The right-hand panel
is40×22 at80×24 (left39, top1) and50×26 at120×40 (left69, top7).
The complete38-column cub/fire group fits to its left, without cropping.

Sections are the den name; Level, Scent held, Scent needed, Scent after;
the five stats and their effects; Confirm and the keyboard hint. A `>`
selects a row. Raised values and effects are green84/plain10; insufficient
scent and the refusal explanation are red203/plain12. The explicit arrows,
numbers and explanation carry the same meaning without colour. A refused
raise displays its attempted total cost; Scent after still describes the
accepted pending choices, never an unaccepted debt.

`rest-menu-{empty,pending,refused}-{80x24,120x40}` pin all three states on
both tiers. The frame uses existing horizontal/vertical rule glyphs only.

## The wide forest (cb05, 2026-10-26)

**The Ashen.** Cinderwick's dead from above, four pixels across and twelve down (two cells by three
north, six by one turned), the same grain as the weasel: a round head, the shoulders, a long thin body,
the legs apart walking. The windup is the tell a person reads: the arms rise slowly up beside the head
(`#..#` over `#..#` over `####`) for thirty ticks; the blow thrusts one arm out (`##.#`); a stagger
splits the body; a death erodes from the head as every foe's does. Grey 247 (plain 7), the smoke's
colour, never bold. The plain tier: `oo` over `||` over `/\` north, `^^` for the raised arms, `|=` for
the blow, `!!` staggered; turned, a strip of six (`/||oo `). The art sheet's foe study gains its row.

**The town.** The night of the fire: ash in two greys (`⠂` `⠐` `·` and bare, 240 and 242 on the floor
233; plain `.` `,` `'` in 8), the broken walls in two pale faces (`▓` `▒`, 245 and 250, alternated by
the cell's parity like the crags' stone; plain `#` `%`), the lane's cobbles in the gravel's glyphs at 250,
the embers `✶` `✵` in 208 and 202 bold on dark red 52 (plain `*` `+` in 9), the wood beyond the back walls
in Gravehollow's night greens. An ember lights the ash and the walls round it: within three columns the
ash warms to 215 and the walls to 223, within six to 137 and 180 (plain 11 and 3); the lane keeps its
one style. A yard's cache is a heap of ash with something under it (`.~~~.` over `(##o##)`, a glint
alternating as the inland caches' do); dug, the hollow in the heap. The way on into Bramblehold shows the
thorn stems. The rest scene at the cold hearth is a roofless room: broken walls either side, the
hearth's stones behind the fire, ash on the floor, an ember's glow in the wall's cracks.

**The landmarks** (`props.lu`, the `props-rich`/`props-plain` atlas's new row): the low embers, a ring of
coals with a bright middle; the ash shelter, the charred frame of a hut (`/\___/\` over `|  _  |` over
`|_| |_|`); a burnt stump (seven of them round the coal roots' point); the lightning-split oak (two
limbs over a V and a stump); the cleft, two blocks of stone round a crack; the willow, a crown over
three trunks with the fronds hanging; Quill's first perch, a dead tree with the raven on its one limb
(`v`); an old scent mark, a stump with the scent's dots beside it. Each is a three-row cluster in the
landmark ink (180 on 235; the coals bright), drawn where `forest.landmark` puts it, and the coal roots'
stumps, the low embers, the ash shelter, the perch and every scent mark say a line on the bottom row
while the cub stands within four cells.

**The dens.** Each den draws the place its name promises (`art.den_rows`, three rows of seven over the
warm patch, `#` a block and `|` a rule on the rich tier): the hollow log's cut timber (`_.===._` over
`( O====` over `'==='`), the split roots (`\ | | /` over `\|_|/` over `/   \`), the briar hollow's bowl in
the brambles (`%%\_/%%`), the grass nest's flattened ring (`,,\_/,,`), the ledge cleft's crack in the stone
(`##\_/##`), the willow root over the water (`\\|_|//` over `(   )` over `~~\_/~~`), the cold den under the
fallen oak's roots (`/\___/\` over `(     )` over `(_/ \_)`), the cold hearth's ring of stones (`o o o o`
round the fire), the last warm hollow where the fire stopped (`_.-~-._` over `( ~ ~ )`). The ember and the
smoke are as before.
