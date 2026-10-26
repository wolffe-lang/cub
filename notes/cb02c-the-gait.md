Footprint: module

# Note — cb02c, the gait

A fix-up on the maintainer's play of cb02b's build (cub trunk `6153d975`), verbatim: "This is a big
improvement. But it still needs work. The branch paths should be the same color as the coastline/forest
paths. The cub moves much too slowly and its tail oscillates too quickly. Make it natural. Enemies should
never overlap with the cub. They should have collision to prevent weird attack moments where the enemy is
behind the cub and can't be hit." Before/after numbers come from one instrument, `cub --measure` (pace, wag,
chase, path styles, the body census over the real-key scripts); frames and logs are under
`notes/cb02c-evidence/`.

## Prediction

`61c3e8c` committed `notes/cb02c-prediction.txt`, the before census (`measure-before.txt`) and before-frames
after the instrument (`a7b7a71`, `2096b90`; goldens byte-identical with it in, 95 ok) and before any
gameplay change. Hits and misses:

| measure | before (measured) | predicted | after (measured) |
|---|---|---|---|
| trot, straight | 42 FP/tick, 4.92 cells/s | 63, 7.38 | 63, **7.38 cells/s** |
| diagonal | 4.80 cells/s | ~7.2 | 7.28 |
| a quarter turn | 4 ticks, 4.83 cells/s, radius 0.41 | 3 ticks, ~0.4 | 3 ticks, 7.30 cells/s, radius 0.46 |
| to the trot / to a stop | 11 / 5 ticks | 11 / 5 | 11 / 5 |
| wag, walking | 4 ticks (7.5 Hz), 2 frames | ~27 ticks, ≥ 4 frames | **26.5 ticks (0.88 s)**, 5 frames |
| wag, standing | never moves | ~60 ticks | 59.5 ticks (1.98 s), 3 frames |
| wag, sneaking / paw 10 | never moves / not measured (tick-driven: 4 at any walking pace) | ~55 / ~18 | 53.7 / 18.0 (0.60 s) |
| foe's drawing in the cub's | 1,879 ticks (1,935 foe-ticks; 1,043 out of an aimed bite's reach, 493 behind the cub's facing) | 0 | **0** |
| bodies touching, out of reach | 2,604 of 3,692 foe-ticks | 0 | **0** of 513 |
| foe inside foe | 71,580 pair-ticks | 0 | **0** |
| branch paths | grass, 64 on 234 (⠖ ⠶); plain 2 on 0 | the shore's | gravel, 247 on 240 (space · ․ ░); plain 7 on 8 |
| golden directories moved | — | 93 of 95 (all but opening-rich/plain) | **95 of 95**, none added |

