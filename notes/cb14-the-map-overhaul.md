Footprint: module

# cb14 — the map overhaul: five new areas, branches with alcoves, larger arenas

Thornmere is a line again, but half again as long: Shingle, Cinderwick, Bramblehold, **the Stand**, Larkmeadow,
**the Burn**, the Teeth, **the Mere**, the Shallows, the Hush, **the Howe**, Gravehollow, with **the Underteeth** a
branch under the Teeth out into the Hush (the-proposals.md §3; items 4, 10 and 12 of the second playtest). Every area
from the Teeth on has two or three branches to guarded alcoves with a slot for cb15's consumables; every boss arena
grew by half; the whole forest holds under the world audit's 1300 rows, every census extended, the save at schema
7 over cb13's and cb15's schema 6, the goldens for every new area's first screen on both tiers. Game code, game-owned tests, witnesses, censuses,
docs and goldens only: no engine, pin or CI change.

Ledger: cb14 — five areas (the Stand, the Burn, the Mere, the Underteeth, the Howe; Gravehollow split off the Hush),
alcoves from the Teeth on whose pine, shard and tuft are cb15's items (R-cb14-6 A), arenas +50 %, CUB 7 (thirteen
slain masks and the gates over cb13's wrapper and cb15's items) and `journey 6` (211 slots), cb15's CUB 6 and
`journey 5` migrating, lore 13..31 through cb15's paths; module; plant #75; final source `0e815256` (on cub trunk
`feb57572`: cb10's, cb12's, cb11's, cb11b's, cb13's and cb15's merges under it); the checked suite 562/0/0 and the
memory gate green on kasumi at `079d3c5a`; the Mac and Linux gates green at `73ff1187` (the Mac: build, checked
562, the walk 9369 ticks, the full golden check at the first attempt; Linux: check-linux after `tools/prepare-pty`
archived a stale engine fixture, check-memory, native goldens, gameplay on both backends, perf at slack 1 inside
the container); a save written by a pre-rebase cb14 build is refused, never migrated (Inputs verified, 10).

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
   byte-equal). Over cb11's bite chain (the rebase onto `f20650d4`) the fights moved again: 33 cases regenerated
   and the goldens rewritten at `aa5698f8` (the Evidence index's "Goldens"). Over cb15 (the rebase onto
   `feb57572`) cb13's and cb15's schema 6 and journey 5 had the numbers first: the save is CUB 7, the snapshot
   journey 6, and theirs migrate (the Evidence index's "The rebase onto cb15").
3. **Censuses** held: `--world-audit` 1300 rows, reached = required everywhere, `path_off` 0, nearest foe ≥ 30 (a
   den-less area reports 1000); den spacing least within an area 122, least onward 135 (the bar 110); bends 0
   reversals; spurs every end named; the foe census green (the old areas' counts unchanged, the new areas 4..6 —
   their alcove guards alone); the boss census every world won, `unwon:0` for all four, `arena_breaches 0`, the
   boar's first-attempt share 98 (two worlds at two attempts), the lynx, the elk and the alpha 100 (over cb11's
   bite chain all four at 100, the Linux gate's census). gen-bench:
   green on the release build (every area under 50 ms at field 200 on kasumi). What did not hold at first (§6 of the prediction, "the fighter's walk to the alpha"): the
   stone mouth stood at the area's centre column and in seed 6 the route passed it to one side — the fighter
   walked into the brush; a gate now stands on the route's centre at its rows (`forest.gate_x`), and the census
   is 100/100.
4. **Render cost**: not measured on the Mac — the loaded-server condition (the-rules.md, the Mac leg) refused the
   first build at 7 GB free; the checked machine's cost was measured instead (below). The memory gate green on
   kasumi's release build: 316 bytes a tick over 519 ticks against the 4096 budget, the crash checkpoint and the
   fresh seed both (`tools/check-memory`); at `5db48d71`, in the Linux gate, 425 and 310 bytes a tick over
   520 and 515 ticks; over cb15, at `079d3c5a` (job20), 482 and 308 over 518 and 519.
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
the hooks the contract names were left and not filled: no item of this lane's (since cb15's merge the alcoves'
pine, shard and tuft are cb15's own items, R-cb14-6 A), no NPC (cb16: the anchors are the landmarks), no part (cb17: `score.area_part` is `none` for the new
areas), no new foe (cb18: `sim.group_count` is 0 for the six areas and the alcove guards are foxes). No other
lane's file touched: `src/sim/sim.lu`'s edits are the ground rules, the gates, the new edges and the alcove
guards (cb10's input and drink paths, cb11's bite chain, cb12's death scene, cb13's journey menu and cb15's pouch
untouched); the save gained its fields under schema 7 (cb13 and cb15 took 6 first, as the-rules.md says the
first to merge does). At the rebase onto cb15's merge the merged code of cb13 and cb15 was extended where the
two met, never rewritten: `journey.lu` (CUB 7 beside their CUB 6 path, untouched), `controls.lu` (seven slots
appended after cb15's), `sim.lu`'s `cache_key` (the alcove kinds through cb15's `give_item`) and `hazards_step`
(cb14's landmarks through cb15's `remember_lore`), `art.lu` (the reveal under cb15's inventory overlay); three
of cb13's migration tests now expect CUB 7 bytes from the same fixture, cb15's `pouch_test` pins `lore.COUNT` 32
for 13, and the current-schema assertions in the tests and tools name CUB 7. No ruling decided: R-cb14-1 ..
R-cb14-6 are recommendations the lane implemented (`docs/DESIGN.md`). Never labelled a PR, merged, tagged, created or closed an issue, edited
`~/.claude` or the planning repo, installed a package. No attribution or co-author trailers.

The Mac held the worktree for git, the walk and the flank searches behind the shared `mkdir` lock (`/Users/mfwolffe/lanes/mac-build.lock`,
the holder's pid checked, the 8 GiB `vm_stat` floor inside it: `/Users/mfwolffe/lanes/cb14/heavy.sh`); the
maintainer's MLX server never touched. kasumi ran every census, the checked tests, the case generation, the
goldens and the Linux gate on cores 12–15 under `/home/mfwolffe/lanes/kasumi-cores-12-15.lock` (a printing wait,
never a kill), in the engine's container (`.lair/tools/in-container`, cb09's recipe adapted:
`/home/mfwolffe/lanes/cb14/kasumi-run.sh`), everything under `/home/mfwolffe/lanes/cb14/`; no process group
signalled; nothing of another lane moved or renamed.

## Inputs verified

Base cub trunk `eb34a399` (cb09 + its note), rebased once onto each merge the orchestrator announced: `1497b5d3`
(cb10), `f6af855c` (cb12), `f20650d4` (cb11), `feb57572` (cb11b `991cc704`, cb13 `918dd9a0`, cb15); the worktree `~/lanes/cb14/cub` on branch `cb14`. Engine
`74b89744` as `lair.pin` names it (staged by `tools/fetch-lair` from the org's lair clone; `LAIR-REV` read), wolf 0.2.35 and lupin 0.1.56 with std `2386522e`
staged by `.lair/tools/fetch-toolchain` (the digests verified by the fetcher on both hosts; kasumi's stage copied
from cb09's, `STAMP` read). The contract, `the-rules.md`, the maintainer's notes (items 4, 10, 12),
`the-proposals.md` §3 (and §4–§6 for the hooks), the bible §2, §16, §19 (and §1, §8, §9), `DESIGN.md`, `ART.md`,
`GLYPHS.md`, `PALETTE.md`, `KEYS.md`, `REPLAY.md`, `SCORE.md`, the notes cb04, cb04a, cb04c, cb05, cb09 and
`sprints/RULES.md` §1–§10 read before the first change; README read and refreshed in its own commit.

Corrections for the planning repo and the hand-over: (1) the contract's "gm01's font rules (`tools/mkfont`,
`font/extent.txt`, the 560-glyph console)" name PAX's files on its unmerged `gm01` branch (pax#209), not cub's: cub's glyph list is
`docs/GLYPHS.md`, held to the code by `src/glyphs_test.lu`, and gm01's `font/extent.txt` draws every braille
pattern and block element, so the four glyphs this lane added (`⠛`, `⡇`, `⢸`, `⣤`) are inside the console's extent
and nothing is owed to PAX; (2) the proposals' "between the Hush and Gravehollow" assumed two areas where cb04
built one — R-cb14-3 splits them (the lane's recommendation, not a decision); (3) "the Teeth's lower den" for the
raft's landing: the Teeth has one den (the ledge cleft, row 18); the raft lands at the Teeth's far end (row 200
east), the shortcut's point being the way back from the Mere's far shore; (4) the lore ids: cb15 holds 0..12 and
this lane's lines start at 13, registered through cb15's nearby-landmark discovery path once cb15 has merged
(the orchestrator's word of 2026-10-28; `lore.lu` carries the lines at stable ids until then); (5) the hand-over's
`rsync -a kasumi:…/tests/goldens/ …` (bringing job18's regeneration back to the Mac) would have left the 228
golden frames job18 removed in place on the Mac: the sync ran with `--delete` (its dry run listed exactly those
228), and the Mac's `git status` set and a hash over every file in `tests/cases` and `tests/goldens` then matched
kasumi's (`286ad08b…` on both); (6) the rebase onto cb11's merge resolved `tests/cases/whisper-flank.pk` to
trunk's (cb11's own prefix-820 recipe) in `355e9b18` while keeping this lane's 808..815 goldens, so the witness
was stale from there until `d2f2a6c7` found it again (the Evidence index's "Goldens"); (7) at the rebase onto
cb15, the auto-mode classifier refused resolving the golden-only commits' conflicts by taking trunk's side
(`git checkout --ours --pathspec-from-file=…`); the maintainer ruled "skip and regenerate": the two golden-only
commits (`66a826fa` "Write the goldens afresh", `aecbaff8` the post-cb11 rewrite) were skipped with `git rebase
--skip` and every golden and case written once more by the repo's generators in `0e815256`; (8) an empty regular
file at `/Users/mfwolffe/lanes/mac-build.lock` (22:19:41Z, no holder, not the `mkdir` protocol's directory) held
every Mac lane's lock; the orchestrator removed it; (9) cb15's note says "cb14 and cb16 start at 13": cb14's
nineteen lines take 13..31, and with `pouch.LORE_SLOTS` 32 the found-lore list is now exactly full, so cb16's
first line needs a capacity change, a format bump (held by `cb14_items_test`: `lore.COUNT == pouch.LORE_SLOTS`);
(10) **a save written by any pre-rebase cb14 build** (the CUB 6 shape with thirteen slain masks and a `gates 0`
line, fourteen lines, which this branch wrote before the rebase onto cb15) **is refused as `save_corrupt` by this
build**: it never shipped, so it is not migrated; CUB 6 is cb13's and cb15's shape now. A playtester who ran a
cb14 branch build starts a new journey (or keeps that file for that build); the shipped CUB 6, 5 and 4 all
migrate. The Linux gate met exactly this: the engine's pty rows start their journey at `target/pty/engine.save`
(`tests/lair.conf`), which persists in kasumi's clone, and the one there was such a pre-rebase save (written
2026-10-28 02:26 local by this lane's own earlier gate) — so `quit`, `ctrl-c`, `trap` and perf-idle ended at once
with `cub: save_corrupt`; the repo's `tools/prepare-pty`, which the game's own gates run first, archived it to
`target/pty/engine-previous-cx7iu4yk/engine.save` (254 bytes, deleted nothing) and every row was green after. The
lane's `job17.sh` (gate tooling under `~/lanes/cb14/`, not in the repo) left `prepare-pty` out and printed only each
step's last line, so job17d's marker said `CB14_KASUMI_EXIT 0` over a red check-linux and a perf-idle `FAILED`;
it now runs `prepare-pty` first, exits nonzero when any step does, and fails the perf step on any `FAILED` line
(`gates/job17-fix.diff`).

Rulings recommended and implemented, none decided (`docs/DESIGN.md`, "The map overhaul"):

- **R-cb14-1 A**: the Howe has no den; the last rest is the Hush's cold den.
- **R-cb14-2 A**: the Underteeth's squeeze is a growth gate of paw 2 (`sim.UNDERTEETH_PAW`); a saved journey
  through it without the paw is corrupt.
- **R-cb14-3 A** (new): the Hush and Gravehollow are two areas (5 and 12); the alpha's fight starts at the cold den
  and the fighter walks the Howe and opens the stone mouth every attempt.
- **R-cb14-4 A** (new): the lookout's reveal is a schematic frame of the stations, not a zoomed render.
- **R-cb14-5 A** (new): the alcove guards stand on top of R-cb05-4's band in the Teeth, the Shallows and the Hush
  (`wide.FOES_LATE_MAX` 12 → 14); the new areas hold 3..6 until cb18.
- **R-cb14-6 A** (new, at the rebase onto cb15): the alcoves' pine, shard and tuft are cb15's PINE, ICE and TUFT,
  given through `sim.give_item` or left on the ground at the cache when the stack is full, as cb15 does for
  marrow and yarrow (`sim.reward_item`); B would keep the scent placeholder (30) for a later lane. The
  maintainer's to overturn.

Hooks left for the lanes under this one: **cb15** (merged first) `lore.alcove_slot(area, cache)` is the alcove
list with its `kind`, filled at the rebase (R-cb14-6 A); the shard "melts at the Burn" stays cb15's hook; **cb16**
one anchor an area in
`forest.landmark` (the lookout and the ruin for the Hermit, the kiln for the Charcoal-burner, the causeway's post
for the Ferryman, the sett's mouth — `forest.portal(seed, CRAGS, EDGE_SETT)` — for Dunmoss, Quill's perch, the
cold hearth; the lost in the Hush; its first lore line needs the wider save, correction 9); **cb17** `score.area_part` names `none` for areas 7..12 (the Hush keeps
`old-den`); **cb18** `sim.group_count(area)` is 0 for areas 7..12 and `sim.area_foes` places only the alcove
guards there (the heron's stone is the Mere's last, rows 196..199 on the route; the sentries' post the stone
mouth's rows 218..220 in the Howe; the glow-worm clusters `lands.glow_row/glow_x`; the wisps the Howe's barrows).

## Evidence index

Every census ran on kasumi's native build at `ec67e933` (the last code commit; the cases, the goldens, the note
and this directory follow it) and sits under `notes/cb14-evidence/`; after cb11's merge the world audit, den
spacing, the foe census, the bends and the spurs ran again at `aa5698f8` (job18), byte-equal to the files here,
and the boss census again in the Linux gate at `5db48d71`; `tools/journey-length.py` is the before/after
instrument (`cub --paths-audit | python3 -I tools/journey-length.py`), the before table from trunk `eb34a399` built
with the same toolchain on kasumi.

- **Checked tests** (`.lair/tools/test`): at `079d3c5a`, over cb15, on kasumi `wolf test: 562 passed; 0 failed;
  0 rejected; 0 unsupported; 0 filtered out` (`checked-tests.txt`; the Mac's at the PR head is in its gate);
  509 on both hosts at `5db48d71` before it, 446 before cb10's and cb12's merges and 482 before cb11's (the branch
  rebased onto each once at the orchestrator's word). The new rows:
  `src/map_test.lu` (the graph, the dens, the arenas' growth, the gates, the alcoves' guards and slots, the mouths, the stones' sinking,
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
- **The rebase onto cb15** (`rebase-cb15/`): the CUB 6 save and the journey 5 recording a binary built at trunk
  `60890a49` wrote (`tests/saves/cb15-v6.save`, `cb15-journey5.pk`: three real runs of that binary, how in
  `tests/saves/provenance.json` and `rebase-cb15/make-cb15-fixtures.py`) migrate: `src/cb14_migration_test.lu`
  holds the CUB 6 (name `birch_7`, played_ms 6974, pine, ice and tuft, two found lines, seeded 127) to its
  exact CUB 7 bytes, the six new masks empty and no gate, the CUB 7 round trip byte-exact; the journey 5
  snapshot read into journey 6 with every pouch slot kept; the four CUB 5 fixtures, a journey 4 and a journey 3
  case still read; a rechecksummed CUB 7 with a missing, out-of-range or doubled gates line, seven or fourteen
  masks or a CUB 6 header refused, CUB 8 refused by name; cb13's rechecksummed wrapper rows refusing at CUB 7
  (`cb13_migration_test`); `tools/world_checks.py` the same migration at file level with the shipping binary.
  `src/cb14_items_test.lu`: cb15's provisional pickups (seven yarrow, six marrow and the tuft, five ice) all on
  open ground in the new map for seeds 1 and 7; the Hush's pine, the Shallows' shard and the Howe's tuft in the
  pouch when dug, a full stack's on the ground; the lookout's and a standing stone's lines in the found-lore
  list. The cases and goldens written once more by the repo's generators on kasumi (`0e815256`; `summary.txt`):
  44 cases off cb14's pre-rebase 44-slot journey 5 regenerated as journey 6, `whisper-flank` found again by
  the widened search with the same keys (start 696, `pty: cb08-whisper-flank ok` on the Mac), every other
  generated case header-only identical and kept; golden keys 7256 → 7630, 238 missing and 612 extra, each
  cb14's own before the rebase; 1916 changed, all the map (218 byte-identical to cb14's pre-rebase goldens,
  1692 changed by both lanes, cb14's world under cb15's drawing, 6 rich final frames with cb15's pickups in
  view); the format bump 0 keys, the items swap 0 keys; the 450 inherited final.states 382 byte-identical to
  trunk's and 68 the map's, none moved against cb14 before the rebase (`golden-classes.txt`, `golden-keys.txt`,
  `final-states.txt`, both instruments beside them). The quick audits at `6dda0fd2` byte-equal to the census
  files here (`job19.log`).
- **The world audit** (`census/world-audit.txt`): 1300 rows, every one `reached == required`, `path_off 0`,
  straight runs ≤ the bar, bank step ≤ 1, nearest foe ≥ 30 or 1000 (den-less). `--area-map SEED AREA FIELD`
  (new) prints an area's map with every destination's cell, ground and flood answer — the instrument that found
  the Howe's cut-off stones, the Gravehollow mark in the brush, the spring on the route.
- **Den spacing** (`census/den-spacing.txt`): green, least within an area 122, least onward 135; **the bends**
  (`census/bends-audit.txt`) green; **the spurs** (`census/spurs-audit.txt`) green, every spur ending at a cache,
  a landmark or a den; **the foe census** (`census/foe-census.txt`) green.
- **The boss census** (`census/boss-census.txt`, the Linux gate's release run at `5db48d71`): four `fairness`
  lines, `unwon:0`, `arena_breaches 0`, every boss won at the first attempt in all 100 worlds (before cb11's
  merge the boar's share was 98); the alpha's fight walked from the cold den through the Howe and the stone mouth
  every attempt (`fight.walk_on`); the walker's stderr diagnostics (a goal blocked mid-fight, replanned) 1 → 7
  lines, no fight lost.
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
  meadow's). The Mac's full golden check at 6d28238f: every case `ok` (first attempt). After cb11's merge, job18
  on kasumi (`aa5698f8`) regenerated every witness and wrote the goldens afresh again: 33 cases changed beyond
  their header (the twelve boss cases, the four coast caches, `end`, `gravehollow`, `howe`, the hawk's two, the
  Howe's six landmarks, Gravehollow's, the Teeth's second, the four world witnesses from the meadow on;
  `42a55f06`) and 88 golden directories (44 cases on both tiers: 31 of those 33, the boar's and the elk's windups
  byte-equal; `whisper-flank`; cb11's twelve `cb11-hand-*` cases, which replay on this lane's world;
  `aecbaff8`), 228 frames gone with the moved ticks; brought back to the Mac byte-equal (correction 5). cb08's
  live flank witness `whisper-flank` had to be found again over cb11's bite chain: a fresh bite is combo 1 (its
  cone 11 left of the aim) and starts the tick after the press, so from where the fighter stands a bite either
  turns into the lynx's centre or lunges off its body, and neither the lane's earlier search (prefixes and aims
  over the lynx fight's keys: 3040 trials) nor cb08's own recipe at its stagger windows found one. cb08's recipe
  widened (`flank/flank-search-moves.py`: the `boss-lynx-beaten` keys through each tick Whisper stands idle
  within three cells of the lynx, every modifier and arrow released, one of eight directions held 4–16 ticks,
  then an aim and Space, judged by `tests/pty_rows.py`'s own check) found it at the 7306th candidate: start 696,
  up+right for 8 ticks, left and Space at 704, the bite started at 705 landing at 708 (the lynx 140 → 128), both
  former centre-cone endpoints missing by at least 10100 (`d2f2a6c7`; every search's log in
  `flank/flank-searches.txt`). Its pty row `pty: cb08-whisper-flank ok (darwin arm64, exit 0, 2185201 bytes
  captured)` on the Mac and `ok (linux x86_64, …)` in the Linux gate, its goldens written on the Mac (frames
  704..710, both tiers). The Mac's full golden check at `5db48d71`: 481 `ok`, 0 `DIFFERS`, at the first attempt.
  `tools/gameplay.py`'s two-cell widening
  bar now reads the route's rows alone (path 0): from the Teeth on every area carries three branches of half
  width 3 by design, and the Hush's 160 rows gave them the median.
- **The memory gate** (`tools/check-memory`, kasumi's release build): green, 316 bytes a tick over 519 ticks, the
  crash checkpoint and the fresh seed, budget 4096; at `5db48d71` in the Linux gate `memory gate: green, crash
  checkpoint and fresh seed; budget 4096 bytes/tick`, 425 and 310 bytes a tick over 520 and 515 ticks; over cb15
  at `079d3c5a` (job20) the same line, 482 and 308 over 518 and 519 (`rebase-cb15/job20.log`).
- **The plant**: PR #75 (`cb14-plant-disconnected`, `1a612e19` on `b1e57f53`, rebased once at each of this
  lane's rebases from `1bbd4979` on `cd757027`; not an ancestor of the branch): a wall of stones across the
  Howe's sixtieth row; `--world-audit` red by name at its first row `0 80 11 3 11 5 1000 3 1 1 100 67 0`
  (reached 3 of 11), `test_cb14_the_howe_s_spine_portals_and_mouths_are_open ... FAILED (trap(assert))` and the
  Howe's texture row, `wolf test: 560 passed; 2 failed` (`plant/plant-run.txt`, kasumi at `1a612e19`). Never
  merged.
- **The walk** (item 5): `walk/walk.pk` (9369 ticks, written on the Mac by `cub --make-walk`, last at `73ff1187`
  in the Mac gate: its keys, its ticks and its first 44 snapshot values are identical to the capture at
  `5db48d71`, which carried the pre-rebase `journey 5` of 44 slots; it now begins `journey 6` with all 211; the
  alpha fixture's growth at the Shingle's start, every shortcut open, the gates shut) and `walk/walk.txt` with
  each area's entry tick — Cinderwick 548, Bramblehold 1645, the Stand 2808, Larkmeadow 3480, the Burn 4378, the
  Teeth 5092, the Mere 6122, the Shallows 6991, the Hush 7888, the Howe 8673, the stone mouth opened at 9369 (9076
  before cb11's merge) — and the frame at each entry on both tiers (`walk/entry-<area>-{rich,plain}.txt`).
- **The gates at the PR head** (over cb15, `73ff1187`; this note's later commit touches `notes/` only):
  the Mac (`gates/mac-gate-73ff1187.log`, behind the lock, the floor clear at 19.4 GB): `build 0`, `walk 0` (the
  stone mouth at 9369, every entry tick and entry frame as before), `test 0` with `wolf test: 562 passed; 0
  failed; 0 rejected; 0 unsupported; 0 filtered out` and 0 SKIP, `goldens attempt 1 exit 0` (507 `ok`, 0
  `DIFFERS`), `CB14_MAC_GATE_EXIT 0`. Linux, kasumi cores 12–15 in the engine's container: job17d
  (`gates/linux-gate-73ff1187.log`) `check-memory 0 memory gate: green, crash checkpoint and fresh seed; budget 4096
  bytes/tick`, `goldens native 0`, `gameplay native 0 gameplay: green (0 skips)`, `gameplay release 0 gameplay:
  green (0 skips)`; its check-linux (`quit`, `ctrl-c`, `trap` red on `cub: save_corrupt`) and perf (`perf-idle:
  latency FAILED: the game ended after 0 keys`) met the stale engine fixture (Inputs verified, 10); job21
  (`gates/linux-check2-73ff1187.log`), after `prepare-pty 0` archived it: `check-linux 0 check-linux: green`
  (`check-fmt: canonical`, `wolf test: 562 passed; 0 failed; 0 rejected; 0 unsupported; 0 filtered out`, 507
  goldens `ok`, 87 pty rows `ok` and 0 `FAILED`, `pty: quit ok`, `pty: ctrl-c ok`, `pty: trap ok (… exit 134 …)`),
  `perf slack 1 0` run as `in-container env LAIR_PERF_SLACK=1 .lair/tools/perf` (`perf: host Linux x86_64, slack
  x1`; 80x24 306 / 300 us, 200x60 2223 / 2211 us; `perf-idle: idle 301 voluntary context switches in 10 s at a
  standstill (bar 240..360) ok`; `perf-idle: latency median 23.2 ms p90 33.7 ms max 33.7 ms over 20 keys (bars
  median 40, p90 70 ms) ok`), `CB14_LINUX_CHECK2_DONE 2026-10-29T00:13:08Z fail=0`. Before the rebase onto cb15,
  both were green at `5db48d71`:
- **The Linux gate** (kasumi cores 12–15, the engine's container, `5db48d71`, `gates/linux-gate.log`):
  `check-linux 0 check-linux: green` (`check-fmt: canonical`, `wolf test: 509 passed; 0 failed; 0 rejected; 0
  unsupported; 0 filtered out`, 481 goldens `ok` and 0 `DIFFERS`, 82 pty rows `ok` and 0 `FAILED`, among them
  `pty: cb08-whisper-flank ok (linux x86_64, exit 0, 2185201 bytes captured)`); `check-memory 0 memory gate:
  green, crash checkpoint and fresh seed; budget 4096 bytes/tick`; `goldens native 0 goldens: art ok` (481 `ok`,
  0 `DIFFERS`); `gameplay native 0 gameplay: green (0 skips)`; `gameplay release 0 gameplay: green (0 skips)`;
  `perf slack 1 0 perf-idle: latency median 13.6 ms p90 33.5 ms max 36.1 ms over 20 keys (bars median 40, p90 70
  ms) ok`, run as `in-container env LAIR_PERF_SLACK=1 .lair/tools/perf` (`perf: host Linux x86_64, slack x1`);
  `CB14_LINUX_GATE_DONE 2026-10-28T13:39:33Z`, `CB14_KASUMI_EXIT 0`.
- **The Mac leg** (the-rules.md's loaded-server rule): the first build refused at 7 GB free; at 6d28238f the
  floor cleared (15.8 GB), the native build, the checked tests (482), the walk and the full golden check all green
  under `/Users/mfwolffe/lanes/cb14/heavy.sh` at the first attempt; the build and the checked tests again at
  b48ee261 (`wolf fmt`). At `5db48d71` (`gates/mac-gate.log`): the floor waited 90 s and cleared at 10.8 GB, then
  `build 0`, `walk 0` (the stone mouth at 9369), every entry frame `0`, `test 0` with `wolf test: 509 passed; 0
  failed; 0 rejected; 0 unsupported; 0 filtered out`, `goldens 0` (481 `ok`, 0 `DIFFERS`) at the first of the
  three attempts, `CB14_MAC_GATE_EXIT 0`.

## Done-when

- [x] Five areas on both tiers, each with its palette, terrain, sprites, gates, den (none for the Howe), shortcut,
      lore and mechanic (ash hides the trail and halves the pace; the stones sink; the mist three cells; the spring
      refills; the sett's growth gate; the lookout's reveal); Gravehollow split off the Hush.
- [x] Branches and alcoves in every area from the Teeth on, 2–3 an area, seeded guard, a `kind` slot, visible as
      a gap in the route's wall; forty alcove bits in the save.
- [x] Arenas +50 % (14 / 14 / 18 / 20), the censuses re-run.
- [x] `--world-audit` seeds 0..49 green over 1300 rows; every census extended and compared; the journey-length
      table before/after; replay determinism (the cases replay; the goldens written once).
- [x] The memory gate green (316 bytes a tick against 4096; 482 and 308 over cb15 at `079d3c5a`).
- [x] Goldens of each new area's first screen on both tiers.
- [x] The walk from the Shingle to the Howe's stone mouth on the Mac, its entry frames in the evidence.
- [x] The note (five sections, the ledger line, the hooks), the plant red by name, the evidence directory.
- [x] The rebase onto cb15: CUB 7 and journey 6 over theirs with the trunk writer's migration witnesses, lore
      13..31 through cb15's paths, R-cb14-6 A, the cases and goldens regenerated once with every changed key's
      cause, the plant red again.
- [x] The full gauntlet at `73ff1187`: Linux green (check-linux after `tools/prepare-pty`, check-memory, native
      goldens, gameplay on both backends, perf at slack 1 inside the container); Mac green (build, checked 562,
      walk, the full golden check at the first attempt). At `5db48d71`, before the rebase onto cb15: both green.
