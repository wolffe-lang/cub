# cb08 — the diagonals and the hitboxes

_Materialised from the body of cub#61 at the merge (`1d0680a1`)._

cb08 — the diagonals and the hitboxes. Exactly one rebase on each announced merge: cb05 `95a4889d`, cb04b `f6a50a58`, cb07 `c8e5cf15`. Runtime/golden head `920fea19`; harness fix `de1f566d`; committed-archive refresh `f10cae53`. Final head `1d0680a1` adds the R7 CI container cache and timing markers after the complete game gate at `f10cae53`. The game sources/fixtures are unchanged; cache/timing tests and real container integration pass. GitHub run `40568069619` was in progress at the required audit; the coordinator applies the full-matrix label required by the CI footprint. The drawing checkpoint is delivered; visual acceptance remains pending.

## Prediction

`ffc67b6d` recorded the prediction before implementation. `8c483f6e` measured the unchanged strike path before gameplay edits; the cb05 baseline was subsequently rerun on pristine trunk `95a4889d` to include the Ashen.

- Diagonal extent: predicted 16×16 pixels, measured 16×16 (8×4 cells); grown 24×24 (12×6). Held. Cardinal drawings stay unchanged; the diagonal rectangle comes from its own bitmap.
- Inward flank contacts: 508 misses before, 0 after across the four bosses and Ashen at gaps 0–1; 3064/3064 now land. Held. The raw aggregate fraction is not the acceptance metric: it includes away aims, gap 2 beyond bite reach, and additional positions from the wider diagonal body.
- Earlier boss wins: not uniformly. Against the final cb07 baseline `c8e5cf15`, beaten-case frame limits are boar 1488→1134, Whisper 1197→1076, elk 1677→1840, alpha 1225→1083. These include changed approach/contact geometry, tick-dependent AI choices and scripted tactics; they are not an isolated damage-speed experiment. Elk is later, despite the three earlier wins. `replay-outcomes-final.txt` records every case: 46 of 196 inherited cases change key content.
- Gait/clearance: final-chain body audit 91,500 ticks with 0 overlaps,0 unreachable contacts and 0 foe overlaps;302,566 directed single-file edge/chord attempts over 50 seeds at both fields,0 misses. The existing crossing bar stays≥9/10: measured 10/10 at 80 and 10/10 at 200, no lane deaths.

Unpredicted fixes:
1. A real quarter/eighth indexing bug remained in the cardinal head-shake collision check: `%2` became `%4`. The landing-body regression caught it. The final cb07 integration retains the corrected semantics, uses both head-shake axes in the census and rotates bitmap motion by facing/2.
2. Several older damage fixtures began inside the cub and relied on settling, or called an anchor-aligned contact “dead ahead.” They now use explicit non-overlapping jaw/front-ring stands; damage, once-only and HUD assertions were not weakened. The Ashen audit retains all 16 first-bite rows and now additionally asserts exact gap and actual committed eighth instead of allowing centre-lock to silently relabel the aim.
3. The witness walker needed real-key tactics: align its jaws before biting; keep combat sidesteps out of unrelated doors/arenas; clear the physical arrival envelope without discarding its exclusion while escaping the extra planning margin; prioritize the imminent Ashen across both pursuers; cycle Tab to the target actually planned; use the quantized bearing when lock is unavailable. Named arrival, later-ordinal parry and wrong-target regressions cover these. They change the instrument's tactics, not player rules, and never assign the live simulation's position or health.
4. A replan could beat its stop target and then steer at the corpse for 18,000 ticks. The named terminal-target regression was red, then green in `02447702`; the same 400 boss rows still win on their first attempt. Thirty-three duration rows changed; health, hits and every other census field stayed identical. Elk seed 39 fell 18,787→811 ticks, health 74/hit 1 unchanged.
5. Actual shifted/shaken art emitted glyphs absent from the whole-pose inventory. The new render audit was seen red on art and again on full replay frames; six measured code points were declared. It now checks 1,092 fresh art frames plus 2,910 committed replay/art frames against GLYPHS. Ten Python regressions include missing, empty and nested-frame rejection.

