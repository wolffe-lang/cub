# cub's replay file

## Pouch checkpoints (cb15, CUB 6 / journey 5; cb14's CUB 7 / journey 6 below)

Key ids0..36 and numeric event ids0..50 are unchanged. `inventory` is
appended key37. A new initial `journey 5` carries204 numeric slots: the
previous37 followed by pine, ice, tuft, tuft-use count, seeded-area mask,
lore count, ground count,32 padded lore-id-plus-one slots, then128 padded
packed pickups. New saved slots37..203 are appended numeric events51..217;
older `journey 3` and `journey 4` remain readable with empty new fields.
Those recorded journey versions select the original six-row rest menu,
including its Up-to-Confirm shortcut; journey5 selects seven rows with Lore.
Only the replay reader sets this compatibility state from its recorded
journey version. No player flag, save field or CLI option can enable it;
ordinary new/resumed live games always use seven rows.
The ordinary arrows, bite/Space, release/Esc, rest/r and inventory keys
fully reproduce the paused overlay; no menu input is omitted or read
from wall time. The six `pouch-*` cases disclose their initial item/lore
fixtures. The drop case walks away from a den before dropping and using r.

CUB 6 text appends `items pine ice tuft uses seeded lore-count ground-count`
after `name` and `played_ms`, then the live lore values and packed pickups.
Original CUB6 wrappers without `items` migrate with an empty extension;
metadata stays outside deterministic numeric snapshots. Text omits padding.
The fixed limits are **32 discovered lore lines** and **128 ground pickups**;
invalid counts, padding, duplicate lore, item caps and packed area bounds
are rejected before use. All dropped items and finite seeded discoveries
survive reload, including the original cell and stable order. Timed effects
and open menus are transient; resuming still wakes at the saved den.

A packed pickup is `(((area*5+kind)*20001+x+10000)*200001+y+100000)+1`,
with cell x in[-10000,10000], y in[-100000,100000], kind0..4 and a valid
area. Zero denotes an unused snapshot slot. CUB 4 and5 validate their old
canonical bytes/checksum before migration; old yarrow/marrow counts are
clamped to the new5/3 caps. New saves enforce every cap. Tuft uses and
ordered, de-duplicated lore are permanent journey state.


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

## Death and counter presentation (cb12)

No replay word, id, journey field or save field changes. The fatal tick still
writes the mark and the death archive immediately. The post-fade `FALLEN` card
and reversed opening eyes are a deterministic part of the fall state; skip keys
are ordinary recorded keys, consumed after the twenty-tick word hold. Without
a skip wake moves from death age30 to381. Old files parse unchanged but use the
new scene timing, as they do for the cb06 opening. Production `--replay` follows
only recorded keys, including the full card when no skip was recorded.

Headless `--script` is a fixture harness: by default it injects an ordinary skip
at the first allowed tick. `--full-death` or `# full-death` retains the full card
for scene goldens. Walkers record the same skip explicitly, so their generated
replays agree live and headless. This fixture convenience never alters a loaded
production `--replay`. The memory probe types a real Space after a traced fall's
minimum hold; the ordinary live recorder owns that event.

The HUD count is computed once from each completed sim tick's exact scent, not
from wall time or the number of render calls. Its integer batches do not alter
replay time, simulation currency, score, saves or death trailers. `# counter-frames`
is a fixture-only output request: each integer gets `count-TICK-INDEX-VALUE.txt`
and `.sty`, in addition to the normal sampled/final frames. The compatibility
row compares every batch byte-for-byte with a `--replay` run sampled differently.

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
| `ghost-x`, `ghost-y`, `ghost-face`, `ghost-pose`, `ghost-area` | one frame of a death's trailer, at its tick (fixed-point x and y, the body's tagged facing (8 + eighth, 8..15; legacy 0..3 quarters remain readable), the pose, the area) |
| `ghost-death N` | the death's serial, at the death tick |

