# cb18 — the new enemies: six foes with their sprites, patterns and tells

The Sol lane (GPT-6.1-Sol) built the six and stopped when its Codex limit ran out (2026-10-28), its last work
uncommitted in the Mac worktree; the Opus lane picked it up on 2026-10-29 (the contract's addendum) and finished
it. Base: cub trunk `763616eb` (cb10–cb17 merged). The pickup began over `ed180ef5` and rebased twice, once at
each merge the orchestrator named and always onto trunk: at cb17's onto `40c6410b`, at cb16's onto `763616eb`
(below). Every commit sha here is the second rebase's; a gate's sha is the head it ran at, named as such.

Footprint: module

## Prediction

Two predictions stand, each committed before the change it predicts: the Sol lane's `b0b88454` (six kinds with
four-way bodies, tells and at least twelve ticks of recovery; 600 arena encounters resolved by the ordinary-key
fighter; the moths dimming the palette, R-cb18-1 A) and the pickup's `90777547`: the lynx's bleeding was the Sol
lane's own uncommitted line, not cb15's; every other old case or golden that moved, moved because cb18 places its
foes in the Stand, the Burn, the Mere, the Underteeth and the Howe. Both held (the evidence below). The pickup
first took the lynx's line out (the addendum's reading); the orchestrator then ruled R-cb18-2 **B** (contract item
2 gives the lynx's bleeding to cb18), and the line is back: restored at the pickup's head it reproduces the Sol
lane's three lynx cases, their goldens on both tiers and its boss census byte for byte
(`pickup/lynx-restore-vs-wip.log`). What the pickup's prediction did not foresee: the whole checked suite, which
the Sol lane had only run filtered, had one red cb14 row and five rows out of the checked machine's step budget
(`pickup/checked-suite-first-red.txt`); the census's hit columns, which counted bleed ticks as strikes; the
marten's bite bleeding, which §6 does not give it; found by the Linux gate and the gameplay gate after the first
rebase, the body census reading a boss's drawing for the six, a killing bleed tick that stood the cub back up, and
the lynx's bleeding unwinnable for the fighter in one world once its falls counted (R-cb18-5); and over cb16, the
Stand's last marten inside the Hermit's talk radius, two checked rows out of the budget and a save row still
asserting CUB 7.

## Forbidden

Original work only; the bible's names. No engine, pin, CI, `tools/check*`, save-format or replay-format change
(cb16's CUB 8, `journey 7` and 48 lore slots unchanged; cb18 saves nothing new); no label, merge, tag, release
or issue; nothing in `~/.claude` or the planning repository. The Sol lane's state was saved before any change
(the local branch `cb18-wip-1029` at `5473eac5`, and `~/lanes/cb18/wip-1029/`: the binary diff, the untracked
files' archive and the status, sha256-listed) and never discarded. Mac work ran behind
`/Users/mfwolffe/lanes/mac-build.lock` with the 8 GiB floor inside it; kasumi work on cores 0–3 under their
flock, in the lane's own clone under `/mnt/steamlib/lanes/cb18/` (its stale synced edits stashed, two stashes,
before the gates over cb16, not discarded); the superseded gates (at the pre-rebase `6c675e25` and `18cc09a0`)
were stopped by their own pids and their own containers' ids, nothing by process group, no other lane's container
touched. One lapse, reported: stopping the lane's own Mac gate runner (22:06Z) just as it took the lock let its
trap remove the lock while its child ran on; the child (a checked-suite run) was stopped by pid about a minute
later, beside hx07's job, which had taken the freed lock. cb16's NPCs never move for cb18: the six's spawns do.

## Inputs verified

Toolchain and engine as pinned (wolf 0.2.35, lupin 0.1.56, std `2386522e`, lair `74b89744`), unchanged.

The Sol lane's commits, kept as they were: `b0b88454` (prediction), `1c86bebc` (six timed patterns and burn),
`74fc2ea5` (four-way drawings and status palettes), `2f8c51f6` (the arena census through ordinary keys),
`a5c46bc0`, `6616168d`, `fb2e96ad`, `fe9acd72`, `2b42c232`, `8d5ac9d7`, `db3bf9df`, `5e6089fe`, `ceab4405`,
`5a02da10` (arena baselines and the plant's red), `6b9c932e`, `0f81a566`, `78bf48b0`, `b57fbff4`, `4a07e302`,
`4e6b6dd2`, `d4109653`, `3dce41c5`, `e3432caf`, `00cae76b`, `f267155f`, `9d89abe3`, and the two approved at the
checkpoint: `1379d8bb` (the new-kind-only `drive_as` walker hook) and `b771d955` (ice melts on entering the Burn).

The pickup's commits (the Sol lane's uncommitted work, verified and committed in chunks, with the pickup's
changes named):

- `90777547` the pickup's prediction.
- `3e1670fc` the six placed in their areas, the marten's theft (one pouch item, returned at the trunk's foot),
  the statuses, the placement search made cheaper with the same slots (the lynx's line out, then; back in
  `ccb44de9`).
- `24aa89cb` the Underteeth lit by its worms; the flash pauses with the pouch.
- `32771247` the body census reads the six's own solidity.
- `e2bbf58e` the foe census admits the new areas' foes and appends their 500-row distribution.
- `c5bafccd` `--new-foe-spawn-census`; `451c3348` its gate on both binaries.
- `ebe2e0d6`, `d3cffd5b`, `fb739ed5` the six's tests (theft, burn, statuses; placements, the heron's pass, the
  wisps' sentries; the inventory overlay above the needles).
- `413b330a` the inherited alcove test the placements reach (below). The boss arena row's split (the pre-rebase
  `389a8ce1`) left at the rebase onto cb16, whose `6eafa61f` makes the same split; cb18's commit was then empty.
