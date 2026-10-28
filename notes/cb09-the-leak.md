# cb09 — Reclaim frame scratch and bound tick memory growth

_Materialised from the body of cub#64 at the merge (`55f73933`)._


cb09 — the leak. This body is the five-section note for materialisation as `notes/cb09-the-leak.md`. Complete Linux and Mac gates are green; the two-hour crash-checkpoint soak is flat within the measured budget.

## Prediction

`19e37aa9` recorded the prediction before implementation: a renderer floor near60KB/tick on a fresh seed and further simulation copies raising the copied crash save toward650KB/tick. `6de733a9` committed the measurement before any fix; `d6500224` committed subsystem attribution before the repair. The renderer prediction held; the simulation-copy prediction did not. Idle simulation and bounded ghost history charged0 bytes/tick. The measured crash-checkpoint renderer was much larger than predicted.

The process-side probe drains a real120×40 pty with no keys, `--mute --no-title`, and reads actual simulation ticks from trace output. Saves and ghosts are private disposable copies. Mac reads `ps` RSS KiB×1024; Linux reads `/proc/<pid>/statm` resident pages×the actual page size, so the pinned image needs no procps package. The known runtime-root/string gap in the ledger is not interpreted as free memory.

Before/after resident bytes per actual tick:

| host | journey | before, original1d0680a1 | after |
|---|---|---:|---:|
| Mac arm64 | copied crash checkpoint |1,601,393.668|−2,503.551|
| Mac arm64 | fresh seed7 |41,118.147|−1,100.653|
| Linux x86-64 container | copied crash checkpoint |1,598,552.786|388.209|
| Linux x86-64 container | fresh seed7 |71,929.563|316.293|

The first Mac fresh measurement had abrupt RSS working-set drops; its final interval was62,711.172 bytes/tick. The stable crash budget plant above is preferred to its initial compressed-window endpoint slope786,306.211. These are RSS slopes, not allocator payload counts. The probe fixes the viewport; the original reproduction's wall-time rates are not directly interchangeable with this instrument.

The copied save resumes at its checkpoint in Bramblehold, area1, field450—not at the original player's reported third-region location. Its bytes equal the supplied copy, SHA256 `fc7ae0b94ecef3f348a98950ccc6e8d7e674dbfa3cd33018e184abff04f4e827`.

Two allocation families were repaired:

- **Frame scratch.** `art.render_with` and `art.render_bare` lacked a frame lifetime. Their descendants rebuilt terrain lookup lists (`forest.shape_of`'s orders and `forest.qsin`'s table), sprite/composition lists and HUD plans into the game-long ambient region. The native named-region census charged1,588,592 bytes/frame on the crash checkpoint, of which terrain alone charged1,501,211; the other layers aggregate87,381. Fresh rendering charged55,705. Both render entrypoints now close a scoped `frame_scratch` region. Full-render charge measured0 afterward. The per-layer figures are aggregate charges, not isolated per-function payload sizes.
- **Idle save comparison.** `run_live` rebuilt `journey.encode(s)` every tick just to compare persistent state. The raw encoder charged5,242 bytes/call. With only the renderer repaired, RSS still grew3,022.291 bytes/tick; without trace,3,073.601 estimated at30Hz, disproving trace as the explanation. The live loop now rotates three reused37-word numeric buffers via `journey.snapshot_into` and compares every word with `same_snapshot`, without hashing. Encoding happens when a real save is staged. Stage/commit/cancel tick order, canonical text/checksum, CUB5, slain masks and replay numbering are unchanged. With both repairs the preliminary Mac crash slope was−1,217.325 over821 actual ticks: working-set reclamation, not a negative allocation claim.

The regression budget is **4096 resident bytes/actual tick**, warmup60/end600, with a2-GiB emergency ceiling and120-second timeout. The confirmed post-fix positive envelope is below1KiB/tick (Linux fixed-row worst388.209; two-hour worst adjacent-minute growth573.122); rounding that calibration envelope up to1KiB and allowing4× allocator/OS slack gives4KiB/tick. That is about10.55× the worst fixed-row slope and7.15× the worst minute interval, not four times a negative RSS number. A timeout, missing samples, absent tick progress, premature exit or ceiling breach is red. A steady4KiB/tick leak is not described as flat merely because it fits this regression margin.

**Two-hour run: GREEN and flat**, `soak.log`, direct `CB09_SOAK_EXIT 0` at2026-10-27T23:55:18Z. Crash-checkpoint idle, real rendering with diff bytes discarded, ghosts from the supplied copy. The first post-warmup minute sample is tick1785/RSS10,158,080 at60.009s; the last is tick216045/RSS3,670,016 at7202.007s:214260 measured ticks,−6,488,064 bytes, **−30.281 bytes/tick** overall. Post-warmup RSS stays within3,670,016–11,042,816 bytes with reclamation rather than accumulating growth; worst adjacent-minute positive slope573.122, below4096. The complete log retains all122 JSON records:121 RSS observations including launch,120 of them at nonzero-tick minute boundaries, plus the final summary. No sample was discarded. Runtime9ea9287a, release SHA256 `b8c2064b91a1309c31bfee4092c46dae5b471b629cf5717b26ff34ad47d94d78`; later commits change only Python harness/tests or prose/evidence.

