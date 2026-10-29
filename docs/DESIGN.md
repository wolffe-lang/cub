# Design constants

## The pouch (cb15, 2026-10-28)

The second playtest's consumable design supplies these numbers. `i` pauses
combat and opens the pouch over the field; no new running-HUD strip is drawn.

| item | cap | effect |
|---|---|---|
| yarrow | 5 | stop bleeding; heal 10 immediately, clamped |
| marrow | 3 | heal 30 in 60 simulation ticks, one health every second tick; damage cancels the remainder |
| pine | 3 | remove the existing trail; lay none for 600 ticks; the lynx disengages |
| a shard of ice | 3 | living locked foe, else nearest foe in the forward ninety-degree cone, within 6 cells; movement halved for 90 ticks |
| the mother's tuft | 1 | passive: consume once on death, retain carried scent, clear the replaced mark; save its use count |

Bleeding has a bounded sixty-tick state, one damage per tick; twenty still
idle ticks lick it away. Yarrow cures it immediately. No actor applies it yet;
the foes pass wires attacks to `sim.bleed`. Water and invulnerability retain
their existing rules. A blocked ice throw and Consume on the passive tuft
keep the item. The Burn calls `sim.melt_ice` on entry when its area lands.

Ground pickups occupy cells, are collected with `r` on their exact cell,
and never intercept a den's `r`. A full stack keeps the pickup. Drop leaves
one; Discard removes one. Ground order, positions and area discovery are
saved. The pool is bounded to **128 pickups**; a full pool refuses Drop and
a full-stack cache reward rather than destroying inventory. Lore appends
stable ids once in discovery order, up to **32 lines**, and is read through
the rest menu's Lore row. Lore ids are append-only: existing coals/frame/stump
lines are10/11/12 without wording changes; cb14's lines are 13..31 (the five
areas', the Howe's five standing stones', the nine alcoves'), which fills the
32 slots: the next line (cb16's) needs a wider save, a format bump.
Menus freeze effect/attack/lifetime clocks and
clear held movement on exit; marrow never catches up for paused ticks.
The opening and closing ticks are both paused, including queued bite links,
the six-tick combo grace, riposte, poise and offscreen loot lifetimes.

`pouch.take_one(mut held_count, kind)` removes one from a given stack and
returns its kind, or -1 when absent/invalid. `sim.take_one(mut s, kind)` routes
all five stacks, including the two legacy Sim fields; taking never consumes
an effect or creates a pickup. `pouch.leave(mut pouch, area, x, y, kind)` places
one at the given **cell** point, not fixed-point coordinates, and returns false
without placement when full or invalid. These are the marten's carry/drop
hooks; no pick-order or new save field is introduced.


Foe drops are stable seed/area/spawn rolls: weasel yarrow10%, hawk yarrow15%,
fox marrow10%. The future boar-kin25% and otter20% use the same roll hook.
Until the new areas land: seven seeded meadow sprigs (roughly36 cells apart),
six seeded Bramblehold marrow pickups, five river shards and the first
tuft four cells east of the first Bramblehold den (the Ember approach). Stand/Burn/Mere/Howe placement uses `seed_alcove`; no
forest generation or enemy damage envelope changes here.


Tuning values in `src/sim/sim.lu`, `src/terrain/terrain.lu` and `src/forest/forest.lu` are mirrored
here with the date they were set and their source; named constants hold the gameplay bars. The design bible (`sprints/lair/cub/design.md` in the planning
repo) is the oracle; a number is **proposed** until the maintainer's play says otherwise (R-CB-7), and new proposals here are submitted for review; the private bible is not edited by this lane.

The connected Shingle, Bramblehold and Larkmeadow share one fight, rest, death and persistent-journey loop.

## Death card and scent count (cb12, 2026-10-27)

Death still writes the scent mark and archive at the fatal tick. Only the wake moves:
`DEATH_FADE=30` ticks dissolve to black, then the original seven-row red `FALLEN`
letterform, doubled to70×14 cells so closing eyes visibly crop it, holds
for `DEATH_HOLD=20` ticks. Any ordinary key from age50 skips, consumed without a
move; `q` skips too, while Ctrl-C remains an interrupt. The opening's rounded eyelids
and `opening_aperture(840..510)` run backwards, one original frame per tick. The
fully closed frame is age380; without a skip the den wake is age381 (`DEATH_TICKS`).
Older death-card descriptions below are superseded by this sequence.

The HUD counter is presentation, not currency. `counter.Count` visits a contiguous
integer batch per simulation tick, using `floor(distance * age / min(distance,20))`.
A gain of8 takes8 ticks;300 takes20 ticks with15 rendered integers a tick. Spending
uses the same schedule downwards; a mid-count change retargets from the last rendered
integer. The big number remains visible at rest; the allocation ledger keeps its
exact currency and pending cost. The sim, saves, score and replay see the exact new
scent immediately. Display state is not saved; loading starts settled at the saved
value. Neither rendering frequency nor wall time advances it (R-cb12-1 A).

Live intermediate integers repaint only the old/new counter rectangle using the
engine's public CUP/SGR/UTF-8 builders and a cached counter-free underlay; the tick's
last integer goes through the ordinary full-frame renderer. The underlay is drawn
once per batch, not once per integer. Neither extra simulation/score/save/replay
ticks nor intentional sleeps are used. This implements the partial-repaint choice
of R-cb12-2, not a stretched count or dropped frames. The original full-frame path
measured63.673/66.215ms per wide1000-gain batch and is retained as the before table in `notes/cb12-evidence/counter-cost-before-partial.json`.
`cb12-counter-frames` measures whole-batch wall time, requires1000 flushed numbers
in20 ticks with0 late/catch-up frames at80×24 and200×60, and compares the final
terminal model with ordinary full-frame output. Its results are in
`target/pty/cb12-counter-cost.json`.

Measured on nomad's release binary,2026-10-28, a1000 gain (50 integers/tick):

| tier / size | before: max render+flush sum | after: max whole-batch wall time | after ticks / late frames |
|---|---:|---:|---:|
| rich80×24 |10.341ms|0.795ms|20 /0|
| rich200×60 |63.673ms|4.263ms|20 /0|
| plain80×24 |9.107ms|0.709ms|20 /0|
| plain200×60 |66.215ms|3.834ms|20 /0|

The after measurement includes the underlay, all integer repaints, trace writes
and the final ordinary frame; it is stricter than the before sum. Every after
batch fits the33.333ms tick, and every1000-value run flushes all1000 integers.
Both raw tables are retained under `notes/cb12-evidence/`.

Headless script fixtures and walkers press the ordinary skip after the minimum
hold; `--full-death` or a `# full-death` script comment keeps the full card. Actual
live play and `--replay` retain recorded key timing. `# counter-frames` enumerates
every integer's frame in a headless fixture for the two-tier goldens.

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
| den | within three cells of a seeded den; a rest resets health, stamina, water, every area's ordinary foes, trail and holds; area changes never revive slain foes, while wounded survivors heal and return home on re-entry (R-cb04f-1 A); death at the last-den respawn resets foes as a rest does (R-cb04f-2 A); beaten bosses, gate, caches, shortcuts and mark persist |
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
| opening | 900 ticks / 30 seconds; shot table below; one decoded key skips the entire opening without also performing a move |

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
`--save-cut` are explicit test witnesses. Quit/interrupt before the stage's
commit tick cancels only that owned stage, preserving the previous journey.
A quit key advances the simulation tick: if an existing stage is due on
that tick, commit it before exit. Quit never prepares a new stage. This
keeps an acknowledged opening skip durable even when quit arrives on the
very next tick; it does not shorten the explicit delayed-write witness.

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

## The bosses and the ghosts, 2026-10-26 (cb04, proposed)

M-CB4: three more areas, four bosses, ghosts from the death replays, the title and the end. Every value
below is proposed; every ruling is a recommendation the lane implemented, not a decision. The fairness
numbers are `cub --boss-census`'s (fifty seeds at both sizes, the scripted real-key fighter in
`src/fight/fight.lu`); the frames are the goldens'.

**The three areas** (`src/forest/forest.lu`, the grove's texture rules: a carved spine, bounded meanders,
two foliage tones, one path kind per area, every walkable cell a bounded walk from a route). The area graph
is a line with the shortcuts as chords: Shingle – Bramblehold – Larkmeadow – the Teeth – the Shallows –
Gravehollow (`forest.AREAS` 6, `DENS` 7, `EDGES` 9).

