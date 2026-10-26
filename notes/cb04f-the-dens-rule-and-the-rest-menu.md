# cb04f — the dens' rule and the rest menu

_Materialised from cub#46's PR body at the merge (27b5c301); the lane's wrapper could not write Markdown notes._

Game-owned world state, checkpoint/replay data, rest scene, regression tooling, docs and goldens only. No engine, pin, CI or shared engine tooling change. The wrapper does not write Markdown report files; this is the full five-section note for materialization as `notes/cb04f-the-dens-rule-and-the-rest-menu.md`.

## Prediction

`5b62a1f` committed `notes/cb04f-prediction.txt` before implementation, on trunk5b10fec (game code7e2c6a77). The checked `test_cb04f_slain_survive_path_and_log` and live `den-world-memory` row failed on unchanged trunk behavior. `notes/cb04f-evidence/cb04f-trunk-test.log` records the checked red; `pty-trunk-red.log` records the semantic pty red. The ledger centre test also failed on trunk.

The prediction held: 50 seeds at fields80/200 give initial live counts by area **[9,10,11,5,5,5]**. The controlled cleared-world census is explicitly a state-fixture census, not 100 played victories. Clear Shingle=0; Bramblehold=10; path return before9/after0; open-log return before9/after0; rest and return9 in both. Bad returns before200/after0; zero skips. The separate checked and pty witnesses really kill through ordinary combat keys and traverse both routes without an intervening rest or death.

Rendered ledger outer borders are7..46,15..64,42..91 at80×24,120×40,200×60. Using screen-edge coordinates, the measured centres are **(27,12), (40,20), (67,30)**. Top edges1,7,17; sizes40×22,50×26,50×26. No clamp is needed at any of the required sizes. Placement clamps to the first/last fully visible column when needed.

## Forbidden

Original game code and art only; no other game's implementation, assets, text or music. No lair change or `lair.pin` change; no CI change, label, merge, tag, issue action or package installation. No planning-repo or user-configuration edits. No attribution trailers. No sibling worktree modified. Mac heavy jobs use the lane's owned HOME/TMPDIR and scripted8GiB free+inactive gate, retrying after180 seconds without lowering it. Linux gauntlets use the8–11 flock/taskset in `localhost/pack-ci:fbee7e864f7dbee6`; long work is detached with pid, log and exit marker. No process-group signalling. The two clean plant worktrees were removed by their exact paths; the Mac play worktree remains for acceptance.

## Inputs verified

Contract, verbatim playtest notes, RULES1–10, preceding cb04a/cb04d notes and the named design/key/source/harness paths read. Base5b10fec carries code7e2c6a77. Engine `57870143ebbb4806b8bee40379e8c6e781f50842`; wolf0.2.35/`cf0c13d`; lupin0.1.56 (version-line identifier294d626; release pin28547b4324524d5477a6e54e4f6888462461a21f); std `2386522eb059cca5a84108562c2c0a0e72345d34`. Both-host identities and the pinned manifest were read twice in `notes/cb04f-evidence/inputs-twice.txt`. Archive fetchers verified the complete wolf/lupin pairs against the pinned digests: Mac wolf `240b84d079b1b9a0d88681ac08fca4816f84778e2d6c94c435ceb2dd6a5f042a`, lupin `9133bfdbb95f6a18745439bf0b2b5280860a5bfeaf9ae038ea120a72d58f7687`; Linux wolf `4cc4045bbbb605c07835bc4f32685953c784eeef4cd3139a48b457dfc90dad1a`, lupin `ad703550ac4787e8e4bb26989d591a731410274d7332f2b4e8b9a64c878822cc`.

## Evidence index

- `6ef1358`, `27cc4f5`: baseline checked/pty failures and controlled 100-journey census.
- `ab2effa`: per-area ordinary-foe masks, retained expiring scent/meat, global rest/death reset, checked coverage.
- `7c1b50b`, `eccc9ff`, `bbed904`: schema5 slain masks, canonical schema4 migration, appended replay slots, old journey3 compatibility, shipping-binary migration/reload checks.
- `c3e2ba4`, `851520b`, `b7ed0ae`, `c8802da`, `788973f`: left-centred ledger, intact compact vignette/labels, no renewed corpse fade, rendered-border measurement.
- `e942add`, `a72f515`: design/art docs and separate README refresh. KEYS unchanged: no key changed.
- `77703f2`: Linux release/native matching goldens, rich/plain, including all three ledger sizes/states. `notes/cb04f-evidence/ledger-centres.txt` measures actual borders; `golden-sha256.txt` inventories the files.