Not reproduced: the171GB death itself (deliberately not repeated), a human walk to the exact unrecorded position, or audible play over two hours. The leak reproduces without sound, loaded ghosts, terminal diff output, foe stepping or a scent trail. No foes-freeze flag was added. PCM/audio assertions remain unchanged in the complete gate.

## Forbidden

No drawings, hitboxes, world shape, foe/boss behavior, movement, score, replay, golden, save schema, engine or pin change. No maintainer save access; only the supplied crash copy was read. No planning-repository or `~/.claude` edits, no package installation, no helper agents, no process-group signals, no maintainer-process stop, no labels/merge/tag/release/issue action, no attribution trailers.

Mac builds/checks run one at a time behind the8-GiB free+inactive+speculative floor. Exit3 when the floor refuses is retained as a resource refusal, not a failed game row. The latest complete runner prints a wait every60seconds indefinitely and retries floor refusals without stopping MLX or the local mk session. Linux uses cores4–7 under its flock, the copied cb08 pinned container recipe and image; nothing of cb08 was moved or renamed. Long jobs have durable pid/log/exit files, and probes kill only their own recorded child with SIGKILL because the original game ignored SIGTERM.

## Inputs, verified

Base6a1db765 (cb08 plus its materialised note); original runtime1d0680a1. Contract, RULES1–10, design bible1/8, DESIGN, cb05/cb04b/cb07/cb08 notes, original reproduction and supplied jetsam record read. Wolf book ownership/regions and ledger chapters read before site investigation. Engine74b89744 unchanged; wolf0.2.35/cf0c13d, lupin0.1.56/294d626, std2386522e, paired archives staged and identities verified by the engine tools. README read against commands, builds, tests and tier placement, refreshed in its own commit, current.

Rulings, recommended and implemented:
- **R-cb09-1 A:** slope in bytes per actual tick, not an absolute-size-only pass.
- **R-cb09-2 B:** process-side probe in tools; allocation ledger diagnostic stays separate from gameplay.
- **R-cb09-3 B, coordinator amendment:** Linux memory gate at tier pr; Mac memory gate in the existing tier-full Mac job. Do not add another Mac job to every PR. The small workflow edit makes this PR cross-cutting; the coordinator applies full-matrix at the final head. The original contract's module guess and both-platform-pr wording are superseded by this amendment.

## Evidence index

- `19e37aa9`: prediction before implementation.
- `6de733a9`: resident probe and before measurements, committed before any fix.
- `d6500224`: allocation census and subsystem measurements.
- `3be0590d`: frame lifetime, exact reusable save checkpoints, three checked regressions.
- `3693439e`: resident gate and actual original-trunk Mac red.
- `7c11c4bd`: README-only refresh.
- `9ea9287a`: diagnostic help and ruled existing Mac full-tier memory row.
- `8cf7a047`: Linux page units without container-package changes.
- `8c117812`: complete stage-fixture repair, retained failures and explicit memory-failure propagation.
- `b765e944`: one-variable repair slopes and durable-job receipts.
- `4d6087f8`: final README-only budget wording check.
- `b9d31817`: Linux green, strict performance,11 byte-equal census pairs and Mac floor refusal.
- `55f73933`: final Mac complete gate and every two-hour soak record.

All evidence below is under `notes/cb09-evidence/` unless an absolute path is named.

**Linux complete gate: GREEN**, source8c117812, `linux-final-2.log`, direct `CB09_LINUX_FINAL_2_EXIT 0` at2026-10-27T22:34:46Z. It passes39 Python tests,422 checked tests with0 failures/rejections/unsupported and0 SKIP lines, both builds/selftests, all committed goldens, every pty row, score goldens and both complete gameplay stages (0 skips). The memory row is GREEN at388.209/316.293 bytes/tick. The inherited performance wrapper defaults to slack3; a separate strict-slack1 run, `perf-strict-linux.log`, exited0 at22:41:09Z: render means285/275µs at80×24 rich/plain and2022/2032 at200×60, under1000/4000; idle301/10seconds; latency median32.6–32.7ms and p90≤33.8, under40/70ms.