6. The first final Linux run passed all 419 checked tests and every pty row except opening-skip-00. Its preserved trace disproves a movement regression: x=0/y=640/speed=0 throughout, scene 1→0 at tick 13. The row injected the key after tick 12 (shot index 0 is not simulation tick 0); the carrying frame took 81.434 ms, but the assertion read after a fixed 50 ms settle. `de1f566d` replaces that guess with a bounded wait for the actual input-bearing transition and one following tick. Every intervening position must remain unchanged; moved, unskipped and absent transitions still fail, as do leaked held movement and natural completion without input. The delayed 81 ms witness was red before the fix; all 16 Python tests now pass. The isolated skip-00 row and complete opening group (completion, all 16 skips, adjacent skip/quit persistence) passed on Linux and Mac. The run at `86c81372` passed all opening rows and reached the stale archive; the complete replacement run at `f10cae53` passed at 18:02:32Z. No game/input/movement code was changed for this harness fault.

7. The next full run reached the committed-archive comparison and rejected the separate death fixture inherited through the rebase. `f10cae53` installs a fresh archive from the merged binary. `ghost-archive-diff.txt` compares all 526 lines: exactly 90 changes, `ghost-face 1`→`ghost-face 10` at ticks 12–101. This is the documented R5 conversion from legacy east quarter 1 to tagged east eighth 8+2. All input keys, timestamps, positions, poses, areas and death tick/count are byte-identical; no HUD or duration change is involved. The old fixture remains `ghost-archive-before-final.pk`; the full red receipt is `full-linux-fixed-ghost-red.log`. Both native/release backends on Linux and Mac now pass the ghost trailer, visible/empty/foreign archive, simulation-independence and plain-mark checks. The remaining gameplay/performance stages passed separately, then the entire gate passed; no game-source change or weakened comparison.

The hit census freezes each target (alpha staggered; guard tested separately), visits every gap 0/1/2 body-ring cell with all eight aims and all four foe quarters, and invokes the shipping damage pass once. It uses combo 3, the unslanted bite, to isolate eight-way geometry. Slanted hits 1/2 and lunge/heavy/dash have separate contact/flank rows; each boss's eight-side first-Space proof runs through the full ordinary-key step path.

INTO means every axis separating the jaws from the nearest foe-cell centre points strictly inward. AWAY means their directional dot product is negative. ALONG is the remaining tangent/mixed set. The Python oracle independently verifies every expected position/aim pair, rejects duplicates/wrong gaps, and requires 100% INTO at gaps 0/1, no AWAY hits and no gap 2 hits. Gap 1 ALONG shrinks intentionally: lateral targets far from the jaws no longer count.

Each entry is landed/total before → after.

| target | gap | INTO | ALONG | AWAY |
|---|---:|---|---|---|
| Boar | 0 | 270/332 → 324/324 | 146/336 → 176/328 | 0/772 → 0/884 |
| Boar | 1 | 310/364 → 356/356 | 170/432 → 64/424 | 0/900 → 0/1012 |
| Boar | 2 | 0/396 → 0/388 | 0/528 → 0/520 | 0/1028 → 0/1140 |
| Whisper | 0 | 244/284 → 276/276 | 138/304 → 152/296 | 2/724 → 0/836 |
| Whisper | 1 | 256/316 → 308/308 | 148/400 → 64/392 | 0/852 → 0/964 |
| Whisper | 2 | 0/348 → 0/340 | 0/496 → 0/488 | 0/980 → 0/1092 |
| Elk | 0 | 310/392 → 384/384 | 146/376 → 200/368 | 0/832 → 0/944 |
| Elk | 1 | 350/424 → 416/416 | 170/472 → 64/464 | 0/960 → 0/1072 |
| Elk | 2 | 0/456 → 0/448 | 0/568 → 0/560 | 0/1088 → 0/1200 |
| Alpha | 0 | 270/332 → 324/324 | 146/336 → 176/328 | 0/772 → 0/884 |
| Alpha | 1 | 310/364 → 356/356 | 170/432 → 64/424 | 0/900 → 0/1012 |
| Alpha | 2 | 0/396 → 0/388 | 0/528 → 0/520 | 0/1028 → 0/1140 |
| Ashen | 0 | 142/152 → 144/144 | 142/216 → 88/208 | 12/592 → 0/704 |
| Ashen | 1 | 174/184 → 176/176 | 182/312 → 64/304 | 4/720 → 0/832 |
| Ashen | 2 | 0/216 → 0/208 | 0/408 → 0/400 | 0/848 → 0/960 |

Raw before/after totals (landed/all pairs): boar 896/5088→920/5376; Whisper 788/4704→800/4992; elk 976/5568→1064/5856; alpha 896/5088→920/5376; Ashen 656/3648→472/3936. Full CSVs and the by-gap tables are under `notes/cb08-evidence/`.

