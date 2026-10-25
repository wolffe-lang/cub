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

| weasel | 130 | 1 |
| fox | 166 | 9 |

Foes have their own threat colours (proposed 2026-10-25), distinct from
cub fur and scent. Crouch changes the whole head posture, not just colour.
The trail changes from `:` to `.` after 150 ticks, disappearing at 300.
Foe death sprites dim and erode over 15 ticks; cub death dissolves over 30.
Both use simulation ticks, never wall-clock time. The leap displaces only
presentation, not its collision body. Both tiers cover identical sim ticks.
