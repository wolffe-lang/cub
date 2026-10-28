# cb13 — the main menu and the saves

_Materialised from the body of cub#72 at the merge (`2eb302dc`)._

## Prediction

- `b629a86b` records the pre-implementation prediction: CUB6 name/played_ms belong to the journey wrapper, never Sim or numeric journey-4 snapshots; exact CUB5 migration; strict atomic registry; unchanged den-fire art beneath the menu.
- Continue, New journey, Load, Playback and Quit are implemented, including most-recent Continue, external save registration, non-destructive legacy import, typed paths and the default saves/replays/ghosts directories.
- Nine focused checked tests, seven replay cases and14 new both-tier menu golden directories (42 files) cover the feature. Existing golden bytes are unchanged by cb13 relative to trunk.
- A missed compatibility error was fixed without weakening its oracle: replay clock footers broke committed-archive equality. All recording bytes omit clock-derived dates; chooser dates use file mtime.

## Forbidden

No cb13 changes to engine/pin/workflows, Sim, inventory, forest, rest art, death presentation or combo implementation. No planning/configuration edits, packages, labels, merges, tags, releases, issue actions or attribution trailers. No access to the play save/ghosts. All fixtures use lane-owned HOME paths.

Mac jobs held the shared mkdir lock and8GiB printing gate. Linux used the engine container, assigned0–3 flock and LAIR_CPUS=0-3. No other lane's process/worktree was changed. Plant worktree pruned only after preserving its red proof and draft.

## Inputs verified

- **Current head2eb302dc7812a59c5055736812d936709accf500**, rebased once onto announced **origin/trunk991cc704f4b8d6f826dac498c618ceb600c820ae**. This follows the individually announced cb10/cb12/cb11 rebases.
- The new trunk adds cb11b's consumed-tick reader oracle, related tests/docs/receipts, and cub#79's Linux/macOS timeout40->60. No src/, case, golden, score or engine bytes changed in that upstream delta.
- The rebase had no conflicts. Among cb13-owned changed files, only README.md and docs/KEYS.md receive the upstream reader-description prose. **src/, tests/cases/, tests/goldens/, tests/pty_rows.py, tests/pty_rows_test.py, tools/world_checks.py, score/ and lair.pin are byte-identical between validated head826a447cd35d9d7dafe93ab99c28cdb2122101f9 and current head2eb302dc7812a59c5055736812d936709accf500.** Therefore the two local gates at826a447c stand for2eb302dc as directed; no gameplay/menu/save/terminal row rerun is owed for those unchanged bytes.
- Ran only the affected Python harness suites plus owned row-import regression: ci_container_test.py, combo_cadence_test.py, combo_oracle_test.py, combo_request_oracle_test.py and pty_rows_test.py — **50 tests pass**. No full gate was needlessly repeated.
- Preserved cb11's combo/repeat policy and reader registration, cb12's render-only counter/death seam and timing, and all inherited fixtures/goldens.
- Engine74b89744e8f8a4ed01539b2fe814daf819b9abfc; wolf0.2.35/cf0c13d, lupin0.1.56/294d626, std2386522e. Complete pairs staged; twice-read identities/digests in notes/cb13-evidence/inputs-twice.txt. Contract/rules/docs and cb11b handoff read. README and KEYS retain the corrected consumed-cadence description.
- R-cb13-1 A/R-cb13-2 A confirmed. R-cb13-3 keeps historical --no-title straight into play (first-run ~/.cub/save); --menu skips only the title. Normal start is title -> fire -> play. Existing gameplay/lair.conf/memory-probe arguments unchanged. cb15 extends CUB6 beneath these fields after rebasing.

## Evidence index