## Forbidden

Original drawings in the existing pixel grammar; no other game's art or code. No engine, engine pin, planning-repo or `~/.claude` edits. R-cb08-7 explicitly authorizes the CI image cache and timing markers; no gate is sampled or removed and the Linux timeout remains 40 minutes. No merge, label, tag, release or issue action; no attribution trailers. No package installation or maintainer process touched.

Linux runs used the assigned first-free 4–7/8–11 locks, never an occupied block or another lane's processes; the logs record the block. Fresh checkouts and copied stages stay under `/home/mfwolffe/lanes/cb08/`. Mac builds/golden/play checks stay under `/Users/mfwolffe/lanes/cb08/`, one build at a time, behind the script's 8-GiB free+inactive+speculative gate. Signals are the engine's isolated pty byte witnesses, not host-process probes.

## Inputs verified

- Base `58969722`; exactly one rebase per announced merge, most recently cb07 `c8e5cf15`. Complete final Linux gate at `f10cae53`: 419 checked tests, 16 Python tests, zero skips, both backend golden/gameplay gates, every pty row and strict performance green. The final runtime gate remains valid for unchanged game sources/fixtures. Later `dea9efa6` and `84e34701` change CI provisioning/timing only; 29 Python tests pass on both hosts, the planner passes, and real Podman export/load/container execution passes. Mac native/release goldens, selftests and diagonal/Whisper live rows passed; later opening and ghost corrections were verified separately on both hosts. Earlier failed attempts remain explicitly labelled receipts, not substitutes for the final full pass.
- Inherited engine `74b89744` from cb04b, with no cb08 pin delta; wolf 0.2.35 (`cf0c13d`), lupin 0.1.56 (`294d626`), std `2386522e`. Complete paired toolchains were staged; the engine tools verified their identities. Release uses the pinned engine's existing `WOLF_MIDEND=0` recipe.
- The contract, verbatim play notes, RULES §1–§10, bible §§1/2/8, DESIGN, ART and the named predecessor records were read. cb04e was never launched; there is no missing cb04e implementation/note to integrate.
- R-cb08-1 A recommended: one NE drawing, the other diagonals quarter-turned. R-cb08-2 A: foes remain four-way. R-cb08-3 A: the cone from the jaws, not a rectangle.
- R-cb08-4 A accepted by the coordinator: preserve anchor-based terrain clearance; use exact diagonal rectangles wherever the game already uses actor/doorway rectangles. Do not widen the world or close its one-cell passages.
- R-cb08-5 A accepted by the coordinator: new `ghost-face` is 8 + eighth (8–15); legacy 0–3 quarters decode to eighths 0/2/4/6. No event or schema renumbering. Legacy-reader and new-trailer round trips pass; REPLAY documents the rule.

Standing, both walk legs, sneak, pant, four hurt bands, breath, five wag offsets and snap have diagonal forms. Their pose rules are shared; ears, paws, shoulders and tail are drawn in the NE bitmap. The other three facings are rotations, never hand redraws. The grown diagonal shares the drawing scaled 3/2. Rest retains its separate side view; plain uses the same occupied cells at its lower resolution. 410 parameter states share 75 distinct drawings, all four rotations on both tiers at 80×24/200×60. The 87-code-point diagonal repertoire is cached for the checked-machine budget and verified against every exhaustive rich sheet; direct enumeration had exhausted that budget. The final declaration has 259 rows; six additional composed glyphs are measured by the new actual-frame gate.

R-cb08-6 recommends A: an unlocked roll faces latched travel; a locked roll tracks the target, quantized to an eighth. cb04b's newer R4 governs this exception to ordinary movement. B (locked body faces travel too) is the one-line `LOCKED_ROLL_FACES_TARGET = false` alternative, not selected. Eight-way regressions for both modes passed. The final strike predicate lives in cb07's strike_reaches and applies jaws_reach_body at both current and commitment endpoints; strike_foes still calls that shared predicate. Motion/HUD behavior is retained.

R-cb08-7 A (confirmed): cache the pinned Linux image through actions/cache, keyed by Containerfile hash plus runner OS/architecture, with no fallback cache key, no registry publication and no engine change. The Linux correctness and performance jobs share that key. Restore/load verifies the expected engine image tag; a miss builds the unchanged recipe and saves its archive atomically. Cache upload runs immediately after successful provisioning, BEFORE tests, so a later test timeout can still leave a usable cache. Failed builds/loads/saves fail closed. Provision/test and wrapper-stage START/END markers include UTC, duration and status; gameplay output is unbuffered. All full censuses, all 4,002 frame checks and all 419 checked tests remain in the PR tier. The correctness/performance budgets remain 40/20 minutes.

