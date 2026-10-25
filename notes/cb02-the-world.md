# cb02 — the world

Materialised from cub#14 (head c3d968d5, merged 2026-10-25) at the merge; evidence under `notes/cb02-evidence/`.

## Prediction
- `82bac83`, `f72898d`: predictions committed before the original scope and before the play-driven additions.
- All 50 seeds reach every den, exit and cache: 150 area rows, 300 cache destinations. Longest straight path/bank runs are 7/5 cells (bar 12); nearest initial foe is 34 cells (bar 30).
- Witness save: 172 bytes, below the predicted 512 bytes but slightly below the 180–300 estimate. Hawk tell: 18 ticks, as predicted. Both hosts/backends have identical goldens; no predicted dusk mismatch occurred.
- 2,389 added / 84 removed wolf lines, net 2,305; the expanded 2,800-line estimate was high.

## Forbidden
Original game work, wolf-std and pinned lair only. No engine, pin or workflow changes; no merge, label, tag, release or issue action. Private planning and user configuration untouched. macOS memory refusals were retried after three minutes, never bypassed. Linux ran in the container on CPUs 4–7 under the assigned lock. Interrupt witnesses type byte 03 through lair's pty runner, never a signal script. All test saves are lane-owned paths.

## Inputs verified
- Base `56f11cf`; engine `aa6c4dc0bc5071d3c07121451d913a8837cd2a6a`, unchanged.
- wolf 0.2.35 `cf0c13d38479f444b69bb8356ad5709d07eff323`; lupin 0.1.56; std `2386522eb059cca5a84108562c2c0a0e72345d34`. Both complete host archive pairs verified; all four digests read twice in `notes/cb02-evidence/digests-twice.txt`.
- Design bible §§1–8, 13, 18–19; cb01/cb01b handoffs, including the unchanged cb03 HUD paragraph. Pack's own `trail.path` centre/width model is the permitted meander reference.
- R-cb02-1 A, R-cb02-2 A and R-cb02-3 A recommended and implemented, not decided by this lane.

## Evidence index
- `f50b9c1`: seeded graph, gate fix, area art, density, pickups/caches, hawk, validated save transaction, replay snapshots and opening. Goldens regenerated because terrain, encounter placement, visible pickup semantics, scene frames and state snapshots changed; old encounter scripts were regenerated as real down-path fights, not renamed empty scenes.
- `a2cb52f`: README-only refresh.
- `d224e8e`: reject conflicting saved-journey seeds, with file/replay assertions; no frame changes.
- `c3d968d`: retained logs, census, measurements and golden hash recipe.

| gate | macOS arm64 | Linux x86-64, locked container 4–7 |
|---|---|---|
| fmt / checked tests | 136 pass, zero skip/unsupported | same |
| native/release selftest and goldens | 43 scripts × two tiers + sheets, 87 directories | byte-identical |
| live pty rows | all 12 pass | all 12 pass |
| gameplay, save failure/roundtrip and mark persistence | both backends pass | both backends pass |
| 80×24 rich/plain average | 106 / 105 µs | 179 / 178 µs |
| 200×60 rich/plain average | 464 / 461 µs | 775 / 774 µs |
| latency median / p90 | 10.4 / 33.3 ms | 13.5 / 13.6 ms |
| idle / 10 s | loud Linux-only skip | 301 switches; repeat 300 |

Complete correctness gates cover source/tool/fixture head `d224e8e` on both hosts. Final head `c3d968d` adds only retained evidence; its playtest binary was rebuilt and selftested. Linux performance was measured at `a2cb52f`, before the CLI-only seed-conflict guard.

All 1,658 golden files, including relative paths, hash to `aba1701db38a96bbc39ab5e214b2e255064450e0c20cef07379720ecc1e651b1` on both hosts. Comparison logs were empty before excluding them. The census is also byte-identical. Evidence is under `notes/cb02-evidence/`.

The gate regression was red before the fix and green after (`notes/cb02-evidence/gate-before.log`, `gate-after.log`): the rightmost cell's fractional span previously aimed at its origin, off-axis. The fix targets the full collision rectangle without widening the lunge. Bite now gives the lunge hint. Thorn glyph/colour pairs are disjoint from labels/walls; every exit mouth has the shadow band.

The 4,869-tick world witness walks the bank → thicket → meadow, parries the hawk, recovers a deliberate death's mark across the edge, and returns by hedge then log. Its explicit 10,000-scent fixture is spent through ordinary den growth; it is a mechanics witness, not a balance claim. Separate encounter scripts use default growth and no injected health/scent; the natural death is replay-verified at tick 573. Save/process and pty witnesses cover quit/resume and self-contained resumed records.

