# Design constants

Tuning values in `src/sim/sim.lu`, `src/terrain/terrain.lu` and `src/forest/forest.lu` are mirrored
here with the date they were set and their source; named constants hold the gameplay bars. The design bible (`sprints/lair/cub/design.md` in the planning
repo) is the oracle; a number is **proposed** until the maintainer's play says otherwise (R-CB-7), and new proposals here are submitted for review; the private bible is not edited by this lane.

The connected Shingle, Bramblehold and Larkmeadow share one fight, rest, death and persistent-journey loop.

## The cub's stats (`src/sim/sim.lu`; the bible's section 3)

| constant | value | meaning | set |
|---|---|---|---|
| `STAT_START` | 1 | heart, wind, fang, paw and nose at the start; each 1-10, grown at dens with scent (cb01) | 2026-10-25 proposed |
| `health_max(heart)` | `40 + 12 × heart` | health at a heart level: 52 at the start | 2026-10-25 proposed (the bible) |
| `stamina_max(wind)` | `60 + 10 × wind` | stamina at a wind level: 70 at the start; moves spend it | 2026-10-25 proposed (the bible) |
| `trot_at(paw)` | `round((TROT_V + 2 × paw) × WALK_PERCENT / 100)` | the trot at a paw level: 75 at the start (8.79 cells a second), 111 at paw 10 | 2026-10-25 proposed (the bible); the dial 198 since cb03 |

## The cub's motion (`src/sim/sim.lu`)

| constant | value | meaning | set |
|---|---|---|---|
| `TROT_V` | 36 | the unscaled stat base, fixed-point units a tick (256 a cell); `trot_at` applies the pace dial | 2026-10-25 proposed |
| `WALK_PERCENT` | 198 | the pace dial (R-cb02c-1 A): the trot, the sneak, the turn rate, acceleration, braking, the foes' speeds, the stride and the sway are its products of cb01b's values (`PACE_BASE_PERCENT` 110) and cb02c's (`GAIT_BASE_PERCENT` 165), rounded to the nearest unit; the one constant to move. 165 was cb02c's; the maintainer's standing word on that build, 2026-10-26: "Bump the cub speed by 20 %" | 2026-10-26 cb03, proposed |
| `SNEAK_V` | 37 | a sneak (Shift+arrow): half the current paw-dependent trot (the ratio the dial keeps); no trail is laid and foes perceive by sight only | 2026-10-25 proposed (the bible, section 4) |
| `ACCEL` | 7 | acceleration, FP units a tick each tick: 4 × 198/110; the starting trot from a stop still in 11 ticks | 2026-10-26 cb03 (derived), proposed |
| `BRAKE` | 14 | braking: 8 × 198/110; a stop from the starting trot in 6 ticks (5 measured after the hold lapses); a cub stops faster than it starts | 2026-10-26 cb03 (derived), proposed |
| `TURN` | 256 | heading units a full turn: 0 north, 64 east, 128 south, 192 west; the diagonals between when two arrows are held | 2026-10-25 cb00 |
| `TURN_RATE` | 29 | the maximum turn rate, heading units a tick: 16 × 198/110, so the turning circle (speed over turn rate) is cb01b's, 0.55 cells measured; a quarter turn in 3 ticks, about in 6 (200 ms); the cub turns, never pivots | 2026-10-26 cb03 (derived), proposed |
| `STRIDE`, `GAIT_CYCLE` | 998, 1996 | a stride, FP units of travel (both paws once), and a wag (two strides): the tail and paws are tied to the ground covered, never the tick (R-cb02c-2 A); 832 at the dial's 165, scaled with it (R-cb03-5 A) so the wag keeps its 0.9 s at the trot | 2026-10-26 cb03 (derived), proposed |
| `SWAY_V` | 34 | the gait's floor, units a tick: a standing (or winding-up) cub's tail still sways, one wag in 59 ticks; 28 at the dial's 165, scaled with the stride (R-cb03-5 A) | 2026-10-26 cb03 (derived), proposed |
| the held key | the engine's `input.Hold` | a press holds `HOLD_TAP_TICKS` 12; an autorepeat run holds one interval plus `HOLD_MARGIN` past its last press (pack's pk01 model, in the engine) | 2026-10-25 the engine's |
| the camera | the cub's cell at the centre | R-CB-3: the world scrolls under the cub in every direction; a resize keeps it at the centre | 2026-10-25 ruling #130 |

Opposite arrows held together cancel (the cub brakes); a blocked cell stops the cub on that axis and the
other axis still slides, so a wall is followed, not stuck to.