Cold-case limit: the canceled run already consumed 40m09s before score completion. Adding cb07's measured remaining gameplay tail (11m38.7s) projects 51m48s, about 11m48s beyond the 40-minute correctness budget, excluding setup/new cache-transfer overhead; the new tail is not measured on that canceled runner. Thus the observed stalled cold build DOES NOT fit. Normal cb07 provisioning was 25.790s, not 21m20.754s. A recipe change, cache miss/eviction or inaccessible branch scope can pay the cold cost again. If provisioning completes, the pre-test save preserves that fill even when tests time out; if provisioning itself times out, there is no completed archive to save. The coordinator watches the first fill and rules on any cold overrun; this patch does not silently raise timeouts. The performance job also remains exposed to its unchanged 20-minute budget on a cold miss.

Named half-cell case: `test_cb08_half_cell_right_of_south_needs_the_cardinal_aim` puts the Ashen 149 FP (0.582 cell) right and 4 cells south, touching the body. Wrong aim 96/cone 85 misses under BOTH old centre and new body predicates; aim 128 lands under BOTH. Thus quantizing the walker's aim alone fixes this specific stall. The real Whisper flank proof still requires body intersection; neither answer makes the other globally unnecessary.

## Evidence index

Implementation chunks:
- `ead6c882`, `9dc9cfb7`, `b0b1bcde`: original diagonal drawing, eight-way body and rendering/live input.
- `6fc6bd37`, `1a026238`: tagged ghost eighths and legacy-reader compatibility.
- `43ab5336`, `af9c3eb5`: jaw/body intersections, charge-edge proof, fixture/parity repairs.
- `e5a162d0`, `33eedc98`: exhaustive pose/glyph validation and golden sheets.
- `1b835582`, `6cd214a3`: narrow-lane and complete independent hit-ring gates.
- `6519bc61`, `12b57a50`, `02447702`: real-key stance/target/route tactics and terminal-target regression.
- `4475f98c`: ONE 16-row exact-gap/actual-aim Ashen first-bite audit, preserving cb04b's toward-arrow correction.
- `96bd4526`, `96a8e976`: isolated pty saves, keyed boss circles and recorded Whisper proof.
- `63438f63`, `ceb6375b`: locked/unlocked roll facings and named half-cell aim distinction.
- `480cd277`, `5d1053df`: cb07 shaken rendering and shared reach endpoints; wait for actual recovery before HUD pickup fixture relocation.
- `b8a58f55`: final-chain journeys, bosses, den/ghost replays, latest real-key flank and both-tier goldens.
- `920fea19`: actual-frame font repertoire gate, its red/green evidence and six measured composed glyphs.
- `de1f566d`: observe the input-bearing opening skip and following tick, with six synchronization regressions.
- `f10cae53`: regenerate the separate death archive; preserve and classify its exact tag-only delta.
- `dea9efa6`, `84e34701`: exact-recipe container cache for Linux correctness/performance, saved before tests, plus stage timing and rejection controls.
- `1d0680a1`: runner-budget attribution and cache integration receipts.
- `223a874b`: README-only refresh. ART, DESIGN, REPLAY and GLYPHS updated; KEYS unchanged.

The real Whisper proof is `tests/cases/whisper-flank.pk`: the existing boss journey's ordinary keys through 755, release modifiers/arrows, then down/left/Space at 756 with no additional movement. Aim 160, slanted cone 149. At 760 Whisper loses 24 health (116→92) while BOTH current-centre and commitment-centre cones miss, minimum integer margin 42,622. No position, health or AI fixture was added. The Linux pty row reproduces the current case in rich/plain and compares terminal capture with headless playback; final Mac native/release goldens and both pty rows also passed. The bounded search tried 3 real-key candidates and is retained with its recipe.

