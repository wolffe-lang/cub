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
