# cb04c — the look of the level

_Materialised from cub#33's PR body at the merge (7a11953a); the lane's wrapper could not write Markdown notes._

# cb04c — the look of the level

Original world sprites, visible scent orbs, body-ring pickups and an opaque stamina-panel margin. No engine, pin, workflow or save-schema change. The five-section note is here for materialization as `notes/cb04c-the-look-of-the-level.md`; this wrapper prohibits Markdown report files.

## Prediction

`66bcf25` committed `notes/cb04c-evidence/prediction.txt` before implementation. The existing death-scent recovery path was present, not missing; its one-cell check became the shared body contact ring. The label census below is exhaustive for world-anchored words at base `8fed728`; all calls are in `src/art/art.lu::draw_world_marks`, through `at_world` → `draw.put_text` (baseline line 651).

| World word | Source/draw call at baseline | Replacement |
|---|---|---|
| ( empty ) / ( hollow ) / ( burrow ) | art.lu:684-698 at_world | empty/filled log ring or rooted burrow |
| Bramblehold | art.lu:762 at_world | thorn stems |
| Larkmeadow | art.lu:764 at_world | flower and grass |
| Old Snag’s clearing | art.lu:765 at_world | tusked boar head |
| Ember | art.lu:766 at_world | seated pointed-eared fox |
| bones, no scent | art.lu:767 at_world | paired bone ends |
| scent-marked tree | art.lu:769 at_world | forked marked trunk |
| The Teeth | art.lu:770 at_world | joined peaks |
| The Shallows | art.lu:772 at_world | ripple bands |
| the old pack’s marks | art.lu:773 at_world | paired tracks |
| Gravehollow | art.lu:775 at_world | arched den mouth |
| the pack’s scent, everywhere | art.lu:777 at_world | paired tracks |
| [ hedge ] / [ ledge ] / [ shallows ] | art.lu:792-807 at_world | woven hedge / steps / stepping-stone ford |

`Ember:` at baseline line 1315 is the bottom-line speaker, not a floating label, and stays. HUD area names, dialogue, interaction hints, den/death cards, boss bar, opening/title/end text are not world-point labels. Logs and coast bundles already had sprites; there are no lever-name draw calls. The new `props-rich/plain` atlas and ART legend show every replacement.

The final 50-seed camera walk renders **121,000 frames**, both tiers, every route row plus all caches (closed/open), shortcut mouths and former label sites: no placeholder word. This is a renderer/camera instrument, not a claim of a player-key walk; gameplay and pty rows independently cover real inputs.

The orb has a white core, pulsing violet halo and **four** deterministic seed/cell/tick motes. Motes stay at x **−3..3**, y **−5..−1**; halo x **−3..3**, y **−2..2**; the whole drawing is **7×8 cells**. Period **96 ticks**. No distance cull; no orb without a mark in this area. Recovery restores scent once and gives eight sparks of radius **1..3** for **12 ticks**. A second death still replaces the first mark. One transient burst is retained, never a growing emitter list.

**R-cb04c-1 A recommended and implemented, not decided:** `sim.PICKUP_MARGIN = 1` cell; `sim.pickup_near(s,x,y)` accepts the drawn body plus its one-cell contact ring, including corners/fractional positions, all facings and the grown wolf. Caches still need `r` and no live guard within six cells. Ordinary drops retain their 300-tick lifetime and show at least one fresh frame before collection. Bundles/caches are brighter, wider and slowly animated.

**The stray c:** a reproduced baseline camera at (22,27) puts the `c` from `bones, no scent` at zero-based row 3, column 22, beside stamina. `hud-original-red.log` prints **codepoint 99**. The old HUD painted only its strokes, leaving the world visible through padding. The repaired panel reserves 5×23 cells and row 3 through column 48 (the water-charge slot). The literal-byte-63 pty witness measures ECHO disabled and live/replay agreement, both sizes/tiers. This proves the reproduced world-label leak, not the exact cause of an unsupplied play-session recording.

