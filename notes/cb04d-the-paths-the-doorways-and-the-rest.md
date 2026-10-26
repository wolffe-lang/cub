# cb04d — the paths, the doorways and the rest

_Materialised from cub#38's PR body at the merge (7e2c6a77); the lane's wrapper could not write Markdown notes._

Wider, smoother paths; doorway shadows that accept body crossings; continuously clipped foes; and a right-side rest ledger with staged, confirmed purchases. Game code, game-owned tests/witness tooling, docs and goldens only: no engine, pin or CI change.

The five-section lane note below is for materialization as `notes/cb04d-the-paths-the-doorways-and-the-rest.md`; this wrapper does not write Markdown report files.

## Prediction

`5d1fea5` committed the prediction before implementation at trunk `5f5b05a111152cf08f75dc0974bb31e266611186`. The doorway diagnosis held: `sim.transitions` tested a one-cell centre radius while the drawing covered7×3 cells. The foe diagnosis was specifically **Bramblehold's centre-to-centre `sim.visible` predicate**, not a camera rounding error. It suppressed a whole sprite as its anchor lost sight. AI perception is unchanged; the renderer now clips each sprite cell.

The path audit sampled50 seeds × fields80/200, per area, over spines, actual cache branches, the shortcut cross-route and the shore. Width is an axis-transverse clear-path run, including intersections and clipped endpoints; the complete distribution is retained, not just these medians. Jaggedness is reversals of nonzero centreline direction within three samples, per ten sampled route cells.

| area | width median before → after | reversals/10 before → after |
|---|---|---|
| Shingle |5 →7|0.512543 →0.089523|
| Bramblehold |7 →9|0.513228 →0.185714|
| Larkmeadow |7 →9|0.851058 →0.132540|
| Teeth |5 →7|1.025664 →0.168142|
| Shallows |7 →9|1.023894 →0.190265|
| Gravehollow |7 →9|1.036283 →0.169912|

The worst generator step was `terrain.meander`'s forced alternating±3..5 anchors every eight cells. They now span sixteen cells with slower noise. Bramblehold's six switchbacks remain; only their apexes round across five rows, with the bend census measured over eight rows either side. Three worst before: Shingle path4 (cache2), seeds46/3/23, reversals per10 **1.590909/1.463415/1.428571**. Three worst after: seed27 path5, seed33 path4, seed25 path5, **0.975610/0.909091/0.909091**. Both-tier120×40 rendered goldens are under `paths-before-frames/` and `paths-after-frames/`.

Doorway census: **806400** shadow/outside-neighbour rows, including diagonal approaches, four body quarters and both cub sizes, with **0 misses**. The baseline's equivalent geometric first-contact census is806400 misses: its centre cannot yet be within the old radius on these first body-contact rows. `doorway-before.py` explicitly reconstructs that translation-invariant predicate; it is not claimed as an old live-loop recording. Independent named checked and live pty rows guard actual transitions.

Foe census: **193200** frames (every route row, both field sizes and tiers), **0 omitted frames** against cell-clipped sprite composition. The old sight predicate on the same camera walk would suppress **39760** foe-frames; that is a predicate comparison, not a claim that all were frame-to-frame flickers. The baseline checked assertion was red before repair.

The existing world gate caught one integration regression: rounding seed43's final Bramblehold switchback brought an ordinary spawn29 cells from den1. `62d09c1` advances only affected final Bramblehold groups along their existing route until both slots retain the30-cell primary-den radius. The named checked witness was red; the600-row world census is green without relaxing any bar.

Goldens: **3171 files**, **220 directories** including score, versus3139/208; twelve new rest-menu directories, none removed. Obsolete timed frame files were removed explicitly when the real-key scripts regenerated. Exact added/removed paths are retained; both hosts hash the3171 path+content records to `f4cd84f71a1da9ec8e841134a121d9c3ac19262bace8426bd00d0f5aa817845f`.

## Forbidden

