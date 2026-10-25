Footprint: module

# Note — cb02b, the grove

A fix-up on the maintainer's play of cb02a (cub#18, `62db9f35`): the forest texture everywhere, a coast a
screen past the view with four branches, solid silhouettes, a cub that is one drawing turned, and a
second area that fills the screen. Before/after frames, logs and the census are under
`notes/cb02b-evidence/`.

## Prediction

`b09441f` committed `notes/cb02b-prediction.txt` and the before-frames before any code change. Both
screenshots reproduced headlessly on cb02a's head (`notes/cb02b-evidence/before-*`; the maintainer's live
save names seed 1, the default; seeds 0–4 captured at 200×60 and 80×24 on both tiers):

- **The flat green fill.** `forest.kind` answered `terrain.DARK` for every cell outside the generated
  rectangle (|x| > 40, local row outside 0..160) and beyond the jetties, and inside wherever the fill
  noise exceeded 130; `SP_DARK` had one variant (U+28FF in colour 22; plain `&`), so a DARK region was one
  glyph in one colour: the full braille cell reads as a solid tile. At 200 columns 119 of 200 columns lay
  outside the rectangle: 76–78 % of the Shingle's forest cells sat in flat runs longer than four cells,
  the longest 62–76 cells. Both jetties (x = ±35..37) were in a view spanning ±100. Measured by
  `flatness.py`; the before table is `flatness-before.txt`.
- **Bramblehold's centred rectangle.** The same bound: textured only within x ∈ [-40, 40] by local row
  0..160; the cub arrives at local row 3, so the 28 rows above and every column beyond ±40 were DARK, and
  the thicket's recolour painted every non-trunk cell one green. The cross path (rows 18..27) had no x
  bound and ran across the rectangle to the DARK wall at ±40. Larkmeadow's gold recolour gave 89.7 % flat.
- Predicted all 91 golden directories move: all 91 moved and four were added (`coast-cache-2/3`, both
  tiers): 95. Predicted about six new directories: four. Predicted 25–40 new code points in GLYPHS.md:
  152 in all (142 braille, six block elements), because every silhouette cell of every facing is listed.
- Predicted the rotated silhouette would read at a 1:2 cell: it does, at eight pixels across; the first
  cut at four pixels (2×3 cells) read as a blob on the sheet, so the cub is 8×16 pixels (4×4 cells north,
  8×2 east), a miss on the footprint, not on the method.
- Predicted the useful walk near 150 at 200 columns: measured 199 with the thorn route and the caches
  alone as targets, 130 once the branches' centrelines count (they are useful routes), 119 at 80 columns;
  WALK_MAX stays 200. Textured share 100 % against the 90 % bar; longest identical foliage run 1 against
  FLAT_MAX 2 (by construction: the variant alternates its glyph set by cell parity). The 300-row audit
  (50 seeds × two fields × three areas) runs in 23 s natively.
- Render cost: 200×60 rich 1137 µs (cb02a 455), 80×24 rich 167 µs (98), inside the slack-1 bars (4000 /
  1000 µs): the coast's per-cell route-distance test is the cost; a follow-on may cache it per column.

## Forbidden

Original work only: the shapes are cub's own; pack's wolf (ears, head, a long body) and its path model
were read for their shape, never copied. No `lair` change, no pin change, no workflow, planning-repo or
`~/.claude` edit; the engine's glyph tiers were enough (the rich tier draws block elements and braille).
No merge, label, tag, release or issue action; the three plants are draft PRs the orchestrator closes.
No attribution trailers. Every heavy launch on nomad ran through `heavy.sh` (retained), whose own
`vm_stat` read enforces the 8 GB floor with three-minute retries; no refusal occurred; scratch stayed
under `/Users/mfwolffe/lanes/cb02b/`; every child was exec'd or waited for; no package installed; the
maintainer's server and the other lanes' directories untouched. The Linux leg (head `8ec5960`, pre-rebase, the same tree) ran in the staged container
on kasumi cores 4–7 under `/home/mfwolffe/lanes/kasumi-cores-4-7.lock` (`ssh kasumi bash -s`, `setsid
-f`, a pid file; nothing killed). Signal witnesses are the engine's pty rows typing byte 03.

