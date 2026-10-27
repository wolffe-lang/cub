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
| x | `78` | forward lunge with two backward windup steps |
| z | `7A` | parry |
| c | `63` | tap dodge; hold/repeat sprint on stamina |
| Tab | `09` | lock nearest, then cycle |
| w | `77` | drink |
| r | `72` | rest at a nearby den; interact with a shortcut or cache |
| m | `6D` | the music off, on again (cb03; `--mute` and `CUB_SOUND=0` keep it off) |
| Enter | `0D` | confirm pending growth when Confirm is selected at rest |
| q | `71` | quit |

Esc (`1B`) releases a lock or leaves the den; it does not quit. It is covered
by the decoder selftest and the live `den-keys` row. The engine keyprobe's
lone-Esc path waits for another byte instead of reporting the timeout, so it
is not a successful keyprobe measurement. Ctrl-C's restoration witness is
only the engine pty row typing byte `03` into its own game session.

Shift+Down remains sneak, never parry. Ordinary terminal byte streams cannot
distinguish Shift+Space. Space aims with recent arrows, including diagonals;
`x` always uses facing. Hold `c` after its initial dodge to sprint; Space
while sprinting makes the forward snapping attack. A repeat within one
second identifies a hold, so two close taps also count. No real key-up
is available; the engine expires the inferred hold after repeats stop.

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

The health/stamina panel owns a solid five-row rectangle and a one-cell
right margin. World lettering used to remain visible through its unpainted
padding: the `c` in the former bones label could sit beside stamina. This
is independent of the key's meaning. The `level-look-after-c` pty row types
byte `63`, checks that terminal echo is disabled, and compares the live
frame to its recorded replay at both sizes and tiers.

## Den and water interaction (cb04a)

Within three cells of a den centre the bottom line says `r rest`. Press
`r` to enter its rest scene. Up/Down wrap over heart, wind, fang, paw, nose
and Confirm. Right stages one level; Left removes one, never below the
current stat. An unaffordable raise is refused and shows the needed scent
in red. Enter or Space on Confirm applies the pending levels together.
Esc or `r` discards pending choices and leaves. Keys1–5 no longer purchase.
The world stays paused, and no arrow remains held on exit. Growth remains
den-only; the displayed Scent after subtracts only accepted pending levels.

Water must first be found at the Shingle spring. The counter at row3 beside
the bars says `Water n/cap  w drink`, or `Water 0/0 - find a spring` before
learning. `w` spends one immediately and heals during the second half of
its one-second animation; a hit interrupts it. Rests refill found capacity.
Meat from ordinary kills is collected and heals immediately, without a key.
`den-contact` injects real arrow/r/Esc bytes at the visible den edge;
`den-checkpoint` plays the recorded den2 walk/rest/death/wake through a pty.

## Cinderwick (cb05)

No new key. `r` beside an ash heap in a yard digs it as it digs a burrow
(a guard stands by every one; the marrow or the herb goes to the pouch); `r`
beside a hollow with old bones reads the forest's line instead, shown four
seconds under the bars. An ember underfoot burns a little every ten ticks
with no key at all: step off it. The Ashen's blow is parried with `z` in its
window as any blow is; the parry opens a sixty-tick riposte. The four pty
rows `town-passage`, `ashen-parry`, `ember-touch` and `yard-cache` replay the
real-key scripts the proof generates and hold the live frame to the
headless one.