Original game code, art and text only. No other game's implementation/assets; no engine, pin, workflow, movement, attack, HUD/bar, planning-repo or user-configuration change. No packages, labels, merges, tags, releases or issue actions; no attribution trailers. Plants were the three granted branches and drafts; the coordinator closed them after reading their named CI failures.

Linux gates ran in the existing `localhost/pack-ci:fbee7e864f7dbee6` container under the4–7 flock and taskset, with `CARGO_INCREMENTAL=0`. Mac heavy jobs checked8GiB through `vm_stat` in their scripts, retried after180 seconds if needed, and used lane-owned HOME/TMPDIR. The first Mac play build at62d09c1 completed its full gate; the coordinator explicitly granted a second final build for the arrival-rearm and empty-cost corrections. The second build exposed a shadow→shadow false crossing during onward journeys; the coordinator granted a third final build after the literal translated-cell correction and real-key departure tests. No process group was signalled. Retain the worktree and final play binary until play acceptance.

## Inputs verified

Engine57870143ebbb4806b8bee40379e8c6e781f50842; wolf0.2.35/cf0c13d; lupin0.1.56/294d626; std2386522eb059cca5a84108562c2c0a0e72345d34. Complete host toolchain pairs staged at the pin, with identities/digests read twice in `inputs-twice.txt`. Contract, verbatim playtest notes, RULES1–10, cb04a/cb04c/cb03a/cb04/cb02 notes and the named design/art/key/palette sources read. README refreshed in its own commit.

**R-cb04d-1: recommend+1 cell on each side**, implemented, not independently ruled: symmetric clearance helps the cub's body in either direction; a single total cell biases one side. The sealed five-cell thorn throat remains constrained rather than opening a bypass. Existing den and gate censuses stay green:100 paths and400 gate-face-tier rows. Entrance→den distances132–221→129–194; entrance→exit184–306→182–268; centreline376–424→352–400. Minimum den/exit ratio0.615702→0.617391; den/centreline0.334906→0.355, retaining both one-third bars.

Observation requested by the coordinator: `sim.transitions` and `sim.cross_edge` had progression/shortcut locks, not a separate mid-fight lock; these rules are retained, and no combat lock is added. No additional ruling is requested.

The panel is40×22 at80×24 (left39/top1),50×26 at120×40 (left69/top7); the whole cub and fire remain visible to its left. Gold double frame, near-black field, bone labels, aligned values, green raised stats/effects and red refused totals have ASCII/console equivalents. Up/Down wrap across five stats and Confirm. Right/Left stage/remove levels; Enter or Space on Confirm applies the shared per-level sum. Esc or`r` discards. Keys1–5 no longer purchase. Pending choices are not saved; confirmed stats retain schema4. Empty allocation needs0 scent.

Arrival placement remains two cells inside. The old one-cell centre exclusion rearms before a return step, while translated non-shadow→shadow body cells remain the trigger: stationary arrivals never bounce, and body overlap does not prevent immediate return. The side-entry live pty witness fails on the first build (both tiers) and passes after correction. The test walker avoids unrelated open doorways. For onward travel it uses ordinary arrow/parry keys to turn while stationary, then walks straight clear of the arrival band before planning the route. Player movement is untouched.

## Evidence index

- `5d1fea5`: committed prediction.
- `3591e31`: baseline sight-cull assertion and renderer repair.
- `c7c9469`: wider paths, rounded bends and baseline distributions/goldens.
- `dce315c`, `58592b0`: allocation, body crossings, exhaustive checks and real-key witness integration.
- `62d09c1`: witnessed seed43 quiet-radius regression and repair.
- `e5ee21d`: immediate return rearm and zero empty-pending price.
- `1a15545`: named shadow→shadow arrival-bounce red/green and literal translated-cell entry.
- `5058a1b`: real-key arrival departures and regenerated onward journeys.
- `083bbce`, `389848a`: final regenerated rest and world goldens.

