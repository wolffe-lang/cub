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
| `z` | `parry` |
| `c` | `dodge` |
| Tab | `lock` |
| `w` | `water` |
| `r` | `rest` |
| `q`, Esc | `quit` |
| Ctrl-C as a byte | `interrupt` |

Every key is recorded from the first build, so a run's file is complete; the scaffold applies the movement
keys and the quit, and the moves act from cb01 on. No numeric event yet (cb01's `health` and `scent`). A
pack replay is a parse failure in cub at its first key, as it should be.

`tests/cases/*.pk` are the goldens' scripts (eight: a standstill, a walk north to the water, a turn east, a
sneak, a long walk south that scrolls the woods, a diagonal, the wide field, a resize), run headless on both
tiers by `.lair/tools/goldens` and diffed against `tests/goldens/`.