| gate | evidence / result |
|---|---|
| complete final Linux gate | `full-linux-archive.log`: exact `f10cae53`, cores 4–7, 17:34:33Z–18:02:32Z; all stages green, EXIT 0 |
| Linux render, 80×24 rich/plain; 200×60 rich/plain | `perf-final.txt`: 302/284 µs; 2112/2072 µs, slack 1, against 1000/4000 µs bars |
| Linux latency and idle | final direct check: median 23.1 ms, p90 34.1 ms, max 34.9 ms; idle 301 voluntary switches/10 s; all strict bars pass |
| earlier final attempts | `full-linux-final.log`: opening synchronization red; `full-linux-fixed-ghost-red.log`: stale tagged-archive fixture red; both causes fixed and full gate repeated |
| final Mac at `920fea19` | `mac-final.log`: both backend goldens, both live rows, selftests green; EXIT 0 at 16:33:03Z |
| latest Linux Whisper and diagonal pty | `cb07-final-witnesses.log`: both rows green, exit 0 |
| ghost archive, both hosts/backends | `ghost-final-mac.log` and `ghost-final.log`: both backends/tiers green; remaining Linux gameplay/performance EXIT 0 at 17:34:27Z |
| opening fix, both hosts | `opening-fixed-linux.log` EXIT 0 at 16:57:30Z; `opening-fixed-mac.log` EXIT 0 at 16:58:20Z; isolated row plus all 18 opening rows |
| final checked tier | 419 passed, 0 failed/rejected/unsupported, 0 SKIP in the complete final run |
| actual rendered repertoire | `glyph-final.log`:1,092 fresh art+2,910 committed frames,227 nonbyte glyphs,0 unlisted;10 Python tests |
| body audit | `body-audit-final.txt`:91,500 ticks,0 overlaps/unreachable/foe overlaps |
| boss fairness | `boss-census-final.txt`:400/400 first-attempt wins; all parry windows≥9;0 arena breaches |
| complete ring oracle | retained before/after CSVs and independent by-gap tables:3064/3064 inward at gap 0/1;0 away/gap 2 hits |
| narrow geometry | `narrow-final.txt`:302,566 attempts,0 misses |
| crossing | `crossing-final.txt`:10/10 at both fields;≥9/10 bar unchanged |
| replay regeneration | `replay-outcomes-final.txt`:46/196 inherited cases change; new flank case is separate; all final art/world/case goldens regenerated |
| strike/HUD regression audits | final-chain preflight:656 strike rows,0 broken;192 HUD rows,0 stray |


Runner-budget attribution (2026-10-27 UTC; durations use the full timestamp precision). Sources: cb07 run40521782832/job122250809829 and cb08 run40557106593/job122376657813, extracted reproducibly in `ci-stage-timing.txt` and `ci-budget-excerpts.log`.

| stage | cb07 UTC bounds; seconds | cb08 UTC bounds; seconds | added seconds |
|---|---|---|---:|
| provision image | 14:31:18–14:31:44;25.790 | 18:14:59–18:36:20;1280.754 |1254.963|
| Python fixtures + fmt |14:31:44–14:31:45;0.635|18:36:20–18:36:21;0.946|0.311|
| checked tier |14:31:45–14:35:39;233.752|18:36:21–18:42:56;395.058|161.306|
| native build |14:35:39–14:35:44;5.263|18:42:56–18:43:04;7.981|2.718|
| release build |14:35:44–14:36:04;20.482|18:43:04–18:43:34;30.189|9.707|
| release selftest + goldens |14:36:04–14:36:09;4.872|18:43:34–18:43:42;8.069|3.197|
| pty rows |14:36:09–14:45:56;586.658|18:43:42–18:54:35;652.335|65.678|
| native goldens |14:45:56–14:46:11;15.087|18:54:35–18:55:02;27.609|12.521|
| score check |14:46:11–14:46:16;4.707|18:55:02–18:55:09;6.354|1.647|
| native gameplay |14:46:16–14:54:38;502.295|not completed|—|
| release gameplay |14:54:38–14:57:54;196.427|not reached|—|

The pre-score delta is25m12.049s;20m54.963s is provisioning. The apt layer alone is1270.0s versus22.2s; libllvm18 spends406.9s between download messages, libclang-cpp18 another210.4s. Contrary to the initial suspicion, every pty row already passed by18:54:35.177. The independent inward census and rendered-glyph audit are in gameplay AFTER score: they cannot explain the preceding40m09s. The remaining4m17.086s of pre-score increase includes checked tests (+161.306s), pty (+65.678s), builds/goldens and runner variation; individual checked-test timings are unavailable because that tier buffers its output. Sampling those later gates would not fix the apt stall.

