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
| r | `72` | rest at the hollow log; leave its screen |
| 1 / 2 / 3 / 4 / 5 | `31` / `32` / `33` / `34` / `35` | grow heart / wind / fang / paw / nose at the den |
| q | `71` | quit |

Esc (`1B`) releases a lock or leaves the den; it does not quit. It is covered
by the decoder selftest and the live `den-keys` row. The engine keyprobe's
lone-Esc path waits for another byte instead of reporting the timeout, so it
is not a successful keyprobe measurement. Ctrl-C's restoration witness is
only the engine pty row typing byte `03` into its own game session.

Shift+Down remains sneak, never parry. No Shift+Space or sprint binding is
claimed: ordinary terminal byte streams cannot distinguish Shift+Space.
