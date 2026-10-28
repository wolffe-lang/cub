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
Ctrl+C is reserved for interrupt on both paths, including enhanced
press/repeat events; releasing c never interrupts. Release Ctrl before
pressing c to roll out of a sprint. The fallback is not described as exact. Negotiation/restoration and every
scripted chord are pty witnesses, not claims of a physical-terminal test.

The inferred repeat window is the larger of the last two short intervals
plus one tick, at most six ticks; a lone tap lasts twelve ticks. An older
opposite arrow can therefore briefly resume after a newer arrow expires.
At default paw1 walking speed, six braking updates bring the cub to rest:
no later than eleven ticks after the last repeat, or seventeen after a
lone tap. These are simulation-tick bounds, not physical keyboard timing.
`test_cb04b_inferred_release_stops_after_last_repeat_within_eleven_ticks`
checks the exact expiry and stopping tick, then eight stationary ticks,
without a wall or foe stopping the cub. Exact-protocol releases do not wait
for this inference window.

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

The bars sit flush on the map since cb07: no panel, no fill, no margin; the
cell beside the stamina bar is the map's own, and what may never show there
is lettering (the `c` of the former bones label once sat beside stamina).
This is independent of the key's meaning. The `level-look-after-c` pty row
types byte `63`, checks that terminal echo is disabled, compares the live
frame to its recorded replay at both sizes and tiers, and holds the edge
free of lettering.

## Den and water interaction (cb04a)

Within three cells of a den centre the bottom line says `r rest`. Press
`r` to enter its rest scene. Up/Down wrap over heart, wind, fang, paw, nose
and Confirm. Right stages one level; Left removes one, never below the
current stat. An unaffordable raise is refused and shows the needed scent
in red. Enter or Space on Confirm applies the pending levels together.
Esc or `r` discards pending choices and leaves. Keys1–5 no longer purchase.
The world stays paused, and no arrow remains held on exit. Growth remains
den-only; the displayed Scent after subtracts only accepted pending levels.

Water must first be found at the Shingle spring. The line on row 5 under
the bars says `Water n/cap  w drink`, or `Water 0/0 - find a spring` before
learning (cb07: the status row above it is gone). `w` spends one immediately and heals during the second half of
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

## Movement tuning and combat studies

`--pace N` is an off-title debug dial,25..300 percent of default player
walk/sprint speed (and acceleration/braking); a recording carries it.
It never changes a saved stat. Normal play defaults to100.

`--combat-witness` is an explicit test-only empty-arena setup for the live
input rows. Its setup is recorded too; it is not a normal journey or an
undisclosed gameplay teleport. `cb04b-*` pty rows report eight aims,
no-arrow roll, long-held chords, releases, displacement and facing.
`cb07-strikes` types Right, its release and three Space presses as
negotiated events, replays the recording headless a frame a tick, and
measures the cub's drawn pixels on every frame: a cell forward-left for
four ticks, a cell forward-right, two cells forward with the head swung
left and right twice, each hit back in place by its last tick.

## cb10 — slow Ctrl repeats and water (2026-10-28)

Legacy Ctrl+arrow refreshes sprint on every decoded sequence. Its own
17-tick grace covers the measured 500 ms initial delay and 60 ms repeat
pattern. The movement half of that Ctrl-arrow gets the same grace; normal
arrows retain the shorter inference described above.
A terminal with exact events still ends sprint immediately on Ctrl-up.
The regression rows inject real legacy byte sequences through the pinned
reader at 250/30 ms and 500/60 ms, not physical-terminal measurements.

Only w spends a mouthful. The fox's landed feint takes up to five scent
instead, never water. The pink hawks can be bitten during their stoop and
36-tick recovery; while circling or showing their stopped-shadow tell,
parry at the stoop or evade. Their shadow and hit body share a 4×1 canvas.

`--small-faults` prints the repeat timing and the three-kill/no-drink
headless fixture's key lists and before/after water and scent counts.
`--hitbox-audit` also runs 32 low-hawk rows (eight aims, gaps zero/one,
stoop/recovery). `--hit-census` includes the hawk's four nonrotating facings.

The fallback grace is 17/30 s (566.7 ms), tested through 500 ms initial
repeat delays, not settings slower than that. On macOS Ghostty cub asks
for kitty flags11 (`CSI >11u`: disambiguation, event types, all keys).
Injected reader and live-pty rows cover Ctrl press `CSI 57442;5u`, Right
press/repeat `CSI 1;5:1C` / `CSI 1;5:2C`, and releases; press-only fixtures
exercise the inferred fallback. Extra reader rows cover an arrow already
repeating when Ctrl goes down, Ctrl held four silent seconds before an
arrow, Ctrl with two arrows, and Ctrl release/re-press mid-run. These are
protocol fixtures, not bytes captured from a physical Ghostty window.
No enhanced-path dropout is reproduced by these rows.

A possible cause outside cub: macOS uses Ctrl+Left/Right for Mission
Control's move-a-space shortcuts by default. If enabled, those keystrokes
may never reach Ghostty; check System Settings > Keyboard > Keyboard
Shortcuts > Mission Control. This is a candidate, not a verified diagnosis
of the reported play session.
