# cb18 — the new enemies: six foes with their sprites, patterns and tells

The Sol lane (GPT-6.1-Sol) built the six and stopped when its Codex limit ran out (2026-10-28), its last work
uncommitted in the Mac worktree; the Opus lane picked it up on 2026-10-29 (the contract's addendum) and finished
it. Base: cub trunk `ed180ef5` (cb10–cb15 merged).

Footprint: module

## Prediction

Two predictions stand, each committed before the change it predicts: the Sol lane's `6b938bcb` (six kinds with
four-way bodies, tells and at least twelve ticks of recovery; 600 arena encounters resolved by the ordinary-key
fighter; the moths dimming the palette, R-cb18-1 A) and the pickup's `87688900`: the lynx's bleeding was the Sol
lane's own uncommitted line, so it comes out and the lynx cases, goldens and boss census return to trunk's
bytes; every other old case or golden that moved, moved because cb18 places its foes in the Stand, the Burn, the
Mere, the Underteeth and the Howe. Both held (the evidence below). What the pickup's prediction did not foresee:
the whole checked suite, which the Sol lane had only run filtered, had one red cb14 row and five rows out of the
checked machine's step budget (`pickup/checked-suite-first-red.txt`); "What the pickup changed" says how each
was answered.

## Forbidden

Original work only; the bible's names. No engine, pin, CI, `tools/check*`, save-format or replay-format change
(CUB 7, journey 6 and the 32 lore lines unchanged); no label, merge, tag, release or issue; nothing in
`~/.claude` or the planning repository. The Sol lane's state was saved before any change (the local branch
`cb18-wip-1029` at `5473eac5`, and `~/lanes/cb18/wip-1029/`: the binary diff, the untracked files' archive and
the status, sha256-listed) and never discarded. The lynx, not a new foe, is left as trunk has it. Mac work ran
behind `/Users/mfwolffe/lanes/mac-build.lock` with the 8 GiB floor inside it; kasumi work on cores 0–3 under
their flock, in the lane's own clone under `/mnt/steamlib/lanes/cb18/`; nothing killed by process group.

## Inputs verified

Toolchain and engine as pinned (wolf 0.2.35, lupin 0.1.56, std `2386522e`, lair `74b89744`), unchanged.

The Sol lane's commits, kept as they were: `6b938bcb` (prediction), `f6d6f9f3` (six timed patterns and burn),
`e1e28b5e` (four-way drawings and status palettes), `2f986f44` (the arena census through ordinary keys),
`91a6ef5b`, `74dd06b9`, `f9b7750e`, `af0284bf`, `042ec06d`, `b755e048`, `e5e300bd`, `e963a3a2`, `f9ad7d06`,
`a1a72f3b` (arena baselines and the plant's red), `36dfe52c`, `62656b6f`, `6fc2991c`, `4c3d0324`, `e5b04709`,
`90e69e51`, `1eed99b2`, `3bf1551b`, `7cf46446`, `3a454f10`, `8504725e`, `129b44c7`, and the two approved at the
checkpoint: `f1637e57` (the new-kind-only `drive_as` walker hook) and `344ba786` (ice melts on entering the Burn).

The pickup's commits (the Sol lane's uncommitted work, verified and committed in chunks, with the pickup's
changes named):

- `87688900` the pickup's prediction.
- `b12543fd` the six placed in their areas, the marten's theft (one pouch item, returned at the trunk's foot)
  and bleeding, the statuses; the lynx's bleeding line taken out; the placement search made cheaper with the
  same slots.
- `f1a17a58` the Underteeth lit by its worms; the flash pauses with the pouch.
- `0e577bf2` the body census reads the six's own solidity.
- `0c1f947a` the foe census admits the new areas' foes and appends their 500-row distribution.
- `1d0adb24` `--new-foe-spawn-census`; `79c3ceec` its gate on both binaries.
- `4076d38c`, `21969833`, `c076e7ea` the six's tests (theft, bleeding, burn, statuses; placements, the heron's
  pass, the wisps' sentries; the inventory overlay above the needles).
- `e08b727d`, `afd61ba2` the two inherited tests the placements reach (below).
- `37ece278`, `1e3c2452`, `3510b37d`, `bec28c80`, `7aa68437`, `04f5543a`, `b76b6e7f`, `e35db175`, `56b33f00` the
  goldens by area (the status sheets, the arena encounters, the Stand, the world walk, the Burn, the Mere, the
  Underteeth, the Howe, the walk to the stone mouth).
- `fd68b7a0` the docs; `a4cec192` the README (README only; read whole: the six's paragraph and the new census
  flag are current, nothing else moved).
- `c3627a03`, `6c675e25` the evidence: the ledgers against `ed180ef5` with the lynx rows out; the pickup's
  controls, censuses and probe.

