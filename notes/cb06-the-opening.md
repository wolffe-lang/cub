# cb06 — the opening

_Materialised from cub#49's body at the merge (`2535ccb0`); the Codex wrapper writes no .md notes._


## Prediction

`16e9e349` committed `docs/cb06-prediction.txt` before implementation:900 ticks /30 seconds, a150-tick /5-second sting, busiest200×60 render+diff below12ms rich /10ms plain. `0a89126d` predicted the item5 shared-art correction before changing it. Timing and cue length match. Across the two item5 measurements at f2047e9c (the renderer is unchanged by the save fix), maxima were2.397ms rich /3.961ms plain, both at age690. The full-gate rerun measured maxima2.232/2.612ms and busiest means2.016ms rich (age744) /2.027ms plain (age630). Both series are retained, not selected for the smallest result: `item5-bench.log`, `item5-linux-final.log` in the evidence directory below.

R-cb06-1: recommend30seconds, implemented, giving the crossing and shock time to read. R-cb06-2: recommendA, one decoded key skips the entire opening without making a gameplay move, implemented. Existing mute/quit handling remains. No additional ruling. The sting uses the mixer's existing minimum one-tick fade rather than the prediction's zero; the live sink cuts the title immediately.

| shot | ticks, end exclusive | duration |
|---|---|---:|
| crossing | 0–210 | 210 |
| first crack and cue | 210–225 | 15 |
| frozen cub; pack walks on | 225–300 | 75 |
| spreading seams | 300–330 | 30 |
| breaking plate | 330–360 | 30 |
| fall | 360–420 | 60 |
| underwater and fade | 420–480 | 60 |
| black | 480–510 | 30 |
| first slow opening | 510–600 | 90 |
| first slow closing | 600–660 | 60 |
| second opening | 660–720 | 60 |
| second closing | 720–765 | 45 |
| third quick opening | 765–789 | 24 |
| third quick closing | 789–810 | 21 |
| final reveal | 810–840 | 30 |
| clear spawn | 840–900 | 60 |

## Forbidden

Original game work; no borrowed game's art, text or music. No engine, pin, workflow, package, planning-repo or user-configuration changes. No merge, label, tag, release or issue action; no attribution trailers. Linux gates used the existing `localhost/pack-ci:fbee7e864f7dbee6` image, under the0–3 flock and taskset. Mac builds/tests used lane-owned HOME/TMPDIR and the scripted8GiB free+inactive floor, never lowered. The earlier a7a9603f pass waited on memory; final item5 gates completed without a memory refusal. The additional Mac builds were explicitly granted after rebase and after item5 play feedback; earlier binaries remain superseded.

This wrapper prohibits Markdown report files. This is the complete five-section lane note instead of `notes/cb06-the-opening.md`; the coordinator can materialise it on trunk. Durable evidence is outside the checkout, under `/Users/mfwolffe/lanes/cb06/evidence/`, keeping the game-code checkpoint at `7f67236cedee079ed3c5d202a4ab311217c4b899`; the final fixture-only follow-up is `2535ccb05f1897f670e54e78e066faf7c50b7dde`.

## Inputs verified

Rebased on cb04f and its note at `1eb0ab8c`; both lanes' test rows and DESIGN sections were retained. Lair stays `57870143ebbb4806b8bee40379e8c6e781f50842`; wolf0.2.35, lupin0.1.56 and bundled std `2386522eb059cca5a84108562c2c0a0e72345d34` are unchanged. The pinned fetcher checked the release archive digests. Repeated identities are in `mac-inputs.txt` and `linux-inputs.txt` in the evidence directory.

The opening remains one `opening 1` event and ordinary recorded keys. The seen flag and current journey schema are unchanged. Old recordings parse but use the new art/duration; old three-card visual compatibility is not claimed. No replay-format migration is needed. The ending's90-tick cards are untouched.

Twenty sampled moments cover every shot, the first blink peak and all shut blinks at80×24,120×40,200×60, both tiers. Both hosts' final manifests match:3,585 files in348 directories, path+content SHA256 `14505dc0641465fd01145a9bf3bab8b40d150a9ff81737ade957bd1ab54e9467`. Relative to the cb04f baseline:390 paths added, none removed. The item5 correction changes existing opening files, not the path set.

## Evidence index