## The Shingle (`src/terrain/terrain.lu`; the bible's section 2)

| constant | value | meaning | set |
|---|---|---|---|
| `LATTICE` | 24 | cells between the cover noise's lattice points, both ways: the woods thicken in patches about this size | 2026-10-25 proposed |
| `BANK_ROW`, `BANK_SWING` | -8, 8 | the Ashwater's edge lies between rows -8 and 0; start follows the bank | 2026-10-25 proposed |
| `REED_ROWS` | 1 | row of reeds at the water's edge (open ground) | 2026-10-25 proposed |
| `SHINGLE_ROWS` | 5 | rows of gravel below the reeds before the grass | 2026-10-25 proposed |
| `COVER_GRASS` | 120 | cover (of 256) under this is grass with the odd trunk (2 in 100 cells) | 2026-10-25 proposed |
| `COVER_WOODS` | 190 | cover under this (and over `COVER_GRASS`) is the woods: canopy with trunks (9 in 100); above it deep forest with canopy and more trunks (12 in 100) | 2026-10-25 proposed |
| what blocks | trunks, deep forest, water | the cub crosses water at shallows only (section 5); the Dark Wood's brush is not pushed through | 2026-10-25 the bible |

## The engine (lair's `clock`, `term`, `input`, pinned by `lair.pin`)

