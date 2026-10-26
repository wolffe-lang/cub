# Terminal keys

Measured 2026-10-25 with the pinned engine's `.lair/tools/keyprobe` inside a
macOS pseudo-terminal, TERM=xterm-256color. These bytes were injected into
the pty, not typed in Terminal.app or iTerm2; those physical-terminal rows
remain unmeasured. The decoder selftest checks every split of each sequence.

| key | measured bytes | action |
|---|---|---|
| Up / Down / Right / Left | `1B 5B 41` / `1B 5B 42` / `1B 5B 43` / `1B 5B 44` | walk |
| Shift+Up / Down / Right / Left | `1B 5B 31 3B 32 41` / `42` / `43` / `44` (same prefix) | sneak |
| Space | `20` | bite |
| x | `78` | lunge |
| z | `7A` | parry |
| c | `63` | dodge |
| Tab | `09` | lock nearest, then cycle |
| w | `77` | drink |
| r | `72` | rest at a nearby den; interact with a shortcut or cache |
| m | `6D` | the music off, on again (cb03; `--mute` and `CUB_SOUND=0` keep it off) |
| 1 / 2 / 3 / 4 / 5 | `31` / `32` / `33` / `34` / `35` | grow heart / wind / fang / paw / nose at the den |
| q | `71` | quit |

Esc (`1B`) releases a lock or leaves the den; it does not quit. It is covered
by the decoder selftest and the live `den-keys` row. The engine keyprobe's
lone-Esc path waits for another byte instead of reporting the timeout, so it
is not a successful keyprobe measurement. Ctrl-C's restoration witness is
only the engine pty row typing byte `03` into its own game session.

Shift+Down remains sneak, never parry. No Shift+Space or sprint binding is
claimed: ordinary terminal byte streams cannot distinguish Shift+Space.

## Physical Shift+Space probe, 2026-10-25

In the maintainer's play terminal, `TERM=xterm-256color`, the pinned engine
keyprobe received `20  b' '` for Shift+Space, then `71  b'q'`. This is a
physical-key measurement supplied from that session, not injected pty
input; the terminal application name was not supplied, so it is not a
claim about both Terminal.app and iTerm2. Shift+Space is indistinguishable
from Space there. Heavy attack uses `s` (`73`; `S` also accepted), while
Space continues to bite.

The pinned engine explicitly ignores CSI-u / kitty and tilde forms in
`input/input.lu` (lines 16–18 and 173). Enhanced protocol negotiation and
restoration on every exit path, with protocol-restore pty rows, must land
in lair before cub can bind the chord. No protocol is enabled by this build.

In connected areas, `r` rests at any den, pushes/crosses the fallen log,
digs/crosses the hedge, or digs an unguarded cache. Context chooses the
operation; stat growth remains den-only. Any decoded key skips the opening
scene. `m` is the music's switch, recorded as `mute` and inert in the simulation
(`docs/SCORE.md`). Otherwise unused keys are recorded as `skip` and do nothing during
play. The new pty save rows use `q` and the engine's typed byte `03` while
a real save stage exists; neither row sends a signal from a script.

## The title and the end (cb04, 2026-10-26)

The game opens on the title: any decoded key begins (the opening for a new journey, the forest for a
resumed one) and is recorded as `title 1` then the key; `--no-title` skips it (the pty rows and the engine's
rows start past it, `tests/lair.conf`). After ten idle seconds the demo plays behind the title; any key
still begins. On the end card `r` keeps playing and `q` leaves; both are the ordinary keys, recorded as
such. The title row and the title-demo row in `tests/pty_rows.py` are the live witnesses; the death
witnesses still type bytes into the pty, never a signal from a script.
