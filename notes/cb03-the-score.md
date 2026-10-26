Footprint: module

# Note — cb03, the score

M-CB3's game half on cub trunk `0bcfd0cb`: the cub a fifth faster through the one dial; an original
score of ten parts rendered by the engine's mixer and played by cue; posture as HUD. Evidence under
`notes/cb03-evidence/`. The maintainer's next play rules every number again (R-CB-7).

## Prediction

`b4a232d` committed `notes/cb03-evidence/prediction.txt` before any change. Hits and misses:

| predicted | measured |
|---|---|
| lr01's engine does not stream, so (B): WAVs per part, a cut live where the mixer fades | held; R-cb03-1 B implemented (`docs/SCORE.md`) |
| the whole bank renders in 1–3 s release on nomad | 0.9 s native for the ten parts, one by one (`--score-render`); the live prepare (eleven WAVs written, the backend probed) takes 0.43 s on the release build (434,772 µs in the `sound-live` row, 429,442 in `mute-key`; the eleven WAVs 35 MB) on release |
| PCM goldens about 25 MB, so R-cb03-4 B (sha256 + a one-second head per part, the whole replay) | the bank is 32 MB of PCM (184 s); B implemented, 3.0 MB committed |
| trot 75 FP/tick, 8.79 cells/s; TURN_RATE 29, ACCEL 7, BRAKE 14, foes 79/86, SNEAK_V 37, paw 10 111 | 75, **8.78 cells/s**; every derived constant as predicted |
| the quarter turn 3 ticks, radius about 0.5; to the trot 11, to a stop 6 | 3 ticks, radius 0.55; 11 / 5 (the hold's lapse, as cb02c measured) |
| the diagonal about 8.7 | 8.77 on a clear window; cb02c's window (30 ticks east first) reads 6.32 because it now meets the woods: the instrument says `diagonal_clear` |
| 94 of 95 golden directories for the pace, then all 95 | all 95 moved at the pace alone (the sheet's `pant` row too: its mouth is now the breath frame); then all 95 again with the posture frames, 8 added (four posture cases, both tiers): 103 directories, 1,779 files |
| the overlap census 0/0/0 | 0 / 0 / 0 over the regenerated 47 scripts (48,894 script-ticks; contact 501, 131 behind the facing) and over 50 seeds × 2 sizes (328,240 ticks) |
| 6–14 new braille cells | 16 (GLYPHS.md 154 → 170) |
| about 200 checked tests, 0 SKIP | 190 (169 + 21), 0 SKIP |

A miss not predicted: the wag. The tail and paws are tied to the ground covered (cb02c), so the faster cub
wagged in 22 ticks and a tail frame held two; the fix is R-cb03-5 A below, which also moved the standing
sway's frame count (3 → 4: the breath widens the body under the tail key) and the gait tests' literals not
at all. A second: the pty rows that are not about the music started with it on and lost the keys typed in
the second the WAVs take to render (canonical input before the terminal opens); they pass `--mute` now.

## Forbidden

Original work only: every part is written for cub (`score/*.part`, the format pax's px32 — the engine's
reader — and nothing played, sampled or quoted); pack's `docs/ART.md` posture paragraph was read for the
idea and cub's drawing is its own. No `lair` change: the pin moved to lair's trunk head `57870143` (read
twice, `git rev-parse origin/trunk` and `git ls-remote`, identical), the goldens on both hosts proving the
move; the live player reaches the engine's output owner through its public fields and std.process, never
an engine edit (the lair need is below). No workflow, planning-repo or `~/.claude` edit. No merge, label,
tag, release or issue action; no plant PR and no CI dispatch (RULES §7: the three plants ran in this lane's
local gauntlet). No attribution trailers. Every heavy job on nomad ran through `~/lanes/cb03/heavy.sh`
(its own `vm_stat` read, the 8 GB floor, three-minute retries: two waits of 180 s at 21:31 and 21:34
local, 6 and 4 GB short, then 25 GB); scratch under `~/lanes/cb03/`; every child exec'd or waited for;
no package installed; the MLX server (:8002), the pool and cb04's worktree and branch untouched. wl69's
agentic queue (three `opencode run` sessions) ran on nomad throughout; the perf gate ran once, at the
final source head, with them running (the numbers below say so). The Linux leg ran on kasumi in the
staged engine container, `LAIR_CPUS=4-7`, under `/home/mfwolffe/lanes/kasumi-cores-4-7.lock` (`ssh kasumi
bash -s`, `setsid -f`, pid file `/home/mfwolffe/lanes/cb03/linux-check.pid`); nothing killed by me.
Signal witnesses are the engine's pty rows typing byte 03. The music plays through `afplay` only in the
two sound rows, for about a second each.

## Inputs verified

- Base trunk `0bcfd0cbc6a6226d76c82b365c5ecabb8a42bdfb` (cb02c's merge), unchanged under this branch at
  hand-back; engine `aa6c4dc0` → `57870143ebbb4806b8bee40379e8c6e781f50842` (lair trunk: lr01's mixer
  at `09f5aa54` and its note); wolf 0.2.35, lupin 0.1.56, std `2386522e` staged by the fetchers on both
  hosts (digests checked by the fetcher).
- The contract, the campaign (M-CB3, innovations 4 and 5), lair's `notes/lr01-the-mixer.md` and
  `docs/SOUND.md`, cb02c's, cb02b's and cb01b's notes, `docs/`, pax's `notes/px32-format.md`, pack's
  posture paragraph, RULES §1–§10 and the guide read.
- What lr01's engine gives a game, read from `src/sound/`: `prepare`/`render` (0–30 s a part),
  `mixer`/`cue`/`tick` (deterministic PCM, four slots, sample-count fades), `wav`, `start`/`finish` (a
  prewritten WAV to afplay or paplay; `finish` waits for the child to end; no cancel, no stream),
  `oss_requests`/`oss_answers` (a stub). `Output`'s fields are public, so a game can kill and reap the
  child itself.
- Rulings recommended and implemented, not decided:
  - **R-cb03-1 B** the music path today: each part rendered once at start to a WAV (`~/.cub/sound/`,
    `--sound-dir`), the current cue's WAV played by the engine's output owner (afplay on macOS, paplay
    on Linux), ended with std.process's kill-then-wait when the cue changes and started again when its
    length is up. The same schedule drives the engine's mixer for the goldens and the tests, where the
    fades are. Live, an area change is a cut, a boss theme replaces the loop without its fade, the sting
    cuts the loop: the note says so because the engine streams nothing (lair's docs/SOUND.md). A is lr02's.
  - **R-cb03-2 A** four health bands (full ≥ 3/4, hurt ≥ 1/2, badly hurt ≥ 1/4, dying), each a frame
    set of the one silhouette (`silhouette.cub_posed`; `docs/ART.md`); B's blend would need more drawings
    than a 1:2 cell reads.
  - **R-cb03-3 A** the numbers only at a den and on the death card (the card gained them), with **B as a
    debug flag**: `--hud` puts cb01b's bars back beside the scent, off by default (`sim.hud`).
  - **R-cb03-4 B** (new) the PCM goldens: a sha256 and length per part plus the part's first second of
    PCM (192 kB) and the whole six-second cue replay (1.15 MB): 3.0 MB committed. A, whole-part PCM, is
    32 MB of goldens (184 s × 192 kB/s), three times cub's frame goldens; the sha is the same oracle,
    the head gives a diff its bytes.
  - **R-cb03-5 A** (new) the gait scales with the dial: `STRIDE` 832 → 998 and `SWAY_V` 28 → 34 as
    products of `WALK_PERCENT` from cb02c's 165 (`GAIT_BASE_PERCENT`), so the wag keeps the 0.9 s at the
    trot, 0.6 s at paw 10 and 2 s standing that cb02c's play set, and a tail frame holds three ticks or
    more at the trot (gait_test's literals stand). B, the stride kept, wags in 22 ticks with two-tick
    frames, the flicker the maintainer retired creeping back at a grown paw.
  - **R-cb03-6 A** (new) the boss duck is the engine's replace fade: the area's loop fades out under the
    theme over its `cue replace fade` ticks and returns when the boss falls. A true duck (the loop held
    at a lower level under the theme) needs a per-slot gain the mixer has not got: a lair need, below.
- Every number is a dated proposal in `docs/DESIGN.md` ("The pace, +20 %", "Posture as HUD", "The score").

## Evidence index

Commits, each its own chunk: `30ba40f` the pace (the dial 198, the stride and sway derived, the diagonal
instrumented, the literals); `0df17fa` the pin and the `sound` link; `7dc27e4` the ten parts and
`tools/score-embed`; `03accd8` the score module; `3e88f9c` the live wiring (`--mute`, `CUB_SOUND`, `m`,
the score commands); `b35a94c` posture as HUD; `b37b434` the tests, `tools/score-check`, the sound pty
rows; `98220a1` the goldens (95 moved, 8 added) and GLYPHS.md; `f328b2d` docs; `934caf1` the score gate
in `tools/check`; `fe8177e` README-only; `62a2158` the score goldens and the muted rows; `19ef4c2` the
parts' levels and seams; `86c1537` the code-point enumeration per cell row.

**The pace** (`cub --measure`, `measure-before.txt` and `measure-after.txt`): trot 63 → **75 FP/tick,
7.38 → 8.78 cells/s** straight, diagonal 7.28 → 8.77 (clear window), the quarter turn 3 ticks at radius
0.46 → 0.55, to the trot 11, to a stop 5, sneak 31 → 37, foes 66/72 → 79/86, paw 10 92 → 111; the wag
26.5 → 26.6 ticks walking, 59.5 → 58.75 standing, 18.0 → 18.0 at paw 10; the fox's duel 0.35 → 0.46
cells gained on the straight, 0.48 → 0.62 lost in the turn. The real-key scripts regenerated through
`--make-world-proof` (the journey to tick 7,017; natural death at 841); the census 0 / 0 / 0.

**The score.** Ten parts, 184 s of music with the silence (`docs/SCORE.md` has the table): title 20 s,
shingle 24, bramblehold 24, larkmeadow 24, boss-boar 16, boss-lynx 12, boss-elk 20, boss-alpha 24, den
10, death 12 (once). The release renders of every part hash identically on nomad and kasumi, native and
release (`score-check-nomad.log`, `linux-check.log`); the cue replay (title, the Shingle, a den, the
Shingle, the boar, a fall, the wake; 180 ticks) hashes `ed2aa4ee…`. Every loop's last tick peaks under
-42 dBFS (the seam bar 256; the loudest, larkmeadow, 179). Render times natively, one part at a time:
0.03–0.12 s each, 0.9 s the ten. The live prepare (eleven WAVs written, afplay probed) takes 0.43 s on the release build (434,772 µs in the `sound-live` row, 429,442 in `mute-key`; the eleven WAVs 35 MB).

**The output.** macOS: the `sound-live` row starts the game with music on and finds `/usr/bin/afplay`
as the game's child during the run, eleven WAVs under `--sound-dir`, none after, no child after; the
closing line reads `sound on backend macos answers 1 … cue title`. The `mute-key` row: `m` ends the child
(no afplay while muted), `m` again cues afresh (`starts 2`), the key recorded as `mute`. `sound-oss`:
`CUB_SOUND_BACKEND=oss` → `oss_ioctl_unsupported` once on stderr before the terminal, `answers 0`, no
child. `sound-mute`: `--mute` and `CUB_SOUND=0` write no WAV and start nothing. Linux (kasumi's
container): the same rows; no paplay, so `player_missing: paplay` once, `answers 0`, the WAVs the sink.
PAX's `/dev/dsp` is gm01's/cb05's: they need wolf-std's ioctl adapter (lr01's follow-on 1) or a PAX
device adapter, then a `paxs` backend word in `score.backend_of`.

| gate | macOS arm64 (nomad) | Linux x86-64 (kasumi, container, cores 4–7) |
|---|---|---|
| fmt / checked tests | 190 pass, 0 failed/rejected/unsupported, 0 SKIP | 190 pass, 0 failed/rejected/unsupported, 0 SKIP |
| native + release, selftest, goldens | 51 scripts × both tiers + art, 103 directories, both backends | byte-identical (206 ok, both backends, 0 differ) |
| score-check | ten parts × two backends, the replay, the seams, the WAV, the refusal: green | green, the same hashes |
| pty rows | all 16 pass (12 + the four sound rows) | all 16 pass (paplay missing named once; the WAVs the sink) |
| gameplay / saves / caches / archives / world audit | both backends green, 0 skips | both backends green, 0 skips |
| body census, 47 scripts | 48,894 ticks: overlap 0, contact 501 (out of reach 0, behind the facing 131), foe in foe 0 | identical |
| body audit, 50 seeds × 2 sizes | 328,240 ticks: 0 / 0 / 0; 100 swarms reached and fought | identical |
| 80×24 rich/plain average | 172 / 165 µs (cb02c 171 / 175) | 306 / 283 µs (cb02c 301 / 284) |
| 200×60 rich/plain average | 1174 / 1149 µs (cb02c 1244 / 1217) | 2076 / 2001 µs (cb02c 2023 / 2011) |
| latency median / p90 | 32.3 / 34.0 ms; repeat 11.2 / 33.6 | 13.6 / 14.6 ms; repeat 13.6 / 33.7 |
| idle / 10 s | loud Linux-only skip | 301 switches; repeat 300 |

Both hosts' complete gates ran at the source head `86c1537f21ca9e081d7ba4edf9616acaad2ddecd`
(`macos-check.log`, `linux-check.log`); the final head adds this note and its evidence only. The perf
gate on nomad ran once, with wl69's three opencode sessions and the MLX server running.

Golden directories moved (all 95, both tiers, none removed): every `tests/cases/*.pk` case's `-rich`
and `-plain` and `art` (the sheet gained the `hurt` and `breath` rows); added: `posture-full`,
`posture-hurt`, `posture-badly`, `posture-dying` (both tiers) and `tests/goldens/score/`. The 1,779
golden files, relative paths included, hash to
`2467abb351745d7e6100141bd23897f0742e9c52d83b355c4faedc97d9bedd2c` (`golden-hash.py` over
`tests/goldens`).

Plants (RULES §7, a `module` lane: local, in this gauntlet, no CI dispatch, no PR), each red on nomad
(macOS arm64), each reverted (`git checkout`, 0 changed files after each):
- **A part that does not parse** (`plant-part-parse-local.log`): `score/shingle.part` bar 2, the flute a
  quarter short. `tools/score-check` red at `--score-list`: `score: shingle: line 16: part 'breath' fills
  bar 2 short by 20160 units (80640 a whole note)`, exit 2, and
  `src/score_test.lu::test_cb03_every_part_parses_at_its_written_length ... FAILED (trap(assert))`.
- **A cue that never ducks** (`plant-no-duck-local.log`): `score.want` never takes the boss branch.
  `src/score_test.lu::test_cb03_a_boss_theme_ducks_the_area_loop ... FAILED (trap(assert))` (with
  `want_decides_in_order` and `the_replay_scenes_cover_the_schedule`, 3 failed), and `tools/score-check`:
  `score-golden replay/release FAILED at byte 480002` (tick 75, where the boar's theme should enter).
- **A hurt band drawn as the healthy frame** (`plant-hurt-healthy-local.log`): `silhouette.cub_posed`
  ignores the band. `src/posture_test.lu::test_cb03_the_hurt_frames_are_the_one_drawing_changed ...
  FAILED (trap(assert))` (with `health_changes_the_cub_alone` and `glyphs_test::
  test_glyphs_doc_matches_the_tier`, 3 failed); `.lair/tools/goldens`: `death-recovery-rich DIFFERS`,
  `fox-feint-rich DIFFERS`, `natural-death-rich`, `rest-rich`, the three hurt posture cases and `art` (8 directories), exit 1. (The first run of this plant read its goldens status through a pipe; the rerun reads it directly.)

## Done-when

- [x] The pace +20 % through `WALK_PERCENT` 198 alone; the derivations as cb02c left them, the test
      literals moved; `--measure` before and after; the census 0/0/0; the real-key scripts and goldens
      regenerated.
- [x] Ten original parts under `score/`, each parsing and rendering to its pinned bytes on both hosts
      and backends, looping without a click; the cue schedule (the area loop, the crossfade, the boss
      duck, the death stop, the den resume) tested and pinned by the replay golden; `--mute`,
      `CUB_SOUND=0`, the `m` key; the title card names the key; the boss slots named in `docs/SCORE.md`.
- [x] The output proved: afplay on macOS as the game's child, gone with it; the WAV sink and the named
      refusals on Linux; R-cb03-1 B stated.
- [x] Posture as HUD: four bands and the breath in the one silhouette, the numbers at the den and the
      death card, `--hud` off by default, the scent counter and the area-name flash kept, the reticle
      unchanged; the sprite tests and the sheet's rows pin the frames; a golden per band.
- [x] Tests (190, 0 SKIP), goldens (103 directories), real-key witnesses and pty rows on both hosts,
      three local plants red, docs (SCORE new; DESIGN, ART, KEYS, REPLAY, GLYPHS, README), this note.
- [ ] The orchestrator watches `tier pr` at the final head.

Lair needs to report (none filed): a streaming sink or a cancel on `sound.Output` (lr02), so a game's
live transitions can carry the mixer's fades; a per-slot gain in the mixer for a true duck; the OSS
device adapter (lr01's wolf-std follow-on) for PAX.

Play binary: `/Users/mfwolffe/lanes/cb03/cub/target/cub`. Isolated play:
`target/cub --save /Users/mfwolffe/lanes/cb03/play.save --ghost-dir /Users/mfwolffe/lanes/cb03/play-ghosts`
(add `--seed 1` only for a new journey; `--mute` for silence, `--hud` for the bars). The maintainer's
`~/.cub/save` is schema 1 and this build reads schema 2 only (since cb02b): play with `--save`. Keep this
worktree until play is accepted.

Prune after merge and play: `/Users/mfwolffe/lanes/cb03/` (the worktree, `tmp/`, `logs/`, `kasumi/`) and
`/home/mfwolffe/lanes/cb03/` on kasumi (its `cub/target/` pruned at hand-back; the clone and toolchain
remain).
