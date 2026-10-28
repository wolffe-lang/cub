# cb15 — consumables and the inventory

_Materialised from the body of cub#73 at the merge (`60890a49`)._

## Prediction

`bd5e0eac` records the prediction before implementation: five capped effects, a paused replayable inventory, deterministic saved pickups and ordered discovered lore. Tuft plant #70 (`4217368d`) is red on the predicted death row; overlay plant #77 (`7aab8d59`) has four genuine compositor assertion reds and zero unsupported rows. Neither plant is for merge.

## Forbidden

Original cub code/art/text only. No engine, pin, CI, planning-checkout, configuration, attribution, label, merge, release or issue change. Mac builds use the shared lock and8-GiB floor; Linux uses the cached container and cores4–7 flock. No other lane's processes/worktrees or the playtest save are touched. The restored den hints and inherited currency assertions are not weakened.

## Inputs verified

Rebased once onto each announced predecessor, ending at `918dd9a0` (cb13). Pins unchanged: lair `74b89744`, wolf0.2.35, lupin0.1.56, std `2386522e`; both-host identities and archive pairs are retained under `notes/cb15-evidence/`.

- `48519664`, `9ad20542`, `63af05cc`: effects/actions, bounded persistence, both-tier pickup/inventory/Lore art.
- `a448187a`, `4b3ad38a`: replay paths, shipping-binary semantics and edge coverage.
- `bc492fbb`, `103c8d26`, `dc05c00c`, `26318e27`: finite first-den tuft placement and complete paused effect/combat/offscreen clocks; public one-item adapter.
- `1c39d60e`, `a3101ddc`, `f5c46fd0`: partial counter repaint respects overlays; bounded terminal/full-render oracle.
- `b9391f71`, `7b136144`: preserve spending confirmation tick25 and all196 downward-count files; exact golden receipts.
- `7c9204b0`: named CUB6 wrapper plus item extension, exact migrations and corrupt-extension regressions.
- `f51a50c1`: input-only third Up in the inherited currency witness, past Lore to Confirm; every currency/save assertion unchanged.
- `c97108da`: inherited named-wrapper witness uses `journey.SNAPSHOT`; name/time and corruption assertions unchanged.
- `60890a49`: post-cb13 checked, replay, migration and lossless-golden preparation evidence.

R-cb15-1 A: lock, else nearest forward-cone foe within6 cells. R-cb15-2 A: no pouch HUD strip. R-cb15-3 A: den r takes one available item, then still rests. All three approved recommendations are implemented.

Correction: **the bible's bleeding (§5) was never built before cb15.** This pass adds its bounded tick/lick/yarrow API; actors apply it in cb18. Pine already reaches lynx tracking; later actors and Burn entry have hooks.

Provisional placements:7 meadow yarrow,6 Bramblehold marrow,5 river shards and1 tuft four cells east of first Bramblehold den1, clear of the existing last-den2 death checkpoint. cb14 replaces/extends these placements. Found coals/frame/stump words retain append-only lore ids10/11/12; cb14/cb16 begin13.

CUB6 appends items **after cb13's name/played_ms**, without another version bump. Old CUB4/5 and original15-line CUB6 wrappers migrate. Metadata remains outside deterministic replay state. Bounds:128 ground pickups and32 ordered de-duplicated lore lines; cell/order, finite discoveries and tuft uses persist. Effects/open menus are transient. Journey5 carries204 slots, preserving old ids and appending new ones. Only recorded journey3/4 enable old six-row rest semantics; live games use seven rows. README and format/key/art/design docs were refreshed and reread.

## Evidence index

`notes/cb15-evidence/` retains first reds, exact inputs, plants, preparation logs and per-directory old/new Git-tree receipts.

