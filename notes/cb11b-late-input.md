# cb11b — late reader input against the consumed-tick policy

_Materialised from the body of cub#82 at the merge (`e858561b`, with cub#79 stacked on it)._

## Prediction

`869a217b` committed the directive/prediction before the fix: the old exact-delivery guards would fail under a slow observer even when the game correctly follows the consumed cadence. A new oracle, driven only by consumed event ticks/kinds, should match the game through late legacy repeats, grace expiry and stamina-refused links.

Confirmed locally with the approved80ms observer stall: the fixed reader passed36 sessions with **414 late consumed events**. Enhanced200ms/plain requested ticks10/16/22 and consumed12/18/24. Legacy nominal30ms actually arrived every3 ticks and produced starts `(8,1),(19,2),(32,3),(49,1),(60,2),(80,1)`; the independent oracle predicted all six, including stamina refusal/recovery. The old guards, restored only on the off-line plant, failed by name under the same stall.

## Forbidden

No gameplay, engine, compiler/runtime, pin, workflow, tools/check*, replay/save schema or game-data changes. No labels, merges, tags, releases, issue actions, attribution trailers, helper agents, packages or personal-save access. Planning checkout and ~/.claude unchanged. No parallel stress build: the coordinator specifically approved the disclosed observer stall alone. Every Mac build/proof runs under the shared lock and8GiB floor; Linux uses the assigned4–7 flock and container wrapper.

## Inputs verified


Basef20650d4; isolated branchcb11b at `/Users/mfwolffe/lanes/cb11b/cub`. Final head a48af5acf0b490d9cc14a990d2e002d2530b685e. Engine74b89744, wolf0.2.35/cf0c13d, lupin0.1.56/294d626, std2386522e remain pinned; complete paired toolchains verified/staged. README read and updated separately.