- `2009a187`: timing, disjoint materials, blinking and cue tests first.
- `66febb17`: crossing, crack, fall and waking animation.
- `53a0ad23`: original crack part, embedded text, schedule and PCM golden.
- `2e56d85a`: shot goldens, full terminal opening, per-shot skips, frame-cost probe.
- `f5cf93df`, `6ac4c195`: opening docs and separate README refresh.
- `4e888bdf`, `a7a9603f`: contrast/recorded-shot witnesses and rebased checkpoint goldens.
- `c3281aab`: item5 source-pair and silhouette witnesses before implementation.
- `14a0c180`: shared gameplay wolves and real Shingle bank/forest sampling.
- `da7d7dae`: item5 opening goldens.
- `a2f47209`, `f2047e9c`: shared-art documentation and README-only refresh.

**Item5, by file and digest.** `src/art/art.lu` calls `draw_pose` and `draw_wolf`, using the unchanged `silhouette.footprint` sizes. Only fur over ice is shaded; other cells retain gameplay fur and attributes. `opening_bank_source` chooses real Shingle gravel or dense closed-forest coordinates; `opening_bank_cell` calls `ground_at`, not a copied glyph/palette table. Both banks have five gravel rows at80×24 (viewport fit), seven at120×40/200×60, and two/four/six rows of thick forest beyond each bank. `src/opening_test.lu` checks every displayed land cell against world-emitted glyph/style pairs, and every sprite cell against the gameplay drawing and physical footprint. Six viewport/tier shards keep full displayed-cell coverage inside the checked-machine step budget.

| final file | SHA256 |
|---|---|
| `src/art/art.lu` | `233b7dc1173bd3be082d09d16d2a1730ab0c1c19ca6a323449c4ae0aad61a335` |
| `src/opening_test.lu` | `6438c95ff4ec3635765a0b697bac6de0b0448df5cd5396263b3870c3b753d9e6` |
| `tests/goldens/opening-crossing-80x24-rich/final.txt` | `230e7e904e37e35bdd4132173325814876f3e5901452546257051b74cf7dfb89` |
| `tests/goldens/opening-crossing-80x24-rich/final.sty` | `2e9e4497e8fc58d7004b725344b0c31a5ef6dd5af7af7975e51f05eb29a2ee51` |

**Final gates at7f67236c, including the save-order fix.** Linux exit0 at2026-10-27T04:02:29Z, Mac exit0 at04:05:56Z. Each passed305 checked tests with zero failed/rejected/unsupported/unit SKIP, selftest, every committed golden on both native/release binaries, PCM score checks, all46 pty rows, both-backend gameplay/persistence/world/body/boss/den checks and slack1 performance. Both current binaries had already been built and verified in the focused matrix; the full gates did not rebuild them. Final latency medians were12.6ms Mac /13.6ms Linux, below the bars. Mac loudly skips only the Linux `/proc` idle metric (two invocations); Linux measures it. Final logs: `/Users/mfwolffe/lanes/cb06/evidence/race-linux-final.log` and `/Users/mfwolffe/lanes/cb06/evidence/race-mac-final.log`; scripts: `race-linux-gate.sh`, `race-mac-gate.sh`, `memory-gate.sh`; matching final manifests: `race-goldens-linux.txt`, `race-goldens-mac.txt`, all under the evidence directory. Earlier item5 evidence is retained as history, not substituted for these final-head results.

`opening-complete` plays through tick900, verifies the Shingle and seen flag, compares its final terminal text/styles to recorded playback, then replays all twenty sampled moments against both-tier goldens. Sixteen skip rows type real arrows in every shot, assert no movement and compare their recordings. The first blink cannot open fully; the cub holds while the pack moves; ice/sky/deep-water styles are disjoint. The final clear frame is exactly the actual seeded spawn view.

**Score.** `crack`:5seconds /960,000 PCM bytes, SHA256 `da3b1bd8ef026208c81adb8247057406467adbd19515efa3460db4356c9e7e5f`, identical on both backends and hosts. Eleven parts plus silence. Title accompanies the crossing, crack replaces it at210, silence starts360, Shingle starts510. Skip cuts crack immediately; gameplay death remains uninterruptible. Mute and `CUB_SOUND=0` pass their live witnesses.

