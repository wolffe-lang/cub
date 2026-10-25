# Design constants

Every tuning number in cub is a named constant in `src/sim/sim.lu` or `src/terrain/terrain.lu`, mirrored
here with the date it was set and by whom. The design bible (`sprints/lair/cub/design.md` in the planning
repo) is the oracle; a number is **proposed** until the maintainer's play says otherwise (R-CB-7), and new proposals here are submitted for review; the private bible is not edited by this lane.

The Shingle now has a fight, rest and recovery loop. The rest of the area graph follows next.

## The cub's stats (`src/sim/sim.lu`; the bible's section 3)

| constant | value | meaning | set |
|---|---|---|---|
| `STAT_START` | 1 | heart, wind, fang, paw and nose at the start; each 1-10, grown at dens with scent (cb01) | 2026-10-25 proposed |
| `health_max(heart)` | `40 + 12 × heart` | health at a heart level: 52 at the start | 2026-10-25 proposed (the bible) |
| `stamina_max(wind)` | `60 + 10 × wind` | stamina at a wind level: 70 at the start; moves spend it | 2026-10-25 proposed (the bible) |
| `trot_at(paw)` | `round((TROT_V + 2 × paw) × 1.10)` | the trot at a paw level: 42 at the start | 2026-10-25 proposed (the bible) |

## The cub's motion (`src/sim/sim.lu`)

| constant | value | meaning | set |
|---|---|---|---|
| `TROT_V` | 36 | the trot's base, fixed-point units a tick (256 a cell): 0.15 cells a tick, 4.4 a second, a cub's pace under pack's wolves' 40 | 2026-10-25 proposed |
| `SNEAK_V` | 21 | a sneak (Shift+arrow): half the current paw-dependent trot; no trail is laid and foes perceive by sight only | 2026-10-25 proposed (the bible, section 4) |
| `ACCEL` | 4 | acceleration, FP units a tick each tick: the trot from a stop in 9 ticks | 2026-10-25 proposed |
| `BRAKE` | 8 | braking: a stop from the trot in 5 ticks; a cub stops faster than it starts | 2026-10-25 proposed |
| `TURN` | 256 | heading units a full turn: 0 north, 64 east, 128 south, 192 west; the diagonals between when two arrows are held | 2026-10-25 cb00 |
| `TURN_RATE` | 16 | the maximum turn rate, heading units a tick: a quarter turn in 4 ticks, about in 8 (267 ms); the cub turns, never pivots | 2026-10-25 proposed |
| the held key | the engine's `input.Hold` | a press holds `HOLD_TAP_TICKS` 12; an autorepeat run holds one interval plus `HOLD_MARGIN` past its last press (pack's pk01 model, in the engine) | 2026-10-25 the engine's |
| the camera | the cub's cell at the centre | R-CB-3: the world scrolls under the cub in every direction; a resize keeps it at the centre | 2026-10-25 ruling #130 |

Opposite arrows held together cancel (the cub brakes); a blocked cell stops the cub on that axis and the
other axis still slides, so a wall is followed, not stuck to.

## The Shingle (`src/terrain/terrain.lu`; the bible's section 2)

| constant | value | meaning | set |
|---|---|---|---|
| `LATTICE` | 24 | cells between the cover noise's lattice points, both ways: the woods thicken in patches about this size | 2026-10-25 proposed |
| `BANK_ROW`, `BANK_SWING` | -8, 4 | the Ashwater's edge wanders between world rows -8 and -4 (the cub starts at row 0) | 2026-10-25 proposed |
| `REED_ROWS` | 2 | rows of reeds at the water's edge (open ground) | 2026-10-25 proposed |
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
never damages. These are recommendations, not decisions by this implementation.

R-cb01-3 recommendation: the bible gives 30 ticks to drink and 40 health over
15 ticks. Prepare for the first 15, heal by exact integer instalments during
the last 15; any damage interrupts and the mouthful is already spent.

Additional proposed values, all 2026-10-25:

| mechanic | values |
|---|---|
| stamina | `REGEN` 2 standing, 1 walking, none during moves; exhausted at zero; `EXHAUST_RECOVER` 24; no sprint binding exists yet |
| posture | fresh above 2/3, tired above 1/3, spent below; limp halves trot below 1/3 health |
| weasel | health 8, damage 10, scent 8 (bible); crouch 12, active 2, retreat/recovery 24 ticks |
| fox | health 24, damage 16, scent 20 (bible); feint 10, gap 6, real crouch 12, active 3, retreat 24 ticks; steals one water on a hit |
| foe motion | 44 pursuit / 48 retreat FP units per tick, acceleration 4, turn rate 16, stamina cap 60, attack costs 12, hunt restores 1/tick |
| perception | 90-degree forward cone, sight 8 cells; scent search 6 cells, newest unexpired visible sample; half-cell ray sampling |
| trail | 300-tick lifetime (bible); one sample per changed cell, none sneaking; old trail remains until expiry |
| water and death | 3 mouthfuls; 40 healed; 30-tick death fade (bible); mark recovery within 1 cell |
| growth | each stat starts 1, cap 10; next level costs 40 × next level (80 for level 2), only at den |
| den | within 1 cell of start; reset health, stamina, water, foes, trail and holds; gate and dropped mark persist |
| collision | ground bodies remain at least 1 cell apart; attack envelope and visual arc are separate |
| Shingle layout | den at seeded start; weasels x=9,13 and fox x=20 at start y; open fight strip x=3..22, y=start-1..start+2; southern path x=-2..2 through start+16; gate across path at start+10 |

The fox on the Shingle is a combat preview, not the later named fox's story
state. Bleeding, cold, further areas, save persistence and the difficulty
selector are not in this pass. It implements the default wolf rules.

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

## Directional attacks, 2026-10-25

The maintainer's word: "Leaps should be directional — pack pulled this off mostly."
`AIM_WINDOW_TICKS = 15` (500 ms, inclusive), the same name/value as pack's
pk06b proposal. Arrows held or pressed in the window before the attack
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