- **The miss on the goldens.** The opening's frames draw the standing cub (`art.draw_cub`), whose rest tail
  is now the middle frame, not cb02b's curled one; and every `final.state` gained the trace's new fields
  (the body facing, the gait, each foe's heading and body gap). 95 directories, 1,686 files.
- **The fox's chase.** Predicted that the split turn rate alone would not make the fox lose in the turns:
  it did not (a duel through a quarter turn left the fox even, −0.01 cells), so R-cb02c-6 A (a turn a foe
  cannot make in one tick checks its run) was added; with it the cub gains 0.48 cells on the fox through
  a 12-tick turn while the fox gains 0.35 on a 30-tick straight. Measured too, and said plainly: a fox
  steering at a zigzagging cub it can see cuts the corners and closes faster than on a straight (9 cells
  to its strike at tick 18 against tick 34): pursuit's geometry, unchanged by any turn rate.
- **Census scope.** The 47 recorded scripts are 52,944 script-ticks after (60,787 before; the faster cub
  finishes the same journeys sooner; families nest, so ticks are shared). Before-frames
  `before-contact-t570-*` show the fox hidden under the cub; `after-contact-t572-*` the fox touching it.

## Forbidden

Original work only: pack's `src/sim/sim.lu` was read for the shape of its separation pass (pairs in a
fixed order, bounded repeats, footprints in cells, reach from the flank), never copied; cub's bodies are
the drawings' own rectangles, its push and its reach rule its own. No `lair` change, no pin change, no
workflow, planning-repo or `~/.claude` edit. No merge, label, tag, release or issue action; no plant PR
and no CI dispatch (RULES §7: the three plants ran in this lane's local gauntlet). No attribution
trailers. Every heavy job on nomad ran through `~/lanes/cb02c/heavy.sh` (its own `vm_stat` read, the
8 GB floor, three-minute retries; one wait at the toolchain fetch, 6 and 5 GB, then 20 GB); scratch under
`~/lanes/cb02c/`; every child exec'd or waited for; no package installed; the MLX server, the pool and the
other lane untouched. The Linux leg ran on kasumi in the staged engine container, `LAIR_CPUS=4-7`, under
`/home/mfwolffe/lanes/kasumi-cores-4-7.lock` (`ssh kasumi bash -s`, `setsid -f`, pid file
`/home/mfwolffe/lanes/cb02c/linux-check.pid`); nothing killed by me. Signal witnesses are the engine's pty
rows typing byte 03.

**A breach to report.** The instrument as first written (`census.observe` and the wag probe building their
bitmaps and frames in the ambient region) grew with the ticks it read: `--measure` over the 47 scripts
peaked at 6.9 GB resident and `--body-audit` at 13.5 GB, and I ran them (with `--world-audit` and
`--make-world-proof`) on nomad directly, not through `heavy.sh`, about twenty times before measuring them:
builds, tests and gates went through the script's `vm_stat` floor, these instrument runs did not. RULES §4
forbids a memory-growing harness on the Mac and wants the floor before every heavy job; both were breached. The first Linux leg (`linux-check-oom.log`, head
`a11758f`) was killed by the container's 12 GB limit in the body audit (exit −9). `4523a56` puts each tick,
script and world in its own region: 43 MB and 19 MB peak now, the outputs byte-identical; the game's own
headless run was never affected (39 MB over the 7,862-tick journey; cb02b's 33 MB over its 9,914).

## Inputs verified

- Base trunk `6153d97555b3e1ae7406b9405df0e2cd10033af9`; engine `aa6c4dc0bc5071d3c07121451d913a8837cd2a6a`
  unchanged; wolf 0.2.35, lupin 0.1.56, std `2386522e` staged by the fetchers on both hosts (digests
  checked by the fetcher).
- The contract, `notes/cb02b-the-grove.md`, `cb02a-the-coast.md`, `cb01b-the-feel.md`, `docs/`, the
  design bible §§3/4/8, the campaign, `sprints/RULES.md` §1–§10 and the guide read; pack's separation read
  for its shape.
- No sprint exists in the code (DESIGN.md: "no run binding"): "the sprint multiplier stays the ratio it is"
  is kept as the sneak's half; the wag test evaluates a sprint's pace through the gait and measures the
  fastest trot the game grants (paw 10, 92 FP/tick, ×1.46).
- Rulings recommended and implemented, not decided:
  - **R-cb02c-1 A** the pace ×1.5: `WALK_PERCENT` 110 → 165, the one dial; `TURN_RATE` 16 → 24, `ACCEL`
    4 → 6, `BRAKE` 8 → 12 and the foes' pursuit 44 → 66, retreat 48 → 72 are its products (constants
    derived from it, pinned by `test_cb02c_the_pace_scales_through_walk_percent`), so the turning circle,
    the start and the stop keep cb01b's feel; the foes keep turn rate 16.
  - **R-cb02c-2 A** the wag tied to the gait: one wag per two strides (`STRIDE` 832 FP, 3.25 cells), the
    paws twice a stride, a standing sway floor (`SWAY_V` 28); five tail frames walking, three standing.
  - **R-cb02c-3 A** the mover yields: a step into a body is not taken; the cub moves first, so a tie goes
    against the foe.
  - **R-cb02c-4 A** (new) the envelopes count from the bodies: a reach of n cells is n − 1 clear cells
    between the bodies (bite and a foe's strike 2, lunge and heavy 4), in sight unless they touch, and
    ground under either body never stands between them. B, the centre reach kept with a small collision
    core, leaves the drawings overlapping (the maintainer's "never overlap"): a 4×4 cub and a 4×3 fox
    cannot both be drawn apart and be within two cells centre to centre.
  - **R-cb02c-5 A** (new) a swing of the cub's body (a turn, an attack's aim) that meets a foe pushes the
    foe aside; with no room the body keeps its facing that tick. B holds every such turn.
  - **R-cb02c-6 A** (new) a turn a ground foe cannot make in one tick checks it toward half its pursuit
    (`FOE_TURN_V` 33): the fox keeps up on the straight and loses in the turns. B, the split turn rate
    alone, measured even.
  - **R-cb02c-7 A** (new) no sprint is added: a sprint binding is a controls change (Shift is the sneak)
    the contract did not ask for.
  - **R-cb02c-8 A** (new) cache guards stand a body's width apart along their branch (two cells weasels,
    four foxes), never inside one another; B settles them apart on the first tick.
  - **R-cb02c-9 A** (new) a foe whose body touches the cub's knows where it is, whatever stands between
    their middles (a trunk under the cub's drawing no longer hides a touching foe).

## Evidence index

Commits, each its own chunk:
- Instrument and prediction: `a7b7a71`, `2096b90` (the instrument), `61c3e8c` (prediction, before census,
  before-frames).
- Path colours: `59901ee` one carve predicate and `forest.path_kind`; `5007909` `art.ground_at`,
  `path_styles`, `path_audit`; `f237821` the world audit's `path_off`; `5fafde9` the tests; `c110e26`
  PALETTE.md.
- Pace: `5316695` the dial, its products, the foes' turn rate and turning pace; `ad04d1a` the duel;
  `27c0320` tests.
- Tail: `2a0175d` the wag measure; `b34b107` the gait phase; `da937b3` the five tail frames and two paw
  frames; `930bc75` drawn from the gait on both tiers, the sheet's wag row; `c1f4679` callers; `b3d5e34`
  GLYPHS.md (152 → 154); `e289e84`; `32d7dbb` and `a11758f` the wag tests.
- Bodies: `c8d483f` footprints without bitmaps; `e3e4c4a` bodies, push, settle, the reach rule;
  `27cc3f8` the drawn body facing, contact on the bodies; `3a5a097` the fixtures on the ring; `4a7d6cd`
  ground under a body; `8b2252c` the swarm and `--body-audit`; `47a7845` the body tests; `6a4723d` the
  gameplay gate holds the census and the audit.
- Witnesses: `a84fb36`, `9abc35e` the walker (bodies, the thorn and hawk witnesses, a passive natural
  death); `8b9400e`, `fac5cc6` the real-key scripts regenerated (the journey to tick 7,862; all four coast
  bundles; natural death at 898; death-recovery's first walk shortened for the pace); `4c3ed52` the trace;
  `bbead48` goldens; `855ead3`, `91ad2c2` DESIGN.md and ART.md; `93e59e4` README-only refresh;
  `4523a56` the instrument flat in memory (a region a tick, a script, a world).

| gate | macOS arm64 (nomad) | Linux x86-64 (kasumi, container, cores 4–7) |
|---|---|---|
| fmt / checked tests | 169 pass, 0 failed/rejected/unsupported, 0 SKIP | 169 pass, 0 failed/rejected/unsupported, 0 SKIP |
| native + release, selftest, goldens | 47 scripts × both tiers + art, 95 directories, both backends | byte-identical (190 ok, 0 differ) |
| pty rows | all 12 pass | all 12 pass |
| gameplay / saves / caches / archives / world audit | both backends green, 0 skips | both backends green, 0 skips |
| body census, 47 scripts | 52,944 ticks: overlap 0, contact 513 (out of reach 0, behind the facing 60), foe in foe 0 | identical, both backends |
| body audit, 50 seeds × 2 sizes | 360,956 ticks: 0 / 0 / 0; 100 swarms reached and fought, 194 of 300 weasels killed | identical, both backends |
| 80×24 rich/plain average | 171 / 175 µs (cb02b 167 / 155) | 301 / 284 µs (cb02b 294 / 274) |
| 200×60 rich/plain average | 1244 / 1217 µs (cb02b 1137 / 1123) | 2023 / 2011 µs (cb02b 2060 / 1931) |
| latency median / p90 | 32.9 / 33.4 ms; repeat 32.7 / 33.4 | 13.6 / 33.7 ms; repeat 13.6 / 33.7 |
| idle / 10 s | loud Linux-only skip | 300 switches; repeat 300 |

Both hosts' complete gates (`tools/check`; kasumi's `check-linux` + `check-perf`) ran at
`4523a5688b43a8d5794b4f6962187331a4b05855` (`macos-check.log`, `linux-check.log`); the final head adds this
note and its evidence only.

Golden directories moved (all 95, both tiers, none added): every `tests/cases/*.pk` case's `-rich` and
`-plain` and `art`. The 1,686 golden files, relative paths included, hash to
`dcd4774114b2a45b3bff44bd119b0d75ecfa9a68bf191478e06f66cac1faa5f2` (`golden-hash.py` over `tests/goldens`;
each host's gate diffs its own output against those files).

Plants (RULES §7, a `module` lane: local, in this gauntlet, no CI dispatch, no PR), each red on nomad
(macOS arm64), each reverted:
- **A branch drawn in the forest's colour** (`plant-branch-colour-local.log`): `src/gait_test.lu::
  test_cb02c_branch_0_draws_the_path_colours ... FAILED (trap(assert))` with branches 1–3 and the wide
  test (5 failed); the native `--world-audit` row `0 80 0 … 1021` (1,021 off-colour path cells), exit 1.
- **The tail wagging on the tick** (`plant-tail-tick-local.log`): `src/gait_test.lu::
  test_cb02c_the_tail_wags_on_the_gait_not_the_tick ... FAILED (trap(assert))`, with the frame and the
  hold tests (3 failed); `--measure` reads 8.00 ticks at every pace. The first run of this plant was red in
  one test only (the period test then read the gait counter, not the drawn phase); `a11758f` tightened it.
- **A foe allowed into the cub's footprint** (`plant-foe-in-footprint-local.log`): `src/gait_test.lu::
  test_cb02c_the_census_sees_an_overlap ... FAILED (trap(assert))` among 14 (the swing test, ten combat
  and feel rows); the native census `overlap 904 … contact_unreachable 904`; `--body-audit` exit 1 at seed
  1, 80 columns (158 overlaps).

After-frames: `after-contact-t572-80x24-{rich,plain}/` (natural death, the fox touching the cub's south
flank), `after-branch-t4401-80x24-{rich,plain}/` (a coast branch in the shore's gravel). The after census is
`measure-after.txt`, the fifty-seed audit `body-audit.txt`, the world audit `world-audit.txt`.

## Done-when

- [x] The four branches, their alcoves and the log branch draw the shore's gravel, both tiers; one path
      kind per area and one style set; `path_off` 0 over 50 seeds × both fields × every area.
- [x] The pace ×1.5 through `WALK_PERCENT`; turn rate, acceleration and braking scaled with it; foes
      retuned; the fox keeps up on the straight and loses in the turns (the duel); the hawk unchanged.
- [x] The tail on the gait, one wag per two strides, five frames walking and a slow sway standing; the
      single rotated silhouette kept; periods pinned standing, walking and at the fastest trot.
- [x] No body inside another, the mover yielding; every foe in contact in a bite's reach; the census zero
      over the 47 scripts and over 50 seeds × both sizes with the swarm; the hit-envelope tests green (two
      combat fixtures, `3a5a097`, moved onto the contact ring: their foes had been placed inside the
      cub's drawing).
- [x] Goldens (95), real-key witnesses, pty rows on both hosts; three plants red locally; DESIGN, ART,
      PALETTE, GLYPHS and the README current.
- [ ] The orchestrator watches `tier pr` at the final head.

Play binary: `/Users/mfwolffe/lanes/cb02c/cub/target/cub`. Isolated play:
`target/cub --save /Users/mfwolffe/lanes/cb02c/play.save --ghost-dir /Users/mfwolffe/lanes/cb02c/play-ghosts`
(add `--seed 1` only for a new journey). The maintainer's `~/.cub/save` is schema 1 and this build reads
schema 2 only (since cb02b): it refuses that file by name (`save_version`), so play with `--save`. Keep this
worktree until play is accepted.

Prune after merge and play: `/Users/mfwolffe/lanes/cb02c/` (the worktree, `base/`, `tmp/`, `logs/`,
`kasumi/`, the bundle) and `/home/mfwolffe/lanes/cb02c/` on kasumi.