**CI save-order correction.** Run40433776827 failed only `opening-skip-01` on macOS. This was cub logic, not an engine/HOME/permission/sync failure. The unchanged row supplies an explicit `--save` under `target/pty/opening-skip-01` and sets its own HOME. Its writer is cub's `src/journey/journey.lu`: `prepare` creates the parent, writes/fsyncs/closes the stage; `commit` renames and syncs the directory. The engine only loads the cub-owned pty rows.

The retained CI artifact records right at event213, the scene ending and seen flag staged at tick214, then quit at event214/tick215—exactly the normal one-tick commit deadline. `src/cub.lu` guarded both prepare and commit with `!quit`, so it suppressed the due commit and aborted the already-synced stage. CI stderr explicitly says `pending save cancelled; previous journey preserved`, and its file contains `opening 0`. Passing local runs committed at215 before quit216. Five unchanged-row runs with fresh outer HOME and `LAIR_MEMORY_GATE=0` passed; that environment does not eliminate the timing race.

- `35251c5d`: prediction from the CI artifact before the fix.
- `19b4decd`: additive `opening-quit-due` regression. All4 adjacent skip/quit cases were seen red on the original Mac binary, including missing default `.cub/` and explicit nested save paths, and each relaunch repeated the opening (`race-regression-red.log`). The original `opening-skip-01` row and its expectation are unchanged; no Darwin skip.
- `b172a024`: the fix is one guard change plus a comment: allow an already-due staged save to commit on quit, while the existing inner `!quit` still forbids preparing a new stage. A write whose delay has not elapsed is still cancelled on exit.
- `79a14ff7`, `7f67236c`: README and DESIGN clarify the commit deadline.

Current native/release binaries on BOTH hosts pass `opening-quit-due` (4 adjacent pairs each,16 total), unchanged `opening-skip-01`, `pending-save` (early quit/typed03 still cancels), `save-failure`, and `resumed-record`. Both default and explicit paths are read back through a real second launch. Logs `race-mac-fixed.log`, `race-linux-focused.log`; failing CI artifact `ci40433776827-macos/pty/opening-skip-01.err` and its `opening-skip-01/fresh.save`; local red `race-regression-red.log`, all under the evidence directory. Full current-head reruns completed through `race-mac-gate.sh` and `race-linux-gate.sh`, with no extra rebuilds. The new adjacent-quit regression also passed in both full gates. No frame/PCM changes were made or regenerated; all final golden checks passed unchanged.

**Artifact-upload permission correction (fixture only).** Run40445788890 passed every pty row, including the save-race regression, but Linux's always-run artifact upload failed to scan a root-owned `opening-quit-due/fresh-*` directory. `tempfile.mkdtemp` creates mode0700; Docker creates it as root while the host uploader runs as another uid. Local rootless podman and Mac runs share the creating uid, hiding the mismatch. There was no mode000 or intentionally unwritable directory: the nested save path really is absent.

- `251db171`: permission-failure prediction before implementation.
- `c38edfd4`: two failure-path tests first; both failed against the original row's leftover0700 home (`fixture-permissions-red.log`).
- `2535ccb0`: each attempt now has a `finally` cleanup. It normalises only that synthetic evidence tree to directories0755 and files0644, retaining partial/failure traces and not following symlinks. The adjacent-quit expectations and game code are unchanged.

`python3 -I tests/pty_rows_test.py` passes on Mac and Linux, including an immediate session-setup exception and a partial-output exception with private nested directory/file. The real `opening-quit-due` row passes on both hosts, four adjacent pairs each. Permission listings verify every directory under `target/pty` is0755 and all18 evidence files are readable. A separate Linux container process as uid65534 reproduced EACCES on a root-owned0700 control directory, then recursively scanned/read the fixed row's entire `target/pty` tree successfully. Evidence: `fixture-permissions-red.log`, `fixture-permissions-green.log`, `fixture-mac-row.log`, `fixture-mac-permissions.log`, `fixture-linux-row.log`, `fixture-linux-uploader.log` under the evidence directory. README read, current; no gameplay, engine, pin, workflow or golden changes, and no expectation relaxed. The305-test/46-row full game gates above are the unchanged game-code checkpoint; the fixture-only follow-up is validated by these targeted failure-path, live-row and cross-uid upload witnesses.

