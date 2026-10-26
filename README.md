# cub

A cub is separated from its pack on a frozen river crossing and carried into the Dark Wood, the part of
Thornmere the pack never hunts. It wakes on a gravel bank at dawn with its mother's scent gone cold and one
thing it knows: home is upstream, and up. A souls-like in the terminal, written in wolf: dens that reset the
forest, scent that is both what foes follow and what the cub spends to grow, death that drops the scent
where you fell, four bosses on the way home, and at the end a wolf, not a cub, that crosses the ford.

The second game of the lair, the wolf games collection, on the collection's shared engine
(`wolffe-lang/lair`, pinned in `lair.pin`); the first is `pack`.

**What is in this build:** a seeded route from the Shingle through
Bramblehold to Larkmeadow, with eight visible dens in those areas, switchbacks and clearings, guarded side
caches and two shortcuts home. The shore runs a screen past the view each
way to its rock jetties, and four winding offshoots leave it for guarded
bundle alcoves, every path in the shore's own gravel; the forest is one
trunk-and-canopy texture to every edge of the screen, the thicket and
meadow filling the field they were made for. The cub, the foes and the
bundle are solid pixel silhouettes, one drawing each, turned to face the
way they go; the cub trots at 8.8 cells a second, its paws and tail
keeping time with its stride. Outlined red health and green stamina bars
stay at top-left, with posture as a second channel: the
ears go back, the tail drops and the trot shortens as it is hurt, and its
breath shows its stamina; the numbers appear at a den and on the death
card. An original score plays through the engine's mixer: a part for each
area, a rest at the den, a sting at a fall, the title over the opening, and
a theme for each boss (`docs/SCORE.md`). Six areas: the Shingle, Bramblehold,
Larkmeadow, the Teeth, the Shallows and Gravehollow, each with its den and
its shortcut back. Four bosses hold their ground in them: Old Snag the boar in
his clearing, Whisper the lynx among the crags' pillars, Alder the elk at
the ford, Ashgrim the shadow alpha at the old den; every attack is
telegraphed long enough to parry, the one unparryable attack of each is
dodged, a second phase begins at half health, and an engaged boss has its own
health bar. The last five deaths stand as fading ghosts where they fell, and
replay their last seconds when the cub comes near. The game opens on a
title and, when the alpha falls, the cub crosses the ford as a wolf. Every body collides as the drawing it is:
nothing is drawn inside another, and a foe that reaches the cub stands
where a bite aimed its way lands. Original log and flotsam
sprites mark the coast; gangly trees, stones, bones, stumps, crows, cairns,
scent grass and a ford fill the meadow. Bite, forward lunge, parry, dodge,
stamina sprint and chain attacks; a
hawk's connected wings and body ask for a parry or an escape. Foes leave visible
scent to collect before it fades. Dens heal, refill water and spend scent
on growth. Death leaves a recoverable mark, even across area edges; a
second death replaces it. An opening scene shows the broken crossing.
On macOS the music plays through `afplay`; on Linux through `paplay` where
it is installed, else the game says so once and plays on in silence.
`--mute`, `CUB_SOUND=0` or the `m` key turn it off.

The journey saves under `~/.cub/save`; resume wakes at the last den with
reset encounters, keeping growth, shortcuts, opened caches, pouch contents,
the dropped mark, the bosses beaten, the end and the field the world was
made for (the terminal's width when the journey began). `--save PATH`
selects a separate journey. Unknown or corrupt files fail by name, never
silently reset. A quit during a staged write preserves the previous save.
Live deaths leave self-contained replay files under `~/.cub/ghosts/`
(`--ghost-dir DIR` elsewhere), each the ghost the next game shows;
difficulty selection comes later. Every tuning proposal is in
`docs/DESIGN.md`.

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
| Space / `x` / `s` / `z` / `c` | aimed bite/combo / forward lunge / heavy / parry / tap dodge, hold sprint |
| Tab / Esc | lock nearest then cycle / release lock or leave den |
| `w` / `r` | drink / rest at a den, open a shortcut, or dig an unguarded cache |
| `m` | the music off, on again |
| 1–5 at the den | grow heart, wind, fang, paw, nose |
| `q` | quit; the terminal is restored on every exit |
| any decoded key during the opening | skip the scene without also making a move |
| any key on the title | begin; after ten idle seconds a demo plays behind the title |
| `r` on the end card | keep playing as the wolf (`q` leaves) |

Arrows held or pressed within 500 ms before Space aim it; lock wins.
`x` always uses facing, with two backward windup steps. Hold `c` after its
initial dodge to sprint; Space during sprint snaps forward.
Press Space during bite recovery to chain left, right, then a longer forward
hop. Shift+Space sent plain Space in the measured play terminal, so heavy
uses `s` rather than an indistinguishable chord. See `docs/KEYS.md`.

## Build and run

```
tools/fetch-lair               stage the engine at lair.pin into .lair/
.lair/tools/fetch-toolchain    stage the pinned toolchain into .wolf-bin/ (wolf 0.2.35, lupin 0.1.56)
.lair/tools/build --release    target/release/cub (and a copy at target/cub)
target/cub                     play/resume; --seed N picks a new journey, --tier plain forces plain
target/cub --save journey      use a separate save file
target/cub --record run.pk     record the run, including resumed state; --replay run.pk plays it back
target/cub --mute              play without music (CUB_SOUND=0 does the same)
target/cub --no-title          start in the forest, no title
target/cub --ghost-dir DIR     read and write the death archives there (default ~/.cub/ghosts)
target/cub --boss-census       fight every boss in fifty seeds at both sizes; a fairness line a boss
target/cub --fight-trace 7 1   narrate one scripted fight (the alpha, seed 1)
```

`cub --help` lists the rest: the headless mode that writes frames for the goldens, `--trace` (one line a
tick on standard error), `--apply`, the glyph probe, the selftest, `--bench` for render/diff timings, and
the score's paths (`--score-list`, `--score-render`, `--score-wav`, `--score-replay`).

## Tests

`tools/check` runs the complete local gate: formatting, checked-machine
tests, native and release builds, decoder selftest, both-tier replay goldens
and posture sheets, the score's PCM goldens and loop seams on both backends
(`tools/score-check`), shipping-binary gameplay and persistence assertions,
pty restoration and replay agreement, and performance. `tools/check-linux`
runs correctness inside `.lair/tools/in-container`; `tools/check-perf`
measures rendering, idle wakes and key-to-frame latency.

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
`--feel-audit`, `--chase-audit` and `--mouth-audit` census the dens,
switchbacks, clearings, pursuit and safe arena approaches. `--measure` reports the pace, the wag, the fox's chase, the path colours
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
Linux correctness on every PR, adding macOS and performance in the full tier.

## Documents

`docs/DESIGN.md` the tuning proposals; `docs/SCORE.md` the music and its cue schedule; `docs/ART.md` the sprites; `docs/GLYPHS.md` every code point the
rich tier uses (PAX's font specification for cub); `docs/REPLAY.md` cub's words in the engine's replay
format; `docs/PALETTE.md` the daylight and dusk colours; `docs/KEYS.md` the measured
pty bytes, the physical Shift+Space result, and the remaining terminal rows. The design bible is in the planning repository (`sprints/lair/cub/design.md`).

## Licence

GNU GPL v3 with the wolf Training Data Permission (see LICENSE and LICENSE-TRAINING-DATA).
