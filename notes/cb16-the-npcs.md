Footprint: module

# cb16 — the NPCs: six who speak, the lost, and the trade

Thornmere has people in it now, and animals that talk (the-proposals.md section 5; item 14 of the second playtest:
"There are no NPCs like were originally planned"). Quill the raven trades from his perch in Larkmeadow and then from
the cub's last den; Dunmoss the badger keeps his sett at the Teeth's foot and, once Whisper is dead, digs the way
under for a winter's bones; Ember the fox warns in Bramblehold, takes her mouthful in Larkmeadow and gives the
mother's first tuft at her den; three ashen (the Charcoal-burner at the Burn's kiln, the Ferryman on the Mere's
causeway, the Hermit in the Stand's ruin) say what the fire was; Fenn, Bracken and Loam, the lost, stand in the Hush
and never attack. Section 5's lines word for word, one a visit, in a frame over the paused forest; the inventory's
list for the wares; CUB 8 for what each has said. Game code, game-owned tests, witnesses, censuses, docs and goldens
only: no engine, pin, workflow or `tools/check*` change.

Ledger: cb16 — the nine (Quill, Dunmoss, Ember, the Charcoal-burner, the Ferryman, the Hermit, Fenn, Bracken,
Loam) at cb14's anchors, the speech frame and the trade list on both tiers, the dig, the toll and the crossing, the
story, Ember's mouthful and tuft, the lost and *Alone*, CUB 8 and `journey 7`, the found-lore list 48; R-cb16-1 .. R-cb16-9 recommended A and implemented; module; plant #87; the final source `4adf03e1` on cub trunk
`40c6410b` (cb17's merge, the branch rebased once onto it); the Mac gauntlet green there; the Linux gauntlet at
`4adf03e1` on kasumi (this note's commit touches `notes/` only).

## Prediction

`6866139b` (`099ac195` after the rebase onto cb17's merge) committed `notes/cb16-prediction.txt` before the first
change, at trunk `ed180ef5`. What it said and what held:

1. **What the base had** held exactly: no NPC; cb02's Ember a prop and a story bit; Quill a landmark line; the lost
   nowhere in the code (so R-cb16-1 is A by default); no ending flags (the card always "Home"); the foxes' feint
   stealing scent (R-cb10-3 A); cb14's anchors; the found-lore list exactly full.
2. **The plan** held: `npc` (data and rules), `folk` (the sprites), `talk` (the frames), `sim.lu`'s appended cb16
   block with four hooks (the step, the keys, the pause, Quill's perch at a rest; and the lost under `strike_foes`),
   plus `npcaudit` and `npcproof` (the census and the witnesses), which the prediction did not name.
3. **Numbers.** Checked tests 562 at the base, 584 at `2ca958a3` (predicted about 580), 593 over cb17's merge.
   Goldens: 508 directories at the base; 6 new (`npc-talk`, `npc-trade`, `npc-toll` on both tiers) and the art
   study's NPC sheet; **29 case directories changed**, frames only (predicted 40-70), and **no `final.state`
   moved** (predicted at most 10): the stillness rule (no arrow held) keeps a recorded cub pushing against a body
   from ever opening a frame. The hit census byte-identical (`53234a37…` at the base and the branch; the
   prediction quoted cb15's older digest). The boss census unchanged in kind: every boss won at the first attempt
   in all 100 worlds, `arena_breaches 0` (the Linux gameplay at `2ca958a3`). The world audit, the foe census, the
   den spacing, the bends and the spurs, base against branch: `census-compare.sh`, queued behind the Mac build lock
   at this note's commit (below). The memory gate: the Linux
   gauntlet's `memory-gate` stage.
4. **What did not hold at first.** (a) The checked machine's step budget: cb04's `a boss never leaves its arena`
   (four bosses, 800 steps in one test) went `unsupported (step budget exhausted)` with the NPC step on, even after
   the step cached the places per area and stopped at a box round them; the row is now four rows, one a boss, the
   assertions and ticks cb04's (`68173d79`). (b) The first walk of the hush first-screen case stopped beside Fenn
   against a fox's body (the cub "still" while the arrow was held): stillness wants no arrow held. (c) cb14's
   lookout row stood the cub still by the Hermit for the whole reveal: no NPC speaks while the reveal runs.

## Forbidden

Original code, art and text only: section 5's lines are the orchestrator's drafts in the bible's register (kept
word for word, `npc.line`); the Hermit's story (lore 32), the frames' words, the sprites and the end card's Alone
line are this lane's; no other game's code, art, text or music. No engine (`lair`) change, no pin, workflow, CI or
`tools/check*` change. No other lane's file touched beyond the adaptations named below; cb17's score files and
cb18's foe data never edited. Never labelled a PR, merged, tagged, created or closed an issue, edited `~/.claude` or
the planning repo, installed a package. No attribution or co-author trailers.

The Mac (`~/lanes/cb16/cub`, branch `cb16`) built and tested behind the shared `mkdir` lock
(`/Users/mfwolffe/lanes/mac-build.lock`, the holder's pid checked, the 8 GiB `vm_stat` floor inside it:
`/Users/mfwolffe/lanes/cb16/heavy.sh`); the maintainer's MLX server never touched. kasumi ran the checked suites, the
plant and the Linux gauntlet on cores 8-11 under `/home/mfwolffe/lanes/kasumi-cores-8-11.lock` (a printing wait,
never a kill), in the engine's container, everything under `/mnt/steamlib/lanes/cb16/` (never `SteamLibrary` or
`wollf`); no process group signalled. The Mac gauntlet skipped the pty rows `sound-live` and `mute-key` by name
(the-rules.md since planning `46518b2`; CI's macOS job runs them).

## Inputs verified

Base cub trunk `ed180ef5` (cb14 + its note), the worktree `~/lanes/cb16/cub` on branch `cb16`; engine `74b89744` as
`lair.pin` names it (staged from the org's lair clone on the Mac, from GitHub on kasumi; `LAIR-REV` read); wolf 0.2.35
and lupin 0.1.56 with std `2386522e` staged by `.lair/tools/fetch-toolchain` (the digests verified by the fetcher:
`aarch64-apple-darwin wolf=240b84d0… lupin=9133bfdb…`; kasumi's stage copied from cb17's clone, `STAMP` read:
`x86_64-unknown-linux-gnu wolf=4cc4045b… lupin=ad703550…`). The contract with its 2026-10-29 addendum, `the-rules.md`,
the maintainer's notes (item 14), `the-proposals.md` section 5 (and 3, 4, 6), the bible sections 1, 2, 6, 7, 14, 15,
16, `DESIGN.md`, `ART.md`, `GLYPHS.md`, `KEYS.md`, `REPLAY.md`, `PALETTE.md`, the notes cb02, cb04, cb10, cb14, cb15 and
`sprints/RULES.md` sections 1-10 read before the first change; the README read and refreshed in its own commit.

Corrections for the planning repo and the hand-over: (1) the contract's "killing one sets *Alone* (read cb04's ending
flags)": cb04 built no ending flags; the end card always said "Home" and `scene.ending.alone` is a name only. The
card names *Alone* now when one of the lost was killed (R-cb16-9); the elk's half of the bible's rule waits for the
elk's choice. (2) "Ember's feint steals a mouthful (it exists? read cb04)": the feint exists, and since cb10's R-cb10-3
A it steals scent, never water; Ember's one mouthful is R-cb16-2. (3) cb15's provisional tuft (four cells east of
Bramblehold's first den) was the first tuft section 4 gives to Ember's den: R-cb16-3 moves it. (4) "Dunmoss opens the
Underteeth for 150 scent after Whisper" met cb14's paw squeeze (R-cb14-2 A): R-cb16-4 keeps both. (5) cb14's
correction 9 (a further lore line needs a wider save): done, 48 slots (R-cb16-8). (6) "a boss led to one kills it":
the rule is built and tested, but every NPC stands 27 or more cells outside every arena (`--npc-audit`) and a boss
never leaves its arena (the boss census), so it cannot fire in this world. (7) cb17's `crossing` part: the
Ferryman's raft carries the cub along the Mere's route from row 12 to row 168 in ninety ticks (`sim.ferry_step`
moves `s.x`/`s.y` a tick), so `score.moment_of` sees the cub on the rows between the causeways and plays it; no
sim flag was added.

Adaptations of other lanes' rows (each named; the behaviour, not the budget, moved them unless said): the "CUB 7"
and `journey 6` / `SNAPSHOT 211` assertions of `areas_test`, `cb13_migration_test`, `cb14_migration_test`,
`denmemory_test`, `grove_test`, `map_test`, `progression_test`, `refuge_test`, `tools/world_checks.py` and
`tests/pty_rows.py` read CUB 8, `journey 7` and 239 (cb14 did the same to cb13's); `cb14_migration_test` and
`map_test`'s journey 5 rows read the widened lore slots; cb15's `test_cb15_provisional_tuft_is_at_the_first_den_not
_the_checkpoint_den` became `test_cb16_bramblehold_seeds_six_marrow_and_the_first_tuft_is_embers` (R-cb16-3);
`cb14_items_test` wants six pickups in Bramblehold and `lore.COUNT` 33 within 48 slots, `pouch_test` 33; cb14's sett
row sets Dunmoss's dig before the paw (R-cb16-4); cb04's arena row is four rows (the step budget, above);
`proof.den_journey` sets the dig with the sett's bit (its fixtures must stay valid saves).

Rulings recommended and implemented, none decided (`docs/DESIGN.md`, "The NPCs"):

- **R-cb16-1 A**: the lost speak section 5's three lines (cb04 built none; B had nothing to keep).
- **R-cb16-2 A**: Ember's feint takes one mouthful of water, once, before the line that names it; B: up to five scent,
  as the foxes' feints.
- **R-cb16-3 A**: the first tuft is Ember's gift at her den (cb15's ground tuft removed; a seeded Bramblehold
  migrates as given); B: keep cb15's ground tuft.
- **R-cb16-4 A**: the dig (150, after Whisper) and the paw squeeze are both the sett's gates; B: the dig replaces
  the paw.
- **R-cb16-5 A**: Dunmoss's marrow 35 (the bible's section 15 price).
- **R-cb16-6 A**: NPCs are not solid.
- **R-cb16-7 A**: Quill never perches in the Hush or the Underteeth; B: the bible's "last perch is the wood's den".
- **R-cb16-8 A**: the found-lore list 48 (a CUB 7 or older at most 32).
- **R-cb16-9 A**: the end card's *Alone* when one of the lost is killed.

## Evidence index

`notes/cb16-evidence/`:

- **The Mac gauntlet at the final source `4adf03e1`** (`mac-gauntlet-4adf03e1.log`, `mac-gauntlet.sh`: the lock
  held through the whole run, every step's `END <step> exit=N`, the first nonzero stops it): `head 0` (the clean
  tree at `4adf03e1`), `fmt 0`, `python-tests 0`, `test 0` with `wolf test: 593 passed; 0 failed; 0 rejected; 0
  unsupported; 0 filtered out` and `skips 0` (no SKIP line), `build 0` (native and release), both selftests 0,
  `goldens-release 0` and `goldens-native 0` (each 513 `ok`, 0 `DIFFERS`, at the first attempt), `prepare-pty 0`,
  `pty 0` (85 rows `ok`: every row but `sound-live` and `mute-key`, the-rules.md since planning `46518b2`),
  `npc-rows-native 0` and `npc-rows-release 0` (`tools/npc_checks.py`: the npc census green over 2200 places, the
  three witnesses on both tiers, the trunk writer's CUB 7 to CUB 8 and its byte-exact resume), `hit-census 0` (the
  release build's census at `53234a37…`), `CB16_MAC_GAUNTLET_EXIT 0`.
- **The Linux gauntlet at `4adf03e1`** (kasumi cores 8-11, the engine's container, `linux-gauntlet.sh`: the
  game's `tools/check-linux` (the python tests, `prepare-pty`, the engine's check-linux: fmt, the checked tests,
  both builds, the selftest, the goldens, the 87 pty rows; the native goldens, the score check, gameplay on both
  backends with the npc rows, the memory gate), `perf` at slack 1 (`LAIR_PERF_SLACK=1` inside the container), the
  hit census): launched at 2026-10-29T22:30:30Z (the flock taken then; `END head exit=0` at `4adf03e1`), still
  running at this note's commit: pid 1970575 (`/mnt/steamlib/lanes/cb16/linux-gauntlet-final.pid`), log
  `/mnt/steamlib/lanes/cb16/logs/linux-gauntlet-final.log`, marker `CB16_KASUMI_EXIT` (and
  `CB16_LINUX_GAUNTLET_EXIT N at <step>`); its verdict is the orchestrator's to read (the brief's rule for a
  detached job over twenty minutes). The same rig's run at `2ca958a3` (below) is the evidence of what it covers.
- **Before the rebase**, at `2ca958a3` on the same kasumi rig (`linux-gauntlet-2ca958a3.log`): `check-linux`'s
  `engine-check` green (`wolf test: 584 passed; 0 failed`, 0 SKIP, every golden `ok`, 87 pty rows `ok`), the native
  goldens and the score check green, `native-gameplay` green (`gameplay: green (0 skips)`, the boss fairness 100 of
  100 first-attempt wins for all four with `arena_breaches 0`, the npc rows); stopped by its pid and its container
  by id at cb17's merge to run the final head (`CB16_LINUX_GAUNTLET_EXIT 137`). The Mac's checked tests at
  `2ca958a3`: 584 passed.
- **The goldens** (`golden-classes.txt`, `golden-diff.py`): written by `.lair/tools/goldens --update` on the Mac's
  native build; 29 case directories changed, every one in its frames alone, no `final.state` (the integer
  snapshot) moved: `burn` (the Charcoal-burner in the first screen), `hush` (Fenn), `hawk-shadow`, `hawk-stoop`,
  `world-hawk`, `world-recovered` (Quill on his Larkmeadow perch), the landmarks `1-1` (plain only: cb15's tuft no
  longer by the split roots), `1-2` (Ember at Bramblehold's entry), `2-0` (Quill on the perch; the perch's own
  line gone), `3-1` (Dunmoss), `5-0` (the lost), `7-0`, `7-1` (the Hermit in the ruin), `8-0` (the Charcoal-burner),
  `9-0` (the Ferryman), each on both tiers but `1-1`; 6 new (`npc-talk`, `npc-trade`, `npc-toll`, both tiers); the
  art study's `npcs-rich` and `npcs-plain`. Both backends and both hosts reproduce them (the Mac gauntlet; the
  Linux gauntlet's goldens stages).
- **The censuses**: the npc census (`npc-audit.txt`, `cub --npc-audit`): 2200 places over seeds 0..49 at both
  fields, every one open ground the area's flood reaches, the nearest 27 cells past an arena's edge. The hit census
  (`hit-census.txt`): byte-identical at the base and the branch. The others base against branch:
  `census-compare.sh`, both native builds byte for byte; queued behind the Mac build lock when this note was
  committed: pid 62161 on nomad, log `/Users/mfwolffe/lanes/cb16/gate/census-compare.log`, marker
  `CB16_CENSUS_DONE` after one `census <name> base_exit= head_exit= equal|DIFFERS` line per census.
- **The migration fixtures** (`make-cb14-fixtures.py`; `tests/saves/cb14-v7.save` and `cb14-journey6.pk`, their
  provenance in `tests/saves/provenance.json`): three real runs of the base binary (`cub-ed180ef5`, the native
  build, sha256 `24a8dfc7…`): a CUB 7 with the sett's shortcut open at the bone cache's den and its journey 6
  recording. `src/cb16_migration_test.lu` holds them to their exact CUB 8 bytes and journey 7 slots;
  `tools/npc_checks.py` does it at file level with the shipping binary.
- **The plant**: PR #87 (`cb16-plant-lines`, `683d38dc` on `2ca958a3`, not an ancestor of the branch): `npc.next_line`
  cycles back to the first line; `test_cb16_every_npc_s_lines_go_in_order_and_the_last_repeats ... FAILED
  (trap(assert))` and Ember's row with it, `wolf test: 12 passed; 2 failed` (`plant-run.txt`, kasumi, the engine's
  container, at `683d38dc`). Never merged.
- **The witnesses** (`cub --make-npc-proof DIR`, `src/npcproof`): `npc-talk` (the frame at tick 110, Quill's first
  line, Space to the wares, Esc), `npc-trade` (100 scent: pine and yarrow bought, 30 left), `npc-toll` (the post at
  tick 417, sixty paid, the far causeway at row 168); the walker's keys and the named presses only, the scent the
  only fixture.

## Done-when

- [x] The six and the three lost at their anchors per seed, drawn on both tiers (the animals in their colours, the
      ashen grey and slow, the lost as shades), facing the cub within four cells, speaking when it stands still
      beside them twenty ticks: one line a visit in order, the last repeating, Space advances, Esc leaves; what each
      has said in the save. Not foes, not solid; a boss led to one kills it (the save's dead mask).
- [x] Quill's perch follows the rests; the trade at section 4's prices; Dunmoss's dig for 150 after Whisper; Ember's
      mouthful and her den's tuft; the Ferryman's 60 and the crossing; the Hermit's story for a marrow; the lost
      never attack, a kill is *Alone*.
- [x] Unit rows: the line order and repetition, the save's NPC state round trip, the purchase's scent and pouch
      arithmetic, the toll; the replay rows of a conversation, a purchase and the toll; the goldens of each NPC's
      drawing and of the speech frame and the trade list on both tiers; the hit census unchanged.
- [x] CUB 8 and journey 7 with the trunk writer's migration witnesses; the found-lore list 48.
- [x] The note (five sections, the ledger line, the anchors), the plant red by name, the evidence directory, the
      README refreshed in its own commit.
- [x] The Mac gauntlet green at `4adf03e1`; [ ] the Linux gauntlet at `4adf03e1`: running (pid 1970575, its log and
      marker above).
- [ ] PR-tier approval is the orchestrator's; the lane read CI once, immediately, and never labelled.

## Hooks and follow-ons

The anchors, for cb18's placements (world cells; `npc.place`, `--npc-audit` prints every seed's): Quill on
Larkmeadow's perch (`LM_PERCH`, row 29), then two rows north of a den; Dunmoss four cells east of the sett's portal
(the Teeth, row ~72, x ~-28); Ember at Bramblehold row 24 (the route's west edge), Larkmeadow row 176 (its east
edge), the Larkmeadow pocket's end (row 210, east); the Charcoal-burner four cells route-side of the Burn's kiln (row
~112); the Ferryman two cells east of the Mere's causeway post (row 12); the Hermit inside the Stand's cutters' ruin
(row ~197); Fenn, Bracken, Loam on the Hush's route edge at rows 40, 82, 132. cb18's new foes share the Stand (the
marten) and the Burn (the adder, the moths) with the Hermit and the Charcoal-burner: a spawn on those cells is the
orchestrator's to resolve. The crossing lands at the Mere's row 168, before the heron's last stone (rows 196-199).
No issue was filed or closed.
