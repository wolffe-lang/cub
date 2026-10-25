# The Shingle palette

The current keyframe is cold daylight on gravel. The rich tier uses xterm
indices; the plain tier uses the sixteen console colours. These are proposed
2026-10-25 values. Dusk and night belong to the connected-area pass, not an
unseen interpolation in this build.

| role | rich | plain |
|---|---:|---:|
| gravel | 240 | 8 |
| gravel marks | 247 | 7 |
| grass | 64 | 2 |
| trunk | 94 | 3 |
| canopy / deep canopy | 28 / 22 | 2 / 0 |
| forest floor | 234 | 0 |
| cub fur / dim fur | 180 / 137 | 11 / 3 |
| water / ripple | 24 / 31 | 4 / 6 |
| reeds | 65 | 2 |

Combat accents use fur colours so they remain legible on gravel without
introducing a new palette: bright for a real crouch, strike, lock and mark;
dim for scent and the den. The fox's false tell is `~`, its real tell `_`.
The trail changes from `:` to `.` after 150 ticks, disappearing at 300.
Death dissolves cells over 30 ticks; it never depends on wall-clock time.

Both tiers use the same ground envelope. A leap's raised apostrophe is an
arc accent, not a displaced collision body. Rich and plain frame goldens
cover the same ticks of every encounter.