**Census bytes unchanged.** The Linux final compares all11 before/after stdout pairs against a binary built from exact1d0680a1: foe-census, den-census, boss-census, crossing-census, hitbox-audit, den-spacing, bends-audit, spurs-audit, encounter-census, strike-census, hud-census. `census/` retains both files in each pair. All11 were independently re-compared after download; all match. Hand spot-check: the hitbox pair contains the same16 aim/gap stands, every landed value true. HUD hash `151d60ab57a3fb9b59c676fb0597764bdca0e426d1dd9bc43f3294607ec8b0ee`; boss hash `4f4604ddff0c78a4882fcaa28674fc977e96d5ef8db89cf44c6983c8b85f06ea`; full hashes in the green log. `git diff --exit-code 6a1db765 -- tests/goldens tests/cases tests/ghosts score src/demo` exits0: no regenerated or removed golden/replay/ghost/score byte.

**Mac complete gate: GREEN**, `mac-final-3.log`, direct `CB09_MAC_FINAL_3_EXIT 0` at2026-10-27T23:29:54Z, attempt6/sourceb9d31817. All39 Python tests,422 checked tests (0 failed/rejected/unsupported,0 SKIP), both builds/selftests, every golden/pty row, score and both gameplay stages pass. The memory rows are−2,503.551/−1,100.653 bytes/tick: crash tick88/RSS5,439,488 →tick605/RSS4,145,152; fresh tick88/RSS3,276,800 →tick609/RSS2,703,360. Negative RSS slopes mean working-set reclamation, not negative allocations. Strict-slack1 render means171/165µs at80×24 rich/plain and1262/1249 at200×60, under1000/4000; latency median≤33.0ms,p90≤33.4, under40/70. Only the expected Linux-only `/proc` idle counter is loudly skipped on Mac. Earlier attempts remain in the log: each status3 floor refusal is retained, not called a game red or a successful complete run. `mac-floor-refused.log` preserves the earlier final2 refusal as well. No memory floor was bypassed.

**The stage-fixture red and repair.** `mac-stage-fixture-red.log` and `linux-stage-fixture-red.log` preserve the initial real Python failure. The existing wrapper test copied check-linux into a synthetic tools tree but omitted new check-memory. The repair supplies that script, retains every ordering/status assertion and adds an explicit failing-memory-row control. All39 Python tests pass afterward. The Linux pre-failure log also preserves both original-source memory-budget reds.

**Plants, draft and never merge:**
- cub#62, `cb09-plant-trunk`,7a6162e9: all src bytes exactly1d0680a1 with only gate/harness additions. Actual local budget reds are in `plant-trunk-mac-budget.txt` and `linux-stage-fixture-red.log`. Immediate once-only CI lookup40592168131 was in_progress.
- cub#63, `cb09-plant-checkpoint`,5458d74f (mutationca89d3f6): compare lengths but omit every saved word. `plant-checkpoint-mac.txt` records `test_cb09_checkpoint_comparison_checks_every_saved_word FAILED(trap(assert))`,1 failure,0 rejected/unsupported. Immediate CI lookup40592269254 was in_progress.
Both negative controls need their eventual CI red recorded by the coordinator and closure unmerged; no label or wait by this lane.

## Done-when

- [x] Prediction and resident measurements committed before repair.
- [x] Subsystem isolation falsifies simulation/ghost attribution and measures renderer/encoder costs.
- [x] Scoped frame scratch and exact reused idle checkpoints; CUB5 and behavior retained.
- [x] Linux tier-pr and existing Mac tier-full resident rows;4096 bytes/tick message and strict failure paths.
- [x] Local original-source budget reds on both hosts and named checkpoint-mutation assertion red; two CI plant drafts.
- [x] Complete Linux correctness+performance green,11 census stdout pairs byte-equal, golden/replay/ghost/score fixtures untouched.
- [x] Strict Linux performance, README review and refresh.
- [x] Complete Mac gate and final Mac crash/fresh slopes.
- [x] Two-hour minute-sampled run completed and inspected flat.
- [x] Final evidence committed/pushed; main PR opened only after those two jobs finish; immediate once-only CI lookup.
- [x] Run lane-audit exactly once at final head; copy its exact last line into hand-back. Coordinator labels/watches CI and closes negative-control drafts.

No issue filed or closed; no engine requirement found. Main PR cub#64, final head `55f73933a49b4a1ef36180b57443ee619fdbbab2`. The immediate once-only CI read found run `40606415222`, queued: https://github.com/wolffe-lang/cub/actions/runs/40606415222 . No label or CI wait followed. The final audit ran exactly once, direct exit1; exact last line **`AUDIT FAIL (footprint: cross-cutting)`**. Source ancestry, attribution, footprint, five sections,16 cited SHAs, PR head and orphan checks pass. Holds are CI still in progress/no completed green tier and the coordinator-owned full-matrix label. Raw audit: `/Users/mfwolffe/lanes/cb09/final-audit.log`. No audit rerun or lane-applied label followed.