Named negative drafts, intentionally left open:
- #11 `4e4c32e`: run **40223353951**, `test_cb02_seeded_centres_are_walkable_and_meander ... FAILED (trap(assert))`.
- #12 `10ab62f`: run **40223358491**, `AssertionError: cut write lost old save`.
- #13 `89931f1`: run **40223360232**, `goldens: world-meadow-plain DIFFERS`.

## Done-when
- [x] Connected seeded areas, all four dens and both shortcut round trips.
- [x] Meanders, safe initial encounter spacing, visible scent pickups and finite guarded caches.
- [x] Hawk tell/parry/dodge, distinct hazard/exit art and opening scenes on both tiers.
- [x] Validated save/resume, cut-write preservation, busy-stage preservation and cross-area marks.
- [x] Real terminal restoration on quit/03 mid-save and named write failure; resumed-record agreement.
- [x] Both-host/backend goldens and 50-seed reachability/density/caches; slack-1 performance.
- [x] Three named CI plants red and retained open.
- [x] README current; no engine change.
- [x] Final-head playtest binary: `/Users/mfwolffe/lanes/cb02/cub/target/cub`, SHA256 `282ae7bc81d09736c4de020b629e2ac89cfcc2ecb78137a486c97a1888277d46`.
- [ ] PR-tier approval is for the coordinator; the lane reads CI once immediately after opening, never waits or labels.

Footprint: module

## Follow-ons
No issue action was taken. The existing physical-terminal glyph/keyboard measurements and engine enhanced-keyboard/perf-idle pipeline follow-ons remain. No new compiler issue was found. Later-area gates, bosses, ghost display, music, difficulty selection and consumable-use controls are deliberately not claimed here; cache inventory already persists and is shown at dens.

### Note — cb02, the world

This is the complete note for materialization as `notes/cb02-the-world.md`; no lane-report Markdown file was written.

The forest now has connected ground rather than an open-ended tutorial approach. Each seed changes the paths, bank, trees and den positions while the graph holds. Thorn hazards have their own ink and glyphs, treeless approaches and exit shadows. Four dens share one growth/rest/death rule. The mark belongs to its area and survives a normal exit; quitting during a pending write preserves the previous journey rather than a partial replacement. Unknown or corrupt saves fail by name. A stale/concurrent `.pending` is not deleted behind another writer's back.

Enemy groups start down the route. Kills leave timed scent pickups; a distant kill is not automatically credited. Side branches end in guarded, finite hollows/burrows. The meadow hawk stops its shadow before the committed strike; its airborne shadow is not a solid body, so dodge can escape it. The opening is original timed art, and all skips and resumed initial state are in the replay.

Reservations for cb04: Old Snag's clearing in Bramblehold and the scent-marked tree in Larkmeadow, with no boss or later-area access yet. Ember's warning is story state separate from the Shingle combat fox. The score hooks are named, but no audio is played.

cb03 draft — the HUD and the score:
1. Wire lr01's cues and the reserved area/den/shortcut/cache/scene hooks to the original score; keep playback deterministic and terminal restoration intact.
2. Preserve the existing HUD handoff verbatim: “build the larger posture-band HUD, lock-on reticle, water mouthfuls and area name alongside the score. Keep this pass's always-visible scent counter and den-only spending, make death loss/recovery clear, and prove small/wide/resized frames on both tiers. The area/boss/den music and the engine mixer remain the score lane's work, not this feel pass.”
3. Exercise the saved/resumed den and both-tier entry/scene frames in small, wide and resized terminals. Do not turn cache inventory into an unplanned field HUD.

cb04 draft — the boar and the lynx's gate:
1. Put Old Snag in the reserved clearing: tell, straight charge, brush-breaking arena, poise/parry/lunge answers and second phase, with actual replay witnesses.
2. Fill the scent-marked tree's night gate toward the Teeth without changing the fixed shortcut identities; extend the versioned save deliberately for bosses/NPC choices.
3. Use the named scene hooks for the first den, elk, Old Alpha's offer and endings as those moments become playable; the opening mechanism already records skips.
4. Carry cross-area death marks, finite cache flags and self-contained resumed/death records into boss and ghost work. Add held-consumable use when its combat rules arrive; do not imply the current pouch counts already cure bleeding.
5. Keep both-tier posture sheets, failed-write preservation, real pty exits and 50-seed route/caches checks as gates.

### Fifty-seed reachability

Each count is reached/required den + incident exit + cache destinations. Every area has two reached caches; nearest foe is the minimum across its dens. Distances and straight runs are cells.

