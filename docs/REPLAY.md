# cub's replay file

The `.pk` format is the engine's (lair's `docs/REPLAY.md`: the header, `t TICK KEY`, `t TICK size WxH`,
the numeric events, the `# score` comment). cub's words in it are its vocabulary (`src/controls/controls.lu`,
`controls.vocab`):

| key | word |
|---|---|
| Up, Down, Left, Right | `up`, `down`, `left`, `right` |
| Shift+Up, Shift+Down, Shift+Left, Shift+Right | `sneak-up`, `sneak-down`, `sneak-left`, `sneak-right` |
| Space | `bite` |
| `x` | `lunge` |
| `s` | `heavy` |
| `z` | `parry` |
| `c` | `dodge` |
| Tab | `lock` |
| `w` | `water` |
| `r` | `rest` |
| `q` | `quit` |
| Esc | `release` |
| 1–5 (inert, retained for old recordings) | `heart`, `wind`, `fang`, `paw`, `nose` |
| Enter at rest | `confirm` (new id27; earlier ids unchanged) |
| `m` | `mute` (cb03: the music off and on; inert in the simulation) |
| Ctrl-C (legacy byte or enhanced key/modifier) | `interrupt` |

Every key is recorded. Numeric `health N` and `scent N` events are explicit
test/debug deltas, not enemy actions: negative health is ordinary interruptible
damage; positive health is clamped to maximum. Health deltas precede scent
deltas, before the tick. These events are accepted in both replay paths.

The scripts cover movement, each combat move, the fox's two tells,
trail expiry, resting and growth, death and scent recovery, and the thorn gate.
Goldens include `final.state`, an integer simulation snapshot, alongside the
cell text and styles. The native and release backends must agree on both
visual tiers, and the semantic gate asserts events actually occurred.

A live death writes the complete run through the fall to `~/.cub/ghosts/`.
`--ghost-dir DIR` overrides that path, and explicitly enables archive writes
for headless tests. Replaying a file live writes no archive unless `--ghost-dir` explicitly requests it.
A zero health event fixes the exact death tick even when no input arrived
there. The filename is seed, final tick and a collision counter, created exclusively;
concurrent games never truncate an earlier archive. `tools/gameplay.py` replays a natural death archive and compares its
entire cub state at that tick. Ghost display and hostile ghosts follow later.

Archive write failures return exit 2 (the live path restores the terminal
first). Files are not pruned or overwritten by this build.

The `heavy` event names the `s` fallback attack (2026-10-25). Space remains
`bite`; recovery presses advance the three-bite combo without a separate
combo key. Recent arrows and lock are sampled in event order, so records
retain the order of same-tick movement and attack events.

## Connected-journey events (schema 1)

`opening 1` starts the timed Moonford opening (900 ticks since cb06). `skip` is any decoded
key with no gameplay binding; any ordinary key also skips while a scene
is active, without also performing its gameplay action. A new live journey
records the opening; old scripts without that event keep their start.

A live recording begins with `journey 1` and `saved-0` through `saved-23`:
seed, difficulty, heart, wind, fang, paw, nose, water capacity, scent,
last den, lit dens, shortcuts, gate, story, deaths, mark present, mark area,
mark x, mark y, mark scent, caches, yarrow, marrow, opening seen. These
fields use the same validator as the save file. A resumed recording or
death archive is therefore self-contained; it never reads `~/.cub/save`.

`--make-world-proof DIR` generates reproducible real-key encounter and
world scripts. The long journey grants 10000 scent as an explicit numeric
fixture, spends it normally at the first den to grow heart/wind/fang, then
walks all three areas, opens both shortcuts, fights a hawk and recovers a
forced death's mark across an area edge. The shorter encounter scripts use
default growth, no injected health/scent, and include a natural death.
The independent `--world-audit` flood checks all den/portal/cache targets,
path straight runs, gentle bank steps, visible forest fill and useful walking distances, and enemy distances over seeds 0..49.

A saved journey keeps its seed. An explicit conflicting `--seed` is a named
`save_seed_conflict`, not a silently ignored override. A replay header that
disagrees with its initial journey snapshot is corrupt and is rejected.
Ordinary scripts without a snapshot still accept a seed override.


The coast refresh also produces `coast-cache-0` and `coast-cache-1`:
ordinary movement, combat and interaction after the connected-journey
witness, collecting both finite bundles. They inherit that witness's
explicit growth-scent fixture, not extra health or teleports. The default-
growth natural-death witness re-engages the fox after retreats. Source
replays are regenerated when routes change; semantic gates still require
the fights, gate opening, deaths, shortcuts and cache collection to occur.

## cb04: the title, the bosses, the ghosts' trailer (schema 3, `journey 2`)

A live recording begins with `journey 2` and `saved-0` .. `saved-28`: schema 2's twenty-five values
(above) then `bosses`, `end`, `played`, `lost`. `title 1` at tick 0 starts the title scene (recorded by a
live game without `--no-title`; the key that ends it follows as itself); `bosses N` is an explicit fixture
for the beaten bits. The new words:

