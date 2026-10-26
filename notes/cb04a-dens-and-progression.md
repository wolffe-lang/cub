# cb04a — dens and progression

_Materialised from cub#34's PR body at the merge (d822a239); the lane's wrapper could not write Markdown notes._

Enterable regional dens, shared levels, found healing and persistent thorn boundaries. Rebased onto cb04c plus its note at bdccb95. No engine, pin or workflow change.

The five-section note below is for materialization as `notes/cb04a-dens-and-progression.md`; this wrapper does not write Markdown report files. Final full-host gates are still running and are handed to the coordinator by request, not claimed green.

- `3bb929d`: prediction before implementation.
- `6c1e13a`, `26f2dd4`: downstream den placement and reachable, paused rest interaction.
- `b5fdc91`, `8cae901`: original regional rest art, shared cubic-priced levels and schema4.
- `c39d056`, `8437100`, `0020b4e`: checkpoint witness, found water/meat, persistent thorn boundary.
- `e2117df`: cb04c sprite/radius/burst integration, nose visibility and HUD-clear ordering.
- `fa2f324`, `d822a23`: regenerated goldens and removal of superseded frame ticks.

## Prediction

The committed prediction is `notes/cb04a-evidence/prediction.txt`. Bramblehold den1 moved from rows7–10 to114–117 on a switchback. The independent tile flood over50 seeds at fields80/200 measures entrance-to-den132–221 cells, entrance-to-exit184–306, centreline376–424. The minimum den/exit ratio is0.61570248; minimum den/centreline0.33490566, above one third. All100 paths pass. One thorn gate, two faces and two tiers across those worlds give400 checked face/tier rows.

The important diagnosis differs from a missing-feature hypothesis: growth, drinking and last-den respawn already existed. Rest required the cub centre within one cell despite its larger drawing. The same real arrow/r/Esc pty row fails on unmodified trunk8fed728 (`visible den edge: r never entered the rest scene`) and passes with three-cell entry. Without a successful rest, `last_den` stayed at the start. Death now shares `wake` with resume; the den8→den2 walk/rest/leave/fatal-hit/wake witness returns to den2 at3968,23680, leaving its mark at3967,24865.

Goldens:174 existing directories moved;32 added; none removed; art and score remain unchanged. The new32 are six regions × two sizes × two tiers, plus den-checkpoint, spring-found, spring-drink and water-refill at both tiers. Exact names are in `golden-directories.txt`. There are3139 golden files,208 directories including score. The path-and-content SHA256 is `c9d908efc0a78725c66533563ce4b1532b60fe14cfe84f6a4cb59ded49c491c3`. Twenty obsolete timed frame files were explicitly removed after regeneration.

## Forbidden

Original cub art and code; no other game's implementation, assets, text or music. The published Dark Souls number series is used only as a cost shape. No engine/pin/workflow, planning-repo or user-configuration edits. No label, merge, tag, release or issue action; no attribution trailers. Signal witnesses use the engine pty's bytes. No sibling branch/worktree was modified. Linux builds/gates use the8–11 flock and engine container; Mac jobs use the lane's8GiB vm_stat gate with180-second retries and owned HOME/TMPDIR. The one final Mac play build is in the running gate. No CI wait; the coordinator takes both remaining local gates.

## Inputs verified

Base8fed728, rebased onto `bdccb95d0d27bc70ede70eca9d1b443cf198fd1d` after cb04c merged. Contracts, verbatim playtest, preceding notes, campaign, docs, RULES1–10 and wolf guide read. Pinned lair57870143, wolf0.2.35/cf0c13d, lupin0.1.56/294d626, std2386522e; complete archive pairs fetcher-verified, both-host pins/digests read twice in `inputs-twice.txt`.

Recommendations implemented, not independently ruled: R-cb04a-1 A retains heart/wind/fang/paw/nose, soft cap10 and hard cap40. Through10: heart `40+12h`, wind `60+10w`, fang `6+2f`, paw `round((36+2p)*WALK_PERCENT/100)`, nose `8+2n` scent cells. Above10: heart+3/point, wind+2/point, fang+1/two points, paw+1 unscaled FP/two points, nose+1 cell/two points. Total level is sum(stats)-4.

R-cb04a-2 A: `cost(L)=round(0.05*(0.02L^3+3.06L^2+105.6L-895))`, current L>=12; k=0.05. Costs at current levels1–20 are **24,25,26,27,28,30,32,34,36,38,40,42,52,62,72,83,94,106,118,130**. First purchase is three8-scent weasels. The den shows each stat's current/next effect and the shared cost. Schema4 persists explicit validated total level, stats and water capacity; schema1/2/3 fail `save_version`; replay snapshots are `journey 3`, slots0–29.

