# Note — cb02a, the coast

Complete note for materialisation as `notes/cb02a-the-coast.md`; the wrapper prohibits Markdown report files. Before/after frames and retained logs are in `notes/cb02a-evidence/`.

## Prediction

- `f287d0d` committed the diagnosis and baseline frames before code changes. No play seed/replay was supplied, so the retained captures cover seeds 0–4, 200×60 and 80×24, both tiers, using `stand.pk` to bypass the opening.
- **Missing forest cause:** `forest.kind` returns DARK outside the finite x=-40..40 area; `SP_DARK` rendered spaces on both tiers. At 200 columns, 119 columns below the bank were therefore blank. Interior density-selected DARK also disappeared. Plain dark canopy was black on black. Bramblehold additionally erased distant terrain. Collision bounds remain closed; the forest no longer vanishes there.
- **Sawtooth cause:** the bank reused the inland curve's alternating eight-cell anchors, while its pre-origin band returned gravel without a lower shore bound. Long-wave engine noise now gives one clean bank row and a five-row horizontal path, with a maximum quantised bank step of one cell.
- Predicted 85 of 87 existing golden directories would move. Actual: all 87 moved, including opening cases whose integer state includes the changed spawn origin; four new cache directories bring the total to 91. Art adds two coast sheets. The exact directory list is retained.
- Proposed N=0 empty forest cells and K=200 cardinal steps to the thorn-route centreline or a branch alcove. Measured over 50 seeds: **zero empty forest, maximum 132 steps**, 150/150 area-destination rows complete, bank step ≤1, inland straight run ≤7, nearest initial foe ≥34 cells.

## Forbidden

Original game code and art only; pack's path was read for its shape, never copied. No lair, pin, workflow, planning-repo or user-configuration edits. No packages installed, labels, merges, tags, releases or issue actions. No attribution trailers.

Every Mac heavy launch passed the scripted 8 GB free+inactive+speculative floor; shortfall waits were three minutes. Scratch stayed under `/Users/mfwolffe/lanes/cb02a/`. Every child was exec'd or waited for. No maintainer server or other lane was touched.

Linux ran in the staged engine container, 12 GB limit, **`LAIR_CPUS=4-7`**, under **`/home/mfwolffe/lanes/kasumi-cores-4-7.lock`**. The lock stayed held until the child exited. Commands entered through `ssh kasumi bash -s`; pids and launch scripts remain under `/home/mfwolffe/lanes/cb02a/`. No process was killed. The cb02 directory was inspected read-only; it retained no launcher, so the exact convention is now recorded in `host-recipe.txt`.

The 16:21 EDT Mac reboot interrupted `proof3.log` while waiting at 7 GB, **before** its heavy command. Prior completed census/proof logs survived; there was no cb02a Linux job then. All final gates cited below ran after the reboot.

## Inputs verified

- Base `f29d6b3`; engine `aa6c4dc0bc5071d3c07121451d913a8837cd2a6a`, unchanged.
- wolf 0.2.35 `cf0c13d38479f444b69bb8356ad5709d07eff323`; lupin 0.1.56; std `2386522eb059cca5a84108562c2c0a0e72345d34`. Complete host archive pairs staged by the fetchers; four release digests read twice in `digests-twice.txt` and checked while staging.
- cb02/cb01b notes and evidence, game docs, design bible §§6/18/19, campaign, pack's `trail.path`, lane rules and wolf guide read.
- **R-cb02a-1 A recommended/implemented:** original wrapped-bundle sprite, counted as “a bundle” at the den. **R-cb02a-2 A:** independently seeded jetties beyond both shore branches. **R-cb02a-3 A:** existing fox, 40 health, existing feint/real tell, not a new foe. **R-cb02a-4 A:** derive bundle inventory from the finite Shingle cache bits; retain schema 1 and the second cache's marrow. These are recommendations, not lane decisions.

## Evidence index

Implementation chunks:
- `7627b26` smooth coastal terrain; `d79f2ea` visible forest fill.
- `09d1735` shore branches/guarded alcoves; `cd51a4c`, `3b2abde`, `71d393e` bounded jetties and inland alcove clearance.
- `b639965` hollow/fallen logs; `0bd117e` wrapped bundles; `888b895` five flotsam sprites and both-tier sheets.
- `818db16`, `ffb5655` rendered full-length forest sweep and independent tile floods; `72cf797` rich scalar-glyph regression; `cfa48d1` guard/treasure separation and direct branch-mouth test.
- `7e24d31`, `ed9fea7`, `376aa27` real-key cache/encounter/journey proofs; `0184faf`, `4e53ad9` goldens.
- `16c36f5` docs; `ca20a05` README-only refresh; `62db9f3` retained evidence.

