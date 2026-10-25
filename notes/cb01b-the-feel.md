# cb01b — the feel (cub#10, merged at b6db871e)

The lane's report, materialised from the PR body at the merge by the orchestrator (the Codex wrapper writes no Markdown). Evidence under `notes/cb01b-evidence/`. Holds the cb02 draft and a cb03 HUD paragraph.

Footprint: module

## Prediction

`37ae3cb` committed the prediction before implementation. Integer goldens remain byte-identical across both backends/hosts. All game frames moved for the HUD; the heading/posture sheet moved for the silhouette. Starting walk/sneak stay below weasel pursuit. Bite/lunge timings and damage remain unchanged; combo cycling/reset and clipped presentation are witnessed. The predicted 125–145 tests was high: 111 checked tests pass, zero skips. Source delta: 866 added, 122 removed wolf lines. Performance remains under the original slack-1 bars.

## Forbidden

No engine source, pin, CI workflow, private planning, memory or configuration edits. No other game's material beyond the permitted pack arc/aim reference. Wolf-std and pinned lair only. No merge, label, tag, release or issue action. Terminal restoration uses the unchanged engine pty rows, including typed byte 03, never a manual signal script. macOS memory-floor refusals were respected and retried after a minute; Linux ran inside the assigned container under CPUs 4–7 flock.

## Inputs verified

- Base: cb01 head `423bc55f`, rebased onto trunk `4cdc6ec` with its materialized note. That note and its cb02 draft are unchanged.
- Engine `aa6c4dc0bc5071d3c07121451d913a8837cd2a6a`, unchanged. No lair PR.
- wolf 0.2.35 `cf0c13d38479f444b69bb8356ad5709d07eff323`, lupin 0.1.56, std `2386522eb059cca5a84108562c2c0a0e72345d34`. Both complete archive pairs staged by the fetcher; all four digests read twice in `notes/cb01b-evidence/digests-twice.txt`.
- The design bible §§3/4/6/8 and the amended feel contract supply the behavior; pack's pk04/pk06 supply presentation/aim language. `AIM_WINDOW_TICKS=15` is confirmed by pack#33 (`43e2b683`, `notes/pk06b-aim-window.txt`), including latest-opposite event ordering and 48/48 realistic diagonal pty sessions after versus 0/48 before. This is a pty measurement, not a claim about every physical keyboard.
- Physical keyprobe, 2026-10-25, the maintainer's play terminal (`TERM=xterm-256color`): Shift+Space received `20  b' '`, then q `71  b'q'`. The application name was not supplied. It cannot distinguish Shift+Space from Space. `s` is the implemented heavy fallback.

## Evidence index

Each play note has its own dated “the maintainer's word” commit; goldens move in that commit with their reason:
- `130da6f`: invariant two-cell body and four headings × four postures; regenerate silhouette frames/sheets.
- `0d25af0`: 110% walk/sneak, nearest-FP rounding (38→42, 19→21); regenerate motion frames. Starting weasel pursuit 44 still wins; dodge stays three cells.
- `bb80e3e`: eight committed aims, lock override, recent/held arrow memory and byte order; new per-tick aim goldens.
- `9dbf31f`: one-cell bite and three-cell lunge presentation triangles, clipped paths, contact marks; regenerate arc frames.
- `17aacb4`: left/right/forward combo, half-cell lean, two-cell third arc and two-tick head shake; per-tick three-hit goldens, unchanged damage.
- `8a2f045`: `s` heavy, two back-steps, four-cell leap and four-tick fading burst; heavy goldens and physical-key documentation.
- `f97489e`: distinct foe head/body/tail sprites, crouch/flee/stagger and 15-tick death fades; expanded foe/posture/fade sheet and encounter goldens.
- `3f48ed8`: always-visible scent beside compact bars, death loss counter; regenerate HUD frames.
- `aaf4009`: speed-adjusted parry/dodge fixtures, nearest-thorn gate targeting, natural-death re-engagement, native/release semantics and live control witnesses; regenerate only affected encounter cases and add natural-death goldens.
- `6a9de1d`: README-only refresh. `4857d31`: measured aim provenance.