- `7b93e71c`, `e19a7b60`: canonical save wrapper/registry and migration/refusal tests.
- `644a1ae4`, `bc568e57`: menu, typed paths, metadata, replay return, safe labels and post-replacement index errors.
- `f991d2b4`: bounded save witness/wide fixture; `40ca2b18`: README-only refresh; `ebbf5ed4`: keyboard/replay contracts; `e8a29e49`, `cd418586`: retained inputs/plant, menu goldens/live evidence.
- `a03bd96b`, `2ca3a009`: sound helpers enter via --no-title and await alternate-screen entry before sampling WAVs. Preparation/probing precedes that boundary; the12-WAV assertion is unchanged.
- `cd8905e6`: exact CI diff showed only appended recorded-clock/Fallen comments. Both ghost footers removed, Fallen derives from ghost-death, and embedded date comments are ignored. Deterministic live ending summaries remain. The exact comparator is unchanged; notes/cb13-evidence/archive-ci-diff.patch retains the red diff.
- `2eb302dc` retains targeted archive/sound/Playback/reader proof in notes/cb13-evidence/archive-linux-green.log; menu/typed-path/title/commit receipts remain in notes/cb13-evidence/menu-pty.log.
- **Validated execution head826a447cd35d9d7dafe93ab99c28cdb2122101f9:** Mac marker0, CB13_MAC_FINAL_EXIT0 at2026-10-28T07:41:45Z; Linux marker0, CB13_LINUX_FINAL_EXIT0 at08:05:55Z. /Users/mfwolffe/lanes/cb13/mac-final.log and /Users/mfwolffe/lanes/cb13/mac-final.exit; /home/mfwolffe/lanes/cb13/linux-final.log and /home/mfwolffe/lanes/cb13/linux-final.exit. Mac covered builds/checked, sound/menu/title/commit/cb10/cb12/cb11 readers, archive equality, memory and full goldens; Linux covered full check-linux/check-perf. These gates carry to current2eb302dc only because the execution/owned-row bytes above are identical and the coordinator explicitly authorized that carry-forward.
- Prior hosted run40650836805 attempt2 was cut by the40-minute Linux limit, not reported as a program green. New trunk supplies60-minute Linux/macOS limits and cb11b's hosted-macOS late-input harness correction.
- Plant draft cub#67,66ba0705, never merge: test_cb13_cub5_fixture_migrates_byte_for_byte_to_cub6 ... FAILED (trap(assert)), zero rejected/unsupported; fix/test committed first. notes/cb13-evidence/plant-migration.log. Plant CI40622577084 was read once; no dispatch/wait.
- One force-with-lease push for this announced rebase. Current-head CI **40747420928** read once immediately, queued. No CI wait or lane-applied label. Coordinator will label full-matrix at this head and watch the hosted legs.
- Requested audit ran once at2eb302dc from the org checkout, exit1: **AUDIT FAIL (footprint: module)**. Fast-forward ancestry, module paths, five sections,15 cited shas, attribution, PR head and process checks pass. The only holds are in-progress CI/no green tier yet. No orphaned lane processes. No second audit at this head.

## Done-when

- [x] Named CUB6 wrapper, exact CUB5 migration, non-destructive import, atomic strict registry and named errors.
- [x] All menu items, seed/wolf prompt, typed paths, real replay player/Esc return, both tiers/sizes.
- [x] Clock-independent archive bytes against committed data; mtime dates; sound entry/readiness fixed.
- [x] All announced rebases once each; upstream combo/counter/death/reader integrations preserved.
- [x] Both local gates green at826a447c and explicitly carried to byte-equivalent2eb302dc;50 affected Python tests green.
- [x] Current head pushed once and CI read once; note contains both execution/current shas.
- [x] Requested current-head audit run once; exact result/CI-only holds recorded above.
- [ ] Current hosted PR/full-matrix verification: coordinator watches; never presumed green.


Ledger: cb13 | main menu and saves | module | CUB6 name/played_ms | plant cub#67 | rebase991cc704 | local gates826a447c stand at2eb302dc | hosted verification pending.

Issues to file/close: none. Materialise this five-section note under notes/ at merge; no Markdown report file was written by this lane.

