# cb11 — Buffer hand-timed bite requests through the combo boundary

_Materialised from the body of cub#71 at the merge (`339c6ff2`)._

## Prediction

Prediction committed before implementation in `3502ce29`, now `a1546c76` after the announced rebases: hand-spaced presses would lose requests at150/200/250ms through the age-5 admission window and one-slot buffer. The unchanged production replay confirmed `[1,2]` with correct left/right offsets once admitted;330ms could reach all three.

**The reported all-left motion was reproduced through the real reader.** An enhanced330ms/plain session recorded bite keys at8,19,28, giving simulation starts `(9,1),(29,1)`. Press2 arrived at age11: the strict `< duration` test dropped it while `start_action` still saw a live bite; press3 restarted strike1. Both holds moved left. `reader-before.tar.gz` retains the exact bytes, timestamps, recording and trace. The deterministic367ms plant pins this endpoint: holds `(6,1,-256,-256),(28,1,-256,-256)`. A pre-fix enhanced hold with500ms repeat delay additionally gave `[1,1,2]`: repeats incorrectly fired bites.

The fix accepts requests at ages1..duration inclusive, keeps two pending requests with their own aims, consumes one per bite end and retains a six-tick grace. Overflow does not overwrite either aim. Costs12/14/18 and durations11/13/17 stay unchanged. Unaffordable queued links discard the queue; other actions, rest, death, area entry and alpha guard clear it. Age0 duplicates do not queue. Drawing geometry and head-shake timing did not need another rewrite.

**R-cb11-2 prediction and red:** the c0a9a2ea Mac rerun exposed the difference between nominal milliseconds and delivered simulation ticks. Nominal100ms presses were consumed at3,7,9, so the final two-tick gap was correctly suppressed; nominal60ms streams acquired three-tick gaps and correctly admitted another strike. Actual sends included602.493→670.008ms instead of nominal600→660ms. The game obeyed the ruled threshold; the wall-clock test asserted the wrong instrument. `9b2e598b` preserves this red and the prediction before the harness repair.

## Forbidden

Original game work only. No engine/pin, workflow, tools/check*, compiler/runtime, planning or ~/.claude edits, helper agents, package installation, labels, merges, tags, releases, issue actions or attribution trailers. No personal save touched. No damage, collision, fighter tactic or gameplay acceptance threshold was loosened. R-cb11-2 changes the instrument, not the <=2/>=3 legacy policy; a late/missing delivered event is an explicit failing DELIVERY diagnostic, not a silent pass.

Mac work holds the shared mkdir/pid lock and8GiB free+inactive+speculative floor. The current bounded leg performs build/checked/targeted stages once, then at most3 full-golden stage attempts; an already-green backend is never rerun for a later memory refusal. Third refusal is handed back for the coordinator's CI substitute, never looped. Linux uses the assigned4–7 flock and the pinned container wrapper. Persistent save schema and replay ids remain unchanged; request/counter state is transient.

## Inputs verified


Original baseeb34a399. Rebased **once onto announced1497b5d3**, then **once onto announcedf6af855c before the R-cb11-2 full gates launched**. Current final head **339c6ff2771b6b05aa31da8a4008c3ca55a3ed54**. cb10's input/sprint,129-unit cap, fox scent theft, low-hawk body/biteability and motion correction remain. cb12's death schedule, counter, partial repaint/render-only seam, one-shot input behavior and gameplay/death expectations remain. Terminal conflicts retain all three lanes' row groups; README conflicts retain both feature descriptions. README re-read and updated separately.

Engine74b89744e8f8a4ed01539b2fe814daf819b9abfc; wolf0.2.35/cf0c13d, lupin0.1.56/294d626, std2386522e. Both complete paired toolchains were verified; no pin change.

R-cb11-1 A, with the accepted legacy fallback: enhanced Space PRESS acts, REPEAT/RELEASE do not (including repeated Shift+Space). The engine's `ESC[>11u` request includes event types and all keys and is asserted in the pty output. Legacy gaps<=2 **delivered simulation ticks** are dropped and refresh the timestamp;>=3 count as presses. The first legacy repeat after a250/500ms delay cannot be distinguished from a tap and may queue one extra strike. Scheduling may also turn nominal60ms into three ticks or nominal100ms into two. KEYS now states both limitations rather than promising physical wall-clock timing.

R-cb11-2 A: gating reader rows pace by observed ticks, writing afterN−1 and acknowledging the carrying trace atN. Requested/recorded ticks and gaps are printed and must match before asserting the unchanged strike sequence. Hand intervals use cumulative30Hz quantization; nominal30/60ms repeats use1/2 ticks; delayed repeats begin at8/15 ticks for nominal250/500ms. Eight unit rows reject late, missing or dropped delivery and verify quantization and default-row registration. B—loosening the policy/assertion—was not implemented.

The old wall-clock variant remains an explicit **measurement-only** command, outside default ROWS and correctness gates:
`python3 -I tests/combo_pty.py --measure-wall-clock --bin target/native/cub`.
It prints nominal/sent times, recorded bite ticks, delivered gaps and observed strikes without interpreting nominal milliseconds as policy inputs. Its CLI was exercised successfully; terminal/process errors remain reported.