| constant | value | meaning | set |
|---|---|---|---|
| `TICK_HZ` | 30 | the simulation's tick | pack's pk00 |
| `MIN_COLS` x `MIN_ROWS` | 80 x 24 | the smallest terminal; the field scales up (R-CB-5 recommends pack's) | pack's pk00 |
| `ESC_TIMEOUT_MS` | 50 | a lone ESC is Esc after this long | pack's pk00 |

## Combat and recovery (2026-10-25, proposed)

The bible supplies bite cost 12 and 3/2/6 ticks, reach 2; lunge cost 30 and
9/3/12 ticks, reach 4; parry cost 10 and 9 active / 6 recovery ticks;
stagger 30 ticks; dodge cost 18, distance 3 cells, 6 + paw/2 iframes and
4 recovery ticks. Tick intervals are half-open: parry ages 0–8 succeed,
age 9 does not. A bite hits each foe once per action; a recovery input queues
one next bite. Bite damage is 6 + 2 × fang, lunge three times that.

R-cb01-1 recommendation A: camera remains centred on the cub; lock turns the
cub toward the foe. First Tab selects nearest visible foe, then stable spawn
order; Esc releases, death releases, sixty unseen ticks release. Range is
8 + nose cells. R-cb01-2 recommendation A: the next bite on the parried foe
before its 30-tick stagger expires deals double damage, once; parry itself
never damages ground foes; the meadow hawk has its distinct parry-kill answer. These are recommendations, not decisions by this implementation.

R-cb01-3 recommendation: the bible gives 30 ticks to drink and 40 health over
15 ticks. Prepare for the first 15, heal by exact integer instalments during
the last 15; any damage interrupts and the mouthful is already spent.

Additional proposed values, all 2026-10-25:

| mechanic | values |
|---|---|
| stamina | `REGEN` 2 standing, 1 walking, none during moves; exhausted at zero; `EXHAUST_RECOVER` 24; no sprint binding exists yet |
| posture | stamina: fresh above 2/3, tired above 1/3, spent below (the fur, and the breath since cb03); health: full at 3/4 and above, hurt at 1/2, badly hurt at 1/4, dying below (the ears, tail and trot since cb03); limp halves trot below 1/3 health |
| weasel | health 8, damage 10, scent 8 (bible); crouch 12, active 2, retreat/recovery 24 ticks |
| fox | health 24, damage 16, scent 20 (bible); feint 10, gap 6, real crouch 12, active 3, retreat 24 ticks; steals one water on a hit |
| foe motion | 79 pursuit / 86 retreat FP units per tick (44 / 48 × 198/110), acceleration 6 (the cub's), turn rate `FOE_TURN_RATE` 16 (cb01b's, not scaled), a turn it cannot make in one tick checks it toward `FOE_TURN_V` 33, stamina cap 60, attack costs 12, hunt restores 1/tick |
| perception | 90-degree forward cone, sight 8 cells; scent search 6 cells, newest unexpired visible sample; half-cell ray sampling |
| trail | 300-tick lifetime (bible); one sample per changed cell, none sneaking; old trail remains until expiry |
| water and death | 3 mouthfuls; 40 healed; 30-tick death fade (bible); mark recovery within 1 cell |
| growth | each stat starts 1, cap 10; next level costs 40 × next level (80 for level 2), only at den |
| den | within 1 cell of a seeded den; reset health, stamina, water, foes, trail and holds; gate, caches, shortcuts and mark persist |
| collision | ground bodies are their drawings' footprints and never share a cell (cb02c, below); reach counts clear cells between bodies; attack envelope and visual arc are separate |
| Shingle layout | den at seeded start; the connected-world table below supersedes the close-spawn preview and straight strip; the thorn branch now ends at start+157 |

The fox on the Shingle is a combat preview, not the later named fox's story
state. Bleeding, cold, areas beyond the meadow and the difficulty selector are not
implemented. The connected journey currently uses the default wolf rules.

Presentation proposals (2026-10-25): a trail is bright enough to read as `:`
for 150 ticks, then `.` until expiry; a dropped mark is visible within
8 + 2 × nose cells. All world-to-screen cell coordinates use floor division,
including negative coordinates. A death dissolve erases cells when
(row × 7 + column × 11) mod 30 is below the fade age; the multipliers are
presentation texture, not gameplay randomness.

## Speed revision, 2026-10-25

The maintainer's word: "Bump cub speed by 10 %." `WALK_PERCENT = 110`
scales `TROT_V + 2 × paw`, rounding to the nearest integer FP unit;
`TROT_V = 36` stays the unscaled stat base. At paw 1, walk 38 → 42
(the exact product is 41.8), sneak 19 → 21 (20.9). This quantisation is
proposed, not an extra tuning increase. Actual start-level walk is
4.921875 cells/s, sneak 2.4609375. `FOE_STALK_V = 44` and
`FOE_RETREAT_V = 48` are unchanged: a starting cub cannot outrun a weasel,
and sneak is below stalk. Paw growth may eventually outrun it as before.
Dodge remains three cells; no run binding or run speed exists yet.
Acceleration 4 and brake 8 remain: walk reaches the cap in 11 ticks and
stops in 6, rather than the old 10 and 5.
cb02c's pace dial (the gait section below) supersedes these numbers:
walk 63, sneak 31, acceleration 6, braking 12, foes 66 and 72.

## Directional attacks, 2026-10-25

The maintainer's word: "Leaps should be directional — pack pulled this off mostly."
`AIM_WINDOW_TICKS = 15` (500 ms, inclusive), the same name/value as pack's
pk06b measurement (pack#33, `43e2b683`, `notes/pk06b-aim-window.txt`):
48/48 diagonal orders hit on both tiers at 200/300/400 ms delays, versus
0/48 before, in a real pty. Arrows held or pressed in the window before the attack
are sampled in byte order; latest opposite wins on each axis, including
Shift+arrows. No arrow means facing. R-cb01b-1 A recommended and implemented:
lock overrides arrows. Each accepted attack commits its aim; arrows after
the key do not bend it. A queued recovery bite captures its own aim.
Movement still uses the engine's shorter Hold lifetime and turn rate.
Bite/lunge reach, cone, timings and damage stay the bible's.

## Leaping presentation, 2026-10-25

The maintainer's word: "Attacks should be leaping jumps, not a '>' that
appears and disappears." `BITE_ARC = 1 cell`, `LUNGE_ARC = 3 cells`:
an integer out-and-back triangle over the unchanged active ticks, returning
at recovery. It is pack's triangular routine shape, owned here because the
engine has no game-arc API. Eighth-cell path samples clip against terrain
and two-cell live body footprints. An already crowded encounter may shorten
a hop to zero. The camera and ground body never move with this offset.
A one-tick `*` marks contact at the foe (or empty apex); no attack arrow
remains. These are presentation proposals, not changes to what hits.

## Three-Space combo, 2026-10-25

The maintainer's word: "The first jump leans slightly left ... the second
attack leans right ... the third attack flies forward with the head shaking
left-right on landing." Accepted recovery chains cycle 1 → 2 → 3 → 1.
`COMBO_LEAN = FP/2`, perpendicular to aim; `COMBO_FINISH_ARC = 2 cells`
(proposed) is longer visually, not a longer hit reach. All three bites
retain cost 12, 3/2/6 timing and the same damage. Third-hit recovery ages
5 and 6 shake the ears left then right, on both tiers. A lapsed window,
rest or another action resets the combo. Refused attacks cannot advance it.

## Heavy attack, 2026-10-25 (proposed)

The maintainer's word: "Shift+Space should unleash a heavy attack: step
back two steps, then leap forward with a particle effect." R-cb01b-3 A:
`s` is the recommended fallback, implemented because the physical terminal
reports Shift+Space as plain Space. No decoder is copied into cub.

| constant | proposal | compared with lunge |
|---|---|---|
| `HEAVY_COST` | 42 stamina | 30 |
| `HEAVY_WINDUP / ACTIVE / RECOVERY` | 15 / 6 / 18 ticks | 9 / 3 / 12 |
| `HEAVY_DAMAGE` | 4 × bite | 3 × bite |
| reach | 4 cells, same cone | unchanged |
| `HEAVY_ARC` | 4 cells, presentation only | 3 cells |
| back-step | 1 cell at age 5, 2 at age 10 | none |
| burst | four ticks from apex, punctuation expands 1 → 2 cells and dims | one contact mark |

Surviving ordinary foes stagger for the existing 30 ticks; no boss poise
rule is added. The back-steps and leap clip against terrain and bodies,
never changing ground position or camera. The heavy cannot chain, does not
break the tutorial gate (the lunge still teaches that), and is refused
while panting. These tuning numbers await play.

## Foe sprites, 2026-10-25 (proposed)

`FOE_FADE_TICKS = 15`: a dead weasel or fox retains its head, two-cell body
and tail briefly, dimming at death, eroding head at age 5 and body at age
10, gone at 15. The fading footprint also clips presentation arcs.
Its collision/damage health is already zero: it cannot bite or award scent
again. `C_WEASEL` and `C_FOX` are palette roles, documented in PALETTE.md.

## Scent HUD, 2026-10-25

The maintainer's word: "There's no scent counter, or larger HUD." Scent is
now always visible as a number beside compact health/stamina bars. Each
bar is eight cells (proposed), filled by the positive fraction of its stat.
The death card names scent lost; recovery and kills update the same state
the HUD reads. Spending remains den-only. The larger posture bands, reticle,
water mouthfuls and area name are reserved for the next HUD pass.

## Encounter witness adjustment, 2026-10-25

The faster approach reaches the first weasel's crouch at tick 40 instead of
42; its unchanged 12-tick tell lands at 52 rather than 54. Parry/dodge
fixture inputs move two ticks earlier; no combat window is widened.
A lunge at the face of the thorn row now targets its nearest thorn rather
than an off-axis centre point (which could miss from two FP units away).
The natural-death fixture re-approaches the fox after its second retreat:
the faster approach otherwise lets the old scent expire before re-engagement.

## The connected world, 2026-10-25 (proposed)

Three fixed nodes now connect: the Shingle, Bramblehold and Larkmeadow.
A lunge opens the thorn route; walking through its exit enters Bramblehold,
then the next path reaches the meadow. Press `r` to push the fallen log
from the thicket or dig the hedge from the meadow. Both shortcuts become
bidirectional. `shortcut.log.push` and `shortcut.hedge.dig` reserve score
hooks; no audio plays yet. Old Snag's clearing and Whisper's scent-marked
tree are reservations, not bosses or open later areas. Ember's warning
is separate from the Shingle combat fox.

All values below are proposed 2026-10-25:

| layout or mechanic | value |
|---|---|
| area bounds | 160 cells along the route; the width is the journey's field (the grove section below): the coast `coast_extent(field)` each way, an inland area `half_width(field)` each side; local origin at the seeded bank den or the new area's north edge |
| centre curve | engine value noise on channels 31..33, sampled at 2× distance, plus eight-cell smoothstep anchors alternating seeded magnitudes 3..5; taper over eight cells at entrances |
| path width | half-width 3..5, separate channels 45..47 sampled at 3× distance |
| straight limit | `STRAIGHT_MAX=12` equal consecutive centre cells; path measured over 50 seeds; the bank uses the coast slope bar below |
| river bank | base -8, swing envelope 8; engine noise channel 9 at cell scale; adjacent bank rows differ by at most one |
| dens | stable ids 0 hollow log, 1 split roots, 2 briar hollow, 3 grass nest; new dens at rows 7..10 or 90..93, x within one cell of the seeded path |
| first foes | `FIRST_FOE_CELLS=30` minimum initial distance from every den in the area, checked independently of spawning |
| branches | two curved cache branches around rows 52 and 132, ending at seeded x=±(half_width-13..half_width-10); two-cell half-width; shortcut branches curve around row 22 toward x=±32 and end there |
| gate | at bank origin+157; five full collision cells, including their fractional spans; a carved branch leaves the main route at 140 and tapers into the gate; exit at 159 |
| portals | one-cell normal trigger, two-cell shortcut reach; arrival two cells inside the destination; exit shadow seven cells by three |
| thicket | sight five cells; creature visibility remains limited, distant foliage stays drawn; 16% trunks, canopy/brush threshold 130/256 |
| meadow | open sight; 3% trunks, 12% tall grass; distinct dusk colours |
| entry / bite hint | 90 ticks, one line rather than a card |
| hawk | 18-tick stopped shadow, three active ticks, 36 recovery; 14 damage; 10-cell detection; two-cell seeded-home orbit over 120 ticks |
| pickups | `DROP_TICKS=300`, one-cell collection radius; bright `*` for the first half, dim `.` after; expired scent is lost |
| deer | flee within seven cells, ordinary 8 health; eating the drop heals 10 first and gives the bible's 5 scent |
| caches | two inland per area (first a lore hollow, second an herb burrow; a weasel trio or fox pair guards it), four on the coast (the grove section); dig within two cells only with no live guard within six; one yarrow in the meadow, one marrow from the second cache elsewhere |
| opening | three original frames, 90 ticks each; any decoded key skips without also performing a move |

| area | path groups | side-branch guards |
|---|---|---|
| Shingle | weasel pair at 52..56, fox at 76..80, weasel pair at 134..138 | trio and fox pair |
| Bramblehold | weasel pairs down the route, outside both den safety radii | trio and fox pair; boar sign, no boar yet |
| Larkmeadow | hawk and deer at each of 52..56, 76..80, 134..138 | trio and fox pair |

The density table describes initial positions, not an invisible spawn timer.
Rest and death reset the current area's encounters. Entry resets local foes,
trails and uncollected ordinary drops, but preserves health, water, growth,
currency, the last den, opened caches/shortcuts and the death mark. Caches
never refill on a rest. A mark in another area's coordinates cannot be
collected locally. Each hawk's shadow is non-solid: dodge can leave it.
The stopped target does not follow the cub. A parry kills the stooping hawk
for the bible's 12 scent; bite, lunge and heavy cannot hit it in the air.

Recommendations implemented, not decisions: R-cb02-1 A persists the mark's
area/position/scent; R-cb02-2 A requires parry or evasion for the hawk;
R-cb02-3 A requires walking over the visible scent drop.

## Journey files and scenes, 2026-10-25

`--save PATH` overrides the live default `~/.cub/save`. Headless/replay
runs write no journey unless explicitly given `--save`. Schema 2 records
seed, wolf difficulty, five growth levels, water capacity, carried scent,
last/lit dens, shortcuts, gate/story flags, deaths, the mark, cache bits
(eight: the coast's four, the thicket's two, the meadow's two), pouch
counts, opening progress and the journey's field (cb02b; a schema-1 file
is refused by name as any unknown version is). Current health and charges are transient:
resume wakes at the last den, healed and refilled, with reset encounters.
The difficulty selector is not added here: non-wolf saves fail by name,
rather than silently playing wolf rules. Future boss/NPC states require a
new validated schema rather than accepting unknown bits now.

The canonical text has a non-cryptographic rolling checksum (seed 7,
multiplier 31, modulus 1000000007). The parser caps text at 1024 bytes;
seed and counters are bounded to ±1000000000 and 0..1000000000 respectively,
growth to 1..10, den/area ids to known values and cache bits to six entries.
Unknown versions, malformed or inconsistent fields and unsupported difficulty
have distinct failure names. Corruption never silently creates a new game.

Saving creates an exclusive sibling `.pending`, writes and syncs it,
closes it, then replaces the destination and syncs the directory. The
same-directory rename is atomic on the supported macOS/Linux hosts. A
post-rename directory-sync failure is named `save_committed_unsynced`,
not misreported as an untouched old save. A stale or concurrent stage is
`save_busy`; the game never deletes another writer's stage. The normal
live delay before replacement is one tick. `--save-delay 1..300` and
`--save-cut` are explicit test witnesses. Quit/interrupt while a stage is
pending cancels only that owned stage, preserving the previous journey.

A resumed recording carries all 25 initial journey fields as versioned
numeric replay events. Playback and death archives therefore need no
external save. The opening is an `opening 1` event; its keys and skip are
the ordinary replay stream. Reserved scene hooks are `scene.den.first`,
`scene.elk.choice`, `scene.alpha.offer`, and `scene.ending.home`, `.alone`,
`.shadow`; those later scenes are not implemented here.


## The coast, 2026-10-25 (proposed)

The Shingle is a horizontal five-row path between water and forest, with
one bank row. The shoreline follows long-wave engine noise, not the
alternating short anchors used by inland paths. Quantisation can make a
level stretch; that is preferable to forcing a sawtooth. Rock jetties sit
at the coast's ends (the grove section below), each three cells wide,
six cells into the water and three past the path. Rock is solid; shore
beyond it is closed.

Four offshoots turn from the shore (the grove section), with the full
inland curve amplitude and a two-cell half-width. They end at local rows
40..45 in radius-four alcoves. Each has one 40-health fox, using its
existing false/real tell and damage, guarding a wrapped bundle. The finite
Shingle cache bits record the bundles; the den shows their count as
“a bundle”. The second cache still gives its marrow. No new consumable
effect is invented.

These implement recommendations R-cb02a-1 A, R-cb02a-2 A, R-cb02a-3 A,
and R-cb02a-4 A (bundle identity from finite cache bits), not decisions.

`--world-audit` checks 50 seeds at both fields (80 and 200; 300 rows). Its
terrain-layer census covers every camera position of every area at the
field's own screen, both tiers, including the bounds' forest fill:
`EMPTY_MAX=0` forbids blank or foreground-equals-background forest cells,
`FLAT_MAX=2` bounds a run of identical adjacent foliage cells (measured
one) and `TEXTURED_MIN=90` is the least share of forest cells outside such
a run (measured 100 %). A separate tile flood from the first den over the
coast's whole extent reaches every alcove cell and checks every reachable
cell is within `WALK_MAX=200` cardinal steps of the thorn route, a branch
or a cache (measured 130 at field 200, 119 at 80). The bank step bar is one
cell; the inland straight-run bar remains twelve. These are proposed
regression limits, not a claim about the time a fight takes.


## The grove, 2026-10-25 (cb02b, proposed)

The maintainer's play of cb02a: the forest was flat green tiles beyond the
corridor, both jetties stood in view, no branch left the coast, and the
second area rendered as a centred rectangle whose path ended at its edge.
All values below are proposed; every ruling is a recommendation the lane
implemented, not a decision.

| layout or mechanic | value |
|---|---|
| the field | the terminal's columns when the journey began, floor `FIELD_MIN=80`; saved (schema 2) and carried in replays; a resize or a resume in another terminal never moves it (R-cb02b-4 A) |
| the coast's extent | `coast_extent(field) = max(120, 3·field/2)` each way from the spawn: 120 at 80 columns, 300 at 200; the jetty at `±(extent + 0..2)` enters view after a walk of one screen (R-cb02b-1 A) |
| the inland width | `half_width(field) = field/2 + 8` each side: 48 at 80 columns, 108 at 200, so the grove fills the screen it was made for (R-cb02b-6 A) |
| the coast's branches | four, two each side of the thorn path (R-cb02b-3 A): mouths at `±(extent·k/3 + jitter)`, k = 1 near, 2 far, the seed jittering each by up to three cells; alcoves at rows 40..45, one 40-health fox and a bundle each (R-cb02b-5 A: no new consumable; the second cache keeps its marrow) |
| the open canopy | on the coast within `OPEN_REACH=16` cells of the shore, the thorn route or a branch; the wood beyond is deep and solid, textured like the rest, so every walkable cell is a bounded walk from a route |
| the cross path | inland, bounded to x = ±33: it ends at the log and the hedge, never at the area's edge |
| the deep forest | the canopy's four glyphs in the deep green with trunks among them, inside and beyond every bound (R-cb02b-7 A: one tone for the deep wood, two for the open canopy) |
| foliage variants | `2·((x+y) mod 2) + hash(x, y, 2)`: adjacent foliage cells never share a glyph set, so the texture has no flat run by construction |
| the census | `coast.texture`: FLAT_MAX 2, TEXTURED_MIN 90 %; the coast flood from the river (`COAST_TOP=-16`) with the branch centrelines as targets, WALK_MAX 200 |
| the silhouettes | pixel bitmaps at two by four a cell; the cub 8×16 (four cells by four north, eight by two east), the fox 8×12, the deer 8×16, the weasel 4×12, the hawk's shadow 8×4, the bundle 10×12; east, south and west are the north drawing turned (R-cb02b-2 A); hit envelopes unchanged |

The schema-2 save adds one line, `field N`, before the check; a schema-1
file is `save_version`; a field outside 80..10000 is `save_corrupt`. The
cache bits are relaid: the coast's four first (bits 0-3), the thicket's
two (4-5), the meadow's two (6-7).


## The gait, 2026-10-25 (cb02c, proposed)

The maintainer's word on cb02b's build: "This is a big improvement. But it still needs work. The branch
paths should be the same color as the coastline/forest paths. The cub moves much too slowly and its tail
oscillates too quickly. Make it natural. Enemies should never overlap with the cub. They should have
collision to prevent weird attack moments where the enemy is behind the cub and can't be hit." Every value
below is proposed; every ruling is a recommendation the lane implemented, not a decision. The numbers are
`cub --measure`'s (before: `notes/cb02c-prediction.txt`).

**The path.** Every path cell draws one ground per area (`forest.path_kind`, `docs/PALETTE.md`): the coast's
four branches, their alcoves and the log's branch were the forest's grass; they are the shore's gravel, as
the shore and the thorn route are. `--world-audit`'s `path_off` holds every walkable path cell of every area
to the path's styles over fifty seeds at both fields.

**The pace (R-cb02c-1 A).** The dial `WALK_PERCENT` 110 → 165, half as fast again; the turn rate,
acceleration, braking and the foes' speeds are its products, so cornering, starting and stopping keep the
feel cb01b's play accepted, only quicker. No sprint is bound (the ratio the dial keeps is the sneak's half).

| measure (30 Hz, paw 1) | before | after |
|---|---|---|
| trot, straight | 42 FP/tick, 4.92 cells/s | 63, 7.38 cells/s |
| diagonal | 4.80 cells/s | 7.28 cells/s |
| a quarter turn | 4 ticks at 4.83 cells/s, radius 0.41 cells | 3 ticks at 7.30 cells/s, radius 0.46 |
| to the trot / to a stop after the hold | 11 / 5 ticks | 11 / 5 ticks |
| sneak | 21 (2.46 cells/s) | 31 (3.63 cells/s) |
| foes' pursuit / retreat | 44 / 48 | 66 / 72 |

The fox keeps up on the straight and loses in the turns: the foes keep cb01b's turn rate (16 against the
cub's 24), and a turn a foe cannot make in one tick checks its run toward half its pursuit (R-cb02c-6 A;
without it the split turn rate alone left the fox even through a turn). The duel (`measure.duel`: the cub
and a fox from one start at full speed): thirty ticks east, the fox 0.35 cells ahead; eight ticks east then
twelve turned south, the cub 0.48 cells further south. A fox steering at a zigzagging cub it can see still
cuts the corners and closes (pursuit's geometry): a zigzag does not shake a fox, a turn wins ground from it.
The hawk's tell, stoop and recovery are unchanged.

**The tail (R-cb02c-2 A).** The wag is tied to the gait: one wag per two strides (`GAIT_CYCLE`), the paws
stepping once each half stride; the tail passes five frames walking (two pixels each side), three in the
standing sway (one pixel), and the plain tier's `,` swings side to side on the same cycle. Measured from the
frame (`cub --measure`): before, 4 ticks walking (7.5 Hz, two frames) and still standing; after, 26.5 ticks
walking (0.88 s), 53.7 sneaking, 59.5 standing (1.98 s), 18.0 at a grown paw's trot (paw 10, 92 FP; 0.60 s).

**Bodies (R-cb02c-3 A, R-cb02c-4 A, R-cb02c-5 A).** A creature's body is the rectangle of cells its drawing
covers (`silhouette.footprint`): the cub four by four facing north or south, eight by two east or west; the
fox four by three (six by two); the weasel two by three (six by one); the deer as the cub. The hawk's
shadow is not solid. No two bodies share a cell, ever:

| rule | value |
|---|---|
| the mover yields (R-cb02c-3 A) | a step into a body is not taken: the cub moves first and yields to a body standing; a foe moves after and yields to the cub where it now is, so a tie goes against the foe |
| a swing (R-cb02c-5 A) | the cub's body takes its turn's or its attack's facing only with room: a foe in the swing steps aside along the line between them (a quarter cell at a time, up to eight, the nearest of eight lines first); with no room the body keeps its facing that tick. A foe's own turn is its own to clear, or it keeps its heading |
| settling | the start of every tick, an area's entry and every reset settle what a fixture or a spawn left overlapping, in the foes' order |
| reach (R-cb02c-4 A) | a reach of n cells is n − 1 clear cells between the bodies: a bite or a foe's strike 2 (one clear cell), a lunge or a heavy 4; in sight unless the bodies touch, and ground under either body never stands between them. So a foe on the contact ring is always in a bite's reach, aimed its way: never behind the cub out of it |
| a touch | a foe whose body touches the cub's knows where it is, whatever stands between their middles |
| presentation | the bite's, lunge's and heavy's leaps stop at a drawn body (a fading one too); the third bite's head shake holds against one |
| guards | a cache's guards stand a body's width apart along their branch (two cells for weasels, four for foxes), never one inside another |

The census (`census`: the footprints read from the drawings, never the collision code) over the 47
real-key scripts: before, a foe's drawing shared a cell with the cub's on 1,879 ticks (1,935 foe-ticks,
1,043 of them out of an aimed bite's reach) and foes overlapped each other on 71,580 pair-ticks; after,
0, 0 and 0, with 513 foe-ticks of bodies touching, every one in reach. `--body-audit` replays the encounter
scripts' keys and a three-weasel swarm from behind in fifty seeds at both sizes: 360,956 ticks, no overlap,
no contact out of reach, no foe in another; the swarm reaches the cub and is fought in all hundred worlds.


## The pace, +20 %, 2026-10-26 (cb03, proposed)

The maintainer's standing word on cb02b's build: "The cub moves much too slowly … Bump the cub speed by
20 %." The dial `WALK_PERCENT` 165 → 198, the one constant; the turn rate, acceleration, braking and the
foes' speeds stay its products as cb02c left them. The numbers are `cub --measure`'s (before:
`notes/cb03-evidence/measure-before.txt`; after: `measure-after.txt`).

| measure (30 Hz, paw 1) | before (165) | after (198) |
|---|---|---|
| trot, straight | 63 FP/tick, 7.38 cells/s | 75, 8.78 cells/s (+19 %: the integer floor of 75.7) |
| diagonal | 7.28 cells/s | 8.77 cells/s (the instrument now measures the diagonal from a standing start; cb02c's window met the woods at this pace) |
| a quarter turn | 3 ticks, radius 0.46 cells | 3 ticks, radius 0.55 |
| to the trot / to a stop | 11 / 5 ticks | 11 / 5 ticks |
| sneak | 31 | 37 |
| foes' pursuit / retreat | 66 / 72 | 79 / 86 |
| paw 10 trot | 92 | 111 |

**R-cb03-5 A, the gait.** The wag and the paws are tied to the ground covered (cb02c), so a faster cub
would wag faster: 22 ticks a wag at the trot, a tail frame of two ticks, the flicker the maintainer's word
retired creeping back at a grown paw. Instead the stride and the standing sway scale with the dial from
cb02c's 165 (`GAIT_BASE_PERCENT`): `STRIDE` 832 → 998 (3.9 cells, still under the body's four), `SWAY_V`
28 → 34, so the wag keeps its 0.9 s at the trot (26.6 ticks measured), 0.6 s at paw 10 (18.0) and 2 s
standing (58.75), and a frame holds three ticks or more at the trot. B, the stride kept, was the faster
wag. The overlap census over the regenerated real-key scripts stays 0 / 0 / 0.

## Posture as HUD, 2026-10-26 (cb03, proposed)

Campaign innovation 5 (pack's ART.md was read for the idea, never copied): the numbers leave the running
HUD. Health is the cub's gait, ears and tail (R-cb03-2 A, four bands as frame sets of the one silhouette:
`sim.hurt_band`, `silhouette.cub_posed`; `docs/ART.md` draws them); stamina is the breath: standing, the
shoulders and haunches widen a pixel each side on the in-breath, one breath in two seconds fresh
(`BREATH_TICKS` 60), 1.2 s tired, and spent the pant's mouth opens and closes every four ticks
(`PANT_TICKS`). The fur still dims when tired or spent. The health tail mark (cb01) is gone with the bars.
The numbers show at a den and on the death card only (R-cb03-3 A); `--hud` (B, a debug flag off by
default) puts cb01b's bars back beside the scent. The scent counter stays the one number on screen; the
area name shows for `ENTRY_TICKS` (three seconds) at an area change; the lock-on reticle is unchanged.

| band | health | ears | tail | trot |
|---|---|---|---|---|
| full | 3/4 and above | out | the full wag, two pixels each side | both paws out a step |
| hurt | 1/2 and above | back along the head | half the wag | both paws |
| badly hurt | 1/4 and above | laid back at the neck | hanging still | one paw out a step |
| dying | below 1/4 | flat; the head drops like the sneak's | hanging still | none: the trot is a stand |

## The score, 2026-10-26 (cb03)

`docs/SCORE.md`: ten original parts, the cue schedule (an area's loop, the title, the den's rest, a boss
theme as the duck, the death sting once, the resume at the den), `--mute`, `CUB_SOUND=0`, the `m` key, and
the music path today (R-cb03-1 B: WAVs per part played by cue, since lr01's engine streams nothing).