- Tuft plant #70: named death row FAILED (trap(assert));16 other rows green,0 rejected/unsupported. CI read once40626629871.
- Overlay plant #77: four inventory/Lore terminal-compositor assertion reds,0 unsupported. Original over-budget attempt retained separately. CI read once40656198080.
- Initial whole gates retained445 passed/1 failed (old combat cursor). Post-cb13 `cb13-first-whole.log` retains529 passed/2 failed: `counter_test::test_cb12_den_spending_and_save_use_exact_currency_during_count` and `registry_test::test_cb13_named_wrapper_preserves_name_time_and_refuses_corruption`. These were inherited input/schema witnesses; the two approved adaptations above fix them. Immediate re-run8/8 green.
- Corrected post-cb13 full checked suites: **531 passed,0 failed/rejected/unsupported,0 SKIP on both hosts**. New wrapper-focused run33/33 green. Linux both builds, both-backend/tier pouch/save/menu semantic rows, and resumed-record/den-contact/rest-allocate pty targets green.
- One corrected-source Linux generation reproduced the rebased expected bytes without any further changes. Import key sets7256/7256,0 missing/extra; all196 downward spending files retained. Against918dd9a0:7084 old keys,172 new,0 removed; **all444 inherited integer final.states byte-identical**.104 directory receipts (92 existing/12 new),2264 modified existing files,172 new,0 removed. Archive sha256 `e4dd58b9b6290610214c7b571227eb1a301ba0af78e392555971d41b3917172c`.
- Independent cb11 hit census **29,280 pairs byte-identical**, sha256 `79039792a9b1799bb1e0a0d66c1a5e99c7edad6632587d7dc74ca9ae4ed28deb`.

Whole final-head gates at **60890a4936a3487e7461ea3252c3c5094a319569** launched2026-10-28: Linux tools/check-linux then tools/check-perf at20:38:25Z, pid584185, `/home/mfwolffe/lanes/cb15/cb13-whole.log`, marker `/home/mfwolffe/lanes/cb15/cb13-whole.exit`; Mac guarded composition of the unchanged tools/check stages, same order with per-stage8-GiB waits (not claimed as a literal tools/check exit), at20:38:12Z, pid62477, `/Users/mfwolffe/lanes/cb15/logs/mac-cb13-whole.log`, marker `/Users/mfwolffe/lanes/cb15/mac-cb13-whole.exit`. Both memory gates are included, not inferred from unit tests. Final whole verdicts and the one immediate final-head CI read follow below; no CI wait or lane-applied label.

The immediate post-push CI read returned only the old heads: no final-head run had registered yet; no retry or wait was made. The single required audit subsequently saw final-head run **40765363048 in_progress**. Audit command from the organization directory: `bash wolf/tools/lane-audit.sh cub cb15 73`; exit1, last line **AUDIT FAIL (footprint: module)**. All footprint, paths, citations, sections and head checks passed. Remaining audit failures are pending CI/no green tier yet and its generic orphan check seeing pid62477: the deliberately detached, still-running Mac whole-gate launcher above, not a stale/deleted-worktree process. The audit is not rerun; the orchestrator owns the CI and both local gate completions.

## Done-when

- [x] Five exact effects/caps, interruption, bleed/lick,600-tick concealment,90-tick half movement/air orbit and passive tuft/use counter.
- [x] Saved deterministic pickups/drops, full-stack/full-pool refusal, den r, consume/drop/re-pickup/discard, Burn/new-area hooks.
- [x] Paused inventory/tooltips/aim on both tiers, complete combat/effect clocks, replay/key vocabulary, saved Lore/scroll/return.
- [x] Unit/integration/replay/golden/migration rows, both plants, unchanged hit census, lossless keys/states and README.
- [ ] Final whole Mac/Linux correctness/performance/memory verdicts: launched at sealed head above; no green claimed while pending.
- [x] Final-head CI queried once immediately after the single force-with-lease; no registered run yet. Audit once subsequently saw40765363048 in_progress. The orchestrator owns tier/label/watches and merge.


Ledger: cb15 | consumables and inventory | module | PR #73 | plants #70/#77 | final head60890a4936a3487e7461ea3252c3c5094a319569. Materialise these five sections as the lane note at merge. No issue to file or close.

