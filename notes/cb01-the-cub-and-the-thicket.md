# cb01 — the cub and the thicket (cub#7, merged at 423bc55f)

The lane's report, materialised from the PR body at the merge by the orchestrator (the Codex wrapper writes no Markdown). Evidence under `notes/cb01-evidence/`.

Footprint: cross-cutting

## Forbidden

Original game work; wolf-std and pinned lair only. No engine edits, pin changes, labels, tags, releases or issue actions. The private planning checkout and user configuration remain untouched. macOS memory gates stayed enabled; Linux ran in the container on CPUs 4–7 under the assigned lock. SIGINT witnesses use the engine pty's byte 03 only.

## Inputs, verified

- Base cub `ed3d8f06`; lair `aa6c4dc0bc5071d3c07121451d913a8837cd2a6a`, unchanged.
- wolf 0.2.35 (`cf0c13d38479f444b69bb8356ad5709d07eff323`), lupin 0.1.56 (archive revision `28547b4324524d5477a6e54e4f6888462461a21f`, version-line pin `294d626`), std `2386522eb059cca5a84108562c2c0a0e72345d34`. Engine fetchers and identity gates verified both host archives.
- wolf archive SHA256: macOS `240b84d079b1b9a0d88681ac08fca4816f84778e2d6c94c435ceb2dd6a5f042a`; Linux `4cc4045bbbb605c07835bc4f32685953c784eeef4cd3139a48b457dfc90dad1a`.
- lupin archive SHA256: macOS `9133bfdbb95f6a18745439bf0b2b5280860a5bfeaf9ae038ea120a72d58f7687`; Linux `ad703550ac4787e8e4bb26989d591a731410274d7332f2b4e8b9a64c878822cc`.
- Design bible §§2–8 and cb00's handoff are the gameplay inputs. New proposals are dated in `docs/DESIGN.md`.

## Prediction

Committed before implementation as `d99abaa` (`notes/cb01-prediction.txt`). Scored 4/5 at the stated outcomes, with the line estimate low:

| prediction | measured |
|---|---|
| integer simulation should keep host goldens identical; fox feint likeliest first mismatch | no mismatch on either backend or visual tier; the conditional fox hypothesis was not exercised |
| parry ages 0 and 8 succeed, age 9 fails | 2/3 at those edges; exhaustive ages 0–9 give 9/10 |
| weasel crouch to bite: 12 ticks | 12 ticks, 400 ms at 30 Hz |
| idle 30–34 wakes/s, latency median below 34 ms, within pack's bars | Linux 30 wakes/s; median 13.3 ms, macOS 10.9 ms; all render and latency bars pass at slack 1 |
| about 1,100 added wolf source/test lines | 1,388 inserted, 25 removed: net 1,363; 26% above the insertion estimate |

## Evidence index

- `fb20b5f`: combat, stamina, foe perception, scent, growth, death and the gate, with timing/mark unit witnesses. Movement goldens regenerated for the open approach and exact half-speed sneak.
- `c5c3550`: encounter/posture rendering, death archives, semantic replay gates, pty extensions, performance CI. Both-tier goldens regenerated for visible foes, den, scent, posture, gate and fade; nine new event cases.
- `dd1116b`: exclusive archive creation and repeat-run preservation. A repeat local gate caught the first clock-based filename reusing `death-0-1.pk`; the fix never truncates an existing archive.
- `45362ce`: foe windups obey turn rate, with surviving-lunge coverage; goldens unchanged.
- `096d088`: geometric nearest lock and live archive-error restoration.
- `f8c237e`: README-only refresh, including build state, controls, 97 tests and the unsaved-world limitation.
- `423bc55`: retained evidence under `notes/cb01-evidence/`.

Local complete checks ran at `f8c237e` after all source/tool/workflow edits; the final commit adds their logs only. The final-head release binary was rebuilt and its selftest passed.

| gate | macOS arm64 | Linux x86-64, container CPUs 4–7 |
|---|---|---|
| fmt, checked-machine tests | 97 pass, 0 skip | 97 pass, 0 skip |
| native + release builds/selftest | pass | pass |
| 17 scripts × rich/plain + sheets, 35 golden directories | pass on both backends | byte-identical to macOS on both backends |
| semantic gameplay checks | pass on both backends and visual tiers | pass on both backends and visual tiers |
| natural death archive | replay-verified at tick 418; repeat archive preserves old file | same |
| five unchanged engine pty rows + den keys, death agreement, archive failure | all eight pass | all eight pass |
| 80×24 rich/plain render average | 37 / 36 us | 67 / 64 us |
| 200×60 rich/plain render average | 257 / 253 us | 430 / 424 us |
| key-to-frame median / p90 | 10.9 / 33.3 ms | 13.3 / 33.2 ms |
| idle | loud Linux-only SKIP, twice because status is rechecked directly | 300 voluntary context switches / 10 s, both runs |