**Rulings.** R-cb18-1 A (the moths dim the palette on both tiers, never blank a glyph): implemented.
**R-cb18-2, to the orchestrator: the lynx's bite and bleeding.** Contract item 2 names the lynx's bite as the
bible's bleeding; the addendum holds the lynx out of scope (not a new foe). The Sol lane had wired it (one line
in `sim.boss_hit`, uncommitted), which moved every lynx row of the boss census and regenerated the three lynx
cases. Recommend A, implemented: cb18 leaves the lynx as trunk has it
(`test_cb18_lynx_bite_stays_trunks_and_does_not_bleed` pins it), and the lynx's bleeding lands as its own change
with its own boss-census comparison; B (wire it here) is kept on `cb18-wip-1029`. R-cb18-3 A (the Sol lane's,
renumbered from its R-cb18-2: an unreturned theft is lost on reset; B would need CUB 8): implemented, the
maintainer's to confirm.

**Every old case and golden that moved, against `ed180ef5`** (row by row in
`notes/cb18-evidence/golden-key-changes.tsv`, 487 rows; `generated-case-receipts.tsv` for the cases):

- *Reverted to trunk, byte-equal:* `tests/cases/boss-lynx-{windup,phase2,beaten}.pk` and the goldens
  `boss-lynx-beaten-{rich,plain}` and `boss-lynx-phase2-{rich,plain}` (43 ledger rows dropped). Cause: the lynx's
  bleeding, out of scope (R-cb18-2). The boss census is byte-identical to trunk's on both builds
  (`pickup/boss-census-final.txt.gz`), so the Sol lane's `bleed-boss-changes.tsv` (lynx rows only) is gone.
- *Kept, caused by cb18's placements (contract item 1, the spawn tables per area):* the Stand's three martens
  move the world walk's keys past the ridge, and so `world-meadow`, `hawk-shadow`, `hawk-stoop`, `world-hawk`,
  `world-recovered`, `world-return`, `coast-cache-0..3` and the Stand's landmark witnesses `landmark-7-0` and
  `landmark-7-1` (cases and goldens); the area scenes `stand`, `burn`, `mere`, `howe`, `underteeth`, the
  landmarks `landmark-8-0`, `landmark-9-0`, `landmark-10-0`, `landmark-11-0..5` and the rests
  `rest-{stand,burn,mere,underteeth}-{80x24,120x40}` (their final states list the appended foes; frames where a
  foe is in view). The Underteeth's also carry the glow-worms' light (`sim.glow_dark_area`: a cave without its
  worms is dark three cells off, contract item 1).
- *The proof of cause* (`pickup/control-no-placement.log`): a control build with the one placement call
  (`append_new_area_foes`) removed regenerates every generated case byte-equal to trunk's generator (0
  differences), and on trunk's keys reproduces trunk's goldens on every case above but `underteeth` and
  `landmark-10-0`, whose `.sty` differs by the dark-cave rule alone. The final build's generators reproduce the
  tree's twelve moved cases exactly and differ from the tree elsewhere only where trunk's own generator does
  (the 35 legacy `journey 4` snapshot headers the tree keeps; `pickup/generators-final-vs-trunk.log`). The foe
  census moves only the new areas' rows (7–11), every old area's bytes unchanged, and appends the distribution
  (`pickup/foe-census-trunk-vs-final.diff.gz`).

**What the pickup changed in the code**, beyond taking the lynx line out:

- *The placement search* (`b12543fd`) finds the same first slot for less: the den refuge is read once a search,
  not once a candidate, and the ring walk jumps over the rows it skipped anyway. The four checked rows that
  decode a save (thirteen `area_foes` calls each) had run out of the step budget:
  `journey_test::test_cb02_all_dens_restore_with_growth_and_water`,
  `cb14_migration_test::test_cb14_the_older_fixtures_still_read`,
  `denmemory_test::test_cb04f_rest_and_death_reset_every_area_but_not_bosses`,
  `map_test::test_cb14_the_burnt_oak_and_the_stone_mouth_open_to_a_lunge_and_save`. They pass, and every
  placement is the one before (the generators and goldens byte-equal, above).
