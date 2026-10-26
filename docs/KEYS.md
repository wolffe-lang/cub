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
| c | `63` | directional roll (never sprint) |
| Ctrl+arrow | legacy `1B 5B 31 3B 35` plus `A/B/C/D`; negotiated press/repeat/release | held sprint |
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

Shift+Down remains sneak, never parry. Cub now opts into the engine's
keyboard session: terminals answering its bounded query enable flags11
(press/repeat/release and all keys). Held arrows persist until release;
two non-opposing arrows form a diagonal, opposites cancel. Releasing Left
while Down remains held resumes Down. Ctrl with arrows sprints and drains
stamina until Ctrl/arrows are released or stamina is empty. `c` only rolls.

Space commits the held direction, including diagonals, at its press;
without arrows it uses facing. A lock does not override an explicitly held
aim. `x` keeps its forward-facing lunge. `c` likewise commits held arrows,
or facing with none: an arrow already held when c is added works. Unlocked
facing follows the roll; a lock retains target-facing. Negotiated
Shift+Space is heavy; `s` remains the heavy fallback on every terminal.

Without a protocol reply the engine retains inferred holds. Legacy
Ctrl+arrow repeat sequences refresh sprint, which expires when they stop
(after their inferred repeat lifetime). Such byte streams cannot report
actual release, promise physical simultaneous keys, or reliably resume a
previous key. Arrow aim and rolls use this inferred state, not true key-up.
The fallback is not described as exact. Negotiation/restoration and every
scripted chord are pty witnesses, not claims of a physical-terminal test.

## Physical Shift+Space probe, 2026-10-25

In the maintainer's play terminal, `TERM=xterm-256color`, the pinned engine
keyprobe received `20  b' '` for Shift+Space, then `71  b'q'`. This is a
physical-key measurement supplied from that session, not injected pty
input; the terminal application name was not supplied, so it is not a
claim about both Terminal.app and iTerm2. Shift+Space is indistinguishable
from Space there. Heavy attack uses `s` (`73`; `S` also accepted), while
Space continues to bite.

The old legacy decoder still ignores enhanced forms for unchanged
consumers. Cub uses `feed_events` and the opted-in session instead. The
keyboard stack is restored on normal quit, typed Ctrl-C and runtime error
through the pinned engine; no engine decoder is copied into this game.

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

Water must first be found at the Shingle spring. The counter on row6 below
the bars says `Water n/cap  w drink`, or `Water 0/0 - find a spring` before
learning. `w` spends one immediately and heals during the second half of
its one-second animation; a hit interrupts it. Rests refill found capacity.
Meat from ordinary kills is collected and heals immediately, without a key.
`den-contact` injects real arrow/r/Esc bytes at the visible den edge;
`den-checkpoint` plays the recorded den2 walk/rest/death/wake through a pty.

## Movement tuning and combat studies

`--pace N` is an off-title debug dial,25..300 percent of default player
walk/sprint speed (and acceleration/braking); a recording carries it.
It never changes a saved stat. Normal play defaults to100.

`--combat-witness` is an explicit test-only empty-arena setup for the live
input rows. Its setup is recorded too; it is not a normal journey or an
undisclosed gameplay teleport. `cb04b-*` pty rows report eight aims,
no-arrow roll, long-held chords, releases, displacement and facing.