**Plants.** Both were seen red locally on kasumi CPUs0–3 over the fix's tests; exact original source was restored and hashed. Draft [#47](https://github.com/wolffe-lang/cub/pull/47), `d873b3ef`: `test_cb06_first_blink_never_opens_fully ... FAILED`, `plant-blink.log`, exit1. Draft [#48](https://github.com/wolffe-lang/cub/pull/48), `d6125b47`: `test_cb06_crack_frame_has_the_cue ... FAILED`, `plant-cue.log`, exit1. Their clean worktrees were removed; the coordinator closes the PRs. One listing for each returned no CI run; no dispatch/wait was added. Earlier superseded gate logs remain available, including the sound-live eleven-WAV expectation that was corrected to twelve.

## Done-when

- [x] Prediction and item5 amendment committed before their implementation changes.
- [x] Original ice/fall/blink sequence; shared in-game wolves and Shingle banks/forest on both sides.
- [x] Every displayed land pair and every wolf cell/footprint witnessed; all three sizes and both tiers pinned.
- [x] Whole-opening skip, recorded-shot agreement, seen flag, mute and exact crack cue preserved.
- [x] Current fix passes the focused persistence matrix on both hosts and both backends; the new regression witnessed all16 adjacent skip/quit pairs.
- [x] Full final-head gates green on both hosts:305 checked tests and46 pty rows each; platform-only skips named.
- [x] Final logs, regression records and representative source/golden artifacts retained outside the checkout; completed Linux build outputs and the clean pushed Mac worktree removed; play binary retained.
- [x] Both required plants red by name and linked above.
- [x] README, DESIGN, ART, PALETTE, SCORE and REPLAY current for this pass.
- [x] Final play binary matches the tested head; full note supplied here for materialisation.
- [ ] Coordinator: accept play, close plants, materialise note and merge only with the required CI green.

Play binary `/Users/mfwolffe/lanes/cb06/cub-play-7f67236c`, SHA256 `2afe227749a3a394a2e511402507523ad11c520803dc50bcc31c98dfd0e6a96d`, identical to the release build. Fresh-save command, fish-compatible with no environment prefix:

```sh
/Users/mfwolffe/lanes/cb06/cub-play-7f67236c --no-title --seed 1 --save /Users/mfwolffe/lanes/cb06/opening-7f67236c-final.save --ghost-dir /Users/mfwolffe/lanes/cb06/play-ghosts --sound-dir /Users/mfwolffe/lanes/cb06/play-sound
```

Final fixture-fix head is **`2535ccb05f1897f670e54e78e066faf7c50b7dde`**. Game code and the retained play binary remain unchanged from7f67236c. Run40445788890 is the upload failure corrected here; the immediate one-time post-push CI listing returned `[]`, so no run ID was indexed at that read; the coordinator can locate/watch the run for the exact final head without the lane waiting or polling. No CI wait or new audit is requested for this follow-up.

The earlier audit at7f67236c remains recorded honestly (not an audit of the fixture-only follow-up): exit1, exact last line **`AUDIT FAIL (footprint: module)`**, with CI not yet green, the then-retained worktree and the then-running detached Mac gate as holds. Both local gates have since exited0 and the clean pushed Mac worktree has been removed. This is not a claim of a new audit pass; the coordinator audits and merges on CI green. Original audit log: `/Users/mfwolffe/lanes/cb06/evidence/race-audit.log`.

Final logs are copied into `/Users/mfwolffe/lanes/cb06/evidence/`. Final opening recordings and regression witnesses are retained under `race-mac-opening-records/`, `race-linux-opening-records/`, `race-mac-witnesses/` and `race-linux-witnesses/`; representative source, crossing goldens and crack PCM bytes are under `final-files/`. Completed Linux `target` outputs were removed only after these copies. The Mac play binary remains at the path above with its verified digest. The complete note is also retained as `/Users/mfwolffe/lanes/cb06/pr-body-permissions.txt` for materialisation. No engine/pin/CI changes or new issue filing are required. The coordinator owns CI watching, plant closure, note materialisation and merge.

Fixture-only source snapshots are retained under `/Users/mfwolffe/lanes/cb06/evidence/fixture-files/`, digests in `fixture-shas.txt`, and the final readable Mac/Linux evidence trees under `fixture-mac-pty/` and `fixture-linux-pty/`. The recreated Mac worktree was again removed only after checking it clean and equal to the pushed head; the game play binary is retained unchanged. Completed Linux target/cache outputs were removed after preserving this evidence.

