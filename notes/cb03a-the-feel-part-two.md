# cb03a — the feel, part two (cub#32, merged at ee1277da)

Materialised on trunk from the PR body by the orchestrator at the merge (a Codex lane writes no note file).

Footprint: module

Discoverable dens, Bramblehold switchbacks and clearings, meadow landmarks, catchable ground foes, directional combos, a stamina sprint, and always-visible outlined bars. Follows #30; rebased over landed trunk `0982079`, including its archive-readability fix. No engine/pin/workflow change.

The five-section lane note below is for materialization as `notes/cb03a-the-feel-part-two.md`; this wrapper does not write Markdown report files.

- `ab33b66`: persistent warm refuges and the den census.
- `dc966d8`: seeded switchbacks and six clearings.
- `2558a63`, `314c414`: meadow landmarks, connected hawk tells, bounded retreats.
- `6388763`, `76f85f0`: directional combat, stamina sprint, outlined bars.
- `6796126`: cb04 schema-3/HUD integration.
- `582a6bb`: safe arena approaches and all 24 forward-contact combo hits.
- `5e5631d`, `e732890`: regenerated real-key scripts, embedded demo and all frame goldens.
- `a32a86f`: README-only refresh.
- `ee1277d`: independently witnessed landing-body head-snap collision fix.

## Prediction

`f56f86b` committed the prediction before implementation; the original text remains at `notes/cb03a-evidence/prediction.txt`.

Before, the existing three areas had 1/2/1 dens. After, the fifty-seed census has **1/3/4** (Shingle/Bramblehold/Larkmeadow); the first meadow hawk pair and branch trio share their downstream refuge. Pairwise Manhattan spacing after the path change is n/a for the single coast den, **45–114** cells in Bramblehold and **22–149** in Larkmeadow. Each new refuge is on the route after its hard cluster; hard means a spawn group of at least three or a pair containing a hawk. Every id rests, heals and round-trips through the save.

Bramblehold has **six** measured turns of at least90 degrees and **six** clearings, not the predicted four/five; centreline cardinal length is **376–424** cells, above the predicted200–280. Rooms are7/9/11 cells across: entry den, shortcut view, cache branch, post-cluster den, briar den, foe cluster. Its original shortcut and boar arena remain reachable.

The suspected “boomerang” is the hawk's one-row diamond shadow and detached plain-tier tell, not a projectile (there is no thrown projectile in this code). The drawing now has a connected beak, wings, body and tail. This is an implementation diagnosis, not proof of what a player perceived.

The isolated chase uses ordinary directions/c/Space after a disclosed setup: default cub stats, one ground foe with100 health so the first hit can be observed without deleting its body. All **150** rows (50 seeds × weasel/fox/deer) catch in **16 ticks**, **775 FP =3.02734375 cells** of Manhattan travel, with overlap/unreachable-contact/foe-overlap **0/0/0**. The initial c dodge is part of that chase. Hawks retain their aerial parry answer, not a ground pursuit.

Sprint is **120 FP/tick (14.0625 cells/s)** at paw1 versus foe retreat86; it costs **12 stamina/second**, plus the first c press's ordinary18-stamina dodge. Sprint Space costs **36** (lunge30), reach4, twice bite damage,3/3/10 ticks; head snaps left/right/left. The first two combo cones rotate−11/+11 heading units (15.47 degrees); the third is exactly forward. All24 dead-ahead-contact combinations (8 aims ×3 hits) land through sim.step. The body retains its committed aim's quarter; only the cone/head slants.

Goldens: all **145 existing non-score directories** moved; **18** added, yielding **163 frame/art directories plus the unchanged score directory**. Added pairs: den-after-cluster, den-bars-80x24, den-bars-120x40, forward-windup, meadow-landmarks, meadow-ford, sprint-80x24, sprint-120x40, sprint-hit. None removed. Exact names: `notes/cb03a-evidence/golden-directories.txt`.

## Forbidden

Original game code and sprites only; pack read for the aim-window shape, never copied. No engine, pin, workflow, planning or user-configuration edit; no package, label, merge, tag, release or issue action; no attribution trailers. Signal witnesses are the unchanged pty byte03 rows. Linux jobs use the staged container,12GB cap, cores4–7 and `/home/mfwolffe/lanes/kasumi-cores-4-7.lock`. Mac heavy work uses `/Users/mfwolffe/lanes/cb03a/heavy.sh`, its own8GB vm_stat gate,180-second retries, isolated HOME/TMPDIR and exec/wait ownership; the MLX server is untouched.

