# cub

A cub is separated from its pack on a frozen river crossing and carried into the Dark Wood, the part of
Thornmere the pack never hunts. It wakes on a gravel bank at dawn with its mother's scent gone cold and one
thing it knows: home is upstream, and up. A souls-like in the terminal, written in wolf: dens that reset the
forest, scent that is both what foes follow and what the cub spends to grow, death that drops the scent
where you fell, four bosses on the way home, and at the end a wolf, not a cub, that crosses the ford.

The second game of the lair, the wolf games collection, on the collection's shared engine
(`wolffe-lang/lair`, pinned in `lair.pin`); the first is `pack`.

**What is in this build:** the Shingle fight and recovery loop. Bite, lunge,
parry and dodge a weasel pair and a fox, follow the fading scent trail,
rest at the hollow log and spend scent on growth. Death drops a recoverable
mark; a second death replaces it. A lunge breaks the southern thorn gate
onto the approach to Bramblehold. The connected areas and save file are
still to come: leaving this build does not persist growth or gate state.
Live deaths leave replay files under `~/.cub/ghosts/`; ghost display comes
later. Every tuning proposal is in `docs/DESIGN.md`.

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
| Space / `x` / `z` / `c` | bite / lunge / parry / dodge |
| Tab / Esc | lock nearest then cycle / release lock or leave den |
| `w` / `r` | drink / rest at the hollow log |
| 1–5 at the den | grow heart, wind, fang, paw, nose |
| `q` | quit; the terminal is restored on every exit |

## Build and run

```
tools/fetch-lair               stage the engine at lair.pin into .lair/
.lair/tools/fetch-toolchain    stage the pinned toolchain into .wolf-bin/ (wolf 0.2.35, lupin 0.1.56)
.lair/tools/build --release    target/release/cub (and a copy at target/cub)
target/cub                     play; --seed N picks a bank, --tier plain forces the plain tier
target/cub --record run.pk     save the run; --replay run.pk plays it back
```

`cub --help` lists the rest: the headless mode that writes frames for the goldens, `--trace` (one line a
tick on standard error), `--apply`, the glyph probe, the selftest, and `--bench` for render/diff timings.

## Tests

`tools/check` runs the complete local gate: formatting, 97 checked-machine
tests, native and release builds, decoder selftest, 17 replay cases on rich
and plain tiers plus the art sheets (35 golden directories), shipping-binary
gameplay assertions, pty restoration and replay agreement, and performance.
`tools/check-linux` runs the correctness gates inside `.lair/tools/in-container`;
`tools/check-perf` measures rendering, idle wakes and key-to-frame latency.

The two compiler backends and both hosts must reproduce the same glyphs,
styles and integer state snapshots. Gameplay checks assert that each named
encounter really happened and replay a natural death file to the same state.
Repeated deaths cannot overwrite an earlier file. The pty tests cover quit,
Ctrl-C, a trap, both visual tiers, den keys, death recovery, and archive-write
failure with the terminal restored. macOS loudly skips the Linux-only idle
counter; Linux measures it. CI runs Linux correctness on every PR and adds
macOS and performance in the full tier.

## Documents

`docs/DESIGN.md` the tuning proposals; `docs/ART.md` the sprites; `docs/GLYPHS.md` every code point the
rich tier uses (PAX's font specification for cub); `docs/REPLAY.md` cub's words in the engine's replay
format; `docs/PALETTE.md` the daylight colours; `docs/KEYS.md` the measured
pty bytes and the still-unmeasured physical terminals. The design bible is in the planning repository (`sprints/lair/cub/design.md`).

## Licence

GNU GPL v3 with the wolf Training Data Permission (see LICENSE and LICENSE-TRAINING-DATA).