A death archive is the run through the fall as before, with the trailer merged in tick order (the last 90
ticks); the ghost reader (`src/ghost/ghost.lu`) is the engine's `replay.from_text` and `replay.args_at`,
nothing the sim does. A headless case shows an archive directory with a `# ghost-dir DIR` comment line
(read only; `--ghost-dir` on the command line wins, and alone enables writes). An archive from another
seed, or without a trailer, is skipped by name.

New `ghost-face` values are 8 plus the clockwise eighth (0 north, 1 north-east,
2 east, through 7 north-west). Values 0..3 in older archives retain their
cardinal directions: the reader converts them to eighths 0/2/4/6. No event
ids or replay/save schema numbers change. The tagged range prevents an old
east-facing ghost from silently becoming north-east.


`--make-world-proof DIR` also writes the boss scripts (`boss-<name>-windup`, `-phase2`, `-beaten`: the
scripted fighter's real keys from the boss's den, cut at its first windup, its second phase and the win),
`end` (the alpha beaten, the three frames, the card, `r`), `ghost-death` and `ghost` (a walk, a fall, and
the walk past its archive in `tests/ghosts/`), the areas' first screens (`crags`, `river`, `hush`, and
cb14's `stand`, `burn`, `mere`, `underteeth`, `howe`, `gravehollow`; `--make-area-proof DIR` writes these
alone), the landmarks (`landmark-<area>-<k>`) and `demo`. `--boss-census`
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