- *`bosses_test::test_cb04_a_boss_never_leaves_its_arena`* (`afd61ba2`) is one test a boss (`_boar`, `_lynx`,
  `_elk`, `_alpha`), the same assertions and the same 200 ticks each. On trunk the four in one test sat at
  exactly the budget: `wolf conform-run --checked` on the test's own body fits 200 ticks and not 201, on both
  hosts (`pickup/boss-budget-probe.txt`; the lane's code fits 198), so any tick the six new kinds add ran it
  out (the Sol lane's first foe commit `f6d6f9f3` already did).
- *`map_test::test_cb14_every_alcove_has_its_own_bit_and_a_named_slot`* (`e08b727d`) counted every non-boss foe
  of the new areas as a guard ("the new areas' foe tables are cb18's and empty"); it counts the guards and
  asserts they keep their saved ordinals ahead of cb18's appended six.

From cb17 (relayed 2026-10-29): the Howe's wisps lead to sentries that are fought inside the Howe's walk rows
(row 150 to the stone mouth), where cb17's `walk` part plays; nothing in either lane changes for it.

## Evidence index

`notes/cb18-evidence/` holds the Sol lane's records (the reds first: `marten-travel-red.log`,
`marten-trunk-red.log`, `moth-orbit-red.log`, `moth-rally-red.log`, `needle-visibility-red.log`,
`phase-alias-red.log`, `wisp-lock-red-2.log`; the arena stage, the hit rings, the equivalences) and the pickup's
under `pickup/`.

- **The plant:** cub#76 (`cb18-plant-no-recovery`, `a1e88cfe`, off the line): the marten without recovery,
  `fairness_recovery_9 RED: no human-scale recovery`, `CB18_PLANT_EXIT 1` (`plant-red.log`, nomad). It stands.
- **The old-kind equivalence:** `old-kind-generated-equivalence.tsv` and `old-kind-walk-equivalence.tsv`: the
  walker hook leaves every old-kind generated case and walk byte-identical (trunk, before, after).
- **The checked suite:** first whole run over the Sol lane's tree, red: 634 passed, 1 failed, 5 unsupported
  (`pickup/checked-suite-first-red.txt`, nomad). After the fixes, kasumi's container over the same source as
  `6c675e25`: `wolf test: 643 passed; 0 failed; 0 rejected; 0 unsupported; 0 filtered out`, `test: 0 SKIP lines`
  (`pickup/checked-suite-kasumi-synced-tree.log.gz`).
- **The goldens:** kasumi's container, the native build over the same source: 509 `ok`, 0 `DIFFERS`; every
  generator against the tree, clean beyond the legacy snapshot headers; the distribution 500 rows. The Mac,
  targeted: the 42 old moved and new-area cases on both tiers (84 `ok`), the generators and censuses as recorded.
- **The Linux gate at `6c675e25`** (kasumi cores 0–3, the engine's container, `tools/check-linux` then
  `env LAIR_PERF_SLACK=1 tools/check-perf`, stopping at the first red step): launched 2026-10-29T21:09:48Z as `setsid -f bash kasumi-gate.sh 6c675e25…`, pid 1896801, log `/mnt/steamlib/lanes/cb18/gate.log`, marker `/mnt/steamlib/lanes/cb18/gate.exit` (its exit, with `CB18_KASUMI_GATE_EXIT N` the log's last line). At hand-back: `END prepare-pty exit=0`, the python tests and pty fixtures `status=0`, `check-fmt: canonical`, `wolf test: 643 passed; 0 failed; 0 rejected; 0 unsupported; 0 filtered out`; the rest (the builds, the goldens, the pty rows, both gameplay gates, the memory gate, the perf pass at slack 1) still running; no green claimed for it.
- **The Mac leg at `6c675e25`** (behind the lock: both builds, the selftest, the checked tier, the six's gameplay
  gate, the generators, then the full golden check, at most three attempts): green at the first attempt (`pickup/mac-gate-6c675e25.log`, the floor inside the lock): `END build exit=0`, `END selftest exit=0`, `END test exit=0` with `wolf test: 643 passed; 0 failed; 0 rejected; 0 unsupported; 0 filtered out` and `test: 0 SKIP lines`, `END new-foes exit=0` (`gameplay: six foes 600 arena resolutions, complete hit rings, six replay outcomes and both-tier frames green`), `END generators exit=0`, `END generators-same-as-recorded exit=0`, `END goldens attempt 1 exit=0 ok=509 differs=0`, `CB18_MAC_GATE_EXIT 0`. It runs no pty row (so neither `sound-live` nor `mute-key`).

## Done-when

- [x] The six with their four-way sprites, tells, windows, weaknesses and scent; placed in their areas (the
  Teeth and the Hush get none); the 500-row distribution gated on both binaries.
- [x] The marten's theft and bleeding, the adder's burn, the yarrow and water cures; the lynx left as trunk's
  (R-cb18-2).
- [x] 600 arena encounters by the ordinary-key fighter; the hit rings; six replayed encounters on both tiers.
- [x] Every old case and golden that moved kept with its cause or reverted (above).
- [x] The plant red by name, off the line (cub#76).
- [x] Test targets: the checked suite (643, 0 unsupported, 0 SKIP); the goldens (509); the generators against
  the tree and trunk; the foe, boss and spawn censuses; the no-placement control; the step-budget probe.
- [x] The Mac leg at the head: green (the evidence index).
- [ ] The Linux gate at the head: launched, running at hand-back (pid, log and marker in the evidence index).

Ledger: cb18 | the new enemies | module | PR #86 | plant #76 | final head: this PR's head.