Complete source/tool/test tree at `4857d312cd76b9c8fc957193b984003f246d87ec`; the final evidence commit `b6db871` adds only evidence and its hash recipe. The playtest binary was rebuilt and selftested at that final head. Evidence lives under `notes/cb01b-evidence/`.

| gate | macOS arm64 | Linux x86-64 container, CPUs 4–7 |
|---|---|---|
| fmt, checked-machine tests | 111 pass, 0 skip | 111 pass, 0 skip |
| native/release builds and selftest | pass | pass |
| 30 scripts × two visual tiers + sheets (61 directories) | pass on both backends | byte-identical on both backends |
| nine pty rows | pass | pass |
| gameplay + natural death archive replay | pass, tick 509 | pass, tick 509 |
| 80×24 rich/plain average | 40 / 39 us | 68 / 67 us |
| 200×60 rich/plain average | 275 / 270 us | 425 / 430 us |
| key-to-frame median / p90 | 32.2 / 33.2 ms | 13.4 / 33.3 ms |
| idle in 10 s | loud Linux-only skip | 301 switches (repeat 300) |

The 2,056 golden files, including path names, hash to `fcb9cc9de4a6973eaf8063652136a1724364b8de1543fe3ac56509e1f9fe3820` on both hosts; comparison logs were checked empty before excluding them from the hash. Linux native/release build trees were pruned after the gates; evidence remains.

The feel-controls pty row opens 22 fresh sessions across both tiers: eight aims, lock override, combo and heavy fallback. These injected bytes exercise the real decoder/live loop and restoration; they are not physical-terminal key measurements. Existing quit, interrupt, trap, replay-agreement, den, death and archive-error rows remain intact.

Named CI plants, both draft and left open, never merge:
- cub#8, `555622057d988b99b3267b80915c8102c8c1e9e7`, run **40215384805**: `test_cb01b_sideways_silhouette_keeps_body_cells ... FAILED (trap(assert))`; old east-facing vertical strip. `plant-sideways.log`.
- cub#9, `a9d9cb738fe9a71f36044a948fcf67f51916dc61`, run **40215387860**: `test_cb01b_bite_has_a_travelling_arc_and_returns ... FAILED (trap(assert))`; zero bite travel. `plant-bite.log`.

## Done-when

- [x] Invariant body, directional arcs, three-hit chain and heavy fallback.
- [x] Faster walk/sneak with weasel/dodge bars, foe sprites and scent counter.
- [x] Both-tier sheets and per-tick attack goldens; cross-host/backend equality.
- [x] Named plants retained open; README current.
- [x] Complete macOS `tools/check` (attempt 6) and Linux `tools/check-linux`, with slack-1 performance, at source head `4857d31`. Attempts 1–5 were memory-floor refusals, not application failures; the gates stayed enabled.
- [x] Final-head playtest build and selftest: `/Users/mfwolffe/lanes/cb01b/cub/target/cub`, SHA256 `4ba4dfc3326194f2046f8731b76db697980d504595a72fd09c72ee3271e99094`. `target/cb01b-build-head.txt` names `b6db871e736ec322cda2c0aaa5beeac8506cb037`.
- [ ] `tier pr` is for the coordinator to watch: run **40216649366**, in progress when the required audit read it. The immediate post-open `gh run list -c <head>` returned no row yet; no polling or CI wait. No label.

## Follow-ons