Since cb14 a live recording begins with `journey 6` and `saved-0` through
`saved-210`: the thirty values below, a slain mask an area (thirteen), the
gates word and cb15's 167 pouch slots (`saved-204`..`saved-210` are the
appended events 218..224); `journey 5` (cb15: 204 values, seven masks),
`journey 4` (37 values, cb05's seven masks) and `journey 3` (30) are still
read. Before cb14, recordings used `journey 3` and thirty values, `saved-0` through
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
Since cb11, an enhanced Space repeat also records no `bite` (its modifier
transitions may still be recorded); releases remain non-actions. The
legacy `bite` word has a <=2-tick repeat filter in inferred mode. An
`exact` recording bypasses that heuristic because the reader already
removed repeat events. No ids, headers or persistent save slots change.
Old recordings still parse, but newly accepted early/end-boundary/grace
requests and suppressed legacy repeats can change their simulated result.
The transient two-request queue is reconstructed from keys, never saved.

`pace N` records the debug percentage25..300 (default100). The explicit
`combat-witness 1` event reproduces the test-only empty-arena setup used
by live chord rows. Neither is part of a persistent journey schema.
Held directions, rather than a recent-arrow window or lock override,
commit bite and roll aim at the input event. `dodge` now means the roll;
`ctrl-down`/`ctrl-up` express sprint, never repeated `dodge`.

## cb10 — compatibility after the small faults (2026-10-28)

The pk 1 vocabulary, saved snapshot and event numbering are unchanged.
Older files still parse and replay their recorded keys; no key is
invented or rewritten. They do **not** promise the same frames: an older
legacy Ctrl recording can sprint across a gap that formerly expired,
sprint moves one fixed-point unit faster, a fox hit now steals scent
rather than water, and a low hawk is biteable. Exact Ctrl-up remains exact.
The existing witnesses are retained; changed frames are identified in
cb10's golden-change receipt. `--small-faults` uses an explicit fixture
and a parsed ordinary-key record, not a claimed saved natural journey.


## The fire menu and CUB 6 (cb13)

Save-only metadata (`name`, `played_ms`) wraps the unchanged simulation
payload. CUB 5 migrates on read with name journey and zero elapsed time;
CUB 4 still migrates with empty slain masks. Numeric replay snapshots remain
`journey 4`, slots0..36; no existing key or event id changes. The menu is
outside the gameplay recording: its keys do not attack, alter the seed of a
resumed save, or consume a gameplay tick. New gameplay still records its
opening event. Old title events reproduce the original title scene.

Live sessions record by default under `~/.cub/replays/`, with `--record FILE`
as the explicit override; deaths remain under `~/.cub/ghosts/`. Replay bytes
are deterministic session data: no wall-clock date is written into a `.pk`.
The chooser's recorded date always comes from the file's modification time,
never a comment inside the archive. Live session files may carry a deterministic
`# ending TEXT` comment (Finished or In progress); death archives retain their
existing byte shape and the chooser derives Fallen from the ghost-death event.
No story ending is invented for an older recording. Duration is (last event
tick + 1)/30. Playback never writes saves or default recordings; Esc returns
to the fire.

`# fire-menu` marks synthetic headless menu fixtures. Only that explicit
comment routes existing up/down/bite/confirm/release/quit keys into the menu
state machine, using fixed `/fixture/` registry and recording data, never
files under the viewer's HOME. `final.state` appends the page, row and action.
The menu fixtures pin both tiers; existing title and den goldens are unchanged.

## The NPCs: CUB 8 and journey 7 (cb16)

Key ids 0..37 are unchanged and no key is added. A live recording begins
with `journey 7` and `saved-0` through `saved-238`: journey 6's thirty
values, thirteen masks and the gates word, then the pouch's seven scalars,
**48** padded lore slots (32 before) and the 128 pickups, then the NPCs'
twelve: what each of the nine has said, the dead mask, Quill's perch (-1
for Larkmeadow's) and the NPCs' flags. `saved-211`..`saved-238` are the
appended numeric events 225..252 (`EV_COUNT` 253). `journey 6`, 5, 4 and 3
are still read: a journey 6 snapshot's pouch takes 32 lore slots, and every
older snapshot meets the NPCs as a CUB 7 save does (nothing said, the sett's
open shortcut as Dunmoss's dig, a seeded Bramblehold as Ember's tuft given).
The speech frame, the trade list, Ember's feint and the crossing are
transient and replayed from the keys; `final.state` gains nothing (its
existing integers are byte-equal for every committed case).

CUB 8 text is CUB 7's lines and one `npcs` line between `items` and `check`:
`npcs S0 .. S8 dead D perch P flags F`. A CUB 7, 6, 5 or 4 file migrates on
its next write; a CUB 7 holds at most 32 found lore lines, a CUB 8 48.

`--make-npc-proof DIR` writes `npc-talk` (Quill's first line at his perch,
from the grass nest: the walk, twenty still ticks, the frame, Space to the
wares, Esc), `npc-trade` (the same walk with a disclosed 100-scent fixture:
pine 50 and yarrow 20 bought) and `npc-toll` (the Ferryman's post from the
dry island with a disclosed 70-scent fixture: sixty paid, ninety ticks on
the water, the far causeway). Every key is the walker's or pressed by name.
## New-foe test arenas (cb18)

`cub --new-foe-proof DIR` writes six `foe-N.pk` records and complete frame
captures on both tiers. These are explicitly staged test arenas, not
production journeys: the command selects each kind and initial arena, then
all movement and attacks are ordinary keys. Each record is parsed through
the existing pk1 vocabulary and replayed from that same initial fixture;
position, health, scent and foe outcome must match the recorded run.

The marten fixture starts with one real held yarrow and
waits for an actual theft before answering. The moth fixture must observe
dimming; the heron fixture must use a dodge and pass; the glow-worm fixture
walks into contact and retains every white frame; the wisp fixture snuffs
rather than kills. The separate600-world arena census uses the real-key
fighter, not fixture assignments after the starting state.

No replay word, numeric event id or save schema changes for these arena
commands. They do not enter the live menu/save/overlay routing. Ordinary
old journeys keep their hawks; no old floating foe is silently retyped.

Each record also has a final rich/plain frame of the actual resolved
encounter, so the absent snuffed wisp and passed heron are pinned visually,
not inferred only from an earlier windup frame. The final diagnostics
separate health, phase and death tick: a passed heron is not a kill and a
snuffed wisp remains alive.
