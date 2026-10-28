# cb10 — cb10: repair sprint water theft and low hawk hits

_Materialised from the body of cub#68 at the merge (`64667bac`)._

## Prediction

Committed before implementation in `50f6c83f` (`notes/cb10-prediction.txt`).

1. **Repeat delay:** partly confirmed. The real pinned reader's legacy Ctrl+Right row at 250/30 ms was already green; 500/60 ms lost sprint at ticks13–15. Both the Ctrl hold and that legacy Ctrl-arrow's movement now get17 ticks, while ordinary arrows keep their existing inference.17/30 s =566.7 ms: tested through a500 ms first repeat, not slower settings. Exact releases remain immediate.
2. **Fox contact rather than kills:** confirmed. The planning lead saying there was only one decrement was wrong: `foes_step` also decremented flasks on a fox hit. The local plant records three bites/kills without w, with water3→2→1→0 on the contacts before those kills; the printed key list is `[29]` (`ctrl-down`), not water. The fix records water3→3 on contacts at ticks1/7/13, scent20→15→10→5, and kills at ticks6/12/18. Reader modifier transitions do not alias to water.
3. **Floaters as pickups:** refuted. They are HAWK, drawn pink (`draw_hawk`, rich181/plain13), with14-damage stoops. `strike_foes` excluded the kind from every bite; the hit census began at kind4 and omitted kind2. Their previous default mammal rectangle also did not match the unrotated shadow.

The maintainer uses **macOS Ghostty**. Cub asks for kitty flags11 (1|2|8). Injected reader rows cover Ctrl press `CSI57442;5u`, arrow press/repeat `CSI1;5:1C` / `CSI1;5:2C`, releases,250/30 and500/60 ms, and press-only fallback. All four enhanced press orders pass: arrow already repeating before Ctrl, Ctrl held four silent seconds before an arrow, a diagonal, and Ctrl release/re-press while the arrow remains held. No enhanced dropout is reproduced. These are protocol fixtures, not a physical Ghostty capture. A possible external cause is macOS Mission Control's default Ctrl+Left/Right space-switch shortcuts; this is documented as a candidate, not a verified diagnosis.

Recommendations implemented:
- **R-cb10-1 A:** +1 fixed-point sprint unit at every paw; B was +5%. Paw1:128→129 units/tick,15→15.1171875 cells/s; paw4:148→149,17.34375→17.4609375 cells/s. Drain remains12 stamina/s. This is the smallest integer increment; subjective play confirmation remains the player's.
- **R-cb10-2 A:** biteable only during STRIKE and RETREAT, one starting bite (8 health); keep airborne immunity during HUNT/CROUCH and the keyed parry kill at the stoop. Existing recovery36 ticks exceeds the12-tick minimum. B was always-biteable. The 4×1 nonrotating body and drawn shadow agree on both tiers and all four headings. No new glow-worm kind, flash or scatter is introduced.
- **R-cb10-3 A:** a landed fox feint steals `min(5, carried scent)`, never water; B was nothing stolen. Zero/few-scent and held-key kill rows are covered.

## Forbidden

No helper agents, engine/pin/workflow changes, package installs, merges, labels, tags, releases, issue actions, attribution trailers, planning-checkout writes or `~/.claude` writes. No access to the player's save. Shared files were approved by function; no cb11 bite chain, combo motion, strike offset or head-shake hunk changed. Guide changes append cb10 headings without reordering existing text. macOS work holds the shared atomic build lock and8 GiB vm_stat floor; Linux uses the assigned cores0–3 flock and the pinned engine container. The plant is a draft and must never merge.

## Inputs verified

- Base `eb34a399`; branch `cb10` in `/Users/mfwolffe/lanes/cb10/cub`, asserted before commits; no rebase owed (first merge in this wave).
- Contract, playtest rules/notes/proposals, bible, repository DESIGN/ART/KEYS/REPLAY/SCORE, cb04/cb04b/cb08/cb09 evidence and canonical RULES read. cb04's note was checked; the original fox-mouthful intent is explicit in bible§8/§15 and the existing design table/test, superseded here by the player's only-w-spends-water rule.
- Engine `74b89744e8f8a4ed01539b2fe814daf819b9abfc`, unchanged. wolf0.2.35/lupin0.1.56 release archives: Mac wolf`240b84d0…`, lupin`9133bfdb…`; Linux wolf`4cc4045b…`, lupin`ad703550…`; bundled std`2386522e…`. Staged stamps and pin checks verify identities; no source-built driver.
- README read and refreshed in its own commit. No save or replay schema change: pk1 key/event IDs and old input records still parse. Older replays do **not** promise byte-identical frames under corrected sprint, fox theft or low-hawk behavior; the changed goldens are enumerated.
- `--small-faults` is an explicitly staged headless fixture using a parsed ordinary-key replay. Each round posts an8-health fox at contact for its real strike, then freezes its AI for a real keyed bite. It is not an undisclosed teleport, natural journey recording, or physical-terminal measurement.

