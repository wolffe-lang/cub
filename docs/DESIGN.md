# Design constants

Every tuning number in cub is a named constant in `src/sim/sim.lu` or `src/terrain/terrain.lu`, mirrored
here with the date it was set and by whom. The design bible (`sprints/lair/cub/design.md` in the planning
repo) is the oracle; a number is **proposed** until the maintainer's play says otherwise (R-CB-7), and a
change here is a change there in the same commit.

The scaffold (cb00) moves a fresh cub on the Shingle. The moves, the foes, the dens, scent and the areas
are cb01's and cb02's; their numbers are the bible's sections 4 to 8 and arrive with them.

## The cub's stats (`src/sim/sim.lu`; the bible's section 3)

| constant | value | meaning | set |
|---|---|---|---|
| `STAT_START` | 1 | heart, wind, fang, paw and nose at the start; each 1-10, grown at dens with scent (cb01) | 2026-10-25 proposed |
| `health_max(heart)` | `40 + 12 × heart` | health at a heart level: 52 at the start | 2026-10-25 proposed (the bible) |
| `stamina_max(wind)` | `60 + 10 × wind` | stamina at a wind level: 70 at the start; nothing drains it yet | 2026-10-25 proposed (the bible) |
| `trot_at(paw)` | `TROT_V + 2 × paw` | the trot at a paw level: 38 at the start | 2026-10-25 proposed (the bible) |

## The cub's motion (`src/sim/sim.lu`)

| constant | value | meaning | set |
|---|---|---|---|
| `TROT_V` | 36 | the trot's base, fixed-point units a tick (256 a cell): 0.15 cells a tick, 4.4 a second, a cub's pace under pack's wolves' 40 | 2026-10-25 proposed |
| `SNEAK_V` | 18 | a sneak (Shift+arrow): half the trot; no trail is laid (cb01) and foes perceive by sight only | 2026-10-25 proposed (the bible, section 4) |
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