The three draft plants failed by name in their own runs, read once and retained. The coordinator has since closed them unmerged:

- #4, `df7f9b9`, run **40209914275**: `test_parry_window_edges` fails when age 9 is accepted (`plant-parry.log`).
- #5, `6c623a6`, run **40209918694**: `test_second_death_replaces_mark` fails when the old mark's scent is accumulated (`plant-mark.log`).
- #6, `428fee9`, run **40209922983**: `goldens: stand-plain DIFFERS` after the rich golden is substituted (`plant-tier.log`).

## Done-when

- [x] Fight/rest/death/recovery loop and southern thorn gate, with both-tier witnesses.
- [x] `tools/check` on macOS; `tools/check-linux` and performance in the Linux container.
- [x] Three named CI failures; README current.
- [x] Playtest binary built at final head on macOS: `/Users/mfwolffe/lanes/cb01/cub/target/cub`, SHA256 `782c0209ae3d541a0b65b9616d2673b6c01653d3df690d3c3948132acffada1a`. `target/cb01-build-head.txt` records the head.
- [ ] PR tier and full-matrix approval remain for the coordinator. The lane reads CI once immediately after opening, never waits or labels.

### Note — cb01, the cub and the thicket

The tooling contract disallows a lane-report Markdown file, so this is the complete handoff note for materialization as `notes/cb01-the-cub-and-the-thicket.md`.

The Shingle now contains the full default-wolf fight loop: bite chains, a stamina-heavy lunge, timed parry and follow-up riposte, collision-bounded dodge, lock cycling and loss of sight, a weasel pair and a fox's two tells, scent tracking and fading, the hollow-log growth screen, interrupted water, death fade, replacement scent mark, recovery and replay archives. Posture carries health/stamina; numeric values appear only in the den. The gate opens into the southern approach, not a completed Bramblehold area. Tests and measurements are indexed above.

Recommendations implemented, not lane rulings:
- **R-cb01-1 A:** the camera stays on the cub; lock turns it toward the foe.
- **R-cb01-2 A:** parry deals no damage; a follow-up bite on that foe within the stagger interval doubles damage once.
- **R-cb01-3 A:** reconcile the bible's 30-tick drink with healing over 15 ticks by preparing for 15, then healing 40 during the last 15; damage interrupts and loses the mouthful.

What remains deliberately outside this pass: connected areas and save/resume, difficulty selection, bleeding/cold, story state for the named fox, ghost display, bosses and music. There is no sprint or Shift+Space binding. Nose currently affects lock/mark range; trail lifetime is the bible's fixed 300 ticks. Physical Terminal.app/iTerm2 glyph/key rows remain unmeasured; `docs/KEYS.md` explicitly distinguishes injected pty measurements.

Issues to file, none filed by the lane:
1. **lair — keyprobe lone Esc coalesces the following key and can keep the probe alive.** At `aa6c4dc0`, inject `1B`, wait 150 ms, then `71` (q). `tools/keyprobe` enters its `while data == b"\x1b"` branch and performs a blocking read; it combines the bytes as `b"\x1bq"`, so its exact-q exit condition does not fire. A second separate q is needed. The initial test timed out with holder 14518 / child 14520; the coordinator ended those exact processes and verified them gone. No signal was sent by this lane. The successful capture omits lone Esc; the game decoder and `den-keys` row separately prove Esc release.
2. **lair — perf-idle exit can be hidden by the tee pipeline in tools/perf.** `python3 .../perf-idle | tee ... || status=1` observes tee's status under POSIX sh. cub's checks additionally invoke perf-idle directly, so its gate cannot pass on that hidden failure. Engine fix should preserve output while checking Python's status directly.
3. **cub — physical-terminal glyph/key measurements** remain the existing owed rows; no claim of Terminal.app/iTerm2 measurement is made here.

cb02 draft — the connected world and persistent journey:
1. Build the fixed area graph around the now-open southern edge; fill from the seed while guaranteeing passable connections and den access. Bramblehold first, then the meadow and the first shortcut back to the Shingle.
2. Add versioned, validated save/resume for seed, default difficulty, growth, water progression, den, opened shortcuts and world/story flags. Preserve the previous save on interrupted/failed writes; unknown/corrupt data is a named failure, not silent reset.
3. Carry this pass's den/growth/flask/death rules through transitions rather than reimplementing them. Decide how a dropped mark is stored across exits; recommend persisting its area, position and scent with the rest of the journey.
4. Add the third ordinary foe, the hawk, with a stopping shadow tell and its parry answer; keep fox story identity separate from the Shingle combat preview.
5. Add dusk keyframes and area art on both tiers, shortcut feedback, and persistence-aware den screens; make every new number a dated proposal.
6. Prove graph reachability across seeds, shortcut round trips, save round trips and failure preservation, cross-area mark recovery, both-backend/host goldens and terminal restoration. Plant an unreachable route, lost save state and wrong-tier frame as named CI failures. Keep the following boss/ghost and score lanes separate.