Inspected hosted run40688342154 (cub#79's full-matrix run): macOS arm64 rejected12 cb11 rows at13:13:16Z,11 before-write latenesses and one late acknowledgement. Example: `cb11-ticks-enhanced-200-plain: DELIVERY late before write: wanted tick21, observed22`. `hosted-red.txt` preserves all12 named rows.

The follow-up corrects cb11's interpretation of R-cb11-2. Requested ticks are pacing targets, not acceptance conditions. The reader acknowledges a new input-bearing trace strictly after the actual pre-write tick; an older event cannot acknowledge a late new write. It waits for consumption instead of failing merely because the target passed. Recorded replay bite ticks must agree with those acknowledgements.

`combo_request_oracle.py` independently predicts exact strike-start ticks/numbers from consumed event kinds/times: inclusive bite endpoint, two pending requests, six-tick grace, enhanced repeat/release rejection, legacy<=2-tick suppression,70 starting stamina,12/14/18 costs and2 restored at each idle tick's end. It reads no observed action, combo or stamina result. Tests pin each cost threshold, recovery ordering, cap, grace boundaries, old all-left/endpoint mutations and missing/stale acknowledgements.

Reader hold/pixel checks now group by each action's start and validate the independently predicted sequence, including repeated strike1 after a real grace lapse. The deterministic three-press replay rows still default to **exactly1/2/3** and retain all direction/hold assertions. Default ROWS never enables the stall. The optional wall-clock measurement remains outside correctness gates.

## Evidence index

- `602ac95f`: late acknowledgements, consumed-cadence/stamina oracle, visual grouping and regression controls.
- `9cd2a169`: protocol/proof documentation.
- `8dae584c`: README-only clarification.
- `deaa8755`: independent12/14/18 stamina thresholds and idle-recovery ordering.
- `a48af5ac`: hosted red, stalled green, raw recordings and off-line plant receipts; reproducible gate scripts.

Receipts under `notes/cb11b-evidence/`:
- `hosted-red.txt`: the actual hosted macOS failure, not a guessed diagnosis.
- `stalled-reader.log`: `--observer-stall-ms 80 --bin target/release/cub`,36 sessions,414 late consumptions, `CB11B_STALLED_READER_GREEN`. The flag deliberately deschedules the observer before each write; it is off in default ROWS and the proof fails if it observes no actual lateness. It changes no game state or simulation clock and is not described as CPU contention or a physical Ghostty capture.
- `stalled-enhanced-200-plain/`, `stalled-enhanced-held250-rich/`, `stalled-legacy-30-rich/`: `record.pk`, `trace.txt`, `sent.txt`, `delivered.txt` retain requested/consumed evidence, including the six-start stamina case and enhanced repeats remaining non-actions.
- `python-tests.log`:70 Python tests pass. Nine delivery/registration controls,11 independent request-policy tests and seven hold-oracle tests are included; late delivery is accepted as input data while absent consumption or wrong predicted/observed actions fail.
- **Plant draft#81**, independent branchcb11b-plant-late, head efbf25a8. Four guard lines restore the old fail-on-late behavior after the fix was committed. `plant-late.log`: `reader proof FAILED: cb11-ticks-enhanced-200-rich: DELIVERY late before write: wanted tick9, observed11`; `CB11B_PLANT_EXIT 1`. Same80ms stall and same unchanged game binary. Never merge. Plant CI40732025694 was read once, queued; no wait/dispatch.

No src/, case, golden, pin, workflow or tools/check* bytes changed relative to base. No golden or census regeneration is owed; complete checks are rerun rather than assuming harness-only work is harmless.

Final-head local gates:
- **Mac completed0 at17:13:43Z**, exacta48af5ac:485 checked tests (0 failed/rejected/unsupported/SKIP),70 Python tests,24 deterministic replay/tier rows and normal36-session reader matrices on both backends, plus the release80ms observer-stall proof with414 late consumptions. Both-backend full goldens passed on the first golden-stage attempt, with no regeneration. `/Users/mfwolffe/lanes/cb11b/mac-final.log`; `/Users/mfwolffe/lanes/cb11b/mac-final.exit` is0. No memory-floor bypass or substitute.
- Kasumi setsid pid316011; `/home/mfwolffe/lanes/cb11b/linux-final.log`; marker `/home/mfwolffe/lanes/cb11b/linux-final.exit`; exact final head, started17:07:06Z. Full tools/check-linux then **`in-container env LAIR_PERF_SLACK=1 tools/check-perf`**, cores4–7. Pending at publication.

The coordinator will add **full-matrix** so the hosted macOS job that exposed this fault proves the final head. The lane does not label or wait on CI.

Ledger: cb11b | consumed-cadence reader oracle | module | main#82 | plant#81 | unchanged gameplay/goldens | hosted macOS verification coordinator-owned.

Final-head CI read once immediately after opening:40735116605, in progress. No label or CI wait.

## Done-when

- [x] Prediction before fix; hosted red inspected and preserved.
- [x] Late consumption continues; expected starts derive independently from actual consumed ticks and full ruled policy, not requested cadence or observed actions.
- [x]70 Python tests; deterministic1/2/3 replay requirement retained.
- [x] Mac80ms observer-stall proof green with414 late consumptions printed; raw records retained; no parallel stress build.
- [x] Off-line plant#81 red by name under the same stall.
- [x] README/protocol docs current; no gameplay/golden/pin/CI edits.
- [x] Final-head bounded Mac gate:485 checked,70 Python, both-backend default reader/deterministic rows,414-late stall proof, both full golden checks first attempt.
- [ ] Final Linux gate, current PR-tier green and labelled hosted macOS gate.
- [x] Final-head CI read once:40735116605, in progress. One lane audit: `AUDIT FAIL (footprint: module)`, only pending CI/no green tier; all ancestry/footprint/sections/SHA/head/process checks pass. No label or CI wait.

Issues to file/close: none acted on; the reported hosted failure is the target of this PR.