Golden prediction: in-level frames moved; title and score stayed. Actual: **171 directories changed (159 existing + 12 new)**, 164 → 176 total including score, none removed. `opening-{rich,plain}`, `title-{rich,plain}` and `score` are unchanged. New pairs: `hud-after-c-{80x24,120x40}`, `scent-orb-{80x24,120x40}`, `scent-recover-{80x24,120x40}`. Exact list: `notes/cb04c-evidence/golden-directories.txt`. Both hosts generate the same **2,803 files**, path+bytes SHA256 `00e0e788cdf917d9d8db9119def7be9a2e27644f693d15829935ca2373280c2f`.

## Forbidden

Original code and drawings only; no other game's source/assets/text/music. No engine, pin, workflow, planning-repo or user-configuration edit; no package install, merge, tag, release, issue action or label. No attribution trailers. All signal witnesses are pty bytes, never signal scripts. hasu uses the supplied rootless podman PATH, existing image, 12 GB, taskset **inside** on cores **0–5**, and `flock /home/mfwolffe/lanes/hasu-A.lock` for heavy work only; editing never holds it. The only host-recipe adaptation is that PATH/block/lock wrapper. Mac heavy components each check the 8 GB vm_stat floor with 180-second retries, isolated lane HOME/TMPDIR, exec/wait ownership. One native build and one release/play build; perf runs directly, without the wrapper that rebuilds. The maintainer's servers and other lanes are untouched. `host-recipe.txt` records the scripts.

## Inputs verified

Base `8fed72893efd10a30db76c99c8d233f31a1ffe3d`; engine `57870143ebbb4806b8bee40379e8c6e781f50842`, unchanged. wolf 0.2.35 / lupin 0.1.56 / std `2386522e`, complete host archive pairs fetcher-verified; four release digests read twice in `digests-twice.txt`. Contract, verbatim playtest, adjacent ownership contracts, cb03a/cb04/cb02a/cb02b notes, ART/GLYPHS/PALETTE/DESIGN/KEYS, campaign, RULES and guide read. README read and refreshed in its own commit.

The progression update owns meat/spring logic. The coordinator fixed the integration boundary: this lane exposes pure `art.draw_meat(mut g,t,row,col,tick)` and `art.draw_spring(mut g,t,row,col,tick,available)` with independent rich/plain sheets and animation tests; it does not read the other lane's Sim fields. **Whichever lands second must replace its temporary `+`/`~` draw calls and use `pickup_near` + `pickup_flash`.** Meat/spring gameplay is not claimed in this build. The water HUD slot is row 3, columns 24–48 on both tiers.

## Evidence index

- `66bcf25`: Record level look prediction.
- `6cba834`: Replace floating world labels with sprites.
- `07f5ed7`: Light scent orbs and collect on the body ring.
- `34a26dc`: Reserve the stamina panel against world glyphs.
- `ec95873`: Cover orb states within checked test budgets.
- `3543c02`: Witness live pickup recovery and byte-c frames.
- `4a130c1`: Regenerate level sprites and pickup goldens.
- `ad0c8a4`: Draw bright animated meat and spring pickups.
- `2601df6`: Update pickup witnesses for the contact ring.
- `897a74c`: Refresh README for visible pickups.
- `68cfa7c`: Document healing colours and reused glyphs.
- `faf213f`: Regenerate healing atlases and water HUD padding.
- `7a11953`: Record level look witnesses and host gates.

Tracked evidence: `notes/cb04c-evidence/`. Full scripts/logs remain under `/Users/mfwolffe/lanes/cb04c/` and `/home/mfwolffe/lanes/cb04c/`.