## Evidence index

Commits:
- `50f6c83f` prediction; `8dbdfdc8` local red regression plant.
- `bdab3cdb` bounded sim fixes, flask regression and sprint cap assertion.
- `db120331` hawk shadow/body,32 keyed low-window hitbox rows and full hit rings.
- `51962c0f` timed reader, Ghostty order/pty, held-key kill and three-kill replay instrumentation; shipping `--small-faults` command.
- `d1d0e126` appended guides; `b0ffded8` README-only refresh.
- `d3382a8f` explained golden changes; `93086e0e` focused proof receipts.
- `29019ffa` correct the stale fox-contact harness expectation and add four mutation-test rows.
- `64667bac` fix the steady motion instrument's half-cell assumption, with a real reed/water red→green regression. Final source head `64667bac6e429d47a4878e6616db1ad03c411109`.

**Plant:** draft #66, `cb10-plant-small-faults` at `8dbdfdc8`. Local nomad checked-machine reds, preserved in `notes/cb10-evidence/plant-red.log`: `test_cb10_legacy_ctrl_arrow_slow_repeat_never_loses_sprint`, `test_cb10_three_kills_and_fox_hits_never_drink`, `test_cb10_low_hawk_is_a_one_bite_body`. No manual plant CI dispatch; automatic PR run40619340656 was read once, in_progress, never waited on.

**Focused proof:** `notes/cb10-evidence/focused-green.log`:24 passed,0 failed/rejected/unsupported. Earlier shipping builds, the independent complete hit-ring oracle (inward gap0/1 misses0),32 low-hawk keyed bites, and exact golden differences are in `notes/cb10-evidence/prepare.log`. Hawk parry/tell fixtures run in the Crags and old-den arenas; the shadow's paint is confined to its 4×1 body at every heading/tier/posture.

**Goldens:**148 files in73 directories intentionally change; zero added/dropped keys. `notes/cb10-evidence/golden-changes.tsv` names every file, reason and before/after SHA256. Hawk-body state gaps and aligned hawk shadows account for the hawk cases (including `art/hawk-rich.{txt,sty}` / `hawk-plain.{txt,sty}`, `hawk-shadow`, `hawk-stoop`, `world-hawk`, late-area/landmark/rest/boss frames); fox water/scent accounts for `fox-feint`, `natural-death`, `boss-boar-beaten` and `old-den`; sprint cap/grace accounts for both sprint sizes. All other existing golden keys are retained byte-equal.

**First full-gate reds, source `93086e0e`:** Linux ended1 at2026-10-28T02:58:47Z because `tools/gameplay.py:66` in the **fox-feint** branch still expected a flask stolen on contact. This was not drinking; the corrected oracle checks the landed16-health hit, unchanged flasks and bounded five-scent theft. Separate spring-drink rows still require a mouthful spent and full healing. Four new Python oracle tests pass and reject the previous water theft, missing/excess theft, a missing hit and underflow. The Mac reached `check: green` (including the new live Ghostty row), then ended3 at02:58:53Z when native-goldens met only3 GB free+inactive+speculative. Receipt: `notes/cb10-evidence/followup-red.txt`. README re-read after the harness-only fix, current.

**Gate -2 follow-up, source `29019ffa`:** kasumi's full correctness, native/release gameplay, memory and performance stages all passed, including perf-idle. The additional motion census then failed at03:37:38Z on its first northbound reed sprint: seed0/field80/Shingle, dy−3552, blocked4. This was **the simulated cub colliding with adjacent water**, not a blocked process. The instrument assumed every stride fit in half a cell; the new129-unit sprint exceeded128 by one. `64667bac` biases the subcell reanchor against travel while retaining the real sample, every terrain class, sixty ticks and fractional residues. No simulation/collision/terrain rule changes. The checked reed-edge row failed before and passes after at fields80/200: dy−7740=60×129, blocked0. Receipts: `notes/cb10-evidence/motion-{reanchor.txt,probe-red.log,probe-green.log}`. README re-read, current.

The Mac -2 complete-check loop repeatedly met the memory floor. Per **R-orch** it was stopped by its recorded pid46534 and individually observed descendants; only the lock owned by46541/cb10 was released. No process-group signal was used. That unbounded complete-check retry policy is retired.