R-cb01b-1 A recommended/implemented: lock overrides arrows. R-cb01b-3 A recommended/implemented: `s` fallback. The heavy proposal is 42 stamina, 15/6/18 ticks, four times bite damage and the existing 30-tick ordinary-foe stagger; reach stays four cells. No harder third combo hit was added and no R-cb01b-2 decision is claimed. Speed rounds the 110% product to the nearest FP unit; all additional tuning is dated proposed in DESIGN.md. The measured 15-tick aim value shares pack's name and behavior, but human play still judges the feel.

Engine follow-on, no lane issue action: enhanced keyboard protocol (CSI-u / kitty) negotiation in `input`, restored on every exit path, with protocol-restore pty tests; then Shift+Space for cub's heavy attack and chords generally. Pinned `input.lu` lines 16–18 and 173 explicitly ignore those forms. The coordinator has the physical probe row. Existing physical font-width measurements and named-application keyboard rows remain owed. No new compiler issue found.

### Note — cb01b, the feel

The note is in the PR body for materialization as `notes/cb01b-the-feel.md`; the lane does not write a Markdown report file.

The cub now keeps one body while turning. Attacks move that sprite rather than draw an attack arrow: bite and lunge remain the original hit envelopes with bounded presentation travel. A crowded encounter can shorten the travel to zero; it never moves the camera or physical body through a foe. Three recovery-window Space presses alternate left/right/forward; the third shakes its head without receiving bonus damage. Heavy is available now on `s`, with a two-step gather, longer leap and fading punctuation burst. Shift+Space cannot be distinguished on the measured terminal and needs the separate engine protocol work.

The weasel/fox now have body sprites and posture tells, with both-tier sheets for every phase and the death fade. The same rule is written in ART.md for future foes and bosses. Scent is visible all the time, changes on kills/recovery and is named on the death card; only the den spends it. The larger HUD is not silently built here.

The speed change moved the first weasel's crouch 42→40 and attack 54→52; the fixtures now press parry/dodge two ticks earlier, without widening either window. The nearest-thorn correction prevents a point-blank southward lunge missing an off-axis centre point. The natural-death witness re-approaches the fox after its second retreat and replay-verifies the resulting death at tick 509. No old replay score is silently reused.

cb03 HUD paragraph: build the larger posture-band HUD, lock-on reticle, water mouthfuls and area name alongside the score. Keep this pass's always-visible scent counter and den-only spending, make death loss/recovery clear, and prove small/wide/resized frames on both tiers. The area/boss/den music and the engine mixer remain the score lane's work, not this feel pass.

cb02 draft — the connected world and persistent journey (unchanged):
1. Build the fixed area graph around the now-open southern edge; fill from the seed while guaranteeing passable connections and den access. Bramblehold first, then the meadow and the first shortcut back to the Shingle.
2. Add versioned, validated save/resume for seed, default difficulty, growth, water progression, den, opened shortcuts and world/story flags. Preserve the previous save on interrupted/failed writes; unknown/corrupt data is a named failure, not silent reset.
3. Carry this pass's den/growth/flask/death rules through transitions rather than reimplementing them. Decide how a dropped mark is stored across exits; recommend persisting its area, position and scent with the rest of the journey.
4. Add the third ordinary foe, the hawk, with a stopping shadow tell and its parry answer; keep fox story identity separate from the Shingle combat preview.
5. Add dusk keyframes and area art on both tiers, shortcut feedback, and persistence-aware den screens; make every new number a dated proposal.
6. Prove graph reachability across seeds, shortcut round trips, save round trips and failure preservation, cross-area mark recovery, both-backend/host goldens and terminal restoration. Plant an unreachable route, lost save state and wrong-tier frame as named CI failures. Keep the following boss/ghost and score lanes separate.

Audit at hand-off: direct exit 1 (`/Users/mfwolffe/lanes/cb01b/audit.log`). All footprint, ancestry, attribution, PR-section and cited-sha checks pass. Outstanding: CI has not finished, and the playtest worktree is deliberately retained at `/Users/mfwolffe/lanes/cb01b/cub` so its binary remains runnable. No orphan processes were found.

