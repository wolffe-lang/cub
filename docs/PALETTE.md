# Area palettes

The current keyframe is cold daylight on gravel. The rich tier uses xterm
indices; the plain tier uses the sixteen console colours. These are proposed
2026-10-25 values. Bramblehold and Larkmeadow use the dusk keyframes below; night is not yet a playable phase.

| role | rich | plain |
|---|---:|---:|
| gravel | 240 | 8 |
| gravel marks | 247 | 7 |
| grass | 64 | 2 |
| trunk | 94 | 3 |
| canopy / deep canopy | 28 / 22 | 2 / 2 |
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


## Dusk keyframes (2026-10-25, proposed)

| role | rich | plain |
|---|---:|---:|
| thicket foliage / floor | 29 / 233 | 2 / 0 |
| meadow grass / floor | 137 / 235 | 3 / 0 |
| dusk trunk | 95 | 3 |
| hawk wings / ground | 181 / 235 | 13 / 0 |
| thorn hazard / ground | 196 / 234 | 12 / 0 |
| exit shadow ink / ground | 238 / 232 | 8 / 0 |
| opening river ink / ground | 153 / 17 | 7 / 4 |

The thicket keeps distant foliage visible while sight still limits creatures;
the meadow keeps long views. Exit mouths share one shadow band on both tiers. Thorn hazard
ink is never label ink, and neither tier uses hash or slash as a gate.
Scent drops share the mark's star, dimming to a dot halfway through their
300-tick lifetime; expiry and collection are simulation events, not colour
interpretations. The hawk's stopping shadow and wings are posture, not
colour alone. Its separate sheet covers circle, stop, stoop, recovery and
three fade stages. Deer use antlers, a two-cell body and legs on both tiers.