The reported play terminal is **Ghostty on macOS**. The fixtures inject **Ghostty-compatible sequences**, not a physical capture or a measurement of the user's repeat preference: PRESS `ESC[32u` (explicit `ESC[32;1:1u` also in the first baseline), REPEAT `ESC[32;1:2u`, RELEASE `ESC[32;1:3u`.

## Evidence index

Current commits:
- `a1546c76`, `6854c037`: prediction and unchanged-game replay/reader reds.
- `e41c23ae`, `4cf80f8c`: capped-two request FIFO, inclusive endpoint/grace/cancellation and Space-only repeat filter.
- `71cb08b4`:24 replay/tier rows and independent hold oracle; gameplay wiring.
- `9b2e598b`: delivered-tick red and R-cb11-2 prediction, before the repair.
- `66859221`: observed-tick reader, explicit delivery guards, eight unit tests and optional non-gating wall-clock mode.
- `768eac8b`: README-only delivered-tick clarification.
- `e90a92f5`: regenerate the six death-affected journeys and50 frame paths after cb12, without generator/tactic changes.
- `339c6ff2`: focused pacing proof, wall-clock measurement, latest SHA receipts and bounded/strict gate recipes.

Receipts are under `notes/cb11-evidence/` unless an absolute active-job path is given.

**Original fault and plant:** `hand-before-complete.log`, `reader-before-complete.log`, `reader-before.tar.gz`, `ghostty-compatible-before.log`. Early instrument mistakes are retained in earlier logs, not treated as gameplay findings. Draft **plant#69**, independent branch `cb11-plant-hand`, head8b301f50, restores sim/controls exactly to trunk after the fixes were committed. `plant-hand.log`: `FAIL cb11-hand-n-150-rich` gives `[1,2]`; **`FAIL cb11-hand-n-367-rich` gives `[1,1]` with both holds left**; `CB11_PLANT_EXIT 1`. Never merge. Plant CI40623855972 was read once at publication, not waited on or re-read.