## Inputs verified

- Base `62db9f35` (cb02a's head; trunk since cb02a's merge is that plus the note commit `4d1bc55`, which
  this branch rebases onto at its final head). Engine `aa6c4dc0bc5071d3c07121451d913a8837cd2a6a`,
  unchanged; wolf 0.2.35, lupin 0.1.56, std `2386522e` staged by the fetchers on both hosts.
- cub#18's body, `notes/cb02-the-world.md`, `notes/cb01b-the-feel.md`, `docs/`, the engine's docs, the
  design bible §§2/8/19, the campaign, `sprints/RULES.md` §1–§10 and the guide read; pack's
  `docs/ART.md` and `tier.lu` read for the wolf's shape.
- Rulings recommended and implemented, not decided: **R-cb02b-1 A** (the coast one screen past the view's
  edge, floor 120: `coast_extent = max(120, 3·field/2)`); **R-cb02b-2 A** (one silhouette, east/west the
  north drawing turned a quarter, pixel for pixel); **R-cb02b-3 A** (four branches, two each side, the
  seed jittering the mouths); **R-cb02b-4 A** (the field is a journey property: the terminal's columns at
  the start, floor 80, saved as schema 2 and carried as the 25th replay value, never moved by a resize or
  a resume; B, recomputing from the current terminal, would invalidate a saved mark in a narrower one);
  **R-cb02b-5 A** (the two new alcoves hold bundles; no new consumable; the second cache keeps its marrow);
  **R-cb02b-6 A** (inland half width `field/2 + 8`: 48 at 80 columns, 108 at 200); **R-cb02b-7 A** (the
  deep wood keeps the canopy's four glyphs in the deep green alone, the open canopy two tones).
- Every number is a dated proposal in `docs/DESIGN.md` ("The grove").

## Evidence index

Commits, each its own chunk:
- `aa7323d` the fill fix (textured deep forest, parity variants, dusk tones); `a09aa79` the field carried
  and every area sized by it (schema 2); `ca57623` the jetties a screen past the view and the flotsam
  along the shore; `bd6bae7` four coast branches and the cache bits relaid; `912d53f` the coast's open
  canopy within reach of a route; `1e45c8d` the thicket and meadow filled to the field, the cross path
  ending at its portals.
- `91005db` the `silhouette` module; `1e32a5d` the cub, foes, hawk and bundle drawn from it; `5b5ce25`
  the sprite tests; `4a2afd5` GLYPHS.md regenerated (152 code points).
- `8698b5f` tests: `src/grove_test.lu` (texture, the coast's reach, four branches, the saved field,
  bounded inland paths, the turned cub); `2de3a4b`, `9c4e30e` the witness walker (routes from the river,
  round bodies, fights in sight, hunts the guards); `2840a3c` the real-key scripts regenerated (all four
  coast bundles opened, ticks 5664–9914); `c9c7499` goldens; `1160458`, `7183d33` docs and README.

| gate | macOS arm64 (nomad) | Linux x86-64 (kasumi, container, cores 4–7) |
|---|---|---|
| fmt / checked tests | 150 pass, 0 failed/rejected/unsupported, 0 SKIP | 150 pass, 0 failed/rejected/unsupported, 0 SKIP |
| native + release, selftest, goldens | 46 scripts × both tiers + art, 95 directories | byte-identical (every directory ok) |
| pty rows | all 12 pass | all 12 pass |
| gameplay / saves / finite caches / archives | both backends green, 0 skips | both backends green, 0 skips |
| world audit | 300 rows: reached = required, flat run 1, textured 100 %, walk ≤ 130, nearest foe ≥ 34 | the same 300 rows, native and release identical |
| 80×24 rich/plain average | 167 / 155 µs | 294 / 274 µs |
| 200×60 rich/plain average | 1137 / 1123 µs | 2060 / 1931 µs |
| latency median / p90 | 10.3 / 33.4 ms; repeat 21.5 / 33.3 | 13.6 / 33.7 ms; repeat 23.3 / 33.7 |
| idle / 10 s | loud Linux-only skip | 300 switches; repeat 301 |

The complete local gate (`tools/check`) and kasumi's `check-linux` + `check-perf` ran at the pre-rebase head `8ec5960ce06288375501d620911da1e639e72764` (`macos-check.log`, `linux-check.log`), whose tree is `7183d33`'s less `notes/cb02a-the-coast.md`; the rebase onto trunk (`4d1bc55`, that note alone) changed no source, fixture or golden. All 1,686 golden
files, relative paths included, hash to `29017328e46924f1b8a45257f3fc7a9e491905cb971fb6627f8a5caeb14162d3`
on macOS (`golden-hash.py`, `golden-directories.txt`); the same 1,686 files hash identically on kasumi (`linux-check.log`, `linux-world-audit.txt`).

After-frames: `notes/cb02b-evidence/after-{shingle-0..4,bramblehold-t1210,bramblehold-t1251,larkmeadow-t2302}-{200x60,80x24}-{rich,plain}/`;
`flatness-after.txt`: flat share 1–5 % everywhere (the Python proxy counts the meadow's grass glyph, so
Larkmeadow's rich frames read 13–15 % there; the game's census, which counts foliage kinds, measures 0).
The release census is `macos-world-audit.txt`.

Plants, draft PRs left open, each red by name locally (`plant-*-local.log`) and in its own run (the
run ids read once, in progress at the read):
- **#19** `cb02b-plant-fill` `eaec415ac5c012e31e66d5adc58e284da0965777`, run **40239940063**:
  `test_cb02b_forest_texture_everywhere ... FAILED` (the deep forest one glyph again).
- **#20** `cb02b-plant-branch` `3e3c507bc1640071714160080554d34206fb161d`, run **40239972706**:
  `test_cb02b_four_branches_leave_the_coast ... FAILED` (with `test_cb02a_each_branch_ends_in_an_alcove`,
  the seam test and the spawn test).
- **#21** `cb02b-plant-cub` `0a434eb8c96b76d33df01e2896d98c50fda5f233`, run **40240008747**:
  `test_cb02b_cub_east_is_the_north_cub_turned ... FAILED` (with the sideways, sprites and glyphs tests).

## Done-when

- [x] The forest texture everywhere, both tiers, every area, to the field's edge; the census over 50
      seeds × both fields × every area (flat run 1, textured 100 %).
- [x] The coast one screen past the view each way; the jetties never both in view; four winding branches,
      two each side, each ending in a guarded bundle alcove; every alcove reached by the flood.
- [x] Bramblehold and Larkmeadow fill the field; the cross path ends at the log and the hedge.
- [x] Solid silhouettes for the cub, every foe, the hawk and the bundle; the cub one drawing in four
      facings; plain ASCII counterparts of the same footprints; hit envelopes unchanged (combat tests).
- [x] Tests, 95 goldens, 12 pty rows, real-key witnesses over all four bundles; three plants open.
- [x] `docs/ART.md`, `DESIGN.md`, `PALETTE.md`, `GLYPHS.md` and the README current.
- [ ] The orchestrator watches `tier pr` at the final head and closes the plants.

Play binary: `/Users/mfwolffe/lanes/cb02b/cub/target/cub`. Isolated play:
`target/cub --save /Users/mfwolffe/lanes/cb02b/play.save --ghost-dir /Users/mfwolffe/lanes/cb02b/play-ghosts`
(add `--seed 1` only for a new journey). Keep this worktree until play is accepted.

Prune after merge/play: `/Users/mfwolffe/lanes/cb02b/` (the worktree, `tmp/`, `logs/`, `plants/`, the
bundle) and `/home/mfwolffe/lanes/cb02b/` on kasumi. No other worktrees were created; every gate process
has exited.
