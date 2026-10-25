# cb00 — the scaffold on the engine (M-CB0, cub's half)

Lane cb00 of track 19 (the cub track, ruling #130; the planning repo's `sprints/lair/cub/00-the-engine/
cb00-the-engine.md`), Fable, crawl 54, 2026-10-25. The lane's main account is in lair's
`notes/cb00-the-engine.md` (the extraction of pack's engine, pack re-pinned with its goldens byte-identical);
this note is cub's: the layout on the engine, the first screen, and the cb01 draft. The repository was a
licence and a README stub (`ba4d1f5`).

## 1. What this pass does

- **The layout on the engine** (`bf7d2e1`, `1c97f48`): `lair.pin` names the engine's commit; `tools/fetch-lair`
  stages it into `.lair/` and refuses a mismatch (a staged tree whose modules the game's symlinks cannot find
  is refused too: the pin plant found the first check blind to dangling links, fixed); `src/<module>` is a
  symlink into `.lair/src/` for each of the ten engine modules, so `use grid` reads as in pack and in the
  engine. The engine's tools run from `.lair/tools/`; `tests/lair.conf` tells them cub's trap tick, the agree
  rows' case and that cub has no run arguments and no bench yet.
- **The controls** (`ef2712c`; `src/controls`): cub's vocabulary over the engine's decoder, the campaign's
  table and the bible's section 4: arrows walk, Shift+arrow sneaks (so Shift+Down is a sneak, not pack's
  parry; cub's parry is `z` alone: R-cb00-4 A), Space bites, `x` lunges, `z` parries, `c` dodges, Tab locks
  on (the engine's decoder gained Tab for it), `w` drinks, `r` rests, `q`/Esc quit, Ctrl-C interrupts.
  Every key is in the replay vocabulary from this build, so a run's file is complete; the scaffold applies
  the movement keys and the quit.
- **The Shingle** (`2ebdda5`; `src/terrain`): the first ground of the bible's section 2, from the engine's
  noise and hash: the Ashwater to the north with a bank that wanders four rows, two rows of reeds, five of
  gravel, then Thornmere's cover from a two-dimensional value noise (lattice 24 cells both ways, built on
  the engine's hash) that draws grass with the odd trunk, the woods, and deep forest in patches. Trunks,
  deep forest and water block the cub; the start is open gravel on every seed (a test over forty).
- **The cub** (`37626c4`; `src/sim`): a position in fixed point, a heading in 256 units a turn that turns at
  `TURN_RATE` 16 toward the held direction (the diagonals when two arrows are held; opposites cancel) and
  never pivots, a speed that rises at `ACCEL` 4 toward the trot (`TROT_V` 36 plus 2 a paw: 38 at the start)
  or the sneak (18) and falls at `BRAKE` 8; the engine's held-key model on the eight movement keys; a
  blocked cell stops the cub on that axis and lets the other slide. The camera is the cub's cell at the
  centre (R-CB-3); a resize keeps it there. The stats of the bible's section 3 as the first constants (heart,
  wind, fang, paw, nose at 1; health 52, stamina 70), draining nothing yet. Every number `docs/DESIGN.md`'s,
  proposed (R-CB-7).
- **The sprites and the frame** (`5906315`, `eb88027`; `src/sprites`, `src/art`): the rich cub is two by two,
  its ears the quadrant blocks on the side it faces (`▝▘` over `██` facing north; `▘█`/`▖█` west; and so
  on) in a tawny 180 on the gravel's 240; the plain cub a bold `C` with `^ > v <` beside it. The ground is
  pack's forest texture plus the Shingle's marks, reeds `⠇⠖` and the water's `≈`. Sixteen rich code points,
  thirteen of them pack's (`docs/GLYPHS.md`, held by a test). The sheet shows the cub facing four ways over
  the Shingle's bands, both tiers committed as goldens.
- **The entry** (`4bed5f2`; `src/cub.lu`): pack's loop shape without the title and the cards: the live loop,
  `--headless` (the engine's frame formats), `--replay`/`--record`, `--apply`, `--art-study`,
  `--probe-glyphs`, `--selftest` (cub's controls through the engine's decoder, whole and split at every byte,
  and the engine's diff property), `--trace`, `--trap-at`, `--ticks`.
- **Goldens and rows** (`d7ecc71`): eight cases on both tiers and the sheets (17 directories, 908 KB): a
  standstill, the walk north to the water (stopped at the reeds), a turn east, a sneak, the scroll (eight
  seconds west along the bank: the Shingle scrolls across the screen; south the cub meets the woods'
  trunks within six rows, which the first scroll case showed and the walk is open along the bank), a diagonal, the wide field, a resize. The engine's five pty
  rows (quit, ctrl-c, trap, agree-rich, agree-plain) with `walk-north` as the agree case.
- **CI** (`30d8301`): the workflow on the engine's planner and tools, the engine staged at `lair.pin` first in
  every job; `tier pr` is the planner's test and the Linux leg, `tier full` adds macOS; no perf job until
  `--bench` (cb01).
- **Docs** (`3a6235a`): `docs/ART.md` started, `docs/GLYPHS.md`, `docs/DESIGN.md` (the first constants,
  proposed, by the bible's sections), `docs/REPLAY.md` (cub's words in the engine's format), the README (the
  premise, what is in this build, the machines, the controls).

## 2. How it was tested

| what | where | result |
|---|---|---|
| `wolf fmt --check`; 75 unit tests on the checked machine (cub's 23 and the pinned engine's 61 through the symlinks, less the overlap `wolf test` counts), 0 SKIP | nomad; kasumi CPUs 4-7 in the container | green both |
| both tiers built, warnings denied; `cub --selftest` on the release binary | nomad; kasumi | green both |
| the goldens: 8 cases on both tiers and the sheets (17 directories) | written on nomad, byte-identical on kasumi at the first try | green |
| the pty rows quit, ctrl-c (the byte 0x03), trap, agree-rich, agree-plain | nomad; kasumi in the container (`notes/cb00-evidence/check-linux-kasumi.txt`) | all five green on both |
| the plant (item 5): the camera fixed on the start's row | `cb00-plant-camera`, cub#1 | red: section 6 |

What the rows and goldens caught: the `diagonal` case's events were written out of tick order by the
generating script and the engine's parser refused it (ticks never decrease), which is the parser working;
the first camera plant was caught by `sim_test`'s camera test before the goldens ran (`tools/check-linux`
runs the tests first), so the plant was narrowed to the camera's row alone, which the unit test (it moves
east) does not see and the scroll golden does.

## 3. Measurements

The scaffold has no perf gate yet (no `--bench`); the live loop's closing line on nomad for a one-minute
walk: render + diff 40 to 60 us a frame at 80x24 rich, the engine's numbers. The goldens: 908 KB. The
kasumi leg (fmt, 75 tests, both builds, the selftest, 17 golden directories, five rows): 95 seconds under
the lock.

## 4. Rulings asked (recommended and implemented)

- **R-cb00-4 (new) Shift+Down**: the campaign's controls table has `z` / Shift+Down as the parry, as pack;
  the design bible's section 4 has sneak as a held Shift+direction. (A) the bible: Shift+arrows sneak,
  parry is `z` alone; (B) the campaign: Shift+Down parries, sneak needs another key. Recommend (A): the
  bible is the newer, fuller oracle and a sneak in four directions needs the four Shift+arrows; a parry on
  one key is pack's `z` habit kept. Implemented.
- R-CB-5 (the campaign's open ruling, the minimum size): pack's 80x24 kept through the engine's `term`;
  nothing of cub's needs more.

## 5. What is next: the cb01 draft (M-CB1, the cub and the thicket)

Following the bible's sections 4, 5 and 8, and section 2's gravel bank and thicket:

1. **The moves** (section 4): bite (Space; 12 stamina; 3/2/6 ticks; reach 2; chains in recovery), lunge
   (`x`; 30; 9/3/12; reach 4; staggers what is not a boss), parry (`z`; 10; a `PARRY_WINDOW` of 9 against
   a telegraphed attack: the foe staggered `STAGGER_TICKS` 30 and a riposte at twice the bite), dodge (`c`;
   18; a 3-cell hop with `DODGE_IFRAMES` 6 + paw/2), lock-on (Tab: the camera and every move face the foe;
   Tab cycles, Esc releases, 60 ticks out of sight releases). Each with its posture glyph on both tiers;
   stamina draining and regenerating (`REGEN` standing, half walking, none running), exhaustion as the
   pant with no sprint, lunge or dodge until `EXHAUST_RECOVER`; the posture HUD's ear and tail bands drawn.
2. **One foe with windups** (section 8): the weasel — fast, bites and retreats, comes in twos; the crouch
   as its windup tell; one bite kills it, a parry sends it fleeing; 8 scent. Perception by sight (a cone)
   and by scent (the trail); a windup glyph, an active window, a recovery. The fox as the second if the
   first lands clean: the feint (a false windup, then the real one; dodge the first, parry the second), the
   stolen mouthful, 20 scent.
3. **The scent trail** (section 6): the cub's trail as a fading line (`TRAIL_TICKS` 300, shorter sneaking,
   none while sneaking), drawn faintly behind the cub on both tiers (the campaign's "the nose"); foes that
   track it show what scent is; scent as the currency, earned from the weasel and fox and shown only at the
   den.
4. **The den** (section 5): the hollow log on the Shingle as the first den; `r` at it rests: full heal, the
   water mouthfuls refilled (`FLASKS` 3; `w` drinks 40 over 15 ticks, interrupted by damage), the foes
   reset, growth spent (`SCENT_LEVEL_BASE` 40 × level on heart, wind, fang, paw, nose) — the den screen, the
   one place numbers appear.
5. **Death and scent recovery** (section 5, R-CB-1): health 0, the fall, a 30-tick fade, the scent left as a
   glowing mark where the cub fell, the cub waking at the last den with full health and flasks and the
   world reset; reaching the mark recovers the scent; dying first loses it (the mark replaced). The death
   written as a `.pk` for the ghosts to come (section 10).
6. **The thicket's edge** (section 2): the gate of thorns at the Shingle's south a lunge breaks, as the first
   use of the lunge and the way into Bramblehold (cb02's area).
7. Goldens for each (a bite landing, a parry, a dodge through a bite, the weasel's retreat, the trail
   fading, a rest, a death and the mark recovered), both tiers; the pty rows unchanged plus a `--bench` and
   the perf gate; `docs/DESIGN.md` grown with every number proposed; `docs/PALETTE.md` begun.

**Issues to file** (the lane files nothing): cub: the macOS owed rows for `docs/GLYPHS.md` (`cub
--probe-glyphs` in Terminal.app and iTerm2) and `docs/KEYS.md` (to be written with cb01, from the engine's
`keyprobe`); cub: `--bench` and the perf gate; cub: a `docs/PALETTE.md` with the dusk and night keyframes
per area.

**How the maintainer looks at it:** `cd ~/lanes/cb00/cub && target/cub` (the release tier built at the
final head by `LAIR_UNPINNED=1 .lair/tools/build --release` on the lane's symlinked engine; or, from a fresh
clone, `tools/fetch-lair && .lair/tools/fetch-toolchain && .lair/tools/build --release`); the arrows walk,
Shift+arrow sneaks, `q` quits; `--seed N` for another bank; `--tier plain` for PAX's view; `--record run.pk`
keeps the walk.

## 6. The plant

`cb00-plant-camera` (cub#1): the camera fixed on the start's row, never following the cub north or south;
the unit tests pass (the camera test moves east) and the goldens go red from the first tick of motion in
`walk-north`, `turn-east`, `scroll`, `diagonal` and `resize` on both tiers. The run id is in the hand-back.