| gate | macOS arm64 | Linux x86-64, locked 4–7 container |
|---|---|---|
| format / checked tests | 144 pass, zero failed/rejected/unsupported/skipped | same |
| native + release, selftest, goldens | 45 scripts × both tiers + art, 91 directories | byte-identical |
| pty rows | all 12 pass | all 12 pass |
| gameplay / saves / finite caches / death archives | both backends pass | both backends pass |
| 80×24 rich/plain average | 98 / 98 µs | 158 / 154 µs |
| 200×60 rich/plain average | 455 / 455 µs | 710 / 717 µs |
| latency median / p90 | 22.8 / 33.3 ms; repeat 11.2 / 33.3 | 23.2 / 33.6 ms; repeat 14.4 / 33.5 |
| idle / 10 s | loud Linux-only skip | 300 switches; repeat 301 |

Both hosts' complete source/fixture gates cover `4e53ad99a1fb55d6199a2979d055652976efc7ff`. Final head `62db9f35367f42fbe75bf9cdd8166991570eb6a0` adds evidence only; the complete local gate passed at that head (exit 0), with its log and exit marker retained under `/Users/mfwolffe/lanes/cb02a/logs/final-head-check.*`. Both hosts' performance passes at slack 1.

All **1,674 golden files**, including relative paths, hash to **`cc587e875248810f085a6ad329485e66a539b5c8087476ac68b0ccf5db31a130`** on both hosts. Comparison logs were empty before hashing. The census is byte-identical too. `golden-directories.txt`, `golden-hash.py`, `measurements.json`, both host logs, census files and `proof-final.log` are retained.

The 4,878-tick world-return witness still visits all three areas, fights the hawk, recovers a cross-area mark and returns by both shortcuts. Cache witnesses continue that ordinary-key journey to ticks 5,108 and 5,720, opening both guarded bundles. Its original explicit growth-scent fixture remains disclosed; no extra health or teleport was introduced. Default-growth encounter scripts still prove actual fights; the natural death and its archive replay occur at tick 757. The sprite sheet and a rendered-frame test ensure the guard does not hide its treasure.

Before/after frames: `notes/cb02a-evidence/{before,after}-{0..4}-{80x24,200x60}-{rich,plain}/final.{txt,sty,state}`. Rich props are emitted as scalar cells, not UTF-8 bytes through the ASCII text helper; the planted local glyph test was red in `notes/cb02a-evidence/props-before.log` before the correction, and green in `notes/cb02a-evidence/props-after.log`.

Negative draft PRs, intentionally left open:
- **#15**, `548b9ee540c2c4b1e51f992c52875fb934ecfdde`, run **40231575421**: `test_cb02a_forest_fill_is_visible_beyond_area_bounds`.
- **#16**, `2ab9f1c08cd22613661d044d8352386b84f5a724`, run **40231627302**: `test_cb02a_each_branch_ends_in_an_alcove`.
- **#17**, `5653e9bca05ac615e3fe74dc4ab431eff4c3b043`, run **40231670604**: `test_cb02a_jetties_never_cut_den_from_thorn_route`.

Each focused local checked test failed by name. Each immediate lane CI read returned `[]` before its run row existed; no polling followed. The coordinator supplied these run ids and observed all three named CI reds, including the jetty plant's collateral blocked-den failures.

## Done-when

- [x] Forest visible on both tiers, in all areas and both tested sizes; full-length 50-seed census.
- [x] Gentle horizontal shore, clean bank, winding guarded offshoots, reachable finite bundle alcoves.
- [x] Seeded solid jetties beyond the branches; den-to-thorn approach stays open; bounded useful walks.
- [x] Original hollow/fallen logs, driftwood/crate/kelp/bottle/net, wrapped bundles and both-tier art sheets.
- [x] Both-host/backend correctness, 12 pty rows, real-key world/cache witnesses, save/mark persistence and slack-1 performance.
- [x] Three named negative CI drafts remain open; no label.
- [x] Docs and README current. No engine change needed; no compiler issue found.
- [ ] Coordinator watches the final PR-tier run and materialises this note on merge.

Play binary: `/Users/mfwolffe/lanes/cb02a/cub/target/cub`, SHA256 `2a0f890da8e752ce125ed1e1409af43233d48b15635a8499953b0e4a651ff1d2`. Isolated play: `target/cub --save /Users/mfwolffe/lanes/cb02a/play.save --ghost-dir /Users/mfwolffe/lanes/cb02a/play-ghosts` (add `--seed 0` only for a new journey). Keep this worktree until play is accepted.

Prune after merge/play: `/Users/mfwolffe/lanes/cb02a/` and `/home/mfwolffe/lanes/cb02a/`. No other worktrees were created; all gate processes have exited. The coordinator closes the three negative drafts. Existing physical-terminal font/keyboard follow-ons remain; no new issue action is requested. Planning correction: cb02's note omitted the concrete Linux lock path; this note supplies it.


Final CI read: the immediate one-time run listing returned `[]`; the required audit then named **40232909681**, still in progress. No CI wait or polling occurred.

The required audit ran once at the final head: last line **`AUDIT FAIL (footprint: module)`**, direct exit 1, `/Users/mfwolffe/lanes/cb02a/logs/audit.log`. Ancestry, footprint, attribution, sections, cited shas and orphan checks passed. Failures were pending CI/no green tier yet, the intentionally retained play worktree, and one glyph-test red paragraph lacking its log in that paragraph. That citation is now repaired above; the audit was not rerun. The coordinator re-audits after CI and play disposition.