- macOS arm64: `macos-final.log`, direct `macos-final.exit` **0**. **247** checked tests, zero failed/rejected/unsupported/SKIP; both backends, all goldens, score PCM, **22 pty rows**, gameplay/save/world/body/boss gates green. Native/release built once at source head `897a74c`; later commits are docs/goldens/evidence only. The updated glyph-role table was checked again (`glyphs-final.log`: 2 green).
- Linux x86-64: `linux-final.log`, direct `linux-final.exit` **0**: **247** checked tests, zero failed/rejected/unsupported/SKIP; both backends, every golden, score PCM, all **22 pty rows**, gameplay/save/world/body/boss gates green. Final plants re-ran and restored before the full gate.
- Mac slack-1 render averages: 80×24 rich/plain **173/166 µs**, 200×60 **1184/1170 µs**. Latency median/p90 **10.4/33.5 ms**; direct repeat **33.0/33.5 ms**. Linux-only idle measurement is loudly skipped on Mac (two invocations), not called zero skips overall.
- Linux slack-1 averages: 80×24 rich/plain **257/238 µs**, 200×60 **1667/1750 µs**; idle **300 switches/10 s** in both direct measurements. Latency median/p90 **15.0/32.9 ms**, direct repeat **15.0/15.3 ms**.
- `look-census.txt`: 50 seeds, 121,000 rendered frames. `first-goldens.log`: focused tests and initial Linux byte-c/recovery pty witnesses. `hud-original-red.log` and `hud-padding-red.log`: the HUD regression before repair. `golden-hash.py` reproduces the cross-host fixture hash.
- Three local hasu-container plants, fixes committed first, each restored; no plant PR or dispatch. `plants/word.log`: `test_cb04c_world_words_are_not_sprites ... FAILED (trap(assert))`. `plants/orb.log`: rich/plain `orb_requires_a_death ... FAILED (trap(assert))`. `plants/radius.log`: `pickup_ring_every_edge_and_outside`, `mark_recovers_once_at_contact_ring_with_burst`, `drop_collection_uses_body_ring ... FAILED (trap(assert))`. `plants.log` records all three nonzero exits and source restoration. No rejected/unsupported substitute for a red assertion.

## Done-when

- [x] Complete label census, original both-tier sprites, legend and 50-seed no-placeholder camera walk.
- [x] Local death orb, bounded seeded drift/pulse, one-shot restoration and burst; foreign area/second death covered.
- [x] Existing pickups brighter, larger, idly animated, body-plus-one-cell reach; every footprint edge and cell beyond tested.
- [x] Pure meat/spring helper sheets and tests; second landing owns their world wiring, per coordination.
- [x] Stamina padding repaired, exact baseline c witnessed, byte-c pty rows and named after-c goldens.
- [x] Three local plants, docs/README, both-host byte-identical goldens, Mac full gate and play binary.
- [x] Linux full gauntlet and slack-1 performance green; final source unchanged between both-host runs and the final documentation/evidence commits.
- [ ] PR-tier CI is the coordinator's watch; no label, no CI wait. Audit status supplied at hand-back.

Play: `/Users/mfwolffe/lanes/cb04c/cub/target/cub --save /Users/mfwolffe/lanes/cb04c/play.save --ghost-dir /Users/mfwolffe/lanes/cb04c/play-ghosts` (add `--mute`; schema 3). SHA256 `d9d0c579055a6aff876735f68467e050792178b9838f7610d1e80e20107334f4`; `target/cb04c-build-head.txt` names the source head. Retain until play is accepted.

Prune after merge/play: only `/Users/mfwolffe/lanes/cb04c/` and `/home/mfwolffe/lanes/cb04c/`. No new compiler/engine issue to file; the existing true-held-key limitation remains the separate engine/combat work. No issue to close. Materialize this note on trunk, and keep the explicit second-landing meat/spring wiring obligation.

Final audit, run once at `7a11953a0499bc40e536e39d27961b4e0f121a26`: direct exit **1**, last line **`AUDIT FAIL (footprint: module)`** (`/Users/mfwolffe/lanes/cb04c/logs/audit.log`). All ancestry, footprint, attribution, sections, cited-SHA and orphan checks pass. Holds are CI still in progress and the intentionally retained play worktree. The one immediate CI read returned `[]`; the required audit identified run **40374669837**, in progress. No CI wait, second listing or label.