Evidence lives under `notes/cb04d-evidence/`. Full local gates run at **389848a**, whose game/witness code is5058a1b; later changes are docs/evidence only. Both final full gates are **exit0**: Linux2026-10-26T21:52:47Z, Mac21:50:14Z. Each has **283 checked tests**, zero failed/rejected/unsupported/SKIP, both backends and every committed golden, PCM score checks, all **27 pty rows**, both-backend gameplay/persistence/world/body/boss/den gates and slack1 performance green. Mac loudly skips only the Linux `/proc` idle metric (two invocations), not silently zero skips overall. Logs: `linux-final.log`, `mac-final.log`; reproducible host scripts alongside them.

Render means in µs (80×24 rich/plain;200×60 rich/plain): Mac182/174;1306/1296, Linux297/278;2142/2138. Direct latency median/p90: Mac23.1/33.4ms, Linux13.6/13.7ms; Linux idle300 and302 switches/10s. Source-final identities and the arm64 play-binary hash are retained in the evidence.

Plants, fixes/tests committed first:
- cub#35,404b049, run**40398961452**: `test_cb04d_doorway_edge_crosses_and_arrival_does_not_bounce` fails.
- cub#36,4403a96, run**40398968367**: `test_cb04d_foe_inside_view_is_not_culled_by_anchor_sight` fails; the local whole-edge assertion also fails.
- cub#37,157a0e0, run**40398974734**: `test_cb04d_confirm_spends_each_intervening_level_cost` fails.

All local plants are `FAILED(trap(assert))`, not compile rejections or unsupported rows. CI named-reds and closure were reported by the coordinator; the lane did not wait on those runs or close the drafts.

## Done-when

- [x] Every shadow boundary/approach, unlocked shortcuts, unchanged arrival and progression locks; edge and immediate-return pty rows.
- [x] Foe cause identified; per-cell clipping; fifty-seed both-tier camera walk and plant.
- [x] Wider paths, before/after width and curvature censuses; six retained switchbacks; three worst before/after frame pairs.
- [x] Den/gate/world/body/boss gates retained; the30-cell spawn regression repaired rather than weakening its gate.
- [x] Right-side panel, all requested rows, zero empty pending, affordable/refused goldens at both sizes/tiers; multi-level cost, lower, cap, discard and save assertions.
- [x] Real-key scripts, pty rows, three CI plants, docs and README.
- [x] Final full Linux and Mac gates, identical goldens, third/granted final Mac play build.
- [ ] Final PR CI belongs to the coordinator; no label and no CI wait.

Final head **7e2c6a7744697072d92a6fdf41e0216f9806bce9**. Play (schema4; add `--mute` for silence):

```sh
/Users/mfwolffe/lanes/cb04d/cub-play-7e2c6a77 --save /Users/mfwolffe/lanes/cb04d/play.save --ghost-dir /Users/mfwolffe/lanes/cb04d/play-ghosts
```

Mach-O arm64; SHA256 `7747cdd4cbc7cde77241bbd07b5cafa538686f1aa527033e219ccc280ce80382`. Build stamp389848a; final-head differences are docs/evidence only.

Audit run once at final head, direct exit1: **`AUDIT FAIL (footprint: module)`** (`/Users/mfwolffe/lanes/cb04d/logs/audit.log`). Ancestry, footprint/paths, attribution, five sections, cited shas, PR head and orphan checks all pass. Holds are only PR CI in progress/no green tier yet and the intentionally retained play worktree. The immediate one-time CI listing was empty; the required audit identified run **40408399261**, in progress. No CI wait, second listing or label.

Pruned: the three clean local plant worktrees, plus only `/home/mfwolffe/lanes/cb04d/cub/target` and its source compiler cache after the successful Linux gate and retained evidence. Linux logs/source and the Mac play worktree/binary remain. Both final gate processes ended normally.

No new engine requirement or issue to file/close. Materialize this note on trunk after merge.