- `3504cbd2`, `aa7d8912`, `01e60e67`, `881f4af9`, `2ebb446a`, `1ca41211`, `f46b9775`, `28452b06`, `80978bd1` the
  goldens by area (the status sheets, the arena encounters, the Stand, the world walk, the Burn, the Mere, the
  Underteeth, the Howe, the walk to the stone mouth).
- `79c58124` the docs; `0460c4c2` the README (README only).
- `0582cf25`, `a445bb8e` the first evidence.
- After the ruling: `ccb44de9` a landed lynx swipe bleeds (R-cb18-2 B, the Sol lane's line); `f8f0496e` the
  marten's bite steals and does not bleed (§6); `69441c4e` the boss census's landed strikes apart from its damage
  events (R-cb18-4 B); `9d9436f2` their tests; `7ae97b10` the lynx's goldens; `99a6cfbb` the marten's arena
  frames; `84e6926c` the docs; `63bbcca4` the README (README only; read whole: the six's paragraph, the bleeding
  sentence and the new census flag are current, nothing else moved); `dcb2a383` the evidence.
- After the first rebase and its gates: `e93e9767` the body census reads art's drawings of the six (`3cf971d7` its
  test); `113bb973` a killing bleed tick ends the step (`bb9e5a4a` its test); `32b1739c` the lynx's fixture
  carries yarrow and the fighter eats it on a bleed (R-cb18-5 A); `766c135d` the lynx's goldens; `2274bc09` the
  docs; `b6145fa0`, `a089d8d1` the evidence and ledgers.
- After the rebase onto cb16: `bd5a6370` the yarrow given to the boss fight's journey only (`fight.fight_journey`;
  in `journey_at` it reached the dens' generated fixtures too); `9b5cc29e` the six's spawns kept out of every
  NPC's talk radius (`73647569` its test; `0724eb94` the spawn census's verdict and its gate; `ac6e7097` the docs
  and the README's lines, cb18's save sentences brought to CUB 8); `4d71189f` cb18's six cases from the generator
  over cb16; `30639d4c`, `87945e8d`, `caf8acd3` the goldens by cause; `ccc88ef2`, `dea161ea`, `c72268e7` the
  ledgers and the evidence; then, for the checked suite over cb16: `755b2388` an area's foe count without placing
  the six, the NPC anchors read only where the six stand; `c181afee` a decode holds its slain masks to the count;
  `48a2b510` the spawn census holds the count to the placements; `15801703` its test; `82e92afe` cb18's save rows
  on CUB 8; `16dbaec6` the docs; `b25010a2` the evidence; `142def2f` the docs' count of the inherited Hush foes; this
  note.

