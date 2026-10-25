# Area palettes

The current keyframe is cold daylight on gravel. The rich tier uses xterm
indices; the plain tier uses the sixteen console colours. These are proposed
2026-10-25 values. Bramblehold and Larkmeadow use the dusk keyframes below; night is not yet a playable phase.

| role | rich | plain |
|---|---:|---:|
| gravel | 240 | 8 |
| gravel marks | 247 | 7 |
| path (the coast's) | 247 on 240 | 7 on 8 |
| grass | 64 | 2 |
| trunk | 94 | 3 |
| canopy / deep canopy | 28 / 22 | 2 / 2 |
| forest floor | 234 | 0 |
| cub fur / dim fur | 180 / 137 | 11 / 3 |
| deer | 180 | 11 |
| hawk | 181 | 13 |
| water / ripple | 24 / 31 | 4 / 6 |
| reeds | 65 | 2 |
| weasel | 130 | 1 |
| fox | 166 | 9 |

**The path (cb02c, 2026-10-25).** The maintainer's word: "The branch paths should be the
same color as the coastline/forest paths." Every path cell has one ground per area,
`forest.path_kind`: on the coast the shore's gravel, for the shore, the thorn route, the
four branches and their alcoves, the log's branch and the gate's exit alike (rich marks
247 on 240, glyphs space `·` `․` `░`; plain 7 on 8, space `.` `,` `:`); inland the grass,
under the area's dusk keyframe (the thicket's path grass 65 on 233, the meadow's 137 on
235). `forest.carved` is the one place a path is carved and it returns that kind, and
`art.path_styles` is the one set of styles a path cell may draw in, so a new path cannot
drift into the forest's colour: `--world-audit`'s `path_off` column counts, over fifty
seeds, both fields and every area, the walkable path cells drawn outside the set (zero).
Before cb02c the branches and the log's branch drew the forest's grass (64 on 234,
`⠖` `⠶`), the canopy's colours, and read as more forest.

Foes have their own threat colours (proposed 2026-10-25), distinct from
cub fur and scent. Crouch changes the whole head posture, not just colour.
The trail changes from `:` to `.` after 150 ticks, disappearing at 300.
Foe death sprites dim and erode over 15 ticks; cub death dissolves over 30.
Both use simulation ticks, never wall-clock time. The leap displaces only
presentation, not its collision body. Both tiers cover identical sim ticks.


## Dusk keyframes (2026-10-25, proposed)

| role | rich | plain |
|---|---:|---:|
| thicket foliage, light / deep | 29 / 23 | 2 / 2 |
| thicket path grass / floor | 65 / 233 | 2 / 0 |
| meadow grass / tall grass / floor | 137 / 143 / 235 | 3 / 3 / 0 |
| the woods round the meadow, light / deep | 58 / 22 | 2 / 2 |
| dusk trunk | 95 | 3 |
| hawk wings / ground | 181 / 235 | 13 / 0 |
| thorn hazard / ground | 196 / 234 | 12 / 0 |
| exit shadow ink / ground | 238 / 232 | 8 / 0 |
| opening river ink / ground | 153 / 17 | 7 / 4 |

The thicket keeps distant foliage visible while sight still limits creatures;
the meadow keeps long views. Each dusk area keeps two foliage tones (cb02b),
so its deep forest is textured like the Shingle's and never one green; the
meadow's own ground stays gold while the woods closing round it are green. Exit mouths share one shadow band on both tiers. Thorn hazard
ink is never label ink, and neither tier uses hash or slash as a gate.
Scent drops share the mark's star, dimming to a dot halfway through their
300-tick lifetime; expiry and collection are simulation events, not colour
interpretations. The hawk's stopping shadow and wings are posture, not
colour alone. Its separate sheet covers circle, stop, stoop, recovery and
three fade stages. Deer use antlers, a two-cell body and legs on both tiers.
