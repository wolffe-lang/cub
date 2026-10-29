# cub

A cub is separated from its pack on a frozen river crossing and carried into the Dark Wood, the part of
Thornmere the pack never hunts. It wakes on a gravel bank at dawn with its mother's scent gone cold and one
thing it knows: home is upstream, and up. A souls-like in the terminal, written in wolf: dens that reset the
forest, scent that is both what foes follow and what the cub spends to grow, death that drops the scent
where you fell, four bosses on the way home, and at the end a wolf, not a cub, that crosses the ford.

The second game of the lair, the wolf games collection, on the collection's shared engine
(`wolffe-lang/lair`, pinned in `lair.pin`); the first is `pack`.

**What is in this build:** a seeded route from the Shingle through
Cinderwick and Bramblehold up the Stand's ridge to Larkmeadow, over the Burn to the Teeth, across the Mere
to the Shallows, through the Hush and the Howe's barrows to Gravehollow, with the Underteeth under the Teeth
(cb14: thirteen areas, every one with two or three branches to guarded alcoves, every boss arena half again
as wide, the Stand's lookout showing the whole forest), the wide forest of cb05: areas of 288, 240 and 224 cells
(the Shingle's 160 stays the tutorial), at most two dens an area and never under 110 route cells apart,
each den drawn as the place its name promises and the retired dens standing as landmarks (the coal roots'
stump-field, the low embers' ring of coals, the ash shelter's charred frame), cache branches in four smooth
shapes (a slow S, a hook, a loop, a 180-degree turn where the field has room) with no sawtooth left, a
fork that rejoins and a second way into the boar's clearing in Bramblehold, pockets that end at an old
scent mark, and Cinderwick: the burnt town between the beach and the wood, its lane between ruined houses,
one-cell passages to walled yards with caches, embers that never went out, and the Ashen, its slow dead,
who walk toward any sound, raise their arms before a heavy blow and never leave the town. Twelve to
eighteen foes in each big area. The shore runs a screen past the view each
way to its rock jetties, and four winding offshoots leave it for guarded
bundle alcoves, every path in the shore's own gravel; the forest is one
trunk-and-canopy texture to every edge of the screen, the thicket and
meadow filling the field they were made for. The cub, the foes and the
bundle are solid pixel silhouettes. The cub has north and north-east drawings,
turned by quarters to face all eight movement and attack directions; foes
keep four facings. The cub trots at 9.375 cells a second, its paws and tail
keeping time with its stride. The HUD is health, stamina and scent and
nothing else: a red health bar and a green stamina bar flush on the
forest at top-left, growing with the stats, their one-word labels beside
them and the water charges in a line under them; the scent the cub carries
as one big number in the bottom right corner, drawn in an original
block-glyph digit font (`#` cells on the plain tier). Gains and spending count
through every integer in at most twenty simulation ticks, retargeting without a
jump; currency changes immediately, even while the number is counting. Posture is a second
channel: the ears go back, the tail drops and the trot shortens as it is
hurt, and its breath shows its stamina. A timely counterattack can regain
recently lost health, shown in grey on the bar. The three-Space combo is
three strikes a person sees: a lunge a cell forward and to the left, a
lunge forward and to the right, then a leap two cells straight forward
with the head shaking left and right twice, each strike held for ticks
and eased back. An original score plays through the engine's mixer: a part for each
of the thirteen areas, a rest at the den, a sting at a fall, the title over the crossing, a sharp crack cue,
a theme for each boss, the lookout's reveal, the Mere's crossing, the Howe's walk to the stone mouth, and
the title's call in the major at Moonford (`docs/SCORE.md`). Thirteen areas: the Shingle, Cinderwick, Bramblehold, the Stand,
Larkmeadow, the Burn, the Teeth, the Mere, the Shallows, the Hush, the Howe and Gravehollow, with the
Underteeth a branch under the Teeth; each but the Howe and Gravehollow has its den and (the town and the
last two apart) a shortcut back; each way on past Bramblehold is held by a gate (a windthrown pine sneaked
under, a burnt oak and a stone mouth a lunge opens, a badger's sett only a grown paw fits). Four bosses hold their ground in them: Old Snag the boar in
his clearing, Whisper the lynx among the crags' pillars, Alder the elk at
the ford, Ashgrim the shadow alpha at the old den; every attack is
telegraphed long enough to parry, the one unparryable attack of each is
dodged, a second phase begins at half health, and an engaged boss has its own
health bar. The last five deaths stand as fading ghosts where they fell, and
replay their last seconds when the cub comes near. The game opens on a
title and, when the alpha falls, the cub crosses the ford as a wolf. Actor bodies
match their drawings and stay apart. Strikes reach from the cub's jaws to any
cell of a foe's body, so a visible flank is a target rather than only its anchor.
Original log and flotsam
sprites mark the coast; gangly trees, stones, bones, stumps, crows, cairns,
scent grass and a ford fill the meadow. Bite, forward lunge, parry, dodge,
stamina sprint and chain attacks; a
hawk's stopped pink shadow asks for a parry or an escape; a bite also
kills it during its stoop and low recovery, on the shadow's four-cell body. Foes leave visible
scent as a bright pulsing orb with seeded drifting motes; death scent uses
the same light within the cub's nose range. Scent and meat pickups are collected within
the cub's body plus a one-cell ring, with a short recovery burst. Landmarks
and caches have original sprites instead of floating world names; their
meanings are in `docs/ART.md`. Kills also leave small healing meat pickups.
Five consumables fit in the pouch: yarrow stops bleeding and heals, marrow
heals slowly, pine hides the trail, ice slows an aimed foe, and the mother's
tuft keeps scent through one death. `i` opens the paused inventory; arrows
select, Space opens Consume / Drop / Discard, and Esc or `i` closes. Dropped
items glow on their cell and can be taken again with `r`. Found lore is kept
in discovery order and read from the rest menu's Lore row.
Enter a den with `r` within three cells: a resting cub breathes beside an
animated fire, with different surroundings in all eleven dens' regions. A larger
ledger sits one sixth of the screen width left of centre, vertically
centred, with the cub and fire beside it. Up/Down select a stat,
Right/Left stage or remove levels, and Enter/Space on Confirm spends the
combined cost. Esc or `r` discards pending choices and leaves. Paths have
broader bends and more clearance; entering any part of an unlocked
shadow doorway crosses it. Visible foes clip at the screen edges rather
than disappearing when their centres lose sight. Slain foes stay gone across
paths and shortcuts; only a den rest or death resets them throughout the
forest. Living foes heal and return to their places on re-entry. Waiting
scent and meat keep their original expiry when you leave and return;
unclaimed scent and meat are not carried through a save reload; consumable
pickups are, including dropped items and finite seeded discoveries.
Water must first be found at the Shingle spring (two mouthfuls), with a
third found later; the counter below the bars shows the charges, and
every rest refills them. Only drinking spends water; a fox's landed feint
steals up to five carried scent instead. Death leaves a recoverable mark, even across area edges; a
second death replaces it. After the thirty-tick fade to black, a fourteen-row red
`FALLEN` appears, followed by the opening's blinking eyes in reverse. Any key
skips once the word has shown for twenty ticks; without a skip the eyes close
before the cub wakes at its den. The mark and ghost are written at the fall,
not after the card. The thirty-second opening shows pale cracked ice at Moonford, the cub freezing
as the pack walks on, a fall into deep water, and three waking blinks onto
the actual Shingle spawn. The same in-game wolf silhouettes cross between
two banks of Shingle-grey gravel and thick forest, drawn by the world
renderer. One key skips the whole sequence.
On macOS the music plays through `afplay`; on Linux through `paplay` where
it is installed, else the game says so once and plays on in silence.
`--mute`, `CUB_SOUND=0` or the `m` key turn it off.

The title leads to the resting cub and fire, with Continue, New journey,
Load, Playback when recordings exist, and Quit. Continue resumes the most
recently played save; Load lists known journeys or accepts a typed path.
New journeys live under `~/.cub/saves/`. `~/.cub/registry` keeps their absolute
paths, names, seeds, difficulty, area, level and last-played time; `--save PATH`
registers a file anywhere. The old `~/.cub/save` is imported as journey without
deleting or rewriting it on import. Resume wakes at the last den with slain
foes still gone, keeping growth, shortcuts, caches, pouch contents, the mark,
bosses, end and original world field. Corrupt files fail by name, never reset.
This build writes CUB 7: thirteen slain masks (one an area) and the gates
(the burnt oak, the stone mouth), then a name and elapsed `played_ms`. CUB 6
migrates with empty masks for the six new areas and no gate opened, keeping its
items, lore, name and time; CUB 5 also with name journey and zero elapsed time,
and CUB 4 with an empty slain set. Earlier schemas fail as `save_version`. A
quit before a staged write's commit tick preserves the previous gameplay save;
an already-due stage commits.
Live sessions record under `~/.cub/replays/` unless `--record FILE` chooses
another path. Deaths also leave self-contained archives under `~/.cub/ghosts/`
(`--ghost-dir DIR` elsewhere). Playback lists both default directories, with
date, length and ending, or accepts a typed path; Esc returns to the fire.
The New journey prompts offer the seed and wolf, the playable difficulty in
this build. Every tuning proposal is in `docs/DESIGN.md`.
Pouch stacks cap at5/3/3/3/1, with at most128 saved ground pickups and32
discovered lore lines (every id 0..31 now has a line: the next line needs a
wider save). The item extension follows name/played_ms in CUB 7 and CUB 6;
CUB 4/5 and earlier CUB 6 wrappers migrate with empty new item fields.

## Where it runs

| machine | tier | state |
|---|---|---|
| macOS, Terminal.app or iTerm2 (arm64) | rich: block elements, braille, 256 colours, true colour where `COLORTERM` says so | pty-tested; physical-terminal glyph measurements remain open |
| Linux, any UTF-8 terminal emulator (x86-64) | rich | the pty rows run on every pull request, inside a container |
| a Linux virtual terminal (`TERM=linux`) | plain: code points 0-255 and the sixteen colours | detected from `TERM`; untested on a VT itself |
| PAX's console | plain today; rich once PAX's font draws `docs/GLYPHS.md` | the installer row and the font row are the cb05 lane's, with pack's pk04 |

The terminal must be at least 80 columns by 24 rows; the field grows to fill a larger one.

## Controls

| key | action |
|---|---|
| arrows | walk; two together for a diagonal; the cub turns toward the held direction at its turn rate |
| Shift+arrow | sneak that way: half speed, no new trail |
| Ctrl+arrow | sprint while held, draining stamina |
| Space / `x` / `s` / `z` / `c` | aimed bite/combo / forward lunge / heavy / parry / directional roll |
| Tab / Esc | lock nearest then cycle / release lock or leave den |
| `w` / `r` | drink / rest, open a shortcut or cache, or pick up an item on the current cell |
| `i` | paused pouch: arrows select, Space opens/actions, Esc or i closes |
| `m` | the music off, on again |
| Up/Down, Left/Right at the den | select a stat, Confirm or Lore; stage/remove a level |
| Enter/Space on Confirm | apply all staged levels; Esc discards |
| `q` / Ctrl+C | quit / interrupt; the terminal and negotiated keyboard mode are restored |
| any decoded key during the opening | skip the scene without also making a move |
| any ordinary key during the death card | skip after twenty ticks of the word; `q` skips too, Ctrl-C still interrupts |
| any key on the title | open the fire menu; after ten idle seconds a demo plays behind the title |
| arrows / Space at the fire | select / choose Continue, New journey, Load, Playback or Quit |
| Enter / Backspace in a path or seed | accept / edit; Esc returns; q quits outside text entry |
| `r` on the end card | keep playing as the wolf (`q` leaves) |

On terminals supporting the negotiated keyboard protocol, arrows stay
held until release and can form diagonal chords. Space and c use the held
direction at the press, or facing with no arrows. Ctrl+arrows sprint;
Space during sprint snaps forward. The roll travels10 cells at paw1,
growing to13 at paw10, with an eight-frame tuck and turn and a recovery.

Press Space during a bite or within six ticks after it to chain left,
right, then a committed forward leap; two pending presses fit, and the
third recovery is longest. Negotiated Space repeats never chain. Legacy
bytes use a short-gap repeat filter, with the delivered-tick and initial-repeat
limitations explained in `docs/KEYS.md`. `x` still uses facing, with two
backward windup steps. Negotiated Shift+Space is heavy; `s` works on every
terminal. Without protocol support, movement and Ctrl+arrow sprint use
inferred repeat lifetimes, not true key release. Ctrl+arrow covers initial
repeat delays through 500 ms; its grace is 567 ms. Exact releases remain
immediate. See `docs/KEYS.md` for the macOS Ghostty protocol fixtures and
the Mission Control shortcut caveat.

## Build and run

```
tools/fetch-lair               stage the engine at lair.pin into .lair/
.lair/tools/fetch-toolchain    stage the pinned toolchain into .wolf-bin/ (wolf 0.2.35, lupin 0.1.56)
.lair/tools/build --release    target/release/cub (and a copy at target/cub)
target/cub                     play/resume; --seed N picks a new journey, --tier plain forces plain
target/cub --save journey      use a separate save file
target/cub --record run.pk     record the run, including resumed state; --replay run.pk plays it back
target/cub --mute              play without music (CUB_SOUND=0 does the same)
target/cub --pace 105          try player movement at105 percent of default
target/cub --no-title          historical name: skip title and menu, straight into play
target/cub --menu              skip the title, land on the fire menu
target/cub --ghost-dir DIR     read and write the death archives there (default ~/.cub/ghosts)
target/cub --den-census        flood fifty seeds for den distance and every thorn-gate face
target/cub --den-spacing       the route walk between dens over fifty seeds (cb05, with --foe-census,
                               --bends-audit, --spurs-audit and --gen-bench)
target/cub --boss-census       fight every boss in fifty seeds at both sizes; a fairness line a boss
target/cub --fight-trace 7 1   narrate one scripted fight (the alpha, seed 1; a third number picks 80 or 200 columns)
target/cub --strike-census     every strike at every aim on both tiers, the drawn body against standing
target/cub --hud-census        every painted HUD cell held to the bars, the labels and the digits
target/cub --encounter-census  one posted Ashen against a fresh cub, Book-II and no-parry play, ten seeds at both fields
target/cub --crossing-trace 1 80  one crossing of Cinderwick narrated while a foe is within two cells
target/cub --hit-census        low-hawk and boss/Ashen body-ring bites: positions, aims and hits as CSV
target/cub --small-faults      reader repeat/press-order rows and the three-kill/no-drink fixture
target/cub --narrow-audit 6 240  walk Cinderwick's single-file edges with diagonal chords
```

`cub --help` lists the rest: the headless mode that writes frames for the goldens, `--trace` (one line a
tick on standard error), `--apply`, the glyph probe, the selftest, `--bench` for render/diff timings, and
the score's paths (`--score-list`, `--score-render`, `--score-wav`, `--score-replay`, `--score-scene`,
`--sound-census`).
Headless `--script` fixtures skip death cards after their minimum word hold;
`--full-death` keeps the full scene. Live play and production `--replay` keep
recorded key timing. A script's `# counter-frames` comment emits every integer
as its own golden frame, without advancing the simulation again.

## Tests

`tools/check` runs the complete local gate: formatting, checked-machine
tests, native and release builds, decoder selftest, both-tier replay goldens
(including pickup sprites, inventory actions, drop/re-pickup, and scrollable lore)
and posture sheets, every combo/roll frame, scaled bars and rally, the score's PCM goldens, loop seams and
scene scripts' cue schedules on both backends, the sound census and a sound-on memory row (`tools/score-check`), shipping-binary gameplay and persistence assertions,
pty restoration and replay agreement, death-word/half-closed/closed-eye goldens,
every integer of gains and spending with replay-deterministic batches, the real
terminal's1000-frame count at both sizes and tiers, exact held-key and eight-direction chord rows,
hand-timed bite requests in all eight facings, real-reader Ghostty-compatible
Space press/release/repeat sequences checked against an independent
consumed-tick/stamina oracle (late delivery is measured, not rejected),
the legacy repeat fallback, regional rest scenes at80×24 and120×40,
found-water/drink/refill and last-den respawn, and performance. Both platform gates
also bound resident growth to 4096 bytes per actual tick over a resumed checkpoint
and fresh seed (`sh tools/check-memory target/release/cub`). Frame scratch is
reclaimed after drawing; idle save checks reuse fixed-size numeric snapshots.
`tools/check-linux`
runs correctness inside `.lair/tools/in-container`; `tools/check-perf`
measures rendering, idle wakes and key-to-frame latency.

Fresh-journey terminal rows use separate save paths. The game gates archive
the previous engine-row save without deleting captures; before invoking
`.lair/tools/pty` directly in a reused checkout, run
`python3 -I tools/prepare-pty`. Separate resume rows load committed saves
written by the accepted cb05 and merged trunk binaries, so fixture isolation
does not replace compatibility coverage.

The two compiler backends and both hosts must reproduce identical glyphs,
styles and integer snapshots. `--world-audit` floods the actual terrain for
50 seeds at both fields, checking every den, exit and cache, the meander
bound and enemy spacing, the forest's texture at every camera position
(no flat run, no empty cell), a bounded walk from every den-reachable
coast cell to a useful route or cache, and every path cell in its area's
one path colour. `--body-audit` holds the bodies apart over the same 50
seeds at both sizes, with a three-weasel swarm from behind in each world;
`--boss-census` fights every boss in the same fifty seeds at both sizes and
holds every world to a win within five lives, every parryable telegraph to
the parry window and every boss to its arena; the gameplay gate replays the
boss, end, ghost and title witnesses and checks a death's trailer against
the sim frame for frame;
`--look-audit` scans fifty seeded camera walks for leftover world labels on both tiers.
`--paths-audit` measures carved widths and centreline steps; `--doorways-audit`
checks all shadow neighbours; `--foes-audit` checks clipped sprites on every
route row. The diagonal art goldens index410 pose states, sharing75 distinct
drawings across four rotations, both tiers and80×24/200×60. `--hit-census`
measures unslanted bites around each boss and the Ashen; its independent gate
checks the complete position/aim ring and requires every inward gap0/1 bite
to land. Focused rows cover the slanted combo strikes and other attack types.
`--narrow-audit 6 240` walks every single-file edge with both diagonal chords
in fifty Cinderwick seeds at both fields, without widening terrain collision.
Older four-way ghost archives keep their original directions alongside new
eight-way recordings. Rest panels have empty, pending and refused goldens at both sizes
and tiers, plus real arrow/confirm/discard pty witnesses. The opening has
every shot at 80×24, 120×40 and 200×60 on both tiers, disjoint sky/ice/water
styles, a full-length terminal run and a recorded real-key skip per shot.
`--motion-census` separates area, terrain, heading and gait over50 seeds.
`--strike-census` measures each strike's drawn body against the standing
one at every age, aim and tier; `--hud-census` renders every frame with and
without the HUD and holds each painted cell to the bars, labels and digits.
`--motion-render` times full frames by area; `--fox-roll-census` checks early
and correctly timed rolls against the fox at body contact.
`--feel-audit`, `--chase-audit` and `--mouth-audit` census the dens,
switchbacks, clearings, pursuit and safe arena approaches. cb05's `--den-spacing`,
`--foe-census`, `--bends-audit` (no bend reverses within eight cells on any inland route or
branch), `--spurs-audit` (every spur ends at something named) and `--gen-bench` (an area's
terrain layer under 50 ms) run in the gameplay gate too. `--measure` reports the pace, the wag, the fox's chase, the path colours
and the body census over the real-key scripts. The sound pty rows start the
game with music on and hold the player to a child of the game, gone with
it; name the OSS stub's refusal; and prove `--mute`, `CUB_SOUND=0` and the
`m` key. The real-key world scripts visit all three areas, fight the hawk,
recover a cross-area mark, return through both shortcuts and open all four
coast bundles. File tests
cover save round trips, cut writes, concurrent stages, corruption and
persisted marks. The pty rows include quit and typed Ctrl-C during a pending
save, named save failures, and self-contained resumed recordings. Physical
font-width and named-terminal keyboard measurements remain open.

macOS loudly skips the Linux-only idle counter; Linux measures it. CI runs
Linux correctness, including the resident-memory gate, on every PR; macOS,
its resident-memory row and performance join it in the full tier.

## Documents

`docs/DESIGN.md` the tuning proposals; `docs/SCORE.md` the music and its cue schedule; `docs/ART.md` the sprites; `docs/GLYPHS.md` every code point the
rich tier uses (PAX's font specification for cub); `docs/REPLAY.md` cub's words in the engine's replay
format; `docs/PALETTE.md` the daylight and dusk colours; `docs/KEYS.md` the measured
pty bytes, the physical Shift+Space result, and the remaining terminal rows. The design bible is in the planning repository (`sprints/lair/cub/design.md`).

## Licence

GNU GPL v3 with the wolf Training Data Permission (see LICENSE and LICENSE-TRAINING-DATA).
