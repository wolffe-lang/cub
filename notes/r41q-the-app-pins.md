# r41q — cub to lair `df11d213` (wolf 0.2.36 / lupin 0.1.58)

_cub's part of r41q (the apps, the games and the docs to the published pair), after the engine's (lair#26)
and cb19's merge (cub trunk `41e35f29`)._

## Prediction

Written before the first change (2026-11-01, base trunk `41e35f29` at `lair.pin` `74b89744`).

- `lair.pin` moves `74b89744` to **`df11d213`** (lair trunk, read twice). The twelve engine commits between
  are lr04's note and r41q's engine half: the toolchain pin, three comments, `ci/games.conf` and notes.
  **No engine source changes**, so the only thing that moves under cub is the compiler, 0.2.35 to 0.2.36,
  and the std (`2386522e` to `78b9d3cb`: the in-place `std.list` mutators keep their signatures).
- The engine's toolchain file at `df11d213` names wolf 0.2.36 / lupin 0.1.58 / std `78b9d3cb`:
  `.lair/tools/fetch-toolchain` accepts the linux x86-64 archives by digest and `.lair/tools/lib-toolchain.sh`
  accepts `wolf 0.2.36 (wolfgang, pin 5adf3d9)`, `lupin 0.1.58 (wolf-interp, reference interpreter at pin
  a5378e3)` and `STD-REV` `78b9d3cb`. No cub source declares the names 0.2.36 adds to the prelude
  (`VaList`, the four `va_*`, `env_arg0`, `env_args_bytes`), so `--deny-warnings` sees no W0304.
- `tier pr` (`plan-test`, `linux`, `gameplay` native and release) stays green with every count as at
  cb19's final head (run 41279501956): **698 tests, zero SKIPs**, both builds, **1034 golden lines ok,
  zero DIFFERS**, **89 pty rows ok**, the score check and the memory gate, and both gameplay gates green.
- `tier full` adds the two macOS legs and the perf gate; the orchestrator labels and watches it.
- The README's one version sentence (`wolf 0.2.35, lupin 0.1.56`) moves to the pair, in a README-only
  commit. It states no counts.

## Forbidden

No merge, label, tag, release, issue filed or closed; no attribution trailer. No build on the Mac; local
runs on hasu block B alone, both lock names held per run; kasumi not touched. No other implementation's
source read. No source, test, golden, tool or workflow of cub changed: `lair.pin` and the README's toolchain line, this note and nothing else.

## Inputs verified

- Base: cub trunk `41e35f29`, cb19's merge (the orchestrator handed cub's pin to r41q after it); cb19's
  final `tier full` (run 41279501956) green there with 698 tests, 1034 golden lines, 89 pty rows, both
  gameplay gates (native 1513 s, release 438 s).
- The engine between `74b89744` and `df11d213`: twelve commits, none in `src/`, so the compiler and the
  std are all that move.
- cub's CI since cb19's R-cb19-7 B runs the gameplay gates in their own jobs (`gameplay` native and
  release, `macos-gameplay`); the gauntlet runs `tools/check-linux` whole, which includes both.
- What waits for this pin: nothing in cub's notes or README names 0.2.36 or the next pin.
- README read: its one toolchain line moves to `wolf 0.2.36, lupin 0.1.58`, a README-only commit; it
  states no counts.
- lair trunk read twice before the pin was written (`git ls-remote` at 00:55:19Z and 00:55:21Z, and the
  commits API): `df11d213785f7694bdf3f3572299abc550d8b903`, lair#26's merge (r41q's engine half). The
  digests behind it are lair#26's: the release API read twice, every pinned archive hashed twice, the
  identities read from the archives; this repo's gauntlet holds the staged `.lair/wolf-toolchain.toml` to
  the same two API passes by script (`engine-pin`).
- 0.2.36's prelude names (`VaList`, the four `va_*`, `env_arg0`, `env_args_bytes`): declared in no `.lu`
  file here, so no W0304 under `--deny-warnings`.

## Evidence index

- `ed6e68ca` Predict lair.pin at df11d213 moves no frame
- `afdeff4f` lair.pin: the engine at df11d213 (wolf 0.2.36 / lupin 0.1.58)
- `55d9e442` README: the pinned pair is 0.2.36 / 0.1.58 (README only)
- The gauntlet at the final head, on hasu block B (`/home/mfwolffe/lanes/r41q/bin/gauntlet-game.sh cub
  <sha>`, its log under `/home/mfwolffe/lanes/r41q/logs/`): the head asserted, `lair.pin` against lair's
  trunk read live, `tools/fetch-lair` (the
  staged `LAIR-REV` asserted), the staged engine's toolchain file proved against the API passes, the
  planner's tests, the image `localhost/r41q-pack-ci:fbee7e864f7dbee6`, `.lair/tools/fetch-toolchain`, then
  `tools/check-linux` (gameplay on both backends included) in the container on CPUs 6-11, and the count (every test ok, zero FAILED, zero SKIP,
  the game's and the engine's split by path). Every step prints `END <step> exit=N`; the wrapper stops at
  the first nonzero one. The END lines and the counts are in the PR body.

## Done-when

The PR is open at its final head with `tier pr` green there, `Footprint: cross-cutting` (a pin), the audit
run once and passing but for the labelled `tier full`, which the orchestrator labels and watches (the
second host's goldens). Nothing to close or file here.