Disclosed deviations: an initial bundle briefly used `/home/mfwolffe/lanes/cb03a-source.bundle` before being moved inside the lane; an accidental rsync destination `/home/` was refused and never retried. Work resumed with exact lane destinations. A transferred `src/.lu-cache` contained Linux ELF objects: the first Mac native link failed before producing a binary; that lane-local cache was removed. One successful Mac play build exists at9d969ac, but final review found the landing-body snap guard bug; the corrected final-head rebuild has now succeeded. That additional build is a disclosed deviation from the one-build plan, necessary to remove the witnessed overlap bug.

## Inputs verified

Rebased over cb04's six-area/boss/ghost/title/end implementation at1855009b. **Save schema3 stays**, including its boss/end/time/lost fields; schema2 is refused by name. Den ids0–6 are valid,7 reserved,8–11 these refuges,12–15 reserved. The16-bit lit mask rejects unimplemented ids. The boss bar remains row1 at column43+, clear of player bars/scent. The final source retains cb04's boss mechanics, alpha reactions, shallows slowdown and body push rules.

Pinned engine57870143; wolf0.2.35, lupin0.1.56, std2386522e. Complete archive pairs staged and fetcher-verified on both hosts. Contract, predecessors, campaign, RULES and guide read; cb04's note/changes read at the rebase.

Recommendations implemented, not decided: R-cb03a-1 A hold c (tap dodges; repeat inference means two taps within one second also count as a hold); R-cb03a-2 A top-left bars; R-cb03a-3 A approximately15-degree slants; **R-cb03a-4 A** an outside-to-outside scripted walk plans outside an unbeaten boss arena rather than taking a body-avoidance detour through it.

The seven additional meadow things and rules: standing stones (solid), bones (quiet deer forage), burnt stumps (solid), crows (lift within5 cells and warn hunters within12), cairns (seeded off-route markers), scent grass (trail lifetime +150 ticks), creek (water off the path, guaranteed carved ford). Single trees and three-root copses are three cells tall. All are original drawings in ART and the meadow atlas/scene goldens. They add no respawning currency.

## Evidence index

Tracked evidence is under `notes/cb03a-evidence/`; full host logs remain under `/home/mfwolffe/lanes/cb03a/` and `/Users/mfwolffe/lanes/cb03a/logs/`.

- Checked suite: **232 green on Linux** after the final landing-ring fix (`head-ring-green.log`),0 SKIP. The added witness was red on Mac (`head-ring-red.log`) before the fix;231 other tests stayed green. Prior full Mac suite:231 green at9d969ac.
- Before that narrow final fix, both hosts/backends passed every frame golden, score PCM, selftest, gameplay/persistence, body audit, boss fairness and all **20 pty rows**. Linux full log: `linux-gate.log`; Mac component logs: `macos-{tests,build-clean,release-goldens,native-goldens,score,pty,gameplay-native,gameplay-release,perf,idle-direct}.log`.
- Final corrected Linux full rerun: `/home/mfwolffe/lanes/cb03a/landing-gate.log`, exit marker `landing-gate.exit` **0**: complete corrected Linux gauntlet green,232 checked tests,0 SKIP, both backends, all goldens/pty/gameplay/world/boss gates. Corrected release goldens already match every pinned byte (`landing-goldens.log`).
- Corrected Mac gate is **green at the final head**, exit0: pid/log/marker `/Users/mfwolffe/lanes/cb03a/mac-final.pid`, `logs/mac-final.log`, `mac-final.exit`; it is pinned to70c2c90 and waits for the already-running formatter/regression job, then runs every component. The predecessor cleared after seven180-second waits:232 Mac checked tests pass. At the final head the rebuild, selftest, both-backend goldens, score, all20 pty rows, native/release gameplay, world/body/boss gates and final slack1 performance/direct idle checks are green. `mac-final.exit` is0; final latency median32.2ms,p90 33.5ms. The Linux-only idle counter remains a loud Mac skip.
- Body census before the narrow final guard correction:81 scripts,**59,632 ticks**,0/0/0; the100-world body audit **328,240 ticks**,0/0/0. The landing-ring test specifically covers a neighbour beside the presented apex that the broad censuses had missed.
- Approach versus cone were separated: boar seed7's shortest walk entered the arena before its mouth and died (boar7-before.log); a west approach strip fixes that route. The inherited lynx18/200 fairness row had zero fight ticks because its approach had already killed the boss; the safe planner removes that detour. An ordinary blocker exposed the quarter-cell arrow threshold (bearing128 versus aim96); after the24 contact hits passed, the walker gained Tab/Space/Esc to latch aim then release movement. **400/400 den→mouth walks pass**, with all destinations outside arenas (`mouth-census.txt`).
- Final boss census (`boss-census.txt`): boar94 first-life/6 second-life; lynx/elk/alpha100 first-life each; unwon0, arena breaches0; shortest tells12/10/16/9. The five-life and parry bars were not changed.
- Performance at slack1 before the final guard-only correction: Mac80x24 rich/plain174/167us,200x60 1207/1183us; Linux305/290us and2022/2010us. Linux301 idle switches/10s; Mac loudly skips that Linux-only metric. Latency gates pass; direct idle-runner statuses were also read, not hidden behind tee.
- Three contract plants, local Linux container, each restored: `plant-den.log` → `test_cb03a_fifty_seed_den_census_rejects_an_empty_area ... FAILED`; `plant-combo.log` → `test_cb03a_combo_cones_slant_left_right_forward ... FAILED`; `plant-sprint.log` → `test_cb03a_sprint_charges_twelve_per_second_and_stops_empty ... FAILED`. These ran before the cb04 rebase; their fixing code/tests remain. No plant PR/dispatch.

