Footprint: module

# cb14 — the map overhaul: five new areas, branches with alcoves, larger arenas

Thornmere is a line again, but half again as long: Shingle, Cinderwick, Bramblehold, **the Stand**, Larkmeadow,
**the Burn**, the Teeth, **the Mere**, the Shallows, the Hush, **the Howe**, Gravehollow, with **the Underteeth** a
branch under the Teeth out into the Hush (the-proposals.md §3; items 4, 10 and 12 of the second playtest). Every area
from the Teeth on has two or three branches to guarded alcoves with a slot for cb15's consumables; every boss arena
grew by half; the whole forest holds under the world audit's 1300 rows, every census extended, the save at schema
6, the goldens for every new area's first screen on both tiers. Game code, game-owned tests, witnesses, censuses,
docs and goldens only: no engine, pin or CI change.

Ledger: cb14 — five areas (the Stand, the Burn, the Mere, the Underteeth, the Howe; Gravehollow split off the Hush),
alcoves with a `kind` slot from the Teeth on, arenas +50 %, CUB 6 with a slain mask an area and the gates word,
`journey 5`; module; plant #75; final source FINAL_SOURCE; the walk on the Mac green (9076 ticks, the stone
mouth opened); Mac build, checked tests and the full golden check green at the first attempt; Linux gate
LINUX_STATE.

## Prediction

`9f0ac776` committed `notes/cb14-prediction.txt` before the first change, at trunk `eb34a399`. What it said and
what held:

1. **The graph** held: thirteen areas, the Hush keeping id 5 and the cold den, Gravehollow 12 split off it
   (R-cb14-3), dens 12..15 the root hollow, the kiln, the dry island and the bone cache, none in the Howe or
   Gravehollow (R-cb14-1), the lengths as written (224 / 192 / 160 / 128). The edge count was wrong: 20 edges, not
   23 — the four re-pointed path edges (1, 4, 5, 6) plus five new path edges (10..14) and five new shortcuts
   (15..19); the prediction counted the re-pointed edges twice. The journey's rows came out exactly as predicted:
   1648 before, 2608 after (`notes/cb14-evidence/journey-length-{before,after}.txt`, seed 1 field 80, the route's
   rows plus its lateral travel: 2732 → 4248 spine cells, 1.55×; the Underteeth 300 cells off the line, not 192 —
   its tunnel wanders). Dens on the way on 9 → 12, bosses 4 → 4.
