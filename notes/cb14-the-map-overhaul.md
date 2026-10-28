Footprint: module

# cb14 — the map overhaul: five new areas, branches with alcoves, larger arenas

Thornmere is a line again, but half again as long: Shingle, Cinderwick, Bramblehold, **the Stand**, Larkmeadow,
**the Burn**, the Teeth, **the Mere**, the Shallows, the Hush, **the Howe**, Gravehollow, with **the Underteeth** a
branch under the Teeth out into the Hush (the-proposals.md §3; items 4, 10 and 12 of the second playtest). Every area
from the Teeth on has two or three branches to guarded alcoves with a slot for cb15's consumables; every boss arena
grew by half; the whole forest holds under the world audit's 1300 rows, every census extended, the save at schema
6, the goldens for every new area's first screen on both tiers. Game code, game-owned tests, witnesses, censuses,
docs and goldens only: no engine, pin or CI change.

## Prediction

`9f0ac776` committed `notes/cb14-prediction.txt` before the first change, at trunk `eb34a399`. What it said and
what held:

PREDICTION_RESULTS

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

The Mac held the worktree for git, one native build at a time and the walk behind the shared `mkdir` lock
(`/Users/mfwolffe/lanes/mac-build.lock`, the holder's pid checked, the 8 GiB `vm_stat` floor inside it:
`/Users/mfwolffe/lanes/cb14/heavy.sh`); the maintainer's MLX server never touched. kasumi ran every census, the
checked tests, the case generation, the goldens and the Linux gate on cores 12–15 under
`/home/mfwolffe/lanes/kasumi-cores-12-15.lock` (a printing wait, never a kill), in the engine's container
(`.lair/tools/in-container`, cb09's recipe adapted: `/home/mfwolffe/lanes/cb14/kasumi-run.sh`), everything under
`/home/mfwolffe/lanes/cb14/`; no process group signalled; nothing of another lane moved or renamed.

## Inputs verified

Base cub trunk `eb34a399` (cb09 + its note); the worktree `~/lanes/cb14/cub` on branch `cb14`. Engine
`74b89744` as `lair.pin` names it (staged by `tools/fetch-lair` from the org's lair clone; `LAIR-REV` read),
wolf 0.2.35 and lupin 0.1.56 with std `2386522e` staged by `.lair/tools/fetch-toolchain` (the digests verified by
the fetcher on both hosts; kasumi's stage copied from cb09's, `STAMP` read). The contract, `the-rules.md`, the
maintainer's notes (items 4, 10, 12), `the-proposals.md` §3 (and §4–§6 for the hooks), the bible §2, §16, §19 (and
§1, §8, §9), `DESIGN.md`, `ART.md`, `GLYPHS.md`, `PALETTE.md`, `KEYS.md`, `REPLAY.md`, `SCORE.md`, the notes cb04,
cb04a, cb04c, cb05, cb09 and `sprints/RULES.md` §1–§10 read before the first change; README read and refreshed in
its own commit.

Corrections for the planning repo: (1) the contract's "gm01's font rules (`tools/mkfont`, `font/extent.txt`, the
560-glyph console)" name PAX's files on its unmerged `gm01` branch (pax#209), not cub's: cub's glyph list is
`docs/GLYPHS.md`, held to the code by `src/glyphs_test.lu`, and gm01's `font/extent.txt` draws every braille
pattern and block element, so the four glyphs this lane added (`⠛`, `⡇`, `⢸`, `⣤`) are inside the console's extent
and nothing is owed to PAX; (2) the proposals' "between the Hush and Gravehollow" assumed two areas where cb04
built one — R-cb14-3 splits them (the lane's recommendation, not a decision); (3) "the Teeth's lower den" for the
raft's landing: the Teeth has one den (the ledge cleft, row 18); the raft lands at the Teeth's far end (row 200
east), the shortcut's point being the way back from the Mere's far shore.

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

EVIDENCE

## Done-when

DONEWHEN
