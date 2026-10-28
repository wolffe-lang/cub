# cb12 — cb12: close the eyes and count every scent

_Materialised from the body of cub#74 at the merge (`5f1356ca`)._

## Prediction

Prediction committed before implementation (`2d74efe8`, originally `90a9e23e`; `notes/cb12-prediction.txt`). Expected the unchanged30-tick fade, then a red original seven-row FALLEN letterform and the opening eyes reversed; deterministic every-integer batches ending within20 simulation ticks without delaying currency. The strokes were doubled to70×14 cells so the half-closed frame visibly crops the word. R-cb12-1 A implemented. R-cb12-2: partial repaint implemented; neither stretched duration nor dropped frames needed for the1000-gain witness.

## Forbidden

Original game code/art only. No engine/pin/CI/planning/configuration edits, helper agents, labels, merges, tags, releases, issue actions or attribution trailers. No other lane's gameplay functions changed. Mac work ran under the shared atomic lock and8GiB gate; the one-time cb15 acquisition yield was observed. Linux uses the assigned12–15 flock and the repository's own container runner. All save/archive/probe paths are lane-owned; the personal play save and MLX server were untouched.

## Inputs verified

Base `eb34a399`; rebased once onto announced cb10 trunk `1497b5d3`, preserving its water/input/floater fixes and independent pty rows. Engine remains `74b89744e8f8a4ed01539b2fe814daf819b9abfc`; complete pinned wolf0.2.35/lupin0.1.56 archives and std`2386522e` staged on both hosts. Contract, shared rules, playtest items5/6, bible, game specifications and cb02/cb03/cb04/cb07 notes read. Save schema remains CUB5: presentation state is transient, not a persistent currency field. README read and updated in its own commit (`6efdf50c`).

## Evidence index

- `6d08d417`, `52900dde`: death schedule, original word and exact reversed opening eye frames.
- `c49bcbb8`, `34d3f5fa`: every integer rendered; cached underlay and counter-only CUP/SGR repaints, with the last integer drawn through the ordinary full-frame renderer.
- `863de471`, `251d34c4`: one-shot input remains one-shot during a count; saves read immediate currency, never the animated number.
- `001fe66b`, `a6bab499`: two-tier word/half-closed/closed goldens and every-integer gain/spending sequences, independent styled-glyph oracle and replay determinism row.
- `b84acfb0`: existing reset/recovery tests press an ordinary skip after the minimum hold; the deliberate death-card row asserts FALLEN instead of the retired numeric overlay.
- `5f1356ca`: combined-head witnesses/goldens regenerated after cb10. `notes/cb12-evidence/golden-keys-after-cb10.txt` names every changed row:776 existing files changed,556 added,0 removed; all other existing golden bytes, art sheets and PCM goldens unchanged. The death-affected world routes and den checkpoint record their skip explicitly.

The fatal tick, scent mark and ghost/archive write remain immediate and unchanged. Only the respawn moves: word from death age30, keys consumed from50, closing eyes through380, automatic wake381. Normal live play and production `--replay` retain recorded keys; headless `--script` fixtures/walkers skip after the minimum hold unless `--full-death`/`# full-death` requests the full card. No extra simulation/audio/save/replay ticks advance the counter. Mid-count gains retarget from the last drawn integer; den spending counts down identically.

Every gain1/8/30/300/1000 is checked in both directions, with exact final ticks and no skipped integers. The actual binaries render30 gain integers and98 gain/spend integers per tier; every glyph/style frame equals a differently sampled production replay. Terminal-model tests cover shrinking/growing digit widths; live pty rows cover both tiers and80×24/200×60, final full-frame parity, full death eyes and one-shot keys during counting.

Measured1000-gain maximum batch cost on nomad release (50 integer frames/tick):

| tier/size | before: render+flush sum | after: whole-batch wall time | after ticks/late frames |
|---|---:|---:|---:|
| rich80×24 |10.341ms|0.795ms|20/0|
| rich200×60 |63.673ms|4.263ms|20/0|
| plain80×24 |9.107ms|0.709ms|20/0|
| plain200×60 |66.215ms|3.834ms|20/0|

The after measurement includes the cached underlay, all partial repaints, trace writes and the final ordinary frame; all1000 integers are flushed. Both raw tables are committed under `notes/cb12-evidence/`. The new pty gate requires20 ticks,0 late/catch-up frames and a batch below33.333ms, not merely the same final number.

Plant: draft #65, `cb12-plant-counter`, intentionally red and never merge. Exact local row `src/counter_test.lu::test_cb12_gain_300_renders_first_batch_not_target ... FAILED (trap(assert))`, exit1 on unchanged base game code; retained in `notes/cb12-evidence/plant-counter.log`. Immediate plant CI read:40619258238 in_progress; no CI wait/dispatch.

Final-head local gates at `5f1356ca57b890f9e2236eba56adac4f0bae6020`: the first Mac attempt passed458 checked tests (0 failed/rejected/unsupported/SKIP), all native/release goldens, every pty row, score-check, both gameplay/census runs (`mac-after-cb10.log:2258,2381`) and the crash-checkpoint/fresh-seed memory gate at4096bytes/tick (`:2427`). Perf then refused to start at7GB free+inactive+speculative (`:2428`, status3). The floor retry's only red was `pty: sound-live FAILED` (`:3492`):12 WAVs existed but its child was `79381 <defunct>`, not a live afplay; the first attempt had observed `/usr/bin/afplay` (`:1573`). Every cb12 row stayed green. Neither attempt's evidence was discarded.

Per coordinator direction, no further whole correctness run: a durable targeted completion reruns `sound-live` alone, then `.lair/tools/perf` and the explicit `perf-idle` status check, under the shared lock and per-stage8GiB floor. Launcher pid88701; `/Users/mfwolffe/lanes/cb12/mac-completion.log`; terminal marker `/Users/mfwolffe/lanes/cb12/mac-completion.exit` (runner pid file `/Users/mfwolffe/lanes/cb12/mac-completion.pid`). If the same preparation race repeats, use cb13's named bounded alternate-screen-readiness wait from cub#72 rather than inventing a different sound fix. Linux final pid135993, `/home/mfwolffe/lanes/cb12/linux-final.log`, marker `/home/mfwolffe/lanes/cb12/linux-final.exit`; the coordinator owns that watch. Main PR CI was read once immediately:40637816418 queued; no CI wait. Lane audit ran exactly once; its last line was `AUDIT FAIL (footprint: module)`, solely for head CI still in progress/no green tier verdict.

## Done-when


- [x] Post-fade FALLEN, reversed eyes, minimum-hold skip; immediate ghost/mark retained.
- [x] Every-integer count, retarget, den spending and immediate saved currency; both tiers.
- [x] Unit, replay, glyph, golden and live terminal rows; zero-drop partial repaint proof.
- [x] Red plant draft retained; README and compatibility documentation current.
- [x] Full Mac checked tests, native/release goldens, every pty row and score-check.
- [x] Final Mac gameplay/censuses and resident-memory gate.
- [ ] Targeted sound-only revalidation and remaining performance stages (durable completion job above).
- [ ] Final Linux correctness/performance gauntlet (pid/log/marker above).
- [ ] Final-head PR-tier green is the coordinator's merge gate; no label requested.

Ledger: cb12 | cub#74 | 5f1356ca | module | death card and scent counter | R-cb12-1 A; R-cb12-2 partial repaint.

No issue filed/closed. Follow-on to file in cub: existing plain HUD health/thorn ink uses palette12, which maps to ANSI bright blue/SGR94; this pass uses verified bright red9/SGR91 for FALLEN and leaves the unrelated palette unchanged.