2. **Save and replay** held: CUB 6 (a mask an area, `gates`), `journey 5` with 44 values, `journey 4` (37) and
   `journey 3` (30) still read, every committed case replays. The count of moved goldens: 77 directories
   changed, 42 new, 6 gone (the prediction said about 40 and 14): the regenerated witnesses are the boss fights
   (the arenas grew, the alpha's walk starts at the cold den), the coast caches and the world witnesses from the
   meadow on (the hawk's body is cb10's, merged under this lane), the Teeth's second and the Hush's landmark (the
   landmarks moved), and `stand`; the rest scenes, the thicket's and the meadow's landmarks, the yards, the town's
   lane and `crags`/`river` changed only in the snapshot header and were kept as committed (their goldens
   byte-equal).
3. **Censuses** held: `--world-audit` 1300 rows, reached = required everywhere, `path_off` 0, nearest foe ≥ 30 (a
   den-less area reports 1000); den spacing least within an area 122, least onward 135 (the bar 110); bends 0
   reversals; spurs every end named; the foe census green (the old areas' counts unchanged, the new areas 4..6 —
   their alcove guards alone); the boss census every world won, `unwon:0` for all four, `arena_breaches 0`, the
   boar's first-attempt share 98 (two worlds at two attempts), the lynx, the elk and the alpha 100. gen-bench:
   green on the release build (every area under 50 ms at field 200 on kasumi). What did not hold at first (§6 of the prediction, "the fighter's walk to the alpha"): the
   stone mouth stood at the area's centre column and in seed 6 the route passed it to one side — the fighter
   walked into the brush; a gate now stands on the route's centre at its rows (`forest.gate_x`), and the census
   is 100/100.
4. **Render cost**: not measured on the Mac — the loaded-server condition (the-rules.md, the Mac leg) refused the
   first build at 7 GB free; the checked machine's cost was measured instead (below). The memory gate green on
   kasumi's release build: 316 bytes a tick over 519 ticks against the 4096 budget, the crash checkpoint and the
   fresh seed both (`tools/check-memory`).
5. **Arenas** held: 11/12 → 14, 14 → 18, 12 → 20, the shapes kept (`map_test`); the hit census and the hitbox
   audit green (their fights are not at a boss).
6. The den-spacing bar held without a move (the kiln at row 112 is 135 from the last warm hollow along the way);
   the Mere's goldens were written on kasumi and are checked by CI's macOS job (the Mac leg below).

The checked machine's step budget, measured with a probe file (never committed) on the trunk base and on the
branch: a Shingle `forest.kind` call fits ~2600 times a test on both; a Hush call fit >6000 times before and 4000
after (its three alcove branches: `in_branch` costs four `spine` evaluations where a cell lies in a branch's row
band), a Gravehollow night frame fit twice before and once after at 80×24 at the alpha's ring. Hence the rows below.

## Forbidden

Original code, art, lore and names only (the proposals' names and lines are the orchestrator's drafts in the
bible's register; the five standing stones' alphas — Harrow, Tarn, Sorrel, Greyback — and every alcove line are
this lane's); no other game's code, art, text or music. No engine (`lair`) change, no pin, workflow or CI change;
the hooks the contract names were left and not filled: no item (cb15: the alcoves' `kind` slot yields scent until
then), no NPC (cb16: the anchors are the landmarks), no part (cb17: `score.area_part` is `none` for the new
areas), no new foe (cb18: `sim.group_count` is 0 for the six areas and the alcove guards are foxes). No other
lane's file touched: `src/sim/sim.lu`'s edits are the ground rules, the gates, the new edges and the alcove
guards (cb10's input and drink paths, cb11's bite chain, cb12's death scene, cb13's journey menu and cb15's pouch
untouched); the save gained its field under schema 6 (cb13 and cb15 bump the schema too: the first to merge takes
6 and this lane rebases, as the-rules.md says). No ruling decided: R-cb14-1 .. R-cb14-5 are recommendations the
lane implemented (`docs/DESIGN.md`). Never labelled a PR, merged, tagged, created or closed an issue, edited
`~/.claude` or the planning repo, installed a package. No attribution or co-author trailers.

The Mac held the worktree for git and the walk behind the shared `mkdir` lock (`/Users/mfwolffe/lanes/mac-build.lock`,
the holder's pid checked, the 8 GiB `vm_stat` floor inside it: `/Users/mfwolffe/lanes/cb14/heavy.sh`); the
maintainer's MLX server never touched. kasumi ran every census, the checked tests, the case generation, the
goldens and the Linux gate on cores 12–15 under `/home/mfwolffe/lanes/kasumi-cores-12-15.lock` (a printing wait,
never a kill), in the engine's container (`.lair/tools/in-container`, cb09's recipe adapted:
`/home/mfwolffe/lanes/cb14/kasumi-run.sh`), everything under `/home/mfwolffe/lanes/cb14/`; no process group
signalled; nothing of another lane moved or renamed.

## Inputs verified

Base cub trunk `eb34a399` (cb09 + its note), rebased once onto `1497b5d3` (cb10's merge) at the orchestrator's
word; the worktree `~/lanes/cb14/cub` on branch `cb14`. Engine `74b89744` as `lair.pin` names it (staged by
`tools/fetch-lair` from the org's lair clone; `LAIR-REV` read), wolf 0.2.35 and lupin 0.1.56 with std `2386522e`
staged by `.lair/tools/fetch-toolchain` (the digests verified by the fetcher on both hosts; kasumi's stage copied
from cb09's, `STAMP` read). The contract, `the-rules.md`, the maintainer's notes (items 4, 10, 12),
`the-proposals.md` §3 (and §4–§6 for the hooks), the bible §2, §16, §19 (and §1, §8, §9), `DESIGN.md`, `ART.md`,
`GLYPHS.md`, `PALETTE.md`, `KEYS.md`, `REPLAY.md`, `SCORE.md`, the notes cb04, cb04a, cb04c, cb05, cb09 and
`sprints/RULES.md` §1–§10 read before the first change; README read and refreshed in its own commit.

Corrections for the planning repo: (1) the contract's "gm01's font rules (`tools/mkfont`, `font/extent.txt`, the
560-glyph console)" name PAX's files on its unmerged `gm01` branch (pax#209), not cub's: cub's glyph list is
`docs/GLYPHS.md`, held to the code by `src/glyphs_test.lu`, and gm01's `font/extent.txt` draws every braille
pattern and block element, so the four glyphs this lane added (`⠛`, `⡇`, `⢸`, `⣤`) are inside the console's extent
and nothing is owed to PAX; (2) the proposals' "between the Hush and Gravehollow" assumed two areas where cb04
built one — R-cb14-3 splits them (the lane's recommendation, not a decision); (3) "the Teeth's lower den" for the
raft's landing: the Teeth has one den (the ledge cleft, row 18); the raft lands at the Teeth's far end (row 200
east), the shortcut's point being the way back from the Mere's far shore; (4) the lore ids: cb15 holds 0..12 and
this lane's lines start at 13, registered through cb15's nearby-landmark discovery path once cb15 has merged
(the orchestrator's word of 2026-10-28; `lore.lu` carries the lines at stable ids until then).

Rulings recommended and implemented, none decided (`docs/DESIGN.md`, "The map overhaul"):

- **R-cb14-1 A**: the Howe has no den; the last rest is the Hush's cold den.
- **R-cb14-2 A**: the Underteeth's squeeze is a growth gate of paw 2 (`sim.UNDERTEETH_PAW`); a saved journey
  through it without the paw is corrupt.
- **R-cb14-3 A** (new): the Hush and Gravehollow are two areas (5 and 12); the alpha's fight starts at the cold den
  and the fighter walks the Howe and opens the stone mouth every attempt.
- **R-cb14-4 A** (new): the lookout's reveal is a schematic frame of the stations, not a zoomed render.
- **R-cb14-5 A** (new): the alcove guards stand on top of R-cb05-4's band in the Teeth, the Shallows and the Hush
  (`wide.FOES_LATE_MAX` 12 → 14); the new areas hold 3..6 until cb18.

Hooks left for the lanes under this one: **cb15** `lore.alcove_slot(area, cache)` is the alcove list with its
`kind` (`lore.PINE`, `SHARD`, `TUFT` beside `MARROW`, `YARROW`, `LORE`; `sim.cache_key` yields `ALCOVE_SCENT` for
the three until the pouch holds them; the shard "melts at the Burn" is cb15's); **cb16** one anchor an area in
`forest.landmark` (the lookout and the ruin for the Hermit, the kiln for the Charcoal-burner, the causeway's post
for the Ferryman, the sett's mouth — `forest.portal(seed, CRAGS, EDGE_SETT)` — for Dunmoss, Quill's perch, the
cold hearth; the lost in the Hush); **cb17** `score.area_part` names `none` for areas 7..12 (the Hush keeps
`old-den`); **cb18** `sim.group_count(area)` is 0 for areas 7..12 and `sim.area_foes` places only the alcove
guards there (the heron's stone is the Mere's last, rows 196..199 on the route; the sentries' post the stone
mouth's rows 218..220 in the Howe; the glow-worm clusters `lands.glow_row/glow_x`; the wisps the Howe's barrows).

## Evidence index

Every census ran on kasumi's native build at `ec67e933` (the last code commit; the cases, the goldens, the note
and this directory follow it) and sits under `notes/cb14-evidence/`; `tools/journey-length.py` is the before/after
instrument (`cub --paths-audit | python3 -I tools/journey-length.py`), the before table from trunk `eb34a399` built
with the same toolchain on kasumi.

- **Checked tests** (`.lair/tools/test`, kasumi, and the Mac at 6d28238f: 482 passed): `wolf test: 482 passed; 0 failed; 0
  rejected; 0 unsupported` (`checked-tests.txt`; 446 before cb10's and cb12's merges, which the branch was rebased
  onto once each at the orchestrator's word). The new rows: `src/map_test.lu` (the
  graph, the dens, the arenas' growth, the gates, the alcoves' guards and slots, the mouths, the stones' sinking,
  the ash, the mist, the spring, the reveal, the mouth bands), the schema-6 and thirteen-area rows in
  `src/areas_test.lu`, `src/refuge_test.lu`, `src/doorrest_test.lu`, `src/denmemory_test.lu`,
  `src/progression_test.lu`, `src/score_test.lu` and `src/forest_test.lu`, the vocabulary rows in
  `src/controls_test.lu`, `src/wide_test.lu` for the extended censuses. Sampling on the checked machine, the flood on the native gate: the map rows
  `test_cb14_the_<area>_s_spine_portals_and_mouths_are_open` walk seed 1's spine row by row (224 rows an area,
  160 for the Hush, 128 for Gravehollow) and check every portal, den, alcove, landmark and arena centre for open
  ground — one seed, every destination (a flood an area is over the budget); the fifty-seed, both-field flood is
  `--world-audit`'s, run natively on kasumi and in the Linux gate. `texture_and_path_bars` samples one drawn row
  an area and every fourth spine row at seed 0 (as cb04 did, two areas a test). The HUD's night fixture
  (`combatproof.hud_fixture`) stands in Gravehollow ten rows below the alpha's ring, where no alcove branch lies
  (the Hush's cells pay for three); the elk's health-bar row is one frame a test. The three row changes are named
  here because the step budget, not the behaviour, forced them.
- **The world audit** (`census/world-audit.txt`): 1300 rows, every one `reached == required`, `path_off 0`,
  straight runs ≤ the bar, bank step ≤ 1, nearest foe ≥ 30 or 1000 (den-less). `--area-map SEED AREA FIELD`
  (new) prints an area's map with every destination's cell, ground and flood answer — the instrument that found
  the Howe's cut-off stones, the Gravehollow mark in the brush, the spring on the route.
- **Den spacing** (`census/den-spacing.txt`): green, least within an area 122, least onward 135; **the bends**
  (`census/bends-audit.txt`) green; **the spurs** (`census/spurs-audit.txt`) green, every spur ending at a cache,
  a landmark or a den; **the foe census** (`census/foe-census.txt`) green.
- **The boss census** (`census/boss-census.txt`): four `fairness` lines, `unwon:0`, `arena_breaches 0`; the alpha's
  fight walked from the cold den through the Howe and the stone mouth every attempt (`fight.walk_on`).
- **The journey's length** (`journey-length-before.txt`, `-after.txt`): rows 1648 → 2608, spine cells 2732 → 4248,
  dens 9 → 12, bosses 4 → 4, the Underteeth 300 cells off the line.
- **The other censuses** (`census/`): doorways `total 3584000 misses 0` (1792000 before), foes `frames 562600
  omitted_frames 0` (331000 before; `tools/gameplay.py` carries both markers), den-census green (100 den paths),
  den-memory 100 journeys 0 failures, hud-census 192 rows 0 stray (the night rows now Gravehollow's), crossing,
  hitbox, look (338800 frames), motion (168000 rows; a gate's cell is no steady-probe ground), strike and hit
  censuses green; gen-bench on kasumi's native build the Shingle at field 200 over 50 ms on the base and on the
  branch alike (70 / 74 ms: the host), the new areas 10..29 ms; the release build's verdict green, every area
  under 50 ms at field 200.
- **The first screens** (`frames/<area>-{rich,plain}.txt`, `first-screens.txt`): the Teeth, the Shallows, the
  Hush, the Stand, the Burn, the Mere, the Underteeth, the Howe, Gravehollow, each from its den (or by the walk on)
  120 ticks down the route, both tiers; the committed cases `tests/cases/{crags,river,hush,stand,burn,mere,
  underteeth,howe,gravehollow}.pk` and their goldens.
- **The witnesses** (`world-proof.txt`, `den-proof.txt`): `--make-world-proof`, `--make-den-proof`,
  `--make-den-memory` and `--make-area-proof` (new) regenerated on kasumi; 26 cases changed beyond their header,
  28 new (`stand`, `burn`, `mere`, `underteeth`, `howe`, `gravehollow`, `hush`, the new landmarks, the new rest
  scenes), 3 gone (`old-den`, `rest-old-den-*`); the cases whose only change was the `journey 4 → 5` header were
  kept as committed.
- **Goldens**: written afresh on kasumi's release build (`.lair/tools/goldens --update` in the container) at
  6d28238f, 458 directories: 77 changed (the twelve boss cases, `end`, the hawk's two, the four coast caches,
  `crags`, `river`, `stand`, `den-checkpoint`, `whisper-flank`, the Teeth's, the Shallows' and the Hush's
  landmarks and the thicket's second and fourth, the Teeth's and the Shallows' rest scenes, the world witnesses
  from the meadow on, the art study), 42 new (the six first screens, ten landmarks, twenty rest scenes, each on
  both tiers), 6 gone (`old-den`, `rest-old-den-*`); every other directory byte-equal (the opening, the title, the
  score, the aims, the postures, the HUD, the dens, the yards, the town, the Shingle, the thicket's and the
  meadow's). The Mac's full golden check at 6d28238f: every case `ok` (first attempt). cb08's live flank
  witness `whisper-flank` was found again over the grown bowl (its keys are the new lynx fight's through tick
  807, every modifier and arrow released, down+left and Space at 808: the 1985th of a search over prefixes and
  aims against `tests/pty_rows.py`'s own check, run on the Mac); its pty row `cb08-whisper-flank` ok on both
  hosts, its goldens written on the Mac (frames 808..815, both tiers). `tools/gameplay.py`'s two-cell widening
  bar now reads the route's rows alone (path 0): from the Teeth on every area carries three branches of half
  width 3 by design, and the Hush's 160 rows gave them the median.
- **The memory gate** (`tools/check-memory`, kasumi's release build): green, 316 bytes a tick over 519 ticks, the
  crash checkpoint and the fresh seed, budget 4096.
- **The plant**: PR #75 (`cb14-plant-disconnected`, `1bbd4979` on `cd757027`): a wall of stones across the
  Howe's sixtieth row; `--world-audit` red by name at its first row `0 80 11 3 11 …` (reached 3 of 11),
  `test_cb14_the_howe_s_spine_portals_and_mouths_are_open ... FAILED (trap(assert))` and the Howe's texture row
  (`plant/plant-run.txt`). Never merged.
- **The walk** (item 5): `walk/walk.pk` (9076 ticks, written on the Mac by `cub --make-walk`: the alpha fixture's
  growth at the Shingle's start, every shortcut open, the gates shut) and `walk/walk.txt` with each area's entry
  tick — Cinderwick 546, Bramblehold 1641, the Stand 2802, Larkmeadow 3474, the Burn 4368, the Teeth 5082, the
  Mere 6080, the Shallows 6949, the Hush 7791, the Howe 8380, the stone mouth opened at 9076 — and the frame at
  each entry on both tiers (`walk/entry-<area>-{rich,plain}.txt`).
- **The Linux gate**: LINUX_LINE.
- **The Mac leg** (the-rules.md's loaded-server rule): the first build refused at 7 GB free; at 6d28238f the
  floor cleared (15.8 GB), the native build, the checked tests (482), the walk and the full golden check all green
  under `/Users/mfwolffe/lanes/cb14/heavy.sh` at the first attempt (`logs/mac-gate-job.log`); the build and the
  checked tests again at b48ee261 (`wolf fmt`), and the flank row at the final witness.

## Done-when

- [x] Five areas on both tiers, each with its palette, terrain, sprites, gates, den (none for the Howe), shortcut,
      lore and mechanic (ash hides the trail and halves the pace; the stones sink; the mist three cells; the spring
      refills; the sett's growth gate; the lookout's reveal); Gravehollow split off the Hush.
- [x] Branches and alcoves in every area from the Teeth on, 2–3 an area, seeded guard, a `kind` slot, visible as
      a gap in the route's wall; forty alcove bits in the save.
- [x] Arenas +50 % (14 / 14 / 18 / 20), the censuses re-run.
- [x] `--world-audit` seeds 0..49 green over 1300 rows; every census extended and compared; the journey-length
      table before/after; replay determinism (the cases replay; the goldens written once).
- [x] The memory gate green (316 bytes a tick against 4096).
- [x] Goldens of each new area's first screen on both tiers.
- [x] The walk from the Shingle to the Howe's stone mouth on the Mac, its entry frames in the evidence.
- [x] The note (five sections, the ledger line, the hooks), the plant red by name, the evidence directory.
- [ ] The full gauntlet: Linux LINUX_SHORT; Mac green (build, checked, walk, goldens at 6d28238f).
