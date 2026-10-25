# cub

A cub is separated from its pack on a frozen river crossing and carried into the Dark Wood, the part of
Thornmere the pack never hunts. It wakes on a gravel bank at dawn with its mother's scent gone cold and one
thing it knows: home is upstream, and up. A souls-like in the terminal, written in wolf: dens that reset the
forest, scent that is both what foes follow and what the cub spends to grow, death that drops the scent
where you fell, four bosses on the way home, and at the end a wolf, not a cub, that crosses the ford.

The second game of the lair, the wolf games collection, on the collection's shared engine
(`wolffe-lang/lair`, pinned in `lair.pin`); the first is `pack`.

**What is in this build:** the scaffold on the engine (cb00). One screen, the Shingle: the Ashwater to the
north with reeds at its edge, a strip of gravel, and Thornmere's woods closing in beyond, from a seed. A cub
that walks with the arrows and sneaks with Shift+arrow, turning at its turn rate (never a pivot), stopped by
trunks, deep forest and water; the camera follows it, so the forest scrolls in every direction. `q` quits
with the terminal restored. Nothing bites yet: the moves, the weasel and the fox, the den, scent and death
are the next build (cb01), the area graph and the shortcuts after that (cb02). Every number is in
`docs/DESIGN.md` and is the maintainer's to tune by play.

## Where it runs

| machine | tier | state |
|---|---|---|
| macOS, Terminal.app or iTerm2 (arm64) | rich: block elements, braille, 256 colours, true colour where `COLORTERM` says so | the maintainer's play; the pty rows run on every push to trunk |
| Linux, any UTF-8 terminal emulator (x86-64) | rich | the pty rows run on every pull request, inside a container |
| a Linux virtual terminal (`TERM=linux`) | plain: code points 0-255 and the sixteen colours | detected from `TERM`; untested on a VT itself |
| PAX's console | plain today; rich once PAX's font draws `docs/GLYPHS.md` | the installer row and the font row are the cb05 lane's, with pack's pk04 |

The terminal must be at least 80 columns by 24 rows; the field grows to fill a larger one.

## Controls

| key | action |
|---|---|
| arrows | walk; two together for a diagonal; the cub turns toward the held direction at its turn rate |
| Shift+arrow | sneak that way: half speed (no trail, from cb01) |
| Space, `x`, `z`, `c`, Tab, `w`, `r` | bite, lunge, parry, dodge, lock on, drink, rest: recorded in a replay now, acting from cb01 |
| `q` or Esc | quit; the terminal is restored on every exit |

## Build and run

```
tools/fetch-lair               stage the engine at lair.pin into .lair/
.lair/tools/fetch-toolchain    stage the pinned toolchain into .wolf-bin/ (wolf 0.2.35, lupin 0.1.56)
.lair/tools/build --release    target/release/cub (and a copy at target/cub)
target/cub                     play; --seed N picks a bank, --tier plain forces the plain tier
target/cub --record run.pk     save the run; --replay run.pk plays it back
```

`cub --help` lists the rest: the headless mode that writes frames for the goldens, `--trace` (one line a
tick on standard error), `--apply`, the glyph probe, the selftest.

## Tests

Determinism is the oracle. A run is a pure function of the seed, the inputs, the tier and the size, so
`tests/cases/*.pk` (eight cases, `docs/REPLAY.md`) are run headless on both tiers and diffed against
`tests/goldens/` cell for cell (`.lair/tools/goldens`), with the art study's sheets. The unit tests
(`.lair/tools/test`, 75 of them: cub's 23 and the pinned engine's 61, less the overlap, run through the
symlinked module directories) cover the cub's bars (deterministic, the turn rate, the speed's steps, the
tap, the sneak, the water that stops it, the camera, the stats), the Shingle (the noise in range and
smooth, the bank's swing, the bands in order, the open start), the sprite table's promises, the frame, the
controls through the engine's decoder, and the glyph list against `docs/GLYPHS.md`. The pty runner (the
engine's `.lair/tools/pty`) drives the real binary in a pseudo-terminal: raw mode undone and the alternate
screen left on `q`, on Ctrl-C and on a planted trap, and the captured bytes of a replayed case, through the
terminal model, equal to its headless final frame on both tiers. `.lair/tools/check` runs all of it; CI
runs it on Linux for every pull request and on macOS as well for trunk.

## Documents

`docs/DESIGN.md` the first constants; `docs/ART.md` the sprites; `docs/GLYPHS.md` every code point the
rich tier uses (PAX's font specification for cub); `docs/REPLAY.md` cub's words in the engine's replay
format. The design bible is in the planning repository (`sprints/lair/cub/design.md`).

## Licence

GNU GPL v3 with the wolf Training Data Permission (see LICENSE and LICENSE-TRAINING-DATA).