Cache validation: `cache-tests-mac.log` and `cache-integration-final.log` show29 Python tests, including cold/warm paths, wrong-tag/load/build/save refusal, stage failure status and unchanged gate ordering. `cache-planner.log` passes. `cache-integration.log` exports a real701,505,536-byte pinned image from the pool's existing approved image, reloads it, enters its container and verifies the pinned wolf; it does NOT claim to measure a fresh GitHub cache download or a cold apt build.

All receipt paths in this index are under `notes/cb08-evidence/`. Historical receipts remain alongside the complete final pass.
The boar charge already used body overlap: all four diagonal edge contacts take 22 damage, each one-cell-outside control misses, and bodies remain disjoint. Its rule was not changed. Alpha guard and hawk exclusion remain covered separately.

Final-runtime plants (drafts; never merge):
- #59, `cb08-plant-body`, `72e2474a`: one-line cardinal rectangle substituted for the diagonal; named test `test_cb08_diagonal_body_is_not_a_rotated_cardinal_rectangle`.
- #60, `cb08-plant-flank`, `2ad66a49`: one-line centre-cone veto restored for Whisper; named tests `test_cb08_whisper_flank_bite_is_not_refused_for_its_centre` and `test_cb08_whisper_flank_all_attacks_and_combos_land_once`.
- Both are one-commit plants atop `f10cae53`. The recorded controls ran before the opening-harness and tagged-archive fixture corrections; the planted functions and checked witnesses are identical after reparenting. Final Linux controls failed by their exact named assertions after canonical formatting: body 1 failure, flank 2 failures, no rejected/unsupported tests. Logs are plant-body-final.log and plant-flank-final.log. Draft PR CI is the unattended negative control; the coordinator watches it.
A test-isolation correction: the first refreshed Mac pty run encountered its own pre-cb05 schema 5/six-mask save and exited `save_corrupt`. Each diagonal pty row now owns a fresh explicit journey; the rerun passed. This did not change the game's save parser. The original failed log is not presented as a green whole run.

## Done-when

- [x] Drawing checkpoint delivered; diagonal extent independently measured; one NE drawing, quarter rotations, both tiers and grown wolf.
- [x] Eight-way body, actor separation, doorway census and real-key narrow-lane clearance.
- [x] Jaw/body-cell strikes; complete independent ring oracle; keyed boss circles; real Whisper flank outside BOTH old centre cones.
- [x] Ashen baseline and ONE 16-row exact-gap, actual-aim audit; alpha guard/hawk rules and boar-charge edge controls.
- [x] All announced rebases exactly once; cb07's motion/HUD preserved, jaws in both strike_reaches endpoints, signed subcell body envelopes and locked/unlocked roll semantics.
- [x] Exhaustive pose sheets, tagged/legacy ghosts, final-chain replay/golden regeneration, README-only refresh and design/art/replay/glyph docs.
- [ ] Drawing accepted by play (the maintainer's eye).
- [x] Final Mac native/release goldens, selftests, diagonal/Whisper live rows and play copy.
- [x] Refreshed named plant negatives, with canonical formatting and expected assertion failures.
- [x] Both-host isolated skip-00 and complete opening-group reruns.
- [x] Full Linux repetition after the committed death-archive refresh: every stage green at `f10cae53`.
- [x] Main PR and draft plants #59/#60, no labels.
- [x] Historical run40557106593 was observed once, then later diagnosed on the coordinator's request after its timeout.
- [x] New-head manual CI lookup performed once immediately after push; no matching run was listed yet. The required audit subsequently observed run `40568069619` in progress; the coordinator labels/watches the full matrix.
- [x] One new-head audit after the R7 push. Exact last line: `AUDIT FAIL (footprint: cross-cutting)`. Holds: CI in progress/no green tier yet, required full-matrix label absent, and retained worktree. Source/head/sections/citations checks pass.

Publication: main #61; draft plants #59/#60 (never merge). Observed R7 run: https://github.com/wolffe-lang/cub/actions/runs/40568069619 . No labels applied by the lane. Final CI footprint is cross-cutting because workflow and CI tools changed under R7. The worktree remains for the coordinator's hand audit and merge.

Final Mac play: `/Users/mfwolffe/lanes/cb08/cub-play-920fea19`, SHA256 `4c8ad935715c2881487da7b6e6b23912e001bcc4b79e35e4914b809501572782` read twice after both backend goldens and both live rows passed. Prior drawing checkpoint and Mac play builds remain intact. No issues were filed or closed. The observed old-six-mask schema5 rejection is a separate relay item; this lane did not change the save parser.

