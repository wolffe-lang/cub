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
| 1–5 at the den | `heart`, `wind`, `fang`, `paw`, `nose` |
| Ctrl-C as a byte | `interrupt` |

Every key is recorded. Numeric `health N` and `scent N` events are explicit
test/debug deltas, not enemy actions: negative health is ordinary interruptible
damage; positive health is clamped to maximum. Health deltas precede scent
deltas, before the tick. These events are accepted in both replay paths.

Thirty scripts cover movement, each combat move, the fox's two tells,
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