R-cb04f-1 A implemented: living wounded foes heal and return to their seeded places on re-entry. R-cb04f-2 A implemented: death's last-den respawn resets every area's ordinary foes, including a save taken during the death card. Beaten bosses remain beaten. Ordinary-foe ordinals do not shift when a boss disappears.

R-cb04f-3 A recommendation, implemented: checkpoint saves carry the six slain masks; resume at the last den is not a rest. Schema4 validates canonically/checksummed and migrates with empty masks; schema1/2/3 remain named `save_version` failures. New recordings write journey4/36 values; old journey3 recordings remain readable. Pending loot keeps its original simulation-tick expiry across area travel, and taken loot never reappears. Unclaimed loot and wounded-foe transient state are not saved, as before; reload creates no replacement drops. Rest/death clears loot globally. No wall-clock dependence.

Plants, local module reds on macOS checked (each exit1, no rejected/unsupported rows): draft PR #39 `cb04f-plant-area-reset` at4cb7d35 makes `test_cb04f_slain_survive_path_and_log` fail while the centre test passes; draft PR #40 `cb04f-plant-ledger-right` at8a543ef makes `test_cb04f_ledger_centre_at_three_sizes` fail while the path/log test passes. Logs: `notes/cb04f-evidence/plant-area.log` and `plant-ledger.log`. No plant CI dispatch; the orchestrator reads the named local reds and closes the drafts.

Final local gates:

- Linux: `notes/cb04f-evidence/linux-gate.log`, exit0 at23:20:37Z. Exact final game-source hashes match `source-sha256.txt`. Format,291 checked tests, both builds, selftest, both-backend/all-case rich/plain goldens, score checks, all pty rows, both gameplay gauntlets, den/gate/doorway/foe censuses, render and idle/latency gates pass. Unit and gameplay skips0.
- Mac: `/Users/mfwolffe/lanes/cb04f/mac-gate.log`, exit0 at23:30:48Z, built once at final head27b5c301. Same full gate passes with291 tests and zero unit/gameplay skips. All3195 committed golden files are unchanged after both backend checks. The two idle probes loudly SKIP because macOS has no `/proc`; the actual Linux idle measurement passes at300 switches/10s. Mac latency passes; no floor was lowered.
- Extra Mac strict checked command (`--no-native-fallback`) passes all8 focused tests; `notes/cb04f-evidence/mac-focused.log`.

## Done-when

- [x] Prediction committed before implementation; required checked and live pty trunk reds retained, then green.
- [x] Slain foes persist across path/door/shortcut changes; living wounded foes heal/home; global rest/death reset; beaten bosses permanent.
- [x] Waiting scent/meat retain expiry across travel; no double collection; finite caches/springs unchanged.
- [x] Save/replay decision implemented; schema4 migration and old journey3 compatibility covered; malformed masks rejected.
- [x] Before/after census over50 seeds and both fields; cb04a den/gate and cb04d doorway/foe censuses retained.
- [x] Measured ledger centres and goldens at80×24,120×40,200×60, rich/plain; staged/confirmed purchases unchanged.
- [x] Both plants named red locally, pushed as draft PRs #39/#40; clean plant worktrees removed.
- [x] DESIGN/ART updated; KEYS unchanged; README refreshed in its own commit.
- [x] Final head pushed and PR#46 opened; CI read once immediately: run **40420539970**, in_progress. No CI wait or label.

Final head **27b5c301d4bab2a6b5af7af74f4525084d467d22**. Play binary **`/Users/mfwolffe/lanes/cb04f/cub-play-27b5c301`**, SHA256 `55b3a21b81ff7d1d28aae8abc00ba6a9fa86f03f0e6535f72f2e56083675d942` (identical to the final release build):

```sh
HOME=/Users/mfwolffe/lanes/cb04f/home TMPDIR=/Users/mfwolffe/lanes/cb04f/tmp /Users/mfwolffe/lanes/cb04f/cub-play-27b5c301 --save /Users/mfwolffe/lanes/cb04f/play.save --ghost-dir /Users/mfwolffe/lanes/cb04f/play-ghosts
```

Completed Linux build outputs were removed from `/home/mfwolffe/lanes/cb04f/cub/target`; host logs and the canonical census evidence remain. Mac worktree/binary are retained for play acceptance.

Audit run once at the final head, direct exit1; last line **`AUDIT FAIL (footprint: module)`**. Log: `/Users/mfwolffe/lanes/cb04f/audit.log`. Holds are only CI still in_progress/no green tier yet, and the intentionally retained Mac play worktree. Ancestry, footprint/paths, attribution, five sections, cited shas, PR head and orphan checks pass. No issue filings or closures recommended. The orchestrator closes draft PRs #39/#40 and watches run40420539970.