R-cb04a-3 A: start0 water; Shingle row24 spring grants2; Larkmeadow row72 upgrades2→3. Rest refills found capacity. `w` spends immediately, prepares15 ticks, heals40 over15 ticks, interrupted by damage without refund. Ordinary kill meat heals10 immediately on collection, clamped; expires300 ticks; gets one visible frame before collection. No boss meat.

Thorn-history evidence is **f50b9c167658a9de7ba82d8cb19e25f7408348f8 (cb02)**: it changed always-drawn closed/open thorns to `if !gate_open`, and moved start+10 to start+157. Neither cb03a nor cb04 deleted the intact gate. R-cb04a-4 A restores persistent torn flanks and an opened five-cell gap on both faces of edge0, with a sealed approach, retaining the existing bit/lunge semantics.

## Evidence index

Tracked evidence: `notes/cb04a-evidence/`. `integration.log` has269 checked tests,0 failures/rejections/unsupported/skips. `combined-gameplay.log` has both-tier native gameplay/persistence/body/boss/label/den/healing gates green on the combined source. `den-census.txt` holds all100 measured paths and400 gate-face-tier checks. `baseline-pty-red.log` and `pty-den-green.log` retain actual live entry/checkpoint results.

The three required local plants ran in the locked Linux container, each restored:
- `plant-den.log`: `test_cb04a_den_enters_at_three_cells_and_pauses_world ... FAILED (trap(assert))`.
- `plant-cost.log`: `test_cb04a_level_cost_matches_the_published_cubic_scaled_by_twenty ... FAILED (trap(assert))`.
- `plant-wake.log`: `test_cb04a_death_wakes_at_rested_den_two_not_the_start ... FAILED (trap(assert))`.

An additional Mac integration plant, `plant-water-hud.log`, puts draw_water before cb04c's clear and fails `test_cb04a_water_survives_the_hud_clear_on_both_tiers`. Restored integration suite:8 green. No plant PRs or CI dispatches.

Final-head gates launched2026-10-26T18:41:16Z at **d822a239ab47c948db66b84c849b2fd3d1c9aca4**:
- Linux pid1069171; `/home/mfwolffe/lanes/cb04a/linux-final.log`; completion `/home/mfwolffe/lanes/cb04a/linux-final.exit`.
- Mac pid39325; `/Users/mfwolffe/lanes/cb04a/logs/mac-final.log`; completion `/Users/mfwolffe/lanes/cb04a/mac-final.exit`.

The Mac gate will produce `/Users/mfwolffe/lanes/cb04a/cub/target/cub --save /Users/mfwolffe/lanes/cb04a/play.save --ghost-dir /Users/mfwolffe/lanes/cb04a/play-ghosts`. `target/cb04a-build-head.txt` stamps the build; only the exit marker proves the full gate completed.

## Done-when

- [x] Downstream den, independently measured50-seed path distance.
- [x] Three-cell hint/entry, r/Esc exit, paused world, actual live-key baseline red/corrected green.
- [x] Original firelit breathing cub, six regional interiors,80×24/120×40 rich/plain goldens.
- [x] Shared levels, next effects, cubic/table, soft caps, validated schema4 and named old-schema refusal.
- [x] Last-rested-den death/mark witness, found water/drink/refill, meat, persistent thorn boundary.
- [x] cb04c integration: draw_meat/draw_spring, shared pickup_near/pickup_flash; nose in/out-of-reach tests. `PICKUP_MARGIN` unchanged.
- [x] Healing HUD `art.draw_water`: row3 col24–48 on both tiers, after the clear. Bars themselves left for cb04b.
- [x] Required plants, regenerated real-key scripts/goldens, docs and README refreshed.
- [ ] Final full Linux and Mac gates: coordinator watches the recorded processes and markers.
- [ ] PR CI: coordinator watches; no label.

No new engine need or issue to file. Planning correction: the thorn-loss commit is cb02's f50b9c16, not cb03a/cb04; respawn already respected last_den, entry was the demonstrated failure. Materialize this note on trunk after merge.

Pruned now: lane-only baseline build/source and20 superseded frame files. After gates finish, merge and play acceptance, prune only `/home/mfwolffe/lanes/cb04a/` and `/Users/mfwolffe/lanes/cb04a/`; retain the Mac worktree/binary until play is accepted. Never prune while either recorded job is alive.

Final audit ran once, exit1: **`AUDIT FAIL (footprint: module)`**.
Ancestry, footprint/paths, head, five sections, cited shas and attribution checks pass. Holds are CI still in progress, the intentionally retained play worktree and the still-running owned Mac gate pid39325 (reported as PPID1/orphan by the audit). The immediate one-time CI listing was empty; the required audit identified run **40380484043** at the final head. Neither job nor CI was waited on after the coordinator's hand-back instruction; the lane's completion monitor was stopped, not the gates.