| seed | Shingle | Bramblehold | Larkmeadow | max straight | bank | nearest foe |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 5/5 | 8/8 | 5/5 | 5 | 2 | 35 |
| 1 | 5/5 | 8/8 | 5/5 | 5 | 4 | 37 |
| 2 | 5/5 | 8/8 | 5/5 | 6 | 4 | 36 |
| 3 | 5/5 | 8/8 | 5/5 | 5 | 2 | 39 |
| 4 | 5/5 | 8/8 | 5/5 | 6 | 3 | 41 |
| 5 | 5/5 | 8/8 | 5/5 | 6 | 4 | 38 |
| 6 | 5/5 | 8/8 | 5/5 | 5 | 2 | 39 |
| 7 | 5/5 | 8/8 | 5/5 | 5 | 3 | 39 |
| 8 | 5/5 | 8/8 | 5/5 | 6 | 3 | 38 |
| 9 | 5/5 | 8/8 | 5/5 | 6 | 3 | 35 |
| 10 | 5/5 | 8/8 | 5/5 | 6 | 3 | 37 |
| 11 | 5/5 | 8/8 | 5/5 | 7 | 3 | 35 |
| 12 | 5/5 | 8/8 | 5/5 | 5 | 3 | 36 |
| 13 | 5/5 | 8/8 | 5/5 | 5 | 3 | 37 |
| 14 | 5/5 | 8/8 | 5/5 | 6 | 3 | 40 |
| 15 | 5/5 | 8/8 | 5/5 | 6 | 3 | 36 |
| 16 | 5/5 | 8/8 | 5/5 | 5 | 4 | 37 |
| 17 | 5/5 | 8/8 | 5/5 | 6 | 4 | 40 |
| 18 | 5/5 | 8/8 | 5/5 | 7 | 4 | 38 |
| 19 | 5/5 | 8/8 | 5/5 | 7 | 3 | 38 |
| 20 | 5/5 | 8/8 | 5/5 | 5 | 3 | 37 |
| 21 | 5/5 | 8/8 | 5/5 | 6 | 4 | 37 |
| 22 | 5/5 | 8/8 | 5/5 | 6 | 3 | 36 |
| 23 | 5/5 | 8/8 | 5/5 | 6 | 3 | 36 |
| 24 | 5/5 | 8/8 | 5/5 | 7 | 3 | 38 |
| 25 | 5/5 | 8/8 | 5/5 | 7 | 3 | 40 |
| 26 | 5/5 | 8/8 | 5/5 | 5 | 5 | 38 |
| 27 | 5/5 | 8/8 | 5/5 | 4 | 4 | 39 |
| 28 | 5/5 | 8/8 | 5/5 | 6 | 4 | 38 |
| 29 | 5/5 | 8/8 | 5/5 | 6 | 3 | 38 |
| 30 | 5/5 | 8/8 | 5/5 | 6 | 3 | 39 |
| 31 | 5/5 | 8/8 | 5/5 | 5 | 4 | 38 |
| 32 | 5/5 | 8/8 | 5/5 | 5 | 3 | 35 |
| 33 | 5/5 | 8/8 | 5/5 | 6 | 3 | 38 |
| 34 | 5/5 | 8/8 | 5/5 | 7 | 3 | 39 |
| 35 | 5/5 | 8/8 | 5/5 | 5 | 3 | 35 |
| 36 | 5/5 | 8/8 | 5/5 | 6 | 3 | 39 |
| 37 | 5/5 | 8/8 | 5/5 | 6 | 3 | 36 |
| 38 | 5/5 | 8/8 | 5/5 | 6 | 3 | 39 |
| 39 | 5/5 | 8/8 | 5/5 | 7 | 4 | 38 |
| 40 | 5/5 | 8/8 | 5/5 | 6 | 3 | 41 |
| 41 | 5/5 | 8/8 | 5/5 | 5 | 4 | 39 |
| 42 | 5/5 | 8/8 | 5/5 | 5 | 3 | 39 |
| 43 | 5/5 | 8/8 | 5/5 | 6 | 3 | 37 |
| 44 | 5/5 | 8/8 | 5/5 | 6 | 3 | 39 |
| 45 | 5/5 | 8/8 | 5/5 | 6 | 3 | 35 |
| 46 | 5/5 | 8/8 | 5/5 | 5 | 3 | 34 |
| 47 | 5/5 | 8/8 | 5/5 | 6 | 3 | 35 |
| 48 | 5/5 | 8/8 | 5/5 | 5 | 3 | 39 |
| 49 | 5/5 | 8/8 | 5/5 | 5 | 5 | 37 |


