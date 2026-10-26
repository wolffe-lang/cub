# cb04's plants: three breaks, each a draft PR on its own branch, red by name in its own run

Each plant is one commit on the final head (`3dd03c9`), never merged, its PR left a draft; the
orchestrator closes them. The runs below are `tier pr` (the Linux leg in the container); the run id
was read once at the push.

| plant | branch, head | PR | run | the break | expected red rows |
|---|---|---|---|---|---|
| a boss that can leave its arena | `cb04-plant-arena`, `44fd002` | #27 | 40263328323 | `boss_may_stand` no longer refuses a cell outside the arena | `bosses_test::test_cb04_a_boss_never_leaves_its_arena`; `gameplay.py` fairness (`--boss-census` exit 1, `arena_breaches` > 0); the boss goldens |
| a telegraph shorter than the parry window | `cb04-plant-telegraph`, `f951529` | #28 | 40263328539 | the lynx's swipe winds up in 6 ticks (3 in phase two) | `bosses_test::test_cb04_every_telegraph_is_at_least_the_parry_window`; `gameplay.py` bosses (the lynx's telegraph under 9) and fairness; the lynx goldens |
| a ghost drawn where no death was | `cb04-plant-ghost`, `dca33dd` | #29 | 40263331511 | `draw_ghosts` marks a ghost beside the cub on every frame | `gameplay.py` ghosts (the plain mark count: an empty archive drew a ghost); every golden frame, both tiers |

Results (read once each when the runs ended):

