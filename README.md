# cub

A cub is separated from its pack on a frozen river crossing and carried into the Dark Wood, the part of
Thornmere the pack never hunts. It wakes on a gravel bank at dawn with its mother's scent gone cold and one
thing it knows: home is upstream, and up. A souls-like in the terminal, written in wolf: dens that reset the
forest, scent that is both what foes follow and what the cub spends to grow, death that drops the scent
where you fell, four bosses on the way home, and at the end a wolf, not a cub, that crosses the ford.

The second game of the lair, the wolf games collection, on the collection's shared engine
(`wolffe-lang/lair`, pinned in `lair.pin`); the first is `pack`.

**What is in this build:** a seeded route from the Shingle through
Bramblehold to Larkmeadow, with four dens, meandering paths, guarded side
caches and two shortcuts home. The shore winds between water and visible
forest, bounded by rock jetties; its offshoots end in guarded bundle
alcoves. Original log and flotsam sprites mark the coast. Bite, lunge,
parry, dodge and chain attacks;
a hawk's stopped shadow asks for a parry or an escape. Foes leave visible
scent to collect before it fades. Dens heal, refill water and spend scent
on growth. Death leaves a recoverable mark, even across area edges; a
second death replaces it. An opening scene shows the broken crossing.

The journey saves under `~/.cub/save`; resume wakes at the last den with
reset encounters, keeping growth, shortcuts, opened caches, pouch contents
and the dropped mark. `--save PATH` selects a separate journey. Unknown or
corrupt files fail by name, never silently reset. A quit during a staged
write preserves the previous save. Live deaths leave self-contained replay
files under `~/.cub/ghosts/`; ghost display, bosses, music, the larger HUD
and difficulty selection come later. Every tuning proposal is in
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
| Space / `x` / `s` / `z` / `c` | bite/combo / lunge / heavy / parry / dodge |
| Tab / Esc | lock nearest then cycle / release lock or leave den |
| `w` / `r` | drink / rest at a den, open a shortcut, or dig an unguarded cache |
| 1–5 at the den | grow heart, wind, fang, paw, nose |
| `q` | quit; the terminal is restored on every exit |
| any decoded key during the opening | skip the scene without also making a move |

Arrows held or pressed within 500 ms before an attack aim it; lock wins.
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
```

`cub --help` lists the rest: the headless mode that writes frames for the goldens, `--trace` (one line a
tick on standard error), `--apply`, the glyph probe, the selftest, and `--bench` for render/diff timings.

## Tests

`tools/check` runs the complete local gate: formatting, checked-machine
tests, native and release builds, decoder selftest, both-tier replay goldens
and posture sheets, shipping-binary gameplay and persistence assertions,
pty restoration and replay agreement, and performance. `tools/check-linux`
runs correctness inside `.lair/tools/in-container`; `tools/check-perf`
measures rendering, idle wakes and key-to-frame latency.

The two compiler backends and both hosts must reproduce identical glyphs,
styles and integer snapshots. `--world-audit` floods the actual terrain for
50 seeds, checking every den, exit and cache, the meander bound and enemy
spacing, plus a bounded walk from every den-reachable coast cell to a
useful route or cache. The real-key world scripts visit all three areas, fight the hawk,
recover a cross-area mark and return through both shortcuts. File tests
cover save round trips, cut writes, concurrent stages, corruption and
persisted marks. The pty rows include quit and typed Ctrl-C during a pending
save, named save failures, and self-contained resumed recordings. Physical
font-width and named-terminal keyboard measurements remain open.

macOS loudly skips the Linux-only idle counter; Linux measures it. CI runs
Linux correctness on every PR, adding macOS and performance in the full tier.

## Documents

`docs/DESIGN.md` the tuning proposals; `docs/ART.md` the sprites; `docs/GLYPHS.md` every code point the
rich tier uses (PAX's font specification for cub); `docs/REPLAY.md` cub's words in the engine's replay
format; `docs/PALETTE.md` the daylight and dusk colours; `docs/KEYS.md` the measured
pty bytes, the physical Shift+Space result, and the remaining terminal rows. The design bible is in the planning repository (`sprints/lair/cub/design.md`).

## Licence

GNU GPL v3 with the wolf Training Data Permission (see LICENSE and LICENSE-TRAINING-DATA).
