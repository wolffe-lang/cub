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

## The Teeth, the Shallows, Gravehollow and the bosses (cb04, 2026-10-26, proposed)

| role | rich | plain |
|---|---:|---:|
| the Teeth: stone (two tones) / gravel / grass / trunk / floor | 243, 250 / 245 / 101 / 95 / 236 | 7, 15 / 7 / 2 / 3 / 0 |
| the Teeth: canopy, light / deep | 58 / 22 | 2 / 2 |
| the Shallows: bank shingle / grass / trunk / floor | 250 / 66 / 94 / 233 | 7 / 2 / 3 / 0 |
| the Shallows: canopy, light / deep; water / ripple (the river's) | 66 / 23; 24 / 31 | 2 / 2; 4 / 6 |
| the shallows (the ford's water half) | `≈` 117 on the water | `~` 14 on 4 |
| Gravehollow: trunk / grass / floor; canopy, light / deep | 59 / 240 / 232; 23 / 17 | 3 / 8 / 0; 2 / 2 |
| Gravehollow: the old scent marks on the grass | `:` `.` 240 | `:` `.` 8 |
| the boar / the lynx / the elk / the alpha | 130 / 179 / 145 / 244 | 1 / 3 / 7 / 8 |
| the alpha's eyes | `●` 196 | none: the plain alpha is its ASCII shape in 8 |
| a ghost by rank, newest first | 251, 248, 245, 242, 239, dim | 7, then 8 |

The new areas' paths are gravel (the Teeth, the Shallows) or the thicket's grass (Gravehollow); the world
audit's `path_off` holds them to `art.path_styles` as before.

## Bars and meadow landmarks (cb03a)

Health fill is red203, stamina fill green84, outline/labels grey250 on
235; plain uses12/10/7 on0. Both bars are directly labelled and separately
outlined, so their meaning never relies on red/green discrimination.
The labels use neutral ink, not status colour. These fixed status colours
have contrast above3:1 on the dark field; the categorical palette checker
also measured adjacent CVD separation18.1 (deutan),44.1 (tritan).
Tree/stone/stump/crow/cairn ink is dark59 on235 (plain8 on0), bones180
(plain7); warm den patches94 on52, embers208 (plain3/9 on0).

## Pickup light

The scent orb's white core is 231, its pale rim and motes 229, its violet
halo alternates 99 and 60. Plain uses 15 / 14 / 13 and 5. The core and
rim are bold; particles are not. The halo preserves the ground under it
rather than painting a solid tile. Shape and animation distinguish it
from the thin ground scent trail, even without colour. Closed bundles
use 229 (plain 15) rather than fur ink; inland cache contents alternate
229 and 220 (plain 15), with glints every 24 ticks.

Meat is salmon 210 with white bone and glints 231 (plain 12/15). A
spring's stone is 250 while available and 242 afterwards (plain 15/8),
with cyan 117 water (plain 14) and a white glint. Availability is also
shown by the spout/ripples versus the empty dotted basin.

## Rest-scene light (cb04a)

The regional rich backgrounds are Shingle17, Bramblehold233, Larkmeadow60,
Teeth236, Shallows23 and Gravehollow232. Plain uses blue4 for coast/river,
black0 elsewhere. The cub's distance-shaded fur steps through95,137,180,223
from dark rump to warm muzzle. Fire tips166, body214, heart229, ember208;
plain red9/yellow11. Text250 (plain7) stays clear of the animation. These
colours belong only to the rest scene; the existing bars are untouched.
The charge display is117 (plain14) on235 (plain0).

The allocation panel (cb04d) uses near-black232, muted-gold179 borders,
and bone-white230 labels; pending increases use84 and refused totals203.
Plain equivalents are black0, gold3, white15, green10 and red12. Arrows,
current/pending numbers and the refusal text duplicate the colour meaning.