**Final -3 jobs, source `64667bac6e429d47a4878e6616db1ad03c411109`, launched2026-10-28 UTC:**
- **Mac bounded leg (R-orch):** pid2349, started03:57:09Z; `/Users/mfwolffe/lanes/cb10/mac-final-3.log`; marker `/Users/mfwolffe/lanes/cb10/mac-final-3.exit`. Build both backends, full checked tier, Python oracle tests, targeted reader/replay/hitbox/hit-census rows on both binaries and the Ghostty live pty row, then **one** further full release-binary/both-tier golden attempt. Memory guards remain enabled, with printing30-second waits under the shared lock. It never reruns the entire complete-check sequence. The log prints `CB10_MAC_BOUNDED_BUILD_CHECKED_TARGETED_GREEN` before attempting goldens; a subsequent floor refusal is explicitly marked and handed to the orchestrator's CI macOS `tier full` substitute, not retried indefinitely. Completed **exit0 at04:03:34Z**: both builds green; full checked tier447 passed,0 failed/rejected/unsupported and0 SKIP; Python/reader/replay/hitbox/hit-census targets and live Ghostty pty green; the **first and only** further full golden attempt passed on both tiers, including art. No R-orch CI substitution was needed for this local golden attempt. The shared lock was released when the bounded job ended.
- **kasumi full leg:** pid74656, started03:59:24Z; `/home/mfwolffe/lanes/cb10/linux-final-3.log`; marker `/home/mfwolffe/lanes/cb10/linux-final-3.exit`. Full container `tools/check-linux`, `tools/check-perf`, repaired full motion census/summary and `--small-faults`, under cores0–3 flock; setsid/source launch verified. Motion outputs: `/home/mfwolffe/lanes/cb10/motion-linux-3.txt` and `/home/mfwolffe/lanes/cb10/motion-linux-3-summary.txt`. Currently waits for its assigned core block.
- Mac -3 is green for the amended bounded leg; Linux -3 remains pending, **not claimed green**. The orchestrator watches the long Linux job and materialises final receipts. Its full-matrix label remains orchestrator-owned. The Mac leg is not represented as a complete local Mac gauntlet.

Ledger: cb10 — repeat grace, +1 sprint unit, only drinking spends water, low hawk body/bite/parry; module; plant#66; final source64667bac; motion diagnostic repaired; final Linux full and bounded Mac jobs launched.

## Done-when


- [x] Prediction committed first; three named local reds and draft plant preserved.
- [x] Real-reader default/slow repeats, exact releases, four Ghostty press orders and live negotiated pty row added.
- [x] Sprint paw1/paw4 caps measured; stamina drain unchanged.
- [x] Three-kill/no-w replay fixture identifies fox contact; bounded scent theft and held-key kill regressions.
- [x] Pink hawks identified; one-bite low windows,4×1 drawing/body and hit census/audit rows; existing parry route verified.
- [x] Both-tier intentional golden deltas named; README and replay compatibility updated.
- [x] Focused24-row checked-machine proof green; shipping native/release targeted proofs green.
- [x] Reed-edge motion regression red before the instrument-only fix, green after at both fields.
- [x] R-orch bounded Mac build/checked/targeted leg green,447 checked tests and0 SKIP; one further full golden attempt green, exit0 at04:03:34Z (log/marker above).
- [ ] Final Linux full gauntlet/performance + repaired motion census completion (pid/log/marker above).
- [ ] CI completion; final-head run40629369060 read once immediately, queued, never waited on or labelled by the lane. Prior-head runs40624767960 and40622833832 were each read once.
- [x] Lane audit run exactly once, at original head93086e0e: `bash wolf/tools/lane-audit.sh cub cb10 68` from the org directory. Exact last line: `AUDIT FAIL (footprint: module)`. Its diff/footprint/sections/SHA checks passed; failures were then-pending CI/no green tier and the managed nohup Mac gate pid13023 classified as an orphan. That first gate ended on its memory-floor marker; the later unbounded -2 loop was stopped per R-orch, and the bounded -3 job is managed above. Full original audit transcript: `/Users/mfwolffe/lanes/cb10/audit.log`. No second audit invocation or claim that the old audit covered either follow-up commit.

Issues to file/close: none acted on. The physical Ghostty sprint report is not reproduced by the enhanced protocol fixtures; collect a physical byte capture if the Mission Control shortcut candidate does not explain it. The orchestrator may resume this lane on either full-gate red.