**Recorded Mac play:** `played/{enhanced,legacy}-{rich,plain}/record.pk`, `trace.txt`, `sent.txt`, `replayed-trace.txt` and `hold-{1,2,3}.{txt,sty}` retain the original short reader sessions, live/replay state parity and full80×24 holds. Text attachments: [rich1](https://github.com/wolffe-lang/cub/blob/339c6ff2771b6b05aa31da8a4008c3ca55a3ed54/notes/cb11-evidence/played/enhanced-rich/hold-1.txt), [rich2](https://github.com/wolffe-lang/cub/blob/339c6ff2771b6b05aa31da8a4008c3ca55a3ed54/notes/cb11-evidence/played/enhanced-rich/hold-2.txt), [rich3](https://github.com/wolffe-lang/cub/blob/339c6ff2771b6b05aa31da8a4008c3ca55a3ed54/notes/cb11-evidence/played/enhanced-rich/hold-3.txt), [plain1](https://github.com/wolffe-lang/cub/blob/339c6ff2771b6b05aa31da8a4008c3ca55a3ed54/notes/cb11-evidence/played/enhanced-plain/hold-1.txt), [plain2](https://github.com/wolffe-lang/cub/blob/339c6ff2771b6b05aa31da8a4008c3ca55a3ed54/notes/cb11-evidence/played/enhanced-plain/hold-2.txt), [plain3](https://github.com/wolffe-lang/cub/blob/339c6ff2771b6b05aa31da8a4008c3ca55a3ed54/notes/cb11-evidence/played/enhanced-plain/hold-3.txt). Third hold is head-shake age5. Exact whole-cell motion is asserted from simulation; rendered fur independently asserts visible direction and head swings. Plain north standing/snap centroids differ by about0.23cell, so pose-centroid change is not mislabelled body translation.

**Cadence red→green:** `mac-rebase-cadence-red.log/.tar.gz` and `r-cb11-2-prediction.txt` preserve the c0a9a2ea Mac failure. `cadence-prepare.log` passes36 observed-tick reader sessions on Linux release: nominal100ms delivered `[6,9,12]`, gaps3/3, strikes1/2/3; nominal60ms delivered6,8,…,34, every gap2, only strike1. All requested ticks equal acknowledgements and replay bite ticks. All enhanced repeats remain non-actions; the accepted delayed legacy repeat still gives1/2.57 Python tests pass, including the eight delivery-oracle controls. `wall-clock-measurement.log` demonstrates the separate non-gating command and prints nominal, sent and consumed intervals. The old wall-clock green runs remain historical measurements, not the current gate's proof.

**Fixture and golden receipts:**38 inherited fixtures have per-file old/new SHA256 and reasons againstf6af855c in `cadence-fixture-receipts.txt`. `cadence-golden-receipts.txt` names every one of768 changed/added/deleted paths against that base, with old/new SHA256 and reason. The cb12 rebase had34 distinct generated-data conflicts (six replay files and28 frame paths;38 resolution occurrences); all cases/sheets were regenerated from merged code, with50 frame paths refreshed. `cb12-regenerated-paths.txt` lists both sets. Inherited art sheets are byte-equal to f6af855c, retaining cb10's hawk and cb12's additions alongside cb07/cb08 combo/diagonal art. The earlier cb10 integration's80 conflicts/130 refreshed paths and prior SHA inventories remain separately labelled historical receipts. The original `fixtures.log` recorded400/400 boss worlds within the unchanged five-life bar (boar96 first/4 second, others100 first), not byte-identical census results: newly admitted combo requests/costs change subsequent fight/AI timing.

**Flank proof:** unchanged bounded real-key search still finds candidate59/544:lynx prefix820, Down12, aim160, hit836, health104→80, both former centre-cone endpoints miss by minimum32578. `find-flank.py`, `flank-recipe.txt`, `flank-search.log` and the latest `cadence-prepare.log` retain the recipe. No position, health or AI injection added.

**Historical completed gates, not claims about the current head:**
- At07bb59f4:449 checked tests,45 Python tests, both Mac reader matrices and both Mac-backend goldens passed. `mac-pre-rebase-visual.log` ends `CB11_MAC_FINAL_VISUAL_GREEN`. `linux-pre-rebase-full.log` ended0 at04:07:37Z, but perf actually ran at **slack3**, not1: exporting outside in-container did not forward the variable. The note corrects that earlier claim.
- Atc0a9a2ea:`linux-c0a9a2ea-full.log` ended0 at05:42:55Z with **slack1** inside the container; median14.0ms/p90 33.4ms against40/70ms. The corresponding Mac leg ended1 at05:55:15Z on the nominal-cadence mismatch above; it never reached the golden stage. It was not a memory refusal and was not retried unchanged.

**Current final-head regates, launched once at339c6ff2 after the cb12 integration:**
- **Mac bounded leg completed0 at06:53:40Z**, exact339c6ff2, `/Users/mfwolffe/lanes/cb11/mac-cadence.log` and `/Users/mfwolffe/lanes/cb11/mac-cadence.exit`. Both builds;485 checked tests (zero failed/rejected/unsupported),57 Python tests;24 replay/tier rows and36 observed-tick reader sessions on each backend; inherited cb10/cb07/cb08 and all three cb12 terminal groups green on both binaries. `CB11_MAC_CADENCE_BUILD_CHECKED_TARGETED_GREEN` at06:53:12Z, then both full golden checks passed in the **first and only** golden-stage attempt. `CB11_MAC_CADENCE_GOLDENS_GREEN`; no memory-floor override or CI substitution.
- Kasumi setsid pid224942; fresh `/home/mfwolffe/lanes/cb11/cadence-final`; `/home/mfwolffe/lanes/cb11/linux-cadence.log`; marker `/home/mfwolffe/lanes/cb11/linux-cadence.exit`; started06:42:18Z. Full `tools/check-linux`, then **`in-container env LAIR_PERF_SLACK=1 tools/check-perf`**, cores4–7 flock. Pending at publication, not claimed green. The shared harness changes Linux rows, so its full gate is rerun too.

Ledger: `cb11 | buffered combo and observed-tick reader | module | main#71 | plant#69 | basef6af855c | head339c6ff2 | no issues filed/closed`.

Earlier once-read CI receipts:40627786382 at07bb59f4,40637241232 atc0a9a2ea. Current339c6ff2 CI read once immediately after its single push:40646571038, in progress. No CI wait or label.

## Done-when

- [x] Prediction first; missing requests and real-reader all-left endpoint red before gameplay fix.
- [x] Capped-two FIFO, early/end requests, six-tick grace, per-request aim, affordability and cancellation; eight facings/both tiers/head shake.
- [x] Mac real-reader recordings and text hold attachments; independent plant#69 red by name.
- [x] R-cb11-2 A: simulation unchanged; gating observed ticks acknowledged/printed; late/missing delivery fails explicitly; wall-clock variant retained outside default gates.
- [x]57 Python tests and36 focused observed-tick Linux reader sessions;24 merged replay/tier rows.
- [x] Exactly one rebase per announced cb10/cb12 merge; both integrations retained; all generated conflicts freshly regenerated and named; per-fixture SHA receipts; README current.
- [x] Current bounded Mac leg green at339c6ff2:485 checked,57 Python, both-backend observed-tick and inherited terminal targets, all goldens on the first attempt.
- [ ] Current full Linux gate and PR-tier green; coordinator watches pending markers.
- [x] Audit at07bb59f4, once: `AUDIT FAIL (footprint: module)`; then-pending CI/tier only.
- [x] Explicitly requested audit atc0a9a2ea, once: `AUDIT FAIL (footprint: module)`; then-pending CI/tier only.
- [x] Requested audit at339c6ff2, once after the PR update: `AUDIT FAIL (footprint: module)`. Only holds are in-progress CI/no green tier; all ancestry, footprint, five-section,12 cited-SHA, head and process checks pass. No CI wait or label.