| word | meaning |
|---|---|
| `title 1` | the title scene from this tick |
| `bosses N` | the beaten bits (1 boar, 2 lynx, 4 elk, 8 alpha), a fixture |
| `ghost-x`, `ghost-y`, `ghost-face`, `ghost-pose`, `ghost-area` | one frame of a death's trailer, at its tick (fixed-point x and y, the body's facing 0..3, the pose, the area) |
| `ghost-death N` | the death's serial, at the death tick |

A death archive is the run through the fall as before, with the trailer merged in tick order (the last 90
ticks); the ghost reader (`src/ghost/ghost.lu`) is the engine's `replay.from_text` and `replay.args_at`,
nothing the sim does. A headless case shows an archive directory with a `# ghost-dir DIR` comment line
(read only; `--ghost-dir` on the command line wins, and alone enables writes). An archive from another
seed, or without a trailer, is skipped by name.

`--make-world-proof DIR` also writes the boss scripts (`boss-<name>-windup`, `-phase2`, `-beaten`: the
scripted fighter's real keys from the boss's den, cut at its first windup, its second phase and the win),
`end` (the alpha beaten, the three frames, the card, `r`), `ghost-death` and `ghost` (a walk, a fall, and
the walk past its archive in `tests/ghosts/`), `crags`, `river`, `old-den` and `demo`. `--boss-census`
fights every boss in fifty seeds at both sizes and prints a `fairness` line a boss (exit 1 on a world
unwon within five lives, a parryable telegraph under the parry window or a boss tick outside its arena);
`--fight-trace KIND SEED` narrates one fight a tick.

## cb03a feel witnesses

`dodge` remains the recorded `c` event. Repeated events infer sprint; no
new decoder or replay opcode is needed. `bite` chooses a snapping lunge
when sprinting. `aim-*` now witness Space rather than `x`, because `x`
uses facing. `forward-windup`, `sprint-80x24`, `sprint-120x40`, `sprint-hit`,
`den-bars-80x24`, `den-bars-120x40` and the meadow/den refuge cases pin the
new frames. The sprint-hit walker approaches a real foe and lands with
ordinary keys, without health, stamina or position fixtures. The chase
census separately isolates each ground species with100 health to observe
a hit without deleting the body; it preserves default cub stats and uses
only movement, c and Space after that disclosed setup. Hawks still require
parry, not a ground chase.

## cb04a: progression (schema4, `journey 3`)

Current recordings use `journey 3` and thirty values, `saved-0` through
`saved-29`. Slot29 is the total level, checked against the five stats.
Slot7 is discovered water capacity0/2/3, not an unconditional three.
Older journey snapshots fail `save_version`; scripts without a snapshot
still start a fresh cub. Versioned save files similarly refuse schema1–3.
The cb04a words remain valid. Since cb04d, numeric stat keys are inert;
arrows allocate pending levels and `confirm` (id27) or `bite` on the
Confirm row applies them. Pending choices are replayed, never saved.

`--make-den-proof DIR` writes the six regional rest scenes at both sizes,
`den-checkpoint`, `spring-drink` and `water-refill`. Scene fixtures explicitly
start at the named den with two found mouthfuls and100 scent; they do not
claim to prove discovery. `den-checkpoint` starts at den8, walks to den2's
contact edge with ordinary keys, enters/leaves, walks away, then uses a
single disclosed fatal health delta. Its death mark and wake are asserted
through both headless and live replay. The spring/drink/refill scripts
start fresh, reach the first spring with keys, use a disclosed30-health hit,
drink, and return to rest. `spring-found` is the long world witness's actual
first discovery. The fox theft witness also walks to the spring first.

The live trace and `final.state` include `resting`, `capacity`, `level` and
`meat` as applicable; these are observations, not input events. The
`den-contact` pty row needs no fixture at all, and fails on the older
one-cell interaction range with the same injected arrow/r/Esc bytes.


The opening keeps `opening 1` and normal key events. Since cb06 the
sequence lasts 900 ticks instead of 270; its shot table is in DESIGN.
Existing recordings parse unchanged but use the new animation and timing.
New recordings reproduce it deterministically; no journey/save field or
replay-format version changes. A skip key is consumed by the scene.

## Held input and pace (cb04b)

Key ids0..27 remain unchanged. New words are `exact`, `ctrl-down`,
`ctrl-up`, `shift-down`, `shift-up`, and `up-release`, `down-release`,
`left-release`, `right-release`. A live negotiated recording starts with
`exact`; ordinary old recordings retain inferred holds. Modifier changes
precede the associated action. A key release never fires its action.
A repeated c in the enhanced stream does not queue another roll.

`pace N` records the debug percentage25..300 (default100). The explicit
`combat-witness 1` event reproduces the test-only empty-arena setup used
by live chord rows. Neither is part of a persistent journey schema.
Held directions, rather than a recent-arrow window or lock override,
commit bite and roll aim at the input event. `dodge` now means the roll;
`ctrl-down`/`ctrl-up` express sprint, never repeated `dodge`.