## Done-when

- [x] Existing-area dens discoverable and persistent;50-seed counts/spacing and hard-cluster checks.
- [x] Six switchbacks, six purposeful clearings; texture/shortcut/world gates.
- [x] Original ominous trees and seven additional meadow forms/rules.
- [x] Bounded flee, connected foe tells,150 chase rows, stamina sprint and snapping attack.
- [x] Three slanted combo hits, eight-direction aims, forward x with two-step windup;24 contact hits.
- [x] Outlined green/red bars at both sizes/tiers; posture retained; --hud retired; den card clear of bars.
- [x] Real-key scripts and pty rows; all frame goldens regenerated/named; three local plants; docs and README refreshed.
- [x] Final corrected Linux full gauntlet, exit0 (`landing-gate.log`).
- [x] Final-head Mac build,232 checked tests, selftest, both-backend goldens, PCM,20 pty rows and native gameplay.
- [x] Final-head Mac release gameplay/performance; durable job74622 completed, mac-final.exit0.
- [ ] PR-tier CI watched by the coordinator; no label.

Final-head play binary (SHA256 `6bad4ff3c506a90b3e59855ef363977782d4fd40a4c35db891cd94a7754972d9`; complete final-head Mac gate green): `/Users/mfwolffe/lanes/cb03a/cub/target/cub --save /Users/mfwolffe/lanes/cb03a/play.save --ghost-dir /Users/mfwolffe/lanes/cb03a/play-ghosts` (schema3; add --mute for silence). `target/cb03a-build-head.txt` identifies70c2c90; `mac-final.exit`, not that build stamp, is the full-gate completion marker. No new engine need found; retain the existing keyboard key-up limitation. Prune after merge/play: only `/Users/mfwolffe/lanes/cb03a/` and `/home/mfwolffe/lanes/cb03a/`; all lane gate jobs have ended; retain the worktree and play binary until play is accepted.

Audit before the tools-only follow-up: direct exit1, `/Users/mfwolffe/lanes/cb03a/logs/audit.log`; last line `AUDIT FAIL (footprint: module)`. All ancestry/footprint/sections/sha/attribution checks passed. Holds: CI in progress and the intentionally retained play worktree. The one immediate CI listing returned `[]`; the required audit then identified run **40270685600** in progress. That run later failed artifact upload on owner-only ghost scratch directories; landed trunk0982079 fixes their permissions/cleanup and checks every gameplay path. No CI wait or label.



### Tools-only readability follow-up

Rebased onto trunk0982079 at head `ee1277da84ca99f3994f14ef88704cdef0376b9f`. The exact diff from70c2c90 is31 lines in tools/gameplay.py only: readable scratch directories, finally cleanup, and the recursive readability assertion. Game code and every golden are unchanged, so the completed Mac proof and binary at70c2c90 stand. The fresh complete Linux gauntlet is green under the same4–7 lock, exit0,232 checked tests and0 SKIP. Both native and release gameplay gates print `gameplay: every path under /work/target/gameplay readable`. Evidence: /home/mfwolffe/lanes/cb03a/readability-gate.log and readability-gate.exit; local copy /Users/mfwolffe/lanes/cb03a/logs/readability-gate.log. No label; Footprint remains module.

Readability follow-up audit at ee1277d: direct exit1, last line `AUDIT FAIL (footprint: module)` (/Users/mfwolffe/lanes/cb03a/logs/readability-audit.log). Footprint module and all path/ancestry/section/sha checks pass. Holds are the new CI run still in progress and the retained play worktree. Immediate one-time run listing returned `[]`; audit identified **40324829083**. No CI wait, extra label or second audit.