**Rulings.**

- R-cb18-1 A (the moths dim the palette on both tiers, never blank a glyph): implemented.
- **R-cb18-2 B, the orchestrator's (2026-10-29): the lynx's bite bleeds, as contract item 2 says.** A landed
  swipe (the lynx's attack 0, the Sol lane's choice) starts sixty ticks of bleeding; a parried or dodged one
  none; yarrow stops it (`test_cb18_landed_lynx_swipe_bleeds_and_yarrow_cures_it`).
- **R-cb18-4, recommended B and implemented: the boss census's hit columns.** cb04 defined `hits0..2` and
  `unparryable_hits` as the strikes taken by attack (cb04's note, item 3; `docs/DESIGN.md`'s table, "hits taken
  by attack 0 / 1 / 2"), and the census counted every step the cub's health fell, the same thing until a bite
  could bleed. With bleeding each bleed tick counted as a hit of whatever attack the lynx was in, unparryable
  when that attack was: the Sol lane's ledger rows said so ("hit counters measure health-loss events including
  DOT, not individual landed strikes"), which is not what the columns mean. B: the hit columns keep cb04's
  meaning (a fall past what the bleed left could take: a bleed tick is one health, a strike ten at least), and an
  appended `damage_events` column (each world's row, and before `arena_breaches` on each `fairness` line) counts
  every fall, the old rule. A control build with the lynx's line off reproduces trunk's census on all 400 rows'
  thirteen columns, and its `damage_events` equals trunk's `hits0+hits1+hits2` on all 400
  (`pickup/census-split-control.log`).
- **R-cb18-5, recommended A and implemented: the lynx's bleeding and its answer.** Once a killing bleed tick was
  one fall (`113bb973`), the lynx left one world unwon within five lives (seed 1 at 80 columns, the beaten
  witness's own world: `proof: the fighter did not beat the lynx`) and 34 of 100 needing more than one. The
  bible names the answer (§9: "the parry …, yarrow, sneaking"): A, the lynx's fixture brings a full stack of
  yarrow, which grows in the meadow on the way (cb15), and the fighter eats one on a bleed through the paused
  pouch; B, shorten or narrow the bleed (the maintainer's balance); C, let the witness and the gate admit the
  falls. A fighter that licks instead was tried twice and failed: never safe within the lynx's 18-tick
  recoveries, and backing out past its ledge range first left four worlds unwon (`pickup/lick-trials.txt`).
  Only the boss fight's journey carries the yarrow (`bd5a6370`); the dens' fixtures keep `journey_at`'s pouch.
- R-cb18-3 A (the Sol lane's, renumbered from its R-cb18-2: an unreturned theft is lost on reset; B would need a
  CUB 9 over cb16's CUB 8): implemented; the orchestrator puts it to the maintainer.

**§6 against item 2.** The ash adder's bite is the burn variant, wired as item 2 says: forty ticks of one health
(`test_cb18_burn_has_forty_ticks_and_does_not_lick_out`), water first (`test_cb18_water_cures_burn_before_the_next_damage_tick`)
or yarrow (`test_cb18_adder_burn_is_not_bleed_and_yarrow_cures_both`), only a landed strike
(`test_cb18_adder_parry_kills_and_only_a_landed_strike_burns`). The marten's was not: the Sol lane's bite also
started bleeding, which neither §6 (the marten steals) nor the bible (§5: bleeding is the lynx's and the shades')
gives it. `f8f0496e` takes it out; the bite steals one pouch item and bleeds nothing
(`test_cb18_marten_takes_one_item_without_bleeding_and_returns_at_the_trunk`). It moved only the marten's two
final arena frames (the health bar: 75, not 60, at the same tick); the six's arena census is byte-identical with
and without it, every generated case and every other golden unchanged (`pickup/marten-without-bleeding.txt`).

**cb16's NPCs and the six** (the orchestrator's rule after cb16's merge: no foe spawns on an NPC's cell or within
its four-cell talk radius; the six move, the NPCs never). `sim.folk` reads every place an NPC can stand in an area
(cb16's `npc.place`: Quill's Larkmeadow perch and every den he perches at, Ember's three, the rest at their
anchors) and `sim.folk_gap` the clear cells between a foe's body and theirs at any facing of either; the slot
search rejects a cell within `npc.FACE_GAP` (four) as it rejects a blocked one (`9b5cc29e`). Before the rule the
Stand's last marten (row 192, the spine's east side) spawned two to four cells from the Hermit's ruin in 94 of
the spawn census's 100 worlds, and nothing else of the six came within the radius; after it, `new-foe-npc-gap:
green, 3400 spawns over 50 seeds at both fields, the nearest 5 clear cells from an NPC (talk radius 4)`, the
500 distribution rows and cb16's `--npc-audit` (2200 places, green) byte-identical before and after
(`pickup/npc-talk-radius.txt`, with the test red without the rule and green with it). The spawn census ends on
that verdict and the gameplay gate requires it (`0724eb94`, its own red rows in `tests/new_foes_test.py`).
The Hermit's anchors and the rest stand where cb16 put them; the Charcoal-burner's kiln, the Ferryman's post,
Dunmoss's sett (the Teeth: none of the six) and the lost (the Hush: none of the six) were never within reach.
Not the six's to move, so reported: the inherited Hush foes stand by the lost, a fox pair within four cells of
Fenn (rows 40–44) and one of Loam (rows 136–140) in every world, sharing cells with them in many (gaps −4 to 3),
and weasels at rows 74–76 within four cells of Bracken in 58 of the 100 (`pickup/inherited-near-npcs.txt`, 560
rows; cb16's note leaves such a spawn to the orchestrator).

**Every old case and golden that moved, against `763616eb`** (row by row in
`notes/cb18-evidence/golden-key-changes.tsv`, 536 rows: 329 added, 171 modified, 36 removed;
`generated-case-receipts.tsv` for the cases: 81 kept with trunk's bytes, 15 imported, 1 added):

- *The lynx's bleeding (R-cb18-2 B and R-cb18-5 A):* `tests/cases/boss-lynx-{windup,phase2,beaten}.pk` and the
  goldens `boss-lynx-beaten-{rich,plain}` and `boss-lynx-phase2-{rich,plain}` (47 ledger rows): the fighter's
  keys and the fight's milestones regenerated.
- *cb18's placements (contract item 1, the spawn tables per area):* the Stand's three martens move the world
  walk's keys past the ridge, and so `world-meadow`, `hawk-shadow`, `hawk-stoop`, `world-hawk`,
  `world-recovered`, `world-return`, `coast-cache-0..3` and the Stand's landmark witnesses `landmark-7-0` and
  `landmark-7-1` (cases and goldens); the area scenes `stand`, `burn`, `mere`, `howe`, `underteeth`, the
  landmarks `landmark-8-0`, `landmark-9-0`, `landmark-10-0`, `landmark-11-0..5` and the rests
  `rest-{stand,burn,mere,underteeth}-{80x24,120x40}` (their final states list the appended foes; frames where a
  foe is in view). The Underteeth's also carry the glow-worms' light (`sim.glow_dark_area`: a cave without its
  worms is dark three cells off, contract item 1).
- *cb16's merge:* cb16's NPCs drawn in frames cb18's placements had re-keyed (64 rows: Quill at his Larkmeadow
  perch in `hawk-shadow`, `hawk-stoop`, `world-hawk`, `world-recovered` and the walk, his line no longer printed
  to a cub passing by; the Hermit in the ruin of `landmark-7-0` and `landmark-7-1`); cb16's toll case
  `npc-toll-{rich,plain}`, whose final state now lists cb18's heron (2 rows, no frame shows it); cb18's six
  imported cases with the generator's `journey 7` header (6 rows, the same keys).
- *The NPC rule:* the rests' final states `rest-stand-{80x24,120x40}-{rich,plain}` (4 rows): the marten at
  x 11, row 188, not x 13, row 192. A control with the rule off reproduces every other file above
  (`pickup/npc-talk-radius.txt`): cb16's merge moved those, not the rule.
- *The proof of the placements' cause* (`pickup/control-no-placement.log`, before the rebases): a control build
  with the one placement call (`append_new_area_foes`) removed regenerates every generated case byte-equal to
  trunk's generator, and on trunk's keys reproduces trunk's goldens on every placement case above but
  `underteeth` and `landmark-10-0`, whose `.sty` differs by the dark-cave rule alone. The foe census moves only
  the new areas' rows (7–11), every old area's bytes unchanged, and appends the distribution and its verdict
  (`pickup/foe-census-trunk-vs-final.diff.gz`).

**The boss census and the fairness census, re-run and compared** (trunk's against the head's; cb16's censuses
are `ed180ef5`'s by cb16's own check, and the head's equals the pre-cb16 final on all 405 lines; the per-world
rows in `notes/cb18-evidence/bleed-boss-changes.tsv`, every moved row with its reason): 68 of the 400 world rows
moved, every one the lynx's; the boar's, the elk's and the alpha's are byte-equal on trunk's columns. The
fairness lines (trunk, then the head):

- `fairness lynx attempts 1:100 2:0 3:0 4:0 5:0 unwon:0 hits 104 18 21 unparryable_hits 21 tells 10 12 15 parry_window 9 arena_breaches 0`
- `fairness lynx attempts 1:100 2:0 3:0 4:0 5:0 unwon:0 hits 107 20 32 unparryable_hits 32 tells 10 12 15 parry_window 9 damage_events 208 arena_breaches 0`

Every world is won in one life again, every parryable tell at least nine, no breach; the strikes the lynx lands
rise from 143 to 159 and its damage events (strikes and the bleed ticks before a yarrow) are 208. The moved rows'
fights run longer or shorter by the pouch's pause and the different fight. The other three bosses' lines are
trunk's with `damage_events` 136, 21 and 89 (their hit sums). The six's own fairness census (`--new-foe-census`,
600 arena encounters) is unchanged by any of the bleeding changes. (Before the two fixes the Sol lane's numbers,
`attempts 1:71 2:16 3:11 4:2`, were a cub fighting on at no health between the deaths of one fall.)

**What the pickup changed in the code to pass the checked suite:**

- *The placement search* (`3e1670fc`) finds the same first slot for less: the den refuge is read once a search,
  not once a candidate, and the ring walk jumps over the rows it skipped anyway. The four checked rows that
  decode a save (thirteen `area_foes` calls each) had run out of the step budget:
  `journey_test::test_cb02_all_dens_restore_with_growth_and_water`,
  `cb14_migration_test::test_cb14_the_older_fixtures_still_read`,
  `denmemory_test::test_cb04f_rest_and_death_reset_every_area_but_not_bosses`,
  `map_test::test_cb14_the_burnt_oak_and_the_stone_mouth_open_to_a_lunge_and_save`. They pass, and every
  placement is the one before (the generators and goldens byte-equal).
- *`bosses_test::test_cb04_a_boss_never_leaves_its_arena`*: one test a boss, the same assertions and the same
  200 ticks each. On trunk `ed180ef5` the four in one test sat at exactly the budget: `wolf conform-run
  --checked` on the test's own body fits 200 ticks and not 201, on both hosts (`pickup/boss-budget-probe.txt`;
  the lane's code fits 198), so any tick the six new kinds add ran it out (the Sol lane's first foe commit
  `1c86bebc` already did). cb16 made the same split for its own reason (`6eafa61f`); the head runs cb16's.
- *The body census* (`e93e9767`, found red by the Linux gate at the pre-cb16 head `435202e0`: `gameplay.bodies`,
  overlap 714 and contact_unreachable 59, every one in a script past the Stand's martens): `census.foe_box` drew
  the six with `silhouette.foe`, which falls through to a boss's drawing for any kind past the Ashen; it reads
  art's own drawings of the six now, and over every case the census is overlap 0, contact_unreachable 0
  (`pickup/body-census-red-green.log`, the witness red on the old census and green on the fix).
- *A killing bleed tick* (`113bb973`, found by the lynx's beaten witness: 27 deaths in one fall): the action step
  ran after the bleed's death and stood the cub up, and each later bleed tick killed it again; the fall now ends
  the tick, as after a foe's blow (`pickup/bleed-death-red-green.log`).
- *`map_test::test_cb14_every_alcove_has_its_own_bit_and_a_named_slot`* (`413b330a`) counted every non-boss foe
  of the new areas as a guard ("the new areas' foe tables are cb18's and empty"); it counts the guards and
  asserts they keep their saved ordinals ahead of cb18's appended six.
- *Over cb16* (both gates at `caf8acd3` red at the checked suite, `wolf test: 671 passed; 1 failed; 0 rejected;
  2 unsupported`, `pickup/checked-suite-over-cb16.txt`): `cb16_migration_test::test_cb16_a_rechecksummed_cub8_with_a_bad_npcs_line_is_refused`
  out of the budget with or without the NPC rule (a decode placed every area's foes, the six among them, only to
  count them for the slain masks), `grove_test::test_cb02b_forest_texture_everywhere` out of it with the rule
  (its anchors were read for every area, the Shingle of every `sim.new` among them), and cb18's own
  `test_cb18_save_reload_discards_only_transient_status_and_held_theft` asserting CUB 7. `sim.area_foe_count` is
  the inherited foes' length plus the six's constant per area (`sim.new_foe_count`: 3, 4, 1, 24, 2), the decode
  holds the masks to it, and the spawn census holds it to `area_foes` in every world (`755b2388`, `c181afee`,
  `48a2b510`, the checked test `15801703`); the anchors are read only in the six's five areas; the save row reads
  CUB 8 (`82e92afe`). Then `wolf test: 675 passed; 0 failed; 0 rejected; 0 unsupported`, 0 SKIP, the goldens
  515 `ok`, every generator equal to the tree past the legacy headers, the boss and foe censuses unchanged.

**The rebase onto cb17's merge** (`40c6410b`, 2026-10-29, once, onto trunk, never onto the branch). Three files
both changed: `docs/DESIGN.md` conflicted where both appended a section (both kept, cb17's first); `README.md`
and `src/cub.lu` (cb17's `--sound-census` and `--score-scene` beside cb18's `--new-foe-spawn-census`) merged
cleanly. Re-run over the rebased tree on kasumi's container (`pickup/after-rebase.log`): both builds 0, the
goldens 509 `ok` and 0 `DIFFERS`, `score-check: green` (its sound census walks cb14's walk to Gravehollow through
the placed six: `sound-census entries 12 ok, cues 30, reveal 1 crossing 2 walk 1, ticks 9952, ends in area 12`),
every generator equal to the tree past the legacy headers. The gates at `435202e0` ran at that rebased head; the
fixes they found followed.

**The rebase onto cb16's merge** (`763616eb`, 2026-10-29, once, onto trunk; 71 commits). Both lanes' intent
kept, file by file:

- `src/sim/sim.lu`: both appended at the file's end (cb16's NPCs in the simulation, cb18's six); both kept,
  cb16's first. The join dropped the closing braces of cb16's `strike_lost` in the first commit that carries it;
  a pass over every commit (`git rebase --exec`) put them back wherever the join appeared.
- `src/cub.lu`: cb16's `--npc-audit` and its witnesses beside cb18's flags and censuses; both kept.
- `docs/DESIGN.md`, `README.md`: both appended; both kept, cb16's first. cb18's save sentences were then brought
  to cb16's CUB 8, `journey 7` and 48 lore slots, and R-cb18-3's B to a CUB 9 (`ac6e7097`).
- `src/bosses_test.lu`: both split cb04's arena row one boss a test for the budget; cb16's taken, cb18's commit
  then empty and dropped.
- `src/map_test.lu`: merged as both wrote it, cb16's CUB 8 and dig rows beside cb18's alcove count.
- `src/proof/proof.lu`, `src/cb14_items_test.lu`, `tools/world_checks.py`, `tests/pty_rows.py`: cb16's alone;
  cb18 changes only `proof.lu`'s boss-proof journey afterwards (`bd5a6370`).
- `tests/cases/`, `tests/goldens/`: the lane commit's bytes taken through the rebase (some frame files merged line
  by line, cb16's NPC hunk beside cb18's foe hunk), then everything regenerated over the combined code and
  checked: 18 golden directories moved and 515 `ok` (`pickup/after-cb16-rebase.log`, with each moved file
  traced to cb16's bytes, cb18's pre-rebase bytes and the tree's).

From cb17 (relayed 2026-10-29): the Howe's wisps lead to sentries that are fought inside the Howe's walk rows
(row 150 to the stone mouth), where cb17's `walk` part plays; nothing in either lane changes for it.

## Evidence index

`notes/cb18-evidence/` holds the Sol lane's records (the reds first: `marten-travel-red.log`,
`marten-trunk-red.log`, `moth-orbit-red.log`, `moth-rally-red.log`, `needle-visibility-red.log`,
`phase-alias-red.log`, `wisp-lock-red-2.log`; the arena stage, the hit rings, the equivalences), the boss-census
ledger `bleed-boss-changes.tsv`, and the pickup's records under `pickup/`.

- **The plant:** cub#76 (`cb18-plant-no-recovery`, `a1e88cfe`, off the line): the marten without recovery,
  `fairness_recovery_9 RED: no human-scale recovery`, `CB18_PLANT_EXIT 1` (`plant-red.log`, nomad). It stands.
- **The old-kind equivalence:** `old-kind-generated-equivalence.tsv` and `old-kind-walk-equivalence.tsv`: the
  walker hook leaves every old-kind generated case and walk byte-identical (trunk, before, after; the lynx's
  differ from trunk by the lynx's bleeding alone).
- **The checked suite:** first whole run over the Sol lane's tree, red: 634 passed, 1 failed, 5 unsupported
  (`pickup/checked-suite-first-red.txt`, nomad); after the fixes, 643 passed, 0 unsupported, 0 SKIP on both
  hosts at the pre-rebase `6c675e25` (`pickup/checked-suite-kasumi-synced-tree.log.gz`,
  `pickup/mac-gate-6c675e25.log`); over cb16, red at `caf8acd3` and green after the fixes
  (`pickup/checked-suite-over-cb16.txt`).
- **The censuses:** `pickup/boss-census-final.txt.gz` (the head's, unchanged over cb16),
  `pickup/boss-census-6c675e25-no-lynx-bleed.txt.gz` (the pre-rebase `6c675e25`, trunk's bytes),
  `pickup/boss-census-lynx-bleed-before-split.txt.gz` (the restored line, the old columns, equal to the Sol
  lane's), `pickup/boss-census-split-control.txt.gz` and `pickup/census-split-control.log`; the NPC rule's
  `pickup/npc-talk-radius.txt` and `pickup/inherited-near-npcs.txt`.
- **The goldens at the head:** regenerated over cb16 from the head's code on nomad (515 `ok`, 0 `DIFFERS`;
  `pickup/after-cb16-rebase.log`); the six's arena records equal to `--new-foe-proof`'s.
- **The gates at the pre-cb16 head `435202e0`** (before the fixes above): the Mac leg green
  (`pickup/mac-gate-435202e0.log`); the Linux gate red at `native-gameplay` (`gameplay.bodies`), log
  `/mnt/steamlib/lanes/cb18/gate-435202e0.log`, marker `gate-435202e0.exit` = 1.
- **The gates at `caf8acd3`** (over cb16, before the budget fixes): both red at the checked suite (above); the
  Mac gauntlet's log `/Users/mfwolffe/lanes/cb18/gate/mac-gauntlet-caf8acd3.log`, marker `.exit` = 1; kasumi's
  `/mnt/steamlib/lanes/cb18/gate-caf8acd3.log`, marker `gate-caf8acd3.exit` = 1.
- **The gates at `b25010a2`** (the code head; the commits after it are docs and this note), both running at
  the hand-back, each stopping at its first red step and printing every step's `END <step> exit=N`:
  - the Mac gauntlet (cub's `tools/check` in its own order behind the lock, the pty rows without `sound-live`
    and `mute-key`, skipped by name in its log; the golden check at most three attempts on the floor): green
    through the head check, the python tests, fmt, `wolf test: 675 passed; 0 failed; 0 rejected; 0
    unsupported` with 0 SKIP, both builds, both selftests and the release goldens (515 `ok`) when this note was
    written; pid 9535 (the `nohup` wrapper), log `/Users/mfwolffe/lanes/cb18/gate/mac-gauntlet-b25010a2.log`
    (its last line `CB18_MAC_GAUNTLET_EXIT N`), marker `/Users/mfwolffe/lanes/cb18/gate/mac-gauntlet-b25010a2.exit`;
  - kasumi's (cores 0–3 under their flock, the engine's container: `tools/check-linux`, then `env
    LAIR_PERF_SLACK=1 tools/check-perf`): pid 2092329, log `/mnt/steamlib/lanes/cb18/gate-b25010a2.log` (its
    last line `CB18_KASUMI_GATE_EXIT N`), marker `/mnt/steamlib/lanes/cb18/gate.exit`.
- The superseded gates, each stopped inside `check-linux`'s engine check after `check-fmt: canonical` and
  `wolf test: 643 passed`: the pre-rebase `6c675e25` at 2026-10-29T21:26:41Z (the ruling) and the pre-rebase
  `18cc09a0` at 22:07Z (cb17's merge); their logs are `/mnt/steamlib/lanes/cb18/gate-6c675e25-stopped.log` and
  `gate-18cc09a0-stopped.log`.

## Done-when

- [x] The six with their four-way sprites, tells, windows, weaknesses and scent; placed in their areas (the
  Teeth and the Hush get none); the 500-row distribution gated on both binaries.
- [x] Bleeding wired as item 2 says: the lynx's landed swipe bleeds (R-cb18-2 B), the marten's bite steals, the
  adder's is the burn variant; yarrow cures bleeding and burn, water burn.
- [x] The boss census and the fairness census re-run and compared, every moved row named with its reason; the
  hit columns keep cb04's meaning (R-cb18-4 B).
- [x] 600 arena encounters by the ordinary-key fighter; the hit rings; six replayed encounters on both tiers.
- [x] Every old case and golden that moved named with its cause (above).
- [x] The plant red by name, off the line (cub#76).
- [x] Over cb16: no spawn of the six within an NPC's talk radius, gated; `--npc-audit` green with the six in.
- [x] Test targets: the checked suite; the goldens; the generators against the tree and trunk; the foe, boss,
  spawn, npc and arena censuses; the no-placement, census-split and NPC-rule controls; the step-budget probes.
- [ ] The full gates at the code head, the Mac gauntlet and kasumi's: running at the hand-back (the evidence index).

Ledger: cb18 | the new enemies | module | PR #86 | plant #76 | final head: this PR's head.