| area | ground | the arena | den | shortcut |
|---|---|---|---|---|
| the Teeth (3, the crags) | stone where the hash runs over 100 or the height under 10, gravel paths, trunks and a cold canopy | a bowl at row 112, radius 12, with three stone pillars 5–7 cells off the spine (the lynx's ledges; flipped to the far side when a pillar would leave the bowl) | 4, the ledge cleft | edges 4/7 Larkmeadow ↔ the Teeth, bit 4, opened by the lynx |
| the Shallows (4, the river) | the river west of its bank (`river_bank` = the spine − 14 + a slow curve), reeds along it, three shingle rows | the ford at row 112, radius 14, centred four cells inland of the bank: its water half is `SHALLOWS`, walkable at half pace | 5, the willow root | edges 5/8 the Teeth ↔ the Shallows, bit 8, opened by the elk |
| Gravehollow (5, the old den) | trunks, a dark floor, canopy, old scent marks on the grass | the old den's bowl at row 112, radius 12 | 6, the cold den | edge 6 the Shallows ↔ Gravehollow; no shortcut: the end |
| Old Snag's clearing (in Bramblehold) | the thicket's own | a clearing at (30, 60), radius 11, off a branch at rows 59..61 | — | bit 1 (the log), opened by the boar |

The den ids 4..6 are the new areas' (7 spare); cb03a takes 8..15 for extra dens in the existing areas and
widens the lit-den bound without a new field (the coordinator's word, 2026-10-26): `journey.lu`'s
`last_den` 0..6 and `lit_dens` 1..127 are the seam to widen at the rebase.

**The bosses** (`sim.lu`, "The bosses"): big bodies on cb02c's rules, their footprints the drawings'
rectangles (`silhouette.foe_size` 4..7), never inside the cub's, the contact ring inside every attack's
envelope. A boss holds its arena: every step, run and yield is refused outside it (`boss_may_stand`, the
boss clause in `push_out`); the cub may leave, and a boss out of engagement (the cub out of the arena and
more than four cells off) trots home and waits. Phase two begins under half health. Every attack is
telegraphed (`CROUCH` for its windup, then `STRIKE`, then `RETREAT` for its recovery); a parry inside its
window turns a parryable strike into a thirty-tick stagger with the riposte open; the one unparryable
attack is beaten by the dodge's frames. Hits spend poise (`POISE` 60; a lunge or a heavy into a
travelling attack staggers at once).

| boss | arena | health, speed, turn | attacks: windup / active / recovery, damage, reach | phase two |
|---|---|---|---|---|
| Old Snag, the boar | the clearing | 240, 54, 8 | gore 14 / 3 / 20, 14, 3, parryable; charge 24 / 18 / 30, 22, 2, unparryable, 1.5 cells a tick along its line | the gore's windup 12; a second charge after the first |
| Whisper, the lynx | the Teeth | 140, 90, 20 | swipe 13 / 2 / 18, 12, 3, parryable; pounce 15 / 6 / 24, 16, 2, parryable, 5 cells a tick; rake 18 / 8 / 20, 10, 4, unparryable | every windup three ticks shorter; it keeps to its ledges (the pillars) until the cub is within nine cells |
| Alder, the elk | the Shallows | 400, 48, 10 | sweep 20 / 4 / 30, 18, 5, parryable; stamp 24 / 2 / 36, 24, 3, unparryable, all round; charge 18 / 14 / 30, 20, 2, parryable, 1.25 cells a tick | the sweep's windup 16 |
| Ashgrim, the shadow alpha | Gravehollow | 300, 63, 16 | bite 12 / 2 / 10, 14, 3, parryable; lunge 15 / 4 / 18, 20, 2, unparryable, 4 cells a tick | windups three shorter; the howl 20 / 1 / 10, heals 30 unless its windup is punished; the mirror: it guards a bite begun within two cells (the cub's bite turned, its riposte open) and hops from a lunge or a heavy within six, on a roll |

| rule | value |
|---|---|
| the bar (R-cb04-2 A) | only a boss has one: row 1, `Name [####................]` of twenty cells in the boss's colour, ` !` in phase two; drawn while the boss is engaged (the cub in the arena or within four cells, so at the mouth under a charge too), gone when it has let the cub go |
| a rest (R-cb04-3 A) | heals an unbeaten boss to full, phase one again; a beaten one stays beaten |
| beaten | the save's `bosses` bit, its shortcut opened (`boss_shortcut`), scent 120 / 200 / 300 dropped (the alpha drops none: the end), the `boss.beaten` cue; the drawing fades over 45 ticks; the alpha beaten sets `end` |
| the score (cb03's slot) | `s.boss` is the engaged boss's index 0..3 (`sim.boss_theme`), −1 otherwise: cb03's `boss-boar` .. `boss-alpha` parts replace the area's loop; the new areas' slots `crags`, `river`, `old-den` stay silent until their parts exist |
| cue hooks | 4..7 `boss.boar` .. `boss.alpha` on engagement, 8 `boss.beaten`, 9 `howl` (the end), 10 `title` |

**Fairness** (`--boss-census`, `tools/gameplay.py`'s gate: every world won within five lives, every
parryable telegraph at least `PARRY_WINDOW` 9, no boss tick outside its arena). The fighter is a script
of real keys from the boss's den: the walker's plan to the arena, a parry when a parryable standing
attack lands within eight ticks, a lunge into a parryable charge, a step aside and a dodge timed to the
landing for the unparryable one, free bites in a stagger, water under half health, a stamina reserve of
18 kept.

| boss | attempts to win, 100 worlds | hits taken by attack 0 / 1 / 2 | unparryable hits | shortest telegraph by attack (ticks) |
|---|---|---|---|---|
| the boar | 1: 86, 2: 12, 3: 2 | 120 / 66 / 68 | 134 | 12 / 24 / 12 |
| the lynx | 1: 100 | 44 / 2 / 14 | 14 | 10 / 12 / 15 |
| the elk | 1: 100 | 40 / 2 / 2 | 2 | 16 / 24 / 18 |
| the alpha | 1: 100 | 228 / 0 / 0 | 0 | 9 / 12 / — (the howl unseen) |

(At cb02c's pace, before the rebase onto cb03's +20 %: the boar 1: 78, 2: 10, 3: 10, 5: 2 with 180
unparryable hits; the others unchanged in attempts. `notes/cb04-evidence/boss-census.txt` and
`boss-census-final.txt`.)

**Ghosts** (R-cb04-1 A: the last five deaths, fading with age; `src/ghost/ghost.lu`). A death's archive
carries a trailer: for each of the last `TICKS` 90 ticks the words `ghost-x`, `ghost-y`, `ghost-face`,
`ghost-pose`, `ghost-area`, and `ghost-death N` (the death's serial) at the death tick, merged into the
replay in tick order. The engine's reader (`replay.from_text`, `replay.args_at`) rebuilds the frames; the
sim never runs for a ghost. At the spot a dim cub (plain `x`) stands in a grey by rank (251, 248, 245,
242, 239 dim; plain 7 then 8); within `NEAR` 8 cells the death's last three seconds play as a ghost
sprite, resting `REST` 60 ticks between plays. The set is read from `--ghost-dir` (live `~/.cub/ghosts`)
at the start and after each death; a file that is not a cub replay, has no trailer (a death archived
before cb04) or is another world's (R-cb04-5, proposed: a ghost belongs to its seed, since its positions
mean nothing elsewhere) is skipped by name on standard error. A headless case names its archive on a
`# ghost-dir DIR` line, read, never written. The engine's reader lacked nothing but the game's words;
`args_at` is linear in the events, so a ghost's frames are read once at load.

**The title and the end.** `--no-title` starts the game as before; otherwise scene 2, the title: the four
silhouettes lit when beaten (the save's `bosses`), the keys, "any key begins" (the opening if unseen); after
`TITLE_IDLE` 300 idle ticks the committed demo (`tests/cases/demo.pk`, embedded by `tools/embed-demo.py`
as `src/demo/demo.lu`) plays behind it. The alpha beaten, 45 ticks on, scene 3: three 90-tick frames of
the ford crossed as a wolf (the silhouette one size larger, 12×24 against the cub's 8×16; the cub draws
as the wolf from then on), the `howl` cue, then the card: time (`played` ticks across sessions), deaths,
scent lost (the mark's scent lost to a second death), bosses n of 4. `r` keeps playing (R-cb04-4 A) and
`q` leaves; the save records `end`.

**Save schema 3** (`journey.lu`, 53 words): schema 2's fields and one line, `bosses N end N played N
lost N`, before the check; `last_den` implemented ids 0..6 and 8..11, `lit_dens` a 16-bit mask (reserved bits refused), `shortcuts` 0..15 (bit 4 needs the lynx,
8 the elk), `mark_area` 0..5, `end` needs the alpha's bit; a schema-2 file is `save_version`, never read
as 3. A live recording begins with `journey 2` and `saved-0` .. `saved-28` (the four new values last).
The world checks hold every save under 512 bytes.

## Findable dens (cb03a, proposed)

Rebased over cb04 at `1855009b2ed0a7b1a0a4fb3cbd00a9629bf5adc6`.
The earlier schema-2 plan is superseded: cb04 landed schema 3 first.
Its boss/ghost/title/end state is retained. The boss bar stays on row1,
starting at column43 or further right, beside the player bars and scent.


Schema 3 from cb04 and all its fields stay unchanged. Den ids 0–3 retain their
meanings. Ids 4–7 are reserved for the later areas; 8–15 are reserved for
extra dens in the existing three areas. Currently 8 is Bramblehold's
coal roots; 9–11 are Larkmeadow's low embers, ash shelter and last warm
hollow. `den_position(seed, id)` remains the position API. `lit` is a
16-bit mask; `den` must name an implemented den. No optional field is needed.

A hard cluster is three or more foes, or any pair containing a hawk.
The trio's branch rejoins the main path before the new den at local row
66–69 in each inland area. The first meadow hawk pair shares that refuge;
the other pairs precede dens at 90–93 and 146–149. Initial entry dens
retain the 30-cell quiet radius; post-fight refuges are deliberately closer.
Every den has a warm seven-cell ground patch, hollow silhouette, ember,
smoke, and a scent-of-home line within ten cells. Rest/save/growth and the
number card use the same rules at every id.

Bramblehold's centreline switches between seeded lateral anchors 18–22
cells either side, every 24 rows after the first 16. The independent dot
product census counts only turns of at least 90 degrees. Six open rooms,
7/9/11 cells across, sit at rows 8,22,52,68,92,134: entry den, shortcut
view, cache branch, post-cluster den, briar den, and foe cluster. Their
centres sit three cells off the path and their floor keeps the area's
textured path palette. The log shortcut and cache branches remain open.

## Meadow tells and pursuit (cb03a, proposed)

The boomerang-like form is consistent with the hawk's one-row diamond
shadow moving around its orbit; it was not a projectile. The tell now
keeps beak, connected wings, body and tail on both tiers. Deer had an
unbounded flee whenever the cub came within seven cells. They now spend
two of their sixty stamina per fleeing tick, then stop and turn for thirty
ticks; a caught deer cannot counterattack. Meadow ground hunters end
their existing 24-tick retreat with the same thirty-tick free-hit pause.
Their retreat cap remains 86 FP/tick, below the proposed sprint120.

## Directional combat and sprint (cb03a, proposed)

Space retains the fifteen-tick recent-arrow window and all eight aims;
lock still overrides arrows. The committed cone is rotated −11/+11/0
heading units (15.47 degrees) across the three-hit combo. Its aperture
stays ±45 degrees. `x` commits the cub's facing, never arrow aim, and
steps back one cell at windup age3, two at age6, then takes the unchanged
age9–11 leap and reach4. Every presentation offset clips against bodies.

Hold `c` to sprint: the first press dodges immediately; a repeat within
thirty ticks starts the inferred hold after the dodge. There is no key-up
in this terminal protocol, so two taps within one second also count as a
hold. Release expires by the engine's repeat window. Sprint is 8/5 trot
(120 FP/tick,14.06 cells/s at paw1), twelve stamina per moving second,
no regeneration while sprinting, stopped at empty. Space during sprint
commits a forward snapping lunge: cost36, reach4, damage twice bite,
3/3/10 ticks. Its three active frames shake the head left/right/left.
These implement R-cb03a-1 A and R-cb03a-3 A, pending play.

## Always-visible bars (cb03a)

The playtest ruling restores two labelled twelve-cell bars at top-left:
red health above green stamina, outlined with box-drawing on rich and
brackets on plain. Scent sits beside them; the area flash keeps its
three-second duration beside the bars. Health/stamina posture remains.
`--hud` is retired; bars cannot be disabled. Den/death numeric cards stay.

## Approach and cone integration (cb03a)

All eight committed aims times all three combo hits are tested against a
foe dead ahead at body contact:24 hits. The slant rotates the hit envelope
and head travel, not the body's quarter; a slight head swing must not flip
the body90 degrees at a diagonal boundary.

The switchbacks exposed an approach that cut across Old Snag's arena
before reaching its west mouth. A carved strip west of the arena, x12–18
from row60 through98, keeps the shortest den approach outside the fight.
The arena itself is unchanged. R-cb03a-4 A recommends that a scripted walk
whose start and destination are outside an unbeaten boss arena also plans
outside it, instead of detouring around an ordinary foe through a boss.
This is implemented in the real-key walker, with no movement override.
The inherited lynx seed18/field200 row had won with zero measured fight
ticks: the generic approach had killed it before the fighter began.

The quarter-cell path-arrow threshold could retain a diagonal when a
blocker was nearly cardinal (old-den seed5: bearing128, aim96). After the
contact tests passed, the walker gained ordinary Tab/Space/Esc keys:
commit intentional lock aim, then release before following the path.
`--mouth-audit` checks all400 actual den-to-mouth walks; the existing
five-life fairness bar and nine-tick parry bar are unchanged.

## Visible pickups (2026-10-26, proposed)

`PICKUP_MARGIN = 1` cell is the shared collection margin. A pickup cell
inside the cub's drawn body or its one-cell contact ring is reachable,
including corners and fractional positions within those cells. The
turned body and the grown wolf both use their actual footprints. This
implements recommendation R-cb04c-1 A; nose growth can widen the same
helper later. Death scent, ordinary scent and cache reach use it; cache
collection still requires `r` and no live guard within six cells.

The existing death recovery path remains in `sim.step`: collect once,
restore the dropped amount, clear the mark. A mark in another area is
not collected. A second death replaces the first mark, counting the
first amount as lost. No new persistent field or replay schema is needed.
A local burst remembers only its tick, position and area, not save state.
Fresh ordinary drops stay for at least their first rendered tick before
collection, so a kill never silently bypasses the pickup drawing.

Presentation bounds: four motes per orb, x=-3..3 and y=-5..-1 cells,
96-tick seeded periodic drift; halo x=-3..3, y=-2..2. The recovery burst
is eight sparks, radius 1..3 cells, twelve ticks. Ordinary drops keep
the 300-tick lifetime, with the bright core throughout rather than a
hard-to-find one-cell dot in its second half. `--look-audit` is a
50-seed both-tier camera walk over every route row and every cache,
shortcut and former label site, not a claim that the camera was moved
there by player keys; the gameplay and pty rows test that separate path.

## Dens, levels and found water (cb04a, 2026-10-26)

This section supersedes the older den reach, linear growth cost, stat cap,
starting water and save-schema descriptions above. Movement and the bars
are unchanged.

The split roots (den1) now lie on Bramblehold's downstream switchback,
rows114–117, rather than rows7–10. `cub --den-census` floods the actual tiles
from the entrance, independently of the centreline formula, over seeds0–49
at fields80/200. It requires entrance-to-den distance to be at least a third
of both entrance-to-exit distance and centreline length.

Within three cells of a den's centre, `r rest` appears. `r` enters the
full-screen rest scene, heals, refills found water and resets encounters;
`r` or Esc leaves without resting a second time. The world does not advance
while the scene is open. Arrows and attacks there are ignored rather than
saved as held movement. The three-cell centre radius is deliberately not
the pickup body's contact ring. Death returns to the last den rested at, with fresh ordinary encounters
in every area. Save resume returns there healed and refilled, but now retains
the slain set (cb04f); it is not a den rest. The death mark stays at the
death's area and position; a second death replaces it (R-CB-1).

The basic rest, five-stat growth, water action and last-den respawn already
existed. The inaccessible interaction was a one-cell centre radius under a
four-by-four (or eight-by-two) cub drawing. A visible-edge `r` never rested,
so it never updated `last_den`; death correctly returned to the still-current
start. Water started at three but had no field charge display or discovery.
The live `den-contact` and `den-checkpoint` rows distinguish entry from wake.

### Shared levels

R-cb04a-1 A recommendation: keep heart, wind, fang, paw, nose. Each starts1,
soft cap10, hard cap40. Total level starts1 and is `sum(stats)-4`.

| stat | effect through10 | after10 |
|---|---|---|
| heart | `40 + 12*h` health | +3 per point |
| wind | `60 + 10*w` stamina | +2 per point |
| fang | `6 + 2*f` bite | +1 every two points |
| paw | `round((36 + 2*p)*WALK_PERCENT/100)` FP/tick | +1 unscaled FP every two points, then the same pace dial |
| nose | `8 + 2*n` scent visibility cells | +1 cell every two points |

The smaller lock radius is `8 + min(n,10) + max(n-10,0)/4` cells; dodge's
secondary paw bonus is `6 + min(p,10)/2 + max(p-10,0)/8` ticks. Integer
plateaus are shown honestly in each stat's next effect. Growth only spends
inside the den; an unaffordable or capped choice spends nothing.

R-cb04a-2 A recommendation: a single shared purchase sequence, not five
independent prices. With current level L>=12,
`cost(L)=round((0.02*L^3 + 3.06*L^2 + 105.6*L - 895)/20)`.
Thus **k=0.05**. This is the published Dark Souls level-cost number series
used as a shape, not game code or assets (reference: Dark Souls Wikidot,
“Soul Level”, https://darksouls.wikidot.com/soul-level). Cub's own table
below12 joins the cubic; first purchase costs three8-scent weasels.
Rounding is positive integer half-up, identical on both backends.

| current L | cost to L+1 | current L | cost to L+1 |
|---:|---:|---:|---:|
|1|24|11|40|
|2|25|12|42|
|3|26|13|52|
|4|27|14|62|
|5|28|15|72|
|6|30|16|83|
|7|32|17|94|
|8|34|18|106|
|9|36|19|118|
|10|38|20|130|

Schema4 keeps the prior boss/mark/cache/den fields and adds `level N`.
Growth is1..40, capacity is0,2 or3, and the level must agree with the five
stats. Schema1/2/3 are `save_version` by name, never reset into a new run.
Recordings use `journey 3`, `saved-0` through `saved-29`. The level is
redundant by design so malformed progression is rejected.

### Healing

R-cb04a-3 A recommendation: both found water and meat. Start with no charges.
The first spring is on the Shingle route at local row24; touching it teaches
water and grants two mouthfuls. The later spring at Larkmeadow row72 upgrades
two to three. Each discovery is finite, represented by capacity0/2/3; the
later upgrade needs the first. Every rest refills that found capacity.
`w` spends a charge immediately, prepares for15 ticks, then heals40 over15
more ticks. A hit interrupts the remaining animation and healing; no refund.
Ordinary kills leave meat alongside scent:10 immediate health, clamped to
the heart cap, once per pickup, expiring after300 ticks. Each fresh drop
gets one visible frame before body-ring collection. Bosses leave no meat.

`art.draw_water` occupies row3, columns24–48, on both tiers, clear of the
health/stamina bars and the boss's row1. Before discovery it says to find a
spring. `sim.healing_pickups` is the only collection path; pickup drawings
are pure and owned by the in-level art pass.

### The thorn boundary

There is one thorn gate, edge0, with two visible faces. The closed five-cell
throat is flanked by solid forest; an opened gate keeps torn thorn flanks
and a clear five-cell gap on both sides. The bit and lunge rule are unchanged.
History shows `f50b9c167658a9de7ba82d8cb19e25f7408348f8` (cb02), not cb03a
or cb04, removed the opened wall's drawing and moved the wall from start+10
to start+157. The intact closed gate was never deleted. R-cb04a-4 A restores
the persistent boundary without adding another progression barrier.
The census checks every gate face/tier on every seed, closed collision and
glyph presence, open passage and remaining flanks.


## Paths, shadows and allocation (cb04d, proposed)

This section supersedes the older one-cell portal trigger, alternating
eight-cell path anchors and immediate numeric-key growth descriptions.

R-cb04d-1 recommends one additional clear cell on each side of carved
paths: symmetric clearance for the cub's body rather than a biased extra
cell. Main route half-widths are4–6 (the Teeth3–4); cache and shortcut
branches have half-width3. The shore gains one row seaward and inland.
The boar approach and joining branch widen too. The sealed thorn collar
and its five-cell gate are deliberately retained, not widened into a bypass.

The forced short-wave anchors now span sixteen cells, with slower value
noise. Bramblehold retains its six switchbacks, rounding each apex across
five rows; a bend's direction is measured across eight rows on either side.
Dens, caches and portals remain derived from the same seeded route model.
`--paths-audit` reports axis-transverse clear widths and signed centreline
steps over50 seeds, both fields, including actual cache branches only.
`tools/path-summary.py` reports reversals of nonzero direction within three
samples per ten sampled route cells, and the complete width distribution.

Any cub-body cell moving from non-shadow onto any7×3 doorway shadow triggers
an available edge, diagonals included. Open shortcuts work by walking too;
`r` still opens them from the permitted side. Progression and shortcut
locks remain unchanged. Arrival remains two cells inside. Its centre rearms outside the old
one-cell trigger; standing still never crosses, while a first deliberate
return step can cross even with the body already overlapping the shadow. The
real-key witness walker routes around unlocked doorways that are neither
its source nor its destination; player collision and movement are unchanged.

Foe rendering no longer consults the centre-to-centre Bramblehold sight
predicate. AI sight, locks and attack rules stay unchanged; each sprite
cell is clipped independently at the camera edge. `--foes-audit` compares
the actor layer with cell-clipped composition over every route row for
fifty seeds, both fields and both tiers. `--doorways-audit` covers every
shadow/outside-neighbour pair, four body quarters and both cub sizes.

Rest allocation is transient: Up/Down wrap through five stats and Confirm;
Right adds an affordable level, Left removes a pending level, Enter/Space
on Confirm applies all pending stats and subtracts the sum of each shared
per-level price. The health/stamina maxima update immediately. Esc or`r`
discards. Numeric keys do not purchase. Schema4 stores confirmed stats
only, never selection, pending choices or refusal feedback. See ART and
KEYS for the panel's layout and controls.


## Den-cycle world memory and ledger placement (cb04f)

An area's ordinary foes have stable seeded ordinals independent of its boss.
A slain ordinal stays dead across paths, doors and shortcuts until a den rest
or death's last-den respawn resets every area. A living wounded foe heals and
returns to its seeded place on re-entry (R-cb04f-1 A); death resets the global
slain set (R-cb04f-2 A). Beaten bosses remain beaten. Slain masks depend only on
seed and simulated play, never wall time. A save on the death card already
represents the reset that its resumed last-den wake will perform.

Unclaimed scent and meat wait in their areas across travel, retaining their
original absolute-tick expiry. Taken or expired pickups never reappear on
re-entry. Finite caches and discovered springs remain persistent as before.
A rest or death discards ordinary loot globally. Checkpoint saves retain the
slain set, not unclaimed loot or wounded foes' transient state: loading does
not create replacement drops or meat (R-cb04f-3 A recommendation).

Schema5 appends `slain A B C D E F` to schema4's canonical payload. Each mask
is range-checked against the area's ordinary spawn count. Schema4 is validated
with its own checksum and spelling, then migrated with six empty masks;
schema1/2/3 still fail `save_version`. Recordings write `journey 4`, 36 saved
values. Old `journey 3` recordings remain readable with empty masks. The six
new event names are appended rather than renumbering existing event ids.

The rest ledger keeps cb04d's sizes, frame, palette and staged purchases.
Its centre is `(cols/2 - cols/6, rows/2)`, using integer screen-edge
coordinates; its left edge is clamped to keep the full panel visible.
Measured centres at80×24,120×40,200×60 are respectively `(27,12)`, `(40,20)`,
`(67,30)`, with left/top `(7,1)`, `(15,7)`, `(42,17)`. None of these sizes
clamps. The original breathing cub and animated fire sit to its right;
at80 columns the fire sits six rows lower, clear of the cub's muzzle.

## Moonford opening (cb06)

R-cb06-1 recommends 30 seconds: 900 simulation ticks at 30 Hz. R-cb06-2
recommends A: one decoded key skips the entire sequence, never a shot at a
time and never a gameplay move. The music toggle keeps its existing
meaning; quit still quits. The seen flag and journey schema stay unchanged.

| shot | interval, ticks from opening (end exclusive) | duration |
|---|---|---:|
| crossing | 0–210 | 210 |
| first crack, cue strike | 210–225 | 15 |
| held cub, pack walking on | 225–300 | 75 |
| rapidly spreading seams | 300–330 | 30 |
| plate breaks, deep water exposed | 330–360 | 30 |
| cub drops, water hides its body | 360–420 | 60 |
| underwater current, shrinking surface, fade | 420–480 | 60 |
| black | 480–510 | 30 |
| first slow opening, dim, at most 60% | 510–600 | 90 |
| first slow closing | 600–660 | 60 |
| second opening, at most 80% | 660–720 | 60 |
| second closing | 720–765 | 45 |
| third opening, at most 95% | 765–789 | 24 |
| third closing | 789–810 | 21 |
| final quick reveal | 810–840 | 30 |
| clear spawn | 840–900 | 60 |

The waking view is the actual seeded Shingle frame, not an illustration of
a different bank. Eyelids are a rounded black mask; the first blink also
dims and sparsely hides detail. The last clear shot equals `art.render`
with the scene disabled, cell for cell. The sim remains suspended until
900 or a skip. Resizing changes composition, not the clock.

Replay syntax remains `opening 1`, plus ordinary recorded keys: no extra
events or save fields. Recordings made with this build reproduce every
shot, and the terminal tests compare their final glyphs and styles to
headless playback. Old recordings are readable but use the new opening's
art and duration; they are not promised visual compatibility with the
old three-card animation. The replay format has not changed; no data
migration is needed. The ending's three 90-tick cards are unaffected.

Twenty sampled moments (all shots, first peak and each blink shut) have
80×24, 120×40 and 200×60 goldens on both tiers. `opening-complete` waits
through the real sequence; `opening-skip-00` through `opening-skip-15`
press a real arrow in each shot and compare the resulting recording.


The item5 play correction reuses `art.draw_pose` / `art.draw_wolf` and
`silhouette.footprint`: no cutscene-only body or scale. `opening_bank_cell`
asks `ground_at` for real Shingle coordinates on both banks, with a
five-row gravel band at80×24 (viewport fit) and the widened coast's seven
rows at120×40/200×60. Two/four/six rows of the world's thick forest lie
beyond each bank. The far bank mirrors depth, not glyphs. Only fur over
pale ice changes shade; other fur uses the normal gameplay palette.
The timing, cue, skip, save and replay rules above do not change.

## The wide forest, 2026-10-26 (cb05, proposed)

The maintainer's word on cb04d's build: "Dens are too frequent and too close. But areas are also too small.
Not enough opportunities to get in fights. Let's have a real overhaul of the maps, extend them, give them
more area, make them more varied, use the names of the dens as assigned as inspiration for some of the
features to render nearby the dens. Make area 2 bigger with more paths. Add a new area between the beach and
the wood, make it a dilapidated town. throw in a few fires on the ground. make the enemies slow moving slow
attacking human zombies. ... Remove sawtooth paths. ... The meadow still feels empty." Every value below is
proposed; every ruling is a recommendation the lane implemented, the maintainer's to change by a line.
This section supersedes the 160-cell area bound, the two-cache branches at rows 52 and 132, the dens at
rows 7..10 / 66 / 90 / 146 and the eight cache bits above.

**R-cb05-1 (recommended A, the maintainer rules): Cinderwick and the Ashen.** Cinderwick (`forest.TOWN`,
area 6) was the village on the Ashwater above the Shingle. The night the fire came it ran up along the
thicket's edge (the coal roots), over the long grass (the low embers, the ash shelter) and stopped at the
last warm hollow; the river has run grey with its ash since. The smoke never lifted: it is always the night
of the fire there. The people who did not leave are the Ashen. The graph is re-threaded Shingle - Cinderwick
- Bramblehold - Larkmeadow - the Teeth - the Shallows - Gravehollow (`EDGES` 10: edge 0 the thorn gate,
now opening on the town; edge 9 the town's way on; the log, edge 2, still runs Bramblehold - the Shingle).

**R-cb05-2 (recommended A): lengths.** `forest.length(area)`: the Shingle 160 (the tutorial, unchanged),
Bramblehold and Larkmeadow 288, Cinderwick 240 (shrunk from 288 to pay for its width, item 8), the Teeth, the
Shallows and Gravehollow 224. Every row position
derives from the length: the arenas at seven tenths (156 of 224), the caches at 60 / 136 / 232, the foe
groups every 44 rows from 40.

**R-cb05-3 (recommended A): dens.** At most two dens an area (`DENS_PER_AREA`) and at least 110 route
cells between dens along the way on (`DEN_SPACING`; a shortcut is short by design and the census reports
it apart). Dens 8 (the coal roots), 9 (the low embers) and 10 (the ash shelter) are retired to landmarks:
`den_exists` is false for them, `den_retired` true; the save keeps their ids (a lit bit stays valid) and a
journey whose last den was one wakes at the nearest kept den of the area (`nearest_kept_den`, by the old
row), lighting it. Den 7 is the cold hearth, Cinderwick's.

| den | area | local row | the place its name promises |
|---|---|---|---|
| 0 the hollow log | the Shingle | the start | the cut timber the cub rests inside (`art.den_rows`) |
| 7 the cold hearth | Cinderwick | 124..127, in the square, nine cells off the lane | a ring of hearth stones, the fire in the middle |
| 2 the briar hollow | Bramblehold | 100..103 | a bowl in the brambles |
| 1 the split roots | Bramblehold | 196..199 | the roots under the lightning-split oak, the oak six cells east (`LM_SPLIT_OAK`) |
| 3 the grass nest | Larkmeadow | 8..11 | a flattened ring of grass; Quill's first perch seven cells east at row 30 |
| 11 the last warm hollow | Larkmeadow | 190..193 | a hollow still warm, where the fire stopped |
| 4 the ledge cleft | the Teeth | 18..21 | a crack in the stone, the cleft six cells west (`LM_CLEFT`) |
| 5 the willow root | the Shallows | 7..10 | the willow over the water, seven cells west (`LM_WILLOW`) |
| 6 the cold den | Gravehollow | 7..10 | the fallen oak's roots |

**R-cb05-4 (recommended A): foes.** Twelve to eighteen in each big area, eight to twelve in the later
three, the boss excluded; `sim.group_plan` places the route groups (`group_count` 5 / 6 / 6 / 5 / 4 / 4
for the town, the thicket, the meadow, the Teeth, the Shallows, Gravehollow) and the guards stand along
the branches' centrelines (a weasel trio, a fox pair, one fox) or in the yards (one Ashen, two at the far
yards, their post their home); a lane group's Ashen take the nearest verge or square ember as home (never a
yard's, behind its walls), the first on the ember and the rest a body's length down the verge. `encounter_row` advances any group inside a den's 30-cell quiet radius in every area now.

| area | length | dens | caches | foes (boss excluded) | landmarks |
|---|---|---|---|---|---|
| the Shingle | 160 | 1 | 4 bundles | 9 | — |
| Cinderwick | 240 | 1 | 4 yards (bits 8..11) | 14: the Ashen only (four lane pairs, six yard guards; at most two on the trail at once, R-cb05-5) | 2 scent marks in yards |
| Bramblehold | 288 | 2 | 3 (bits 4, 5, 12) | 18: weasel and fox pairs, a trio and two foxes at the caches | the coal roots, the split oak, 2 scent marks |
| Larkmeadow | 288 | 2 | 3 (bits 6, 7, 13) | 18: hawks over every open stretch with deer under them, weasels in the grass, a fox pair | Quill's perch, the low embers, the ash shelter, a scent mark |
| the Teeth | 224 | 1 | 0 | 8: fox pairs, a weasel pair, two hawks | the cleft, a scent mark |
| the Shallows | 224 | 1 | 0 | 8: hawks and deer, a fox pair | the willow |
| Gravehollow | 224 | 1 | 0 | 9: fox pairs, a weasel trio | a scent mark |

**The routes.** A path through wood is one curve: anchors every 32 rows (`ROUTE_LATTICE`) alternating
9..12 cells on a drift of 4..7 that turns every six anchors (`SWEEP_ANCHORS`), the noise detrended to zero
at both portals, the end segments ramps (a smoothstep from a zero anchor runs straight). Two curves summed
ran straight where their slopes cancelled; a sixteen-row alternation at these swings reversed within three
cells at every apex (0.50 per ten samples against cb04d's 0.15; this shape 0.07). Bramblehold keeps its
six switchbacks on legs of 36 rows swinging 24..28 (the longer legs still meet at ninety degrees), the
apexes at rows 20 + 36 k: the way in runs straight for four rows (the arrival cell stays on the route) and
slants straight to the first apex (a smoothstep there bent one way and then the other within eight rows, a
reversal the bends census sees). `STRAIGHT_MAX` 12 holds (measured 9 inland, 8 on the Shingle, 10 on the
town's lane).

**R-cb05-5 (recommended A, implemented; item 8): the swarm.** At most two Ashen pursue the cub at once
(`ASHEN_PURSUERS`): one that hears the cub takes its trail (`Foe.chasing`); a third that hears it keeps its
post, turned toward the sound, until one of the two is parried (the long stagger clears the trail), loses the
cub (a standing cub is never heard) or dies. Hearing 16 → 10 cells (`ASHEN_HEARING`), 4 → 2 sneaking
(`ASHEN_HEARING_SNEAK`); the lane's first third (80 of 240 rows) carries one pair (row 40), the rest at 88,
160 and 204; groups of three nowhere. The crossing census (`cub --crossing-census`): a fresh cub with the
Shingle's heart and no flask walks the lane from the throat to the hearth with Book-II play (walk, bite,
one parry, no roll), ten seeds at both fields; the bar is nine of ten with no death on the lane (measured ten
of ten before and after, health 48–52 of 52: the scripted cub was never in danger; the maintainer's deaths
were a human's in a swarm). The hitbox audit (`--hitbox-audit`): a bite from each of the eight aims, the cub
touching the Ashen and a cell off, lands sixteen times of sixteen; the hit test was already the drawn body
(`sim.in_reach`, cb02c) and the anchor cone passes from every position in reach, so nothing changed for it.

**The lane** (`town.lane`) is a street, not a path through wood, and three censuses pull three ways on a
street: the straight-run bar (no run over twelve), cb04d's jaggedness (no step out and back within three
samples) and the bends census (no opposite turns within eight cells). The route meander failed the first
and cut house corners (it wanders five cells within a plot); a plot-pitched smoothstep failed the first;
two-row eases failed the second; four-row eases on a plot pitch failed the third. The lane that satisfies
all three weaves on anchors every two plots (`LANE_PITCH` 28 rows, at the even plots' middle rows), three
to six cells to alternate sides, three beside the road in and out, zero beyond (the thorn throat and the
way on stand at x = 0); each anchor sits mid-cell so the apex row never pokes a cell out of its flat; the
blend eases four rows out of an anchor, slants straight (a cell every two or three rows: no counted turn)
and eases four rows into the next. A house's near wall is placed by the lane's farthest reach toward it
over its plot's rows (`lane_edge`: an end row, or the middle where the plot holds an anchor swung that
way), so the verge widens where the street bends away and no wall is ever carved.

**Measured on the final generator** (fifty seeds, both fields; `notes/cb05-evidence/`): den spacing least
within an area 122 route cells, least onward 116 (bar 110); foes 9 / 16 / 18 / 18 / 8 / 8 / 9 an area in
every seed, none within 30 cells of a den; 0 reversals within eight cells on any route or branch (7,676
counted turns); cb04d's jaggedness per ten samples 0.068 / 0.105 / 0.057 / 0.100 / 0.103 / 0.111 against
0.090 / 0.186 / 0.133 / 0.168 / 0.190 / 0.170 before, widths 7/9/9/7/9/11 at the median; 700 world-audit
rows with 0 unreached and the longest straight run 10; every spur ends at a cache, a landmark or a den;
generation at field 200 on the Mac release build 14 / 7 / 7 / 3 / 3 / 2 / 4 ms (bar 50); render means 173 /
164 µs at 80×24 and 1260 / 1290 at 200×60 (cb04d: 182 / 174, 1306 / 1296); the town's lane 0 counted turns; the crossing
census ten of ten at both fields.

**The branches** (`forest.Branch`, `branch_point`, `in_branch`): a cache branch leaves the route at its
row on the side the switchback has swung away from (Bramblehold) or by parity, with half width 3 and an
alcove of radius 4 at its end, in one of four shapes drawn from a seeded order of the four so no two in an
area are alike where the field allows: a slow S (the amplitude 6..12), a hook (a run, a quarter turn of
radius 7, a climb of 12..18), a loop (a ring of radius 10 round a copse, entered at its pole, the cache at
the far pole), a 180-degree turn (radius 8, back three fifths of the way) where the reach allows (46 cells,
the 200 field; the hook needs 20, the loop 30). Every shape bends toward the side whose nearest den is
the farther off. Bramblehold also has a fork that rejoins (rows 92..188, 14..18 cells west, eased over 24
rows inside one leg each end), a second way into the boar's clearing from the south (row 130) and two
pockets; the meadow, the Teeth and Gravehollow one pocket each: a stub of 7..9 cells with an old scent
mark at its end.

**Cinderwick** (`src/town/town.lu`; the block plan of item 8, from the maintainer's play of `cd7e5022`: "I
was hoping the town map would be more rectangular, that is take up more width of the screen"): a rectangle
across the field. The lane (half width 4, the route's spine) runs the town's 240 rows with a verge of 4
cells of ash; 14 plots a side from row 20 every 14 rows (a thirteen-row house with its walls on the first
and last rows, then the one-cell passage), the passage after plots 2 and 10 grown into a cross street of 8
rows that runs the town's whole width; plots 6 and 7 are the square, open ash across the width with rubble
(never about the hearth), the hearth nine cells off the lane, an ember each side. A side street (half width
3) runs north–south at x = ±44 from the first cross street to the last, so every street loops: the lane,
two cross streets, the square and the side streets make the blocks, and every passage row runs on behind
the yards to the side street (a corridor a cell wide). A house is 8..10 cells wide with a two-row door in
its near wall and a ruin's fallen cells (one in nine, never a corner, never the far wall); behind it a yard
5..8 deep with one two-cell gap in its top or bottom wall into the corridor and a back wall (the lane's
plots reach x = ±34 at most, a cell of wood short of the side street); beyond the back walls the closed
wood. At the 80 field (half width 48) the side streets are the town's edge: 94 cells of the field's 97. At
the 200 field (108) a second row of plots faces the side streets' outer sides (near walls at ±52, back walls
to ±72) and an outer ring at x = ±80 closes the blocks: the same plan scaled by blocks, never by wider
streets; `town.wide(field)` says which. An ember (`terrain.EMBER`) stands in 42 % of the plots, in the
verge for the odd plots and the yard for the even (the side plots the same); light 2 within three columns
of one, 1 within six (the ash and the walls warm up; the lane's cobbles keep their one style for the path
audit); a cub any part of whose body covers one (`sim.on_ember`, the body as the frame draws it) loses
`EMBER_HURT` 2 every `EMBER_TICKS` 10. Caches in the yards of plots 2, 4, 9 and 12 (lore, marrow, lore,
lore: `lore.lu`), every guard thirty cells and more from the hearth; scent marks in the yards of plots 3
and 10. The town's bound (`town.bound`): from six rows before the first plot to six after the last, within
the side streets' outer edge (the ring's at 200). The length shrank from 288 to 240 to pay for the width;
the hearth sits at rows 124..127, so the den spacing holds (least onward 116, the 110 bar).

**The Ashen** (`sim.ASHEN` 8, `src/silhouette/silhouette.lu`): health 36, walk `ASHEN_V` half a weasel's
stalk (40 FP a tick), hearing `ASHEN_HEARING` 16 cells of a trotting cub (four of a sneaking one), a touch
always; the windup `ASHEN_WINDUP` 30 ticks (the arms rise, slowly: the tell a person reads), the blow
`ASHEN_DAMAGE` 22 at reach 2, the recovery `ASHEN_RECOVERY` 40 standing; a parry staggers it
`ASHEN_STAGGER` 60 with the riposte open (a lunge or a heavy 30); a bite from behind (out of the cone it
faces) lands twice; scent `ASHEN_SCENT` 25. It never steps outside the town's bound (`forest.in_town`), and
when it hears nothing it walks to its home ember and stands. Two cells by three (four by twelve pixels),
grey 247 (plain 7).

**Lore** (`src/lore/lore.lu`): a cache that holds a line shows it on the bottom row for `LINE_TICKS` 240
when dug (`sim.lore`, `sim.lore_until`, transient); a scent mark or Quill's perch shows its line while the
cub stands within four cells. The town's lore says where the fire went (`TOWN_FIRE`).

**The censuses** (`src/wide/wide.lu`, gated by `tools/gameplay.py`): `--den-spacing` (the route walk over
the real tiles between an area's dens and onward through both portals to the next area's first den; the
shortcut-linked distance reported), `--foe-census`, `--bends-audit` (along every route, fork and branch
sampled a cell at a time, the turn is the cross product of the baselines four samples back and ahead,
counted above 16; a reversal is two counted turns of opposite sign within eight samples; none on any
inland route or branch, the coast's offshoots reported), `--spurs-audit` (every branch's and pocket's end
within three cells of a cache, a landmark or a den, and reached), `--gen-bench` (the terrain layer over a
whole area under 50 ms at field 200).

**Measured** (fifty seeds, both fields, this lane's final head; before on trunk `7e2c6a77`): den spacing
before, Manhattan, Bramblehold 45..62 and Larkmeadow 22..149 (three and four dens); after, route cells,
least within an area 119 (Bramblehold), least onward 117 (Larkmeadow to the Teeth), the least by a
shortcut 67 (the ledge). Foes before 9 / 9 / 11 / 4 / 6 / 4; after 9 / 16 / 18 / 18 / 8 / 8 / 9 (the town
second). The bends census: 0 reversals within eight cells on every inland route and branch (the coast's
offshoots 0 too). cb04d's per-ten measure on the spines, the shortcut and the shore: Shingle 0.078,
Bramblehold 0.116, Larkmeadow 0.072, the Teeth 0.139, the Shallows 0.141, Gravehollow 0.157 (before
0.090 / 0.186 / 0.133 / 0.168 / 0.190 / 0.170). Generation: at most 38 ms an area at field 200 (the
Shingle; native tier, Mac arm64). The frame: see the note.

## Held motion and combat (cb04b,2026-10-26)

This section supersedes the historical198 dial, recent-arrow attack
window, c-held sprint, three-cell dodge, presentation-only combo and
fixed-width HUD above. The default pace dial is211, up6.5657% from198.
Paw1 trot80FP/tick (9.375 cells/s), paw10 118 (13.828125). Sprint is8/5
trot:128 and188FP/tick. Sneak is half trot. Acceleration8, braking15,
turn31, foe pursuit84/retreat92, stride1064 and sway36 remain derived from
the one constant. Signed fractional integration carries diagonal residues
rather than losing each tick's fractions. There is no Bramblehold penalty.
Shallows visibly wade at half walk/sprint; sneak already uses half trot
and is not halved again. The existing low-health limp halves normal walk.

Exact holds are engine KeyState views. Press/repeat/release and modifier
changes are represented by game replay words, including the negotiated
mode at the start. Opposites cancel; non-opposing axes combine. Space
commits held arrows, else facing. c is a tap roll, never sprint; Ctrl-held
arrows sprint for12 stamina/second, no regeneration while sprinting, and
stop at zero. The sprint snap attack remains36 stamina,3/3/10 ticks,
reach4 and twice bite damage. The fallback and its limits are in KEYS.

### The ruled roll

Distance in cells is `max(10,ceil(2*14*trot_at(paw)/256))`:10 at paw1,
13 at paw10. Eight travel ticks use cumulative `d*(16t-t*t)/64`,t=0..8;
six further ticks recover without movement or actions. Direction latches
at c's press and ignores turn rate; no arrows uses facing. Unlocked the
cub faces that direction; locked it keeps facing the target. Cumulative
per-axis rounding makes a diagonal the same distance within fixed-point
quantisation. Eighth-cell path samples prevent tunnelling, and each axis
clips independently against terrain/bodies, allowing a wall slide.

The iframe interval is half-open: ages0..9 at paw1; age10 is vulnerable.
Paw5 adds one tick and paw10 another, capped12. **The first two of the
six recovery ticks are invulnerable at paw1**; the last four are not.
At paw10 the first four recovery ticks are protected, the last two not.
Stamina18 and refusal while exhausted remain. The roll has eight original
tuck-and-turn frames, not an invulnerability blink.

### Three committed bites

The body, not only the hit envelope, moves. Hit1 lunges a quarter-cell
forward and half-cell to aim-left, hit2 to aim-right; both settle their
sideways lean in recovery. Hit3 travels two cells forwards during its
active ticks and stays there. Path/body collision can shorten the travel.
The camera holds at commitment during the bite so the body motion remains
visible. Rich uses pixel/subcell translation; plain rounds either sign
away from zero rather than asymmetrically dropping positive half cells.
Both tiers share a conservative union footprint for the translated body.

All three retain3 windup/2 active ticks and base bite damage. Recoveries
are6/8/12, totals11/13/17; costs12/14/18. A recovery input queues one next
bite with its own committed aim. A refused link spends nothing and cannot
advance. A lapsed chain starts from1 again. The third recovery is longest.

### Rally and the HUD

Actual damage opens a45-tick (1.5s) window. The initial lost-health pool
falls linearly with elapsed ticks; previous regained points are deducted.
A damaging hit restores at most `floor(8*remaining/45)` health and never
more than the remaining pool or missing health. A new hit received carries
only the then-regainable pool into the new window plus its actual loss.
Death/rest/growth clear it. At age45 nothing is regainable.

Health stays red; regainable health is grey stipple/dots immediately after
it, with an explicit rally number. Stamina stays green. Each bar has one
cell per10 maximum points rounded up, capped30; labels and outlines stay
at rows1/3 on both tiers. Status numbers are row5 and water row6, after the
HUD clear. Stat levels1/10/40 are golden at80x24 and120x40. The boss bar
retains its own size and row1 area to the right of these bars.


### Elk census counter correction (cb04b)

R4's latched eight-way facing exposed the scripted player's blind forward
lunge: an arrow alongside x does not turn its already-committed aim.
At seed15 the player remained at88 health while five2500-tick budgets
expired; several lunges aimed64/96/224 against bearing160. This was not
an iframe or charge-balance failure. The elk's stagger counter now chooses
x only inside its existing45-degree facing cone; otherwise it falls
through to the existing held-direction bite or approach/turn, as a real
player must. No roll, damage, timing, seed or limit changes. All300 non-elk
census rows stay byte-identical; other elk win-attempt counts stay the same.
Seed15 wins its fourth budget at both fields. The74 changed elk rows'
durations/hits and the before/after frames are retained as evidence.

## The three strikes and the HUD (cb07, 2026-10-27)

The maintainer's word after playing cb04b and cb05: "Attack combos STILL
aren't rendering. It should attack forwards-left, forwards-right, then
straight forwards with a head shake." cb04b's lean was a quarter cell
forward and half a cell across for one tick, rounded to one braille pixel:
invisible at thirty ticks a second. This section supersedes "Three
committed bites" above.

**The strikes.** `sim.strike_offset(hit, age)` is the body's displacement
from the commitment point: the windup (ages 0-2) stands still; hit 1 lunges
a whole cell forward and a whole cell to the aim's left from age 3 through
6, hit 2 the mirror, hit 3 two cells straight forward from age 3 through
8 (`sim.strike_hold`); then each eases back a step a tick to the commitment
point by its last age, so the next link starts in place and a cub that
bites does not drift. `combo_motion` moves toward the offset's point from
wherever the body is (a lunge a wall or a foe shortened still eases home).
The hit cone and reach follow the body (`in_reach` measures the drawn
bodies' gap, cb02c), so a bite lands where the drawn jaws are. The third
hit's head shakes two full swings across the committed aim, a cell to the
left at ages 5-6, right at 7-8, left at 9-10, right at 11-12
(`sim.head_shake`, `sim.shake_cells`): a diagonal aim swings the head a
cell on both axes and never back along the aim; the sprint snap keeps
cb04b's three-tick swing across the body's facing. Costs 12/14/18,
durations 11/13/17, three windup and two active ticks, the link window
from age 5: all cb04b's. `COMBO_LEAN` is a whole cell now.

**The snapping pose** (`silhouette.cub_posed`, pose 5; `art.plain_cub`):
the jaws thrown open at the nose (`##....##` over `.##..##.`), the head
narrow with the ears back, the tail streaming straight behind; its
centroid sits two hundredths of a cell ahead of the standing drawing's,
so the measured displacement is the lunge and no more. The rich tier
composes the shaken head and the body into one drawing
(`motionart.shifted_shaken`), so a head swung diagonally never erases the
body's front; the plain tier puts the ear mark a cell outside the body on
both swings.

**The instrument.** `cub --strike-census` (`combatproof.strike_rows`)
draws the cub alone at every age of every hit at every aim on both tiers
and holds it against the standing drawing at the commitment point: the
cells changed, the centroid's move in hundredths of a cell along the aim
and to its left (pixels, two across and four down a cell, on both tiers),
the cells across the aim, the swing, and the cells the shaken drawing
paints that the same drawing with its head still does not. Before: rich
hit 1 peaked at 0.50 forward and 0.50 left (aim east) for one tick, 0.35
and 0.35 on a diagonal; hit 3 reached 2 forward from age 4 and stayed. After:
hit 1 at 1.04 forward and 1.00 left for ages 3-6 (aim east; 1.08 and 1.03
on a diagonal), hit 2 the mirror, hit 3 at 2.04 forward for ages 3-8 with
the head out on every swing age, and every hit's last age identical to
standing; the plain tier exactly 1.00/1.00 and 2.00 on the cardinals, 1.41
and 2.83 on a diagonal (whole cells on both axes). The `cb07-strikes` pty row drives three Space presses through
the real input loop and reads the same numbers off the recorded journey's
frames.

**The HUD** is health, stamina and scent and nothing else. The status row
(`HP a/b … rally f`), the 7x40 filled box and the two full-width filled
rows are gone; the numbers stay in the `--hud` debug line (`hud_text`).
`art.hud_plan` lists every cell the HUD paints with its kind (a bar cell,
a label cell, a digit cell); `draw_hud` paints those cells with the map
cell's own background under each, so the bars sit flush on the forest:
the one-word labels at column 1 of rows 1 and 3, the bar cells from
column 9 (`HUD_BAR_COL`; the bracket column stays the map's), filled cells
solid in the bar's colour, the rally stretch the grey stipple, the rest of
the bar's width a dim `─` track (plain `-`) so the length reads without a
rail. cb04b's growing width (`bar_cells`, ten points a cell) and the
fixed-point fill stay. The water line (`Water n/cap  w drink`, cb04a) sits
on row 5 (`HUD_WATER_ROW`) straight under the stamina bar, painted last
(cb04b's ordering, re-proven with the fills gone) and counted as a label.
R-cb07-2: recommended A, no rails or caps at all.

**Scent** is one big number in the bottom right corner (`src/digits`): an
original three-by-five pixel digit font. On the rich tier the pixels are
quadrant blocks, two across and two down a cell, so a digit is two cells
wide and the number three rows tall with a blank pixel row on top (every
quadrant block is drawn, U+2596-259F with the half and full blocks;
`docs/GLYPHS.md` gained U+259A and U+259C). On the plain tier each pixel is
a bold `#` cell, so a digit is three cells wide and a cell apart and the
number five rows tall. The number ends on the frame's last row, one cell
in from the right edge, and grows leftward with the digits; a small
`scent` label sits on its middle row to its left. At 80x24 on the rich
tier the label and three digits cover twelve columns on three rows; four
digits cover fourteen. Rich digits are gold (221), plain bright yellow.

**The census.** `cub --hud-census` (`combatproof.hud_row`) renders the
frame with and without the HUD (`art.render_bare`) and counts the cells
that differ: `painted`, and `stray` for any outside the plan, which must
be zero. Before: 360 painted cells at 80x24 and 600 at 200x60 whatever the
stats (the fills). After: 51 at stat 1 and scent 0 on the rich tier (57
plain), 100 at stat 40 and scent 1234, the same at both fields, never a
stray cell; 192 rows over both tiers, both fields, day and night, four
scent values, three stat levels, with and without a rally.

**The Ashen (item 3, after the rebase onto cb05; R-cb07-1).** `foe_health(ASHEN)` 36 → **20**, `ASHEN_DAMAGE`
22 → **14**; the back-bite doubling, the two-pursuer cap, the hearing and the stagger untouched. The
instrument is `cub --encounter-census` (`cross.encounter`): a fresh cub (the Shingle's heart and wind, no
flask) five cells from one posted Ashen with every other foe of the town removed, ten seeds at both fields,
two plays: Book-II (the walker's: walk at it, bite in reach so Space links the strikes, parry the windup two
ticks before the blow, never roll) and the no-parry player (the same without the parry: what a blow costs a
cub that missed the window). The bar is Book-II's: at most 35 % of `health_max` lost in at least nine of
ten seeds at each field. Before (36/22): Book-II fells it in 94 ticks losing 0 of 52 in all twenty rows;
no-parry fells it in 62 ticks losing 12 (one blow of 22 less the rally's regain). After (20/14): Book-II 70
ticks, 0 lost; no-parry 38 ticks, 0 lost — the blow that landed at 36 now never lands before the third bite
fells it, and a blow that does land costs 14 (27 %) where it cost 22 (42 %). The scripted cub was never in
danger either way, as cb05 found; the maintainer's losses are a human's, and the numbers cut what a missed
parry costs. cb05's crossing census stays ten of ten at both fields and its hitbox audit green; the boss
census stays 400 of 400.

**The walker, two rules (cb07).** A tick spent fighting in place is not a still tick: a strike blocked on
both axes (a foe ahead, a wall beside) leaves the cub exactly where it stood, and cb04b's quarter-cell
carry had hidden that the walker's thirty-still-ticks replan fired in the middle of a fight; a passive walk
(never biting) against a foe is still stuck and replans round the body. A strike at a foe in reach aims at
the eight-way direction nearest the foe's bearing (`walker.aim_at`), not at the per-axis quarter-cell
arrows, which pressed a diagonal at a foe a little to one side and put hit 1's slanted cone past it — with
the strikes easing back to the same point every time, that miss repeated for the whole budget (seed 1 of
the crossing, `notes/cb07-evidence/ashen/crossing-trace-seed1-stall.txt`). `cub --crossing-trace SEED
FIELD` narrates a crossing while a foe is within two cells (`walker.walk_narrated`). The cone test itself
is cb08's (the hit test moving to the foe's body).

**The three rulings, each a one-line switch, recommendation A built.** R-cb07-3 `art.HUD_WATER_LINE`
(A true: the water line on the play HUD; B: the debug line alone — `hud_text` carries health, stamina,
scent, rally and water either way). R-cb07-4 `digits.PLAIN_DIGITS_TALL` (A true: the 3x5 `#` font, five
rows on the plain tier; B: `digits.stroke_glyph`, a three-row font of `_` and `|` strokes, the same
width). R-cb07-5 `art.SCENT_LABEL_ALWAYS` (A true: the label stays beside four digits, fourteen columns;
B: the label drops at four digits). `hud_plan_with` and `digits.plain_cells_of` take the switches as
arguments so the B paths are tested without flipping them.
## Hand-timed bite requests (cb11)

This supersedes the age-5 link window above, not the strike drawings,
11/13/17-tick durations, 12/14/18 costs, hitboxes or head-shake ages.
A fresh Space at ages 1 through duration inclusive queues a bite. The
inclusive endpoint matters because input runs before action completion:
the former strict bound dropped a press at age 11 while start_action still
saw an active bite, so a later press restarted strike 1 and moved left again.

The queue holds at most two requests, each with its committed aim. At a
natural bite end, consume one and start combo % 3 + 1 if stamina permits;
carry the remaining request. Overflow is ignored without replacing an aim.
An unaffordable queued link discards both requests without spending stamina.
With no queued request, the completed strike opens a six-tick grace: a
fresh Space starts its successor immediately. Outside it, start strike 1.
Other actions, rest, death, area entry and the alpha's guard clear the queue
and grace. Same-tick duplicate presses (age 0) do not queue.

Enhanced Space repeats never request a bite; legacy <=2-tick gaps are
suppressed and >=3-tick gaps are fresh. The first legacy repeat after a
long OS delay remains indistinguishable from a press (KEYS documents this).
No persistent save fields or replay ids are added: the request queue is
transient and deterministically reconstructed from the recorded keys.

## Eight-way bodies and jaw reach (cb08)

The cub's body facing is the clockwise eighth, north0 through north-west7.
Even eighths use the original cardinal drawing; odd eighths use the second,
north-east drawing turned by quarters. Its16×16-pixel extent gives an8×4-cell
body; the grown diagonal wolf is24×24 pixels,12×6 cells. Foes keep their
four-way drawings. Actor separation, presentation clipping and doorway
shadows use these exact rectangles. Terrain clearance remains anchor-based:
this change does not widen paths or close their single-file passages.

A strike starts at the front edge of that body, at its leading cell centre
on a directed axis and the transverse midpoint on a cardinal facing. The
cone uses the committed attack direction, including the first two strikes'
slants. It tests every foe body-cell centre, not the foe's anchor. Reach
keeps the existing cell metric: at most2 cells on either axis for a bite,
4 for lunge, heavy and dash. A qualifying jaw-to-cell ray must be clear
outside both bodies. Alpha guard, hawk exclusion, damage and once-per-action
hit accounting are unchanged. The boar's travelling charge already tests
body overlap; an edge-contact/one-cell-outside witness covers all four
diagonal cub facings without changing its rule.

`--hit-census` freezes each boss and an Ashen and strikes every body-ring
position at gaps0–2, with eight aims and four foe quarters. It uses the
unslanted third bite to isolate the aim geometry; separate tests cover the
first two slants and every attack type. `tools/hit-census.py` independently
checks complete ring membership, reports into/along/away aims by gap, and
requires every inward gap0/1 bite to land, every away bite to miss, and every
gap2 bite to remain beyond reach. Lateral targets admitted by the old
body-gap/centre-cone combination can now lie beyond the jaws' reach; losing
those hits is intentional, not a wider cone.

`--narrow-audit AREA LENGTH` drives both diagonal chords across every open
axial edge of each single-file corridor, fifty seeds at fields80/200. It
uses real movement keys, without foes and with disclosed extra health to
isolate clearance from ember damage. A legal diagonal exit at a corridor
mouth counts when the axial boundary is crossed into passable ground.
The independent crossing census retains ordinary combat, starting health
and its existing9-of-10 survival bar. Its scripted walker aligns to a
non-overlapping jaw stance before biting; that is a witness tactic, not a
new player rule or a mutation of the running simulation.


The roll keeps cb04b's distinction: without a lock, body facing follows
latched travel; with a lock, the body tracks the target, now in eighths.
R-cb08-6 recommends this A reading. The B reading (body follows travel even
while locked) is a one-line `LOCKED_ROLL_FACES_TARGET = false` change in
`sim`; it is not selected. This does not change travel, timing or iframes.

A target0.58 cell right and due south is a separate aim problem: the wrong
SE first-strike aim96/cone85 misses under both centre and jaw/body tests;
cardinal aim128 lands under both. The walker's quantized bearing fixes that
specific case. Body intersection remains independently necessary for a
flank whose cells enter the cone while its centre does not. Neither fix
replaces the other generally.

## cb10 — the small faults (2026-10-28)

- **R-cb10-1 A:** sprint is `trot_at(paw) * 8 / 5 + 1`, the smallest
  fixed-point increment, rather than B's five percent. At paw 1 the cap
  is 128 → 129 units/tick (15 → 15.1171875 cells/s); paw 4 is 148 → 149
  (17.34375 → 17.4609375 cells/s). Drain stays 12 stamina/s.
- Legacy Ctrl+arrow sprint has a 17-tick (566.7 ms) grace from each
  decoded refresh, covering a 500 ms first repeat and 60 ms later repeats.
  The Ctrl-arrow's movement hold gets the same grace; normal arrows keep
  their shorter inference. Exact modifier releases
  are still immediate. This cannot recover a modifier the terminal never
  reports, nor turn a legacy stream into physical key-up events.
- **R-cb10-2 A:** the pink foes are hawks, not pickups. They keep airborne
  immunity during circling and the stopped-shadow tell. A parry at the
  stoop kills them; bites also kill in the low STRIKE and RETREAT phases
  (3 active ticks, 36 recovery ticks). Their unrotated body is the
  four-by-one-cell shadow on both tiers, one starting bite (8 health).
  B would make them always biteable; A is implemented. No glow-worms,
  scatter or white flash are introduced by this correction.
- **R-cb10-3 A:** only drinking spends water. The old fox-hit path also
  decremented flasks; this was not a kill-path or decoder alias. A landed
  fox feint now takes `min(5, carried scent)` instead. B would steal
  nothing. Killing a foe never invokes drinking.

`--small-faults` runs the real-reader timed-repeat rows and an explicitly
staged headless replay fixture: three fox contacts followed by three real
keyed bites, without w. The fixture reports the keys, health, scent and
flasks at every contact and kill; it is not a natural journey recording.

Ghostty/macOS's negotiated path is tested separately with flags11,
press/repeat/release, modifier order, a four-second silent Ctrl hold and
diagonal chords. Exact holds never use the 17-tick fallback timeout. No
enhanced fault is reproduced by these injected fixtures; a physical
Ghostty key capture remains needed if the report persists.

## The map overhaul, 2026-10-28 (cb14, proposed)

The maintainer's word on the second playtest (`the-maintainer-s-notes.md` items 4, 10 and 12): "We want more areas.
The game is too short." / "Exploration is only rewarded in early levels. Only early levels have branch-off paths." /
"Boss arenas are too small across the board." The orchestrator's proposals (`the-proposals.md` section 3) name the
five areas, their lore, their sprites, their placement, the branches and the arenas; this section is what was built.
Every value is proposed; every ruling is a recommendation the lane implemented, the maintainer's to change by a line.

**R-cb14-1 (recommended A, implemented): the Howe has no den.** The last rest is the Hush's cold den (den 6); the
Howe and Gravehollow are the walk to the end. **R-cb14-2 (recommended A, implemented): the Underteeth's squeeze
is a growth gate of paw 2** (`sim.UNDERTEETH_PAW`). **R-cb14-3 (recommended A, implemented): the Hush and
Gravehollow are two areas.** cb04 built one area (5, "Gravehollow") holding the deep wood, the cold den and the old
den's arena; the proposals put the Howe "between the Hush and Gravehollow", which the bible's sections 2 and 16
keep apart (the dark wood with the way to the old den; the old den itself). Area 5 keeps its id and the cold den
and is the Hush (160 rows: the wood, its arena rows cut); Gravehollow is area 12 (128 rows: the stone mouth at its
entry, the old den's bowl at row 89). B would put the Howe before area 5 unchanged, with the cold den right after
the stone mouth, which is what the maintainer's "a den here makes the end easier" refuses. **R-cb14-4 (recommended
A, implemented): the lookout's reveal is a schematic**, not a zoomed render: for sixty ticks the frame shows the
whole of Thornmere as a climbing line of stations, the areas' names fading in four ticks apart where they lie, the
Underteeth under the Teeth, the cub's area marked (B, a true pulled-back render of the terrain, is a renderer the
engine lacks). **R-cb14-5 (recommended A, implemented): the alcove guards stand on top of R-cb05-4's band** in the
Teeth, the Shallows and the Hush (`wide.FOES_LATE_MAX` 12 -> 14); the new areas hold their guards alone (3..6,
`FOES_NEW_MIN/MAX`) until cb18 fills their tables. **R-cb14-6 (recommended A, implemented at the rebase onto
cb15): the alcoves' pine, shard and tuft are cb15's items**: a dug alcove gives `pouch.PINE`, `ICE` or `TUFT`
through `sim.give_item`, or leaves it on the ground at the cache when the stack is full, as cb15 does for marrow
and yarrow (B, the scent placeholder of 30 kept until a later lane, is the other choice; the maintainer's to
overturn). The area and standing-stone lines are registered in the found-lore list by cb15's landmark path
(`sim.hazards_step`, within four cells), the alcove lines by its dig path.

**The graph** (`forest.AREAS` 13, `EDGES` 20): Shingle - Cinderwick - Bramblehold - **the Stand** (7) - Larkmeadow -
**the Burn** (8) - the Teeth - **the Mere** (9) - the Shallows - the Hush (5) - **the Howe** (11) - **Gravehollow** (12),
with **the Underteeth** (10) a branch from the Teeth (edge 18, the sett at row 72 west of the route) out into the
Hush (edge 19, the roots at row 40 west). Path edges 10..14 are the new areas' ways on; cb02's edge 1 now leads
Bramblehold into the Stand, 4 Larkmeadow into the Burn, 5 the Teeth into the Mere. Shortcuts: the scree (edge 15,
bit 16: from the Stand's west at row 60 down to Bramblehold's east at row 212, beside the split roots), the dry
streambed (16, bit 32: the Burn's east at row 40 to Larkmeadow's east at row 250), the log raft (17, bit 64: the
Mere's west at row 190 to the Teeth's east at row 200), the sett (18, bit 128), the roots (19, bit 256); each opens
from the new area's side with `r`, then both ways (`SHORTCUTS_ALL` 511). cb02's hedge, ledge and shallows become
chords that skip the Stand, the Burn and the Mere. A cb14 mouth carves its own curved run from the route
(`forest.mouth_run`); cb02's row-22 band is untouched in its five areas.

| area | length | den (row) | gate at its far end | shortcut back | alcoves (bits) |
|---|---|---|---|---|---|
| the Stand (7) | 224 | 12 the root hollow (96..99) | the windthrown pine: three rows, open only to a sneaking cub | the scree | 3 (34..36) |
| the Burn (8) | 224 | 13 the kiln (112..115) | the burnt oak: a lunge within four cells pushes it over (`gates` bit 1) | the streambed | 3 (37..39) |
| the Mere (9) | 224 | 14 the dry island (104..107) | none (the heron is cb18's) | the raft | 3 (40..42, over the water as reed causeways) |
| the Underteeth (10) | 192 | 15 the bone cache (100..103) | the sett's squeeze into it: paw 2 | it is one (the Teeth <-> the Hush) | 3 (43..45) |
| the Howe (11) | 224 | none | the stone mouth: a lunge opens it (`gates` bit 2; the sentries are cb18's) | none | 3 (46..48) |
| Gravehollow (12) | 128 | none | the end | none | 2 (49, 50) |
| the Hush (5) | 160 (was 224) | 6 the cold den | none | the roots, from below | 3 (31..33) |
| the Teeth (3), the Shallows (4) | 224 | as cb04 | as cb04 | as cb04, and the sett / the raft | 3 each (25..30) |

(The bit numbers are `forest.cache_bit`'s: the Teeth's 16..18, the Shallows' 19..21, the Hush's 22..24, the
Stand's 25..27, the Burn's 28..30, the Mere's 31..33, the Underteeth's 34..36, the Howe's 37..39, Gravehollow's
40, 41: `CACHE_BITS` 42.) Every alcove is a cb05 branch (the four shapes, a seeded order, the mouth rows scaled
to the area's length: 60/136/232 of 288 are 46/105/180 of 224) ending in a hollow or a burrow with a guard a
tier above the area's (from the Teeth on: foxes of health `sim.ALCOVE_GUARD_HEALTH` 36, a pair, a pair and
one) and a slot (`lore.alcove_slot`): a lore line in the middle alcove of each area (`lore.ALCOVE_FIRST`..), a
consumable's kind in the others (yarrow, marrow, pine, a shard of ice, the mother's tuft: `lore.PINE`, `SHARD`,
`TUFT` are cb15's pine, ice and tuft since its merge, given through `sim.give_item` or left at the cache when
the stack is full: `sim.reward_item`, R-cb14-6). The journey's `caches` word holds every bit
(`journey.cache_limit`).

**The ground** (`src/lands/lands.lu`; the kinds `terrain.NEEDLES`..`GATE`, 12..22):
- *the Stand*: pines two cells tall in columns (`PINE`, 11 % of the floor, a wall where the stand's noise runs
  over 150), a needle floor (`NEEDLES`), the route needles; the lookout a ledge eight cells east of the route at
  row 200 (`forest.lookout`), the cutters' ruin beside it; the windthrown pine across rows 218..220.
- *the Burn*: charred trunks (`CHAR`, 9 %; every third leaning), ash drifts two cells wide where the fire's noise
  ran hot (`DRIFT`: half pace, no trail laid), embers under the ash (`EMBER`, 4 % of a drift: `EMBER_HURT` as
  Cinderwick's, and a flare of four ticks underfoot), ash everywhere else; the burnt oak across rows 218..220.
- *the Mere*: still water (`WATER`) with a reed causeway (`REEDS`) for the first and last sixty rows, four islands
  threaded on the route (centre rows 72, 110, 150, 186; the dry island the widest, radius 11, its reach in
  columns twice its rows) with a fringe of reeds round turf, and between them the route on stepping stones
  (`STONE`, the route's width, four rows a stone): a stone sinks `sim.STONE_BEAT` 30 ticks after the cub first
  steps on it and rises `STONE_RISE` 150 ticks after; a cub on a sunk stone is in the water (half pace, a point
  of stamina a tick). The stones are not path (`forest.on_path` false; the path audit holds the reeds). The
  branches over the water are reed causeways.
- *the Underteeth*: a tunnel of half width 3..4 through wet stone (`CAVE`), six chambers off it (rows 24 + 32 k,
  eight to twelve cells to alternating sides, radius 5..8, a neck to the tunnel), eight glow-worm clusters on the
  tunnel's floor (`GLOW`, rows 12 + 24 k, three cells; light three cells round each: beyond three cells of the cub
  and of every cluster the frame is dark), the spring in the second chamber (`SPRING`, three cells by two: a cub
  standing in it has its water refilled), drips falling a cell a tick in one column of twelve. The floor's path
  kind is gravel.
- *the Howe*: turf, twelve barrows (`MOUND`, three cells wide, rows 16 + 16 k, 7..20 cells off the route to
  alternating sides), five standing stones (`MENHIR`, two cells tall, rows 30 + 40 k, six to eight cells off the
  route to alternating sides; each a landmark with an alpha's line, the mark on its face drawn when the cub is
  within four cells), a few trees, the wood's dark where the noise runs over 170; the stone mouth across rows
  218..220 with a wall of stone either side.
- *Gravehollow*: the Hush's night wood, the old den's bowl forced open (radius 20).

**The gates** (`terrain.GATE`, open ground to the forest and its flood, held by `sim.gate_shut`): the windthrown
pine (the Stand, a sneak), the burnt oak (the Burn, `sim.GATE_OAK`), the sett (the Teeth, paw 2), the stone mouth
(the Howe, `sim.GATE_MOUTH`). A lunge within four cells of the oak's or the mouth's middle, facing it, opens it for
the journey (`sim.gates`); a bite there shows the hint. An open gate draws dim.

**The arenas** (item 12): the boar's clearing 11 -> 14 (`forest.BOAR_RADIUS`), the lynx's bowl 12 -> 14
(`LYNX_RADIUS`), the elk's ford 14 -> 18 (`ELK_RADIUS`), the old den's bowl 12 -> 20 (`ALPHA_RADIUS`); the shapes
kept (the clearing round, the bowl with its three pillars, the ford astride the bank). The alpha's arena is
Gravehollow's; its fight starts at the cold den as before and the fighter walks the way on through the Howe and
opens the stone mouth with a lunge (`fight.walk_on`), every attempt, as a player does after a death.

**The reveal** (the Stand's lookout): the cub within two cells of the lookout starts sixty ticks of the map
(`sim.reveal_at`, `sim.revealing`); it re-arms when the cub is six cells off. Transient, never saved; the replay
carries it through the keys.

**Save schema 7** (`journey.lu`, over cb13's and cb15's schema 6): schema 5's lines, the slain line with thirteen
masks (`forest.AREAS`), `gates N` (0..3), then cb13's `name` and `played_ms` and cb15's `items` line before the
check, seventeen lines; `shortcuts` 0..511 (bit 128 needs paw 2), `caches` under 2^42, `mark_area` 0..12,
`last_den` 0..7 and 11..15. A schema-6 file (seven masks, cb13's wrapper, cb15's items, `journey.AREAS_V5`)
migrates with its items, lore, name and time kept, empty masks for the six new areas and no gate opened; a
schema-5 file the same way with name `journey` and no time; schema 4 as before; 1..3 refused by name. The
replay's snapshot is `journey 6`: `saved-0`..`saved-210` (the thirty values, the thirteen masks, the gates,
cb15's 167 pouch slots; slots 204..210 are events 218..224, appended); a `journey 5` snapshot (cb15: 204 values,
seven masks), `journey 4` (37) and `journey 3` (30) are still read.

**The score** (`score.area_part`): the new areas and Gravehollow are `none` (the silence) until cb17; the Hush
keeps cb04's `old-den` slot. **The NPC anchors** (cb16) are the landmarks: the lookout and the ruin (the Hermit),
the kiln (the Charcoal-burner), the causeway's post (the Ferryman), the sett (Dunmoss), Quill's perch as before.
**The foe tables** (cb18): `sim.group_count` is 0 for the six areas; their alcove guards are foxes until then.

**Measured** (fifty seeds, both fields; `notes/cb14-evidence/`): see the note's tables (the world audit's 1300
rows, the den spacing, the foe census, the bends, the spurs, the journey's length before and after, the boss
census, the generation and render costs).

## The missing soundtracks, 2026-10-29 (cb17, proposed)

`docs/SCORE.md`: fourteen original parts, a part for every area (the Teeth, the Shallows, the Hush,
Cinderwick, the Stand, the Burn, the Mere, the Underteeth, the Howe, Gravehollow), Moonford at the end (the
title's call in D major, where the title played before), and three moments the schedule reads from the
ground (`score.moment_of`, read-only over the simulation): **the reveal** (`sim.revealing`'s sixty ticks;
the part is eight seconds and holds to its end like the sting, only a fall cutting it), **the crossing**
(the Mere's local rows 61..163, between its sixty-row causeways), **the walk** (the Howe from its fourth
standing stone, local row 150, to the stone mouth); a change between an area's part and its moment sounds once
it has held 30 ticks (`score.SETTLE`). **The Hush's wait** (R-cb17-1 A): 300 ticks of the
silence after an entry while the cold den (den 6) is unlit, then the shadows' motif; once lit, the motif at
once. **The bank** (R-cb17-2 A): a replay's mixer holds the cues its own scenes reach, at most the engine's
sixteen. **The prepare** (R-cb17-3 A): one part rendered, written and dropped at a time. The numbers (300
ticks, row 150, the 60-row causeways, the parts' lengths and levels) are the maintainer's to change by play.
