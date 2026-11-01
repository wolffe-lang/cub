# cb19 — the three rulings: the foes' spacing, an old save at the door, the marten's theft

The maintainer's rulings on cub#89 ("Apply the spacing rule to every foe"), cub#91 (A) and R-cb18-3 (B), and
cub#90's flaky row. Claude lane (Opus 5.5), one agent. Base: cub trunk `c8669f2c` (cb18). Branch `cb19`, the Mac
worktree `~/lanes/cb19/cub`; the Linux work on hasu block B (CPUs 6–11, both flocks per run), kasumi offline.

Footprint: module

## Prediction

`48424f9a` (`notes/cb19-prediction.txt`), committed before the first change. It held, item by item, but for what
it did not foresee (the list after the items):

- **Item 1.** Red at `c8669f2c` in the Hush alone, the very 560 rows of cb18's
  `notes/cb18-evidence/pickup/inherited-near-npcs.txt` (byte-identical, `spacing/census-red-at-base.txt`): a fox
  pair by Fenn (rows 40–44) and one by Loam (136–140) in all 100 worlds, the weasel trio by Bracken (74–76) in 58;
  nearest gap -4. Green with the rule: the nearest foe 5 clear cells from any NPC in every one of the 100 worlds.
  The censuses moved exactly where predicted (below). The prediction said 10 to 40 golden directories would move,
  the cases that walk the Hush: 36 moved (18 cases, both tiers), every one "foe moved by the gap": the 17 cases it
  named and `cb18-walk`, which walks the Hush too.
- **Item 2.** At `c8669f2c` a CUB 1 `~/.cub/save` stops every start: `cub` and `cub --save NAME` exit 2 with
  `cub: save_version` before the terminal opens (the rows' base runs, below). After: never.
- **Item 3.** At `c8669f2c` a theft is lost on rest, death and reload (cb18's test asserted it). After: kept, CUB 9 /
  journey 8, the counts as predicted (242 values, events 253..255, EV_COUNT 256).
- **Item 4.** The cause read from the nightly 41194607711's artifact held: the game's first traced tick consumed
  five bytes (the opening's skip `?`, the arrow and Space) while the opening was still active, so the scene ate
  the Space; the row typed by wall clock. The proof under a forced stall (hasu block B, cub's CI image, the row
  and the game on CPU 6 beside busy loops on the same CPU, one cb19 release binary for both rows): beside one
  loop trunk's row stayed green 20 of 20, and so did the paced one (`feel/stress-1-load-35062ef0.log`); one loop
  does not slow the start past trunk's 0.15 s settle. Beside eight, trunk's row is red 18 of 20, each
  red by cub#90's own line (`rich n did not commit the injected aim`, `rich se …`, `plain s did not start heavy`,
  `plain live combo missing 1`) (`feel/stress-8-loads-35062ef0.log`). The first paced row was red there too, 8 of
  20, every one at its combo (`rich combo: DELIVERY no traced tick with strike 2`), which the prediction did not
  foresee (below). The row as it stands (`7fa6cfb1`) beside the same eight loops, trunk's row again in the same
  job: running at the hand-back (hasu, `setsid -f`, both block locks: log
  `/home/mfwolffe/lanes/cb19/stress3-7fa6cfb1.log`, every run's line `stress3 <tree> run <n> exit=<N> …` and each
  tree's `stress3 <tree> red <R> of 20`, marker `stress3-7fa6cfb1.exit`, pid file `stress3-7fa6cfb1.pid`).

What the prediction did not foresee:

- **The checked machine's budget.** The first whole checked suite (`35062ef0`, `checked-suite.txt`) was red: 688
  passed, 2 failed, 7 unsupported. Seven rows ran out of the step budget: six of cb19's theft rows and cb02b's
  `test_cb02b_forest_texture_everywhere`, which the rule alone puts out of it (the plant's own CI run, which carries
  the rule without the fixes, is red at that row: cub#92). The rule reads the NPCs in every placement, the Shingle
  of every `sim.new` included (Quill can perch at its den), where cb18 had kept `sim.new` free of them. The fixes:
  `a1df4fda` `spawn_keeps_gap` tests the NPCs' box before it makes a foe (`folk_gap`'s own far test, moved first);
  `bbef4837` a route group that keeps the gap where the den rule left it never moves, so its row is not asked the
  arena question either (R-cb19-1's own statement: a foe that keeps the gap does not move by a cell); `ab2330b1`
  the texture row builds one `sim.new` a field, not one a position (its 18 positions and asserts unchanged);
  `2b0d44a9` the theft rows wake the lynx journey at the Stand (`sim.wake`, the decode's own last step) instead of
  decoding it twice; `5b78dca9` the two rows that then decode record the theft as `marten_steal` does (the bite's own
  step stays `robbed`'s rows' and the witness's), and the journey 7 half of the snapshot row is its own row, on the
  Shingle's journey holding a theft in its journey 8 values. At `660006ab` 3 rows were still out of the budget; at
  `ab2330b1`, the code head: 698 passed, 0 failed, 0 rejected, 0 unsupported, 0 SKIP.
- **The paced combo under the stall.** Beside eight loops the game itself cannot keep real time: in a red run's
  `rich-combo.trace` tick 3 began strike 1 at 0.80 s, and ticks 4 to 41 were all stepped at 1.390 s, one wake, 38
  ticks in half a millisecond; the loop reads input only at a wake's first due tick, so strike 1's request window
  (ages 1..11) passed with no byte readable in it, whatever the injector did. Two fixes: `a9482466` parses the trace
  once a line (re-reading the whole trace every poll was the injector's own delay on a starved CPU) and presses each
  link at the strike's second traced tick, the earliest a legacy Space is not a repeat (`bite_key_tick`), not the
  fourth; `7fa6cfb1` plays the combo again, up to five times in the session, when a link was read only after its
  strike had ended (the cub idle and rested first); a link read inside its window that does not chain is never
  retried, and the row still requires strikes 1, 2 and 3 by the trace.
- **Two rows red.** cb02's `test_cb02_save_rejects_unknown_corrupt_and_inconsistent_data` used `CUB 9` as the
  unknown version (now `CUB 10`); cb05's retired-den row was refused by CUB 9's decode, which compared the journey's
  re-encoding with the text, and a retired last den wakes at a kept one: CUB 9 is now read by its own lines, as CUB
  8 is (`b4a912e6`).
- **The witness's pickup.** `r` takes an item on the cub's own cell at the tick's start; the witness waited for the
  cub to stop before pressing it and the cub coasted off the drop's cell (`recovered -1` at `35062ef0`): `660006ab`
  presses it the first tick the cub stands there.
- **The marten's arena frames did not change.** The prediction said `new-foe-arenas`' foe-9 frames would gain the
  glyph: they are byte-identical, since in none of them does the marten hold the yarrow. The carrying marten's
  goldens are the art study's two new sheets and the witness's case on both tiers.

## Forbidden

Original work only; the bible's names. No engine, pin, CI, `.github/` or `tools/check*` change (`tools/gameplay.py`,
`tools/world_checks.py` and `tools/npc_checks.py`, the repo's own gates, gain the new rows; the Footprint stays
module). The save format and the replay format are versioned, not broken: CUB 9 and journey 8, CUB 4..8 and
journey 1..7 still read (`REPLAY.md`, `DESIGN.md`). No label, merge, tag, release or issue edit; nothing in
`~/.claude` or the planning repository. The maintainer's `~/.cub/` (its `save.cub1-20261025` included) and
`~/lanes/play/save` were never read or written: every row and probe sets its own scratch `HOME` (the pty rows under
`target/pty/<row>/home-*`, the lane's runs under `~/lanes/cb19/home` and the pinned trees' `target/test-home`).

Mac work ran behind `/Users/mfwolffe/lanes/mac-build.lock` (the mkdir protocol, pid and lane files) with the 8 GiB
floor inside it (`~/lanes/cb19/heavy.sh`); hasu work in the lane's image `localhost/cb19-pack-ci:fbee7e864f7dbee6`
(built there from `.lair/ci/Containerfile`), `--memory 12g`, `taskset -c 6-11` inside the container, both block
locks held per run (`flock hasu-block-B.lock`, inside it `flock hasu-B.lock`), the long jobs under `setsid -f`
with a pid file. Nothing killed by process group.

**One runner ignored, by the orchestrator's ruling.** Early in the lane a Mac runner of mine (pid 94258, a build
and a census queued against the live worktree) was left waiting; my `kill 94258` was refused by the auto-mode
classifier and I handed back. On resume the orchestrator ruled: do not stop it by any means, let it finish, and
ignore its result entirely. It exited on its own; its log, its binary and the census output it wrote are not
evidence and nothing here cites them (the census file it wrote into the lane's evidence folder was deleted). From
then on no build ran against the live worktree: every build is a pinned worktree `~/lanes/cb19/build-<sha>` of a
committed head (`~/lanes/cb19/pinned-build.sh`), removed by its exact path when done. Two superseded waiters of my own
(the `0c8d5e00` build and the `fdd1cd38` rows, both still waiting for the lock) were stopped through the harness
before they took it, and their pinned trees removed by exact path.

A process lapse, reported: a few edits (the README's two refreshes among them) were made by a `python3 -`
heredoc in a compound Bash command, against the-rules' shell line (files by the Write tool). Each edit is in its
commit's diff and was read there.

The Mac lock: pk09's 20-run proof took it back within seconds of each release for over half an hour at a time
(2026-11-01 02:05–02:40Z and before), so the lane's 30 s waiters rarely saw it free; nothing was done about it but
waiting, by the protocol.

## Inputs verified

Toolchain and engine as pinned, unchanged: wolf 0.2.35, lupin 0.1.56, std `2386522e`, lair `74b89744` (staged in
`.lair` by `tools/fetch-lair`; the Mac's wolf `240b84d0…` and lupin `9133bfdb…`, Linux's `4cc4045b…` and
`ad703550…`, as `.wolf-bin` pins them). The PATH wolf (0.2.36) was never used: every gate runs `.wolf-bin/wolf` or
`.lair/tools/*`.

Read before the first change: `the-rules.md` with its Launch-fact corrections, `design.md`, trunk's `DESIGN.md`,
`KEYS.md`, `REPLAY.md`, the notes of cb13, cb04f, cb11, cb16 and cb18, cub#89, #90, #91 and #50, RULES §1–§10.
cb18's probe file was the census's red witness (byte-identical rows). The nightly 41194607711's pty artifact was
downloaded (`~/lanes/cb19/evidence/nightly-41194607711/`); its `plain-e.trace` shows tick 1 reading five bytes.
The CUB 1 fixture `tests/saves/cub1.save` (sha `31598ba4…`) was written by hand from cb02 `f50b9c16`'s
`src/journey/journey.lu` (schema 1's payload and its rolling check), never from a player's file
(`tests/saves/provenance.json`).

**Rulings** (each the recommendation, implemented):

- **R-cb19-1 A: a displaced foe moves along its own route, never deleted.** It keeps its area, kind, count and
  ordinal (the slain masks index it). A route group moves together, by the fewest rows from where the den rule left
  it to the nearest row where every member keeps the gap, the den's quiet radius holds and no member stands in an
  arena, forward on a tie; a branch's guards step together along their branch, back toward the route first; a guard
  with no route takes the nearest open cell that keeps the gap. A foe that keeps the gap does not move by a cell; a
  boss is never moved (every NPC stands 27 and more cells off every arena). The decode's count is the unspaced
  placement's: the rule moves, never adds (`sim.inherited_area_foes_as`, `sim.spaced_row`, `sim.spaced_shift`,
  `sim.spaced_cell`, `sim.spawn_keeps_gap`).
- **R-cb19-2 A: how the cub can tell.** The stolen item's own glyph and colour one cell ahead of the marten's head on
  the rich tier, a bold `+` in the item's colour on the plain, up its trunk too (`inventory.carried`,
  `art.carry_cell`, `art.draw_marten_carry`).
- **R-cb19-3 A: a marten already holding an item cannot steal a second;** its bite does its plain damage
  (`marten_steal`'s rule, kept; `test_cb19_r3_a_marten_holding_an_item_cannot_steal_a_second`).
- **R-cb19-4 A: a marten slain by anything drops what it holds** at the trunk's foot as when bitten, and the
  journey's record clears (`new_foe_status`'s rule, now clearing `sim.thefts`;
  `test_cb19_r4_a_marten_dead_of_anything_drops_its_item`).
- **R-cb19-5 A (new): a save from a newer cub is never renamed,** only left in place with one named warning (a
  newer cub can still read it); a `--save NAME` from a newer cub, or a corrupt one, is refused by its sentence. The
  orchestrator accepted it at the resume.

The orchestrator's reading of item 2 (the resume, 2026-11-01): a legacy `~/.cub/save` never blocks any start,
`--save NAME` included; a `--save NAME` too old for this build gets the offer and is kept as `NAME.cubN-old`; CUB 4..8
migrate as today; CUB 1..3 are kept as `save.cubN-old` with the offer. Implemented so.

**The commits** (oldest first):

- `48424f9a` the prediction.
- Item 1: `4939299b` the spacing census (`wide.foe_npc_census`, `cub --foe-npc-census`); `7252451d` the rule; `2255cc80`
  its evidence; `9ea5aad9` the gates on both binaries (with item 3's witness) and their tests; `09b6c5cf`
  `wide.FOES_NEW_MIN`'s comment corrected (cb18 filled the new areas' tables); `36822199` the fifteen cases whose
  walks cross the Hush, regenerated by their own generators; `e6559563` the goldens of the 18 cases that walk the
  Hush, both tiers (staged with the rule's binary `7252451d` alone); `9dc62df0` their ledger; after the first whole
  checked suite, `a1df4fda` and `bbef4837` (above).
- Item 4: `3207904f` `feel-controls` paced by the game's own trace; after the heavier stall, `a9482466` and
  `7fa6cfb1` (above).
- Item 2: `5271f7d6` the old-save pty rows and the CUB 1 fixture (red first: committed before the fix);
  `4a572364` the refusal sentences; `b792efb0` `registry.migrate` never stops the start, a too-old save kept;
  `7b86b5e1` the start's lines and the sentences at every failure site; `273d0e98` the title's line and its key on
  New journey; `d10fdc3b` the unit rows; `fdd1cd38` the rows read the title after it is drawn.
- Item 3: `3fc0d21d` the kept theft by spawn; `e6bb9de7` CUB 9 and journey 8; `f04485e3` the carrying marten on both
  tiers; `bd303f20` the theft witness `cub --make-theft-proof DIR` and journey 8's replays; `e32e9aef` the unit rows
  and cb18's row turned; `0c8d5e00` older rows' CUB 8 / journey 7 pins brought to CUB 9 / journey 8; `5136a077` the
  witness walks on through the marten's early tell; after the first whole checked suite, `b4a912e6` (CUB 9 read by
  its own lines; cb02's unknown version `CUB 10`), `2b0d44a9`, `5b78dca9` and `ab2330b1` (the budget, above) and
  `660006ab` (the witness's pickup); `4302e199` the witness's case `tests/cases/marten-theft.pk` (sha256
  `869f7662…`) and the carrying marten's goldens, both tiers; `d1b07866` their ledger.
- Docs: `c399548a` DESIGN, `1fcdc341` REPLAY, `35062ef0` KEYS, `49b8f364` the README (README only; read whole: the
  saves paragraph, the six's paragraph and the census flags are current, nothing else moved); `7508519a` DESIGN's
  cub#90 paragraph brought to the combo under the stall; this note and its evidence.

**Item 1, every moved row with its reason** (`spacing/censuses-base-vs-7252451d.txt`, each census run by the base's
binary and the rule's, `cmp`'d):

- byte-identical: the foe census (counts only, the rule moves no foe in or out of an area), the hit census (frozen
  bosses), cb18's new-foe spawn census and arena census, the new-foe hit rings, the den spacing, the bends, the
  spurs, the npc audit;
- the world audit: only the Hush's nearest-foe-to-a-den column, 100 rows, 30..35 cells to 38..41
  (`spacing/world-audit-hush-rows.diff`): the moved foes stand farther from the cold den;
- the boss census: only the alpha's rows (`spacing/boss-census-alpha-rows.diff`): its fighter walks the Hush from the
  cold den past the moved foes; its fairness line `attempts 1:100`, landed `hits` 89 to 107, `damage_events` 107,
  `arena_breaches 0`, every world still won in one life. The boar, the lynx and the elk byte-identical.
- the generators (`spacing/generators-base-vs-7252451d.txt`): every case generator run by the base's binary equals
  the tree; by the rule's binary 15 cases change (the walkers' world moved): `boss-alpha-beaten`,
  `boss-alpha-phase2`, `boss-alpha-windup`, `cb18-walk` (from `walk.pk`), `end`, `gravehollow`, `howe`,
  `landmark-11-0`..`landmark-11-5`, `landmark-12-0`, `landmark-5-0`; regenerated in `36822199`
  (`spacing/case-receipts.tsv`, each with its generator and sha).
- the goldens (`goldens/item1-foe-moved-by-the-gap.tsv`): 36 directories, the 18 cases that walk the Hush on both
  tiers, the 15 regenerated and `hush`, `rest-hush-80x24` and `rest-hush-120x40`, whose cases are unchanged and
  whose world moved; every one "foe moved by the gap". They were staged by the rule's binary alone, so nothing of
  items 2–4 is in them; the head's binary then moves nothing else but item 3's three directories
  (`goldens/item3-the-carrying-marten.tsv`: the art study's `marten-carry-plain` and `marten-carry-rich` sheets, the
  new `marten-theft` case on both tiers). 519 directories at the head: the base's 517 and the two new.
- `bbef4837` (a group that keeps the gap at its den-rule row is not asked the arena question) and `a1df4fda` move
  nothing: the spacing census at the code head `ab2330b1` is byte-identical to the rule's (`7252451d`'s, `cmp`, on
  nomad and on hasu), its release goldens 517 `ok`, 0 `DIFFERS` (nomad), and the theft witness's record
  byte-identical to the committed case on both hosts (`hasu-check-ab2330b1.log`: the Linux build, the checked suite
  698 passed, 0 unsupported, the census and the witness).

**Item 2, the sentences.** Every save refusal is now `journey.refusal` / `journey.write_failure` /
`registry.failure`: the file, the version found, the versions this cub reads (CUB 4 to CUB 9), what to do, the
error's name in brackets at the end; the Load page wraps it over up to eight lines. For example, the default start
over a CUB 1 legacy save prints once on stderr and shows on the title: `~/.cub/save is a CUB 1 save; this cub reads
CUB 4 to CUB 9. Kept as ~/.cub/save.cub1-old, nothing deleted; a new journey starts here.`

**Item 3, the format.** CUB 9 is CUB 8's lines and one `thefts K0 K1 K2` line after `npcs` (each the item kind a
Stand marten holds by its spawn rank, -1 none); a CUB 8 reads holding no theft. The replay's journey 8 carries 242
values (the three slots saved at 239..241, their numeric events 253..255, EV_COUNT 256); journey 7 and older read as
before (`REPLAY.md`).

**Item 4, the fix.** `tests/pty_rows.py`'s `feel-controls` now waits on the game's own trace for every injection:
the opening's skip consumed and scene 0 traced, then the chord consumed, then the committed action, as cb11's
`cb11-ticks-enhanced-*` rows do (`FeelDelivery`, `feel_rows`, `feel_until`, `feel_send`, `feel_open`,
`feel_combo_once`); no wall-clock settle decides anything. Its combo presses each link at the strike's second traced
tick and plays the combo again (at most five times) only when a link was read after its strike had ended.

## Evidence index

`notes/cb19-evidence/`:

- `spacing/census-red-at-base.txt` (the census at `c8669f2c`: RED, 560 rows, nearest -4),
  `spacing/census-green-at-7252451d.txt` (green: 16,600 foes, 574 moved, nearest 5, 100 worlds),
  `spacing/censuses-base-vs-7252451d.txt`, `spacing/world-audit-hush-rows.diff`,
  `spacing/boss-census-alpha-rows.diff`, `spacing/generators-base-vs-7252451d.txt`, `spacing/case-receipts.tsv`.
- `goldens/item1-foe-moved-by-the-gap.tsv` and `goldens/item3-the-carrying-marten.tsv`: every golden directory that
  differs from `c8669f2c`'s, with its files changed, added and removed, its case and its cause.
- `oldsave/rows-head-660006ab-and-base-c8669f2c.log`: `cb19-old-save-default` and `cb19-old-save-named` green on
  the head's release binary (`660006ab`) and red on `c8669f2c`'s (exit 2 before the terminal opens, no title, the
  legacy save neither kept nor left); `oldsave/base-c8669f2c-default.stderr` and `oldsave/base-c8669f2c-named.stderr`
  are the base's whole stderr in those runs: `cub: save_version`. The eleven older save and menu rows
  (`pending-save`, `save-failure`, `resumed-record`, `cb04b-held-resume`, `trunk-save-resume`, `cb05-save-resume`,
  the five cb13 menu and registry rows) green with them at `35062ef0` on nomad.
- `theft-proof-660006ab.log`: the witness green (steal at tick 176, death 216, the wake 266 holding it, bitten back
  571, recovered 701, 711 ticks) and its replay from the record's own snapshot, keys and one delta, parity 1.
- `feel/nightly-41194607711-plain-e.trace` (the red: tick 1 `in 5 keys 9`, the opening's skip, the arrow and Space
  read at once) and `feel/nightly-41194607711-rich-e.trace` (the same run's green row);
  `feel/stress-1-load-35062ef0.log` and `feel/stress-8-loads-35062ef0.log` (hasu, every run's exit and first
  problem line); the row as it stands under the same stall is the running `stress3-7fa6cfb1` (above).
- `checked-suite.txt`: the non-ok rows and the summary of each whole checked suite on nomad (`35062ef0`,
  `660006ab`, `ab2330b1`); `hasu-check-ab2330b1.log`: the code head on hasu.
- `plant/plant-census-35d6a446.txt`, `plant/plant-run-35d6a446.log` (below).

- **The plant:** cub#92 (`cb19-plant-gap`, `35d6a446`, off the line: base + the census + the rule + the Hush's first
  fox put back where the seed put it, inside Fenn's talk radius): `foe-npc-gap: RED, 100 of 16600 foes within 4
  clear cells of an NPC, the nearest -4`, its first row `foe-near-npc 0 80 5 1 -11 40 -4`, the gameplay gate's
  validator red `a foe inside an NPC talk radius` (nomad, `CB19_PLANT_DONE`). Its CI run 41262727931 is red
  earlier, at the checked suite (cb02b's texture row out of the budget, the rule without the fixes); the census red
  is nomad's, by name. It stands.
- **The gauntlets at the final head** (this note's head), both detached at the hand-back, each stopping at its first
  red step and printing every step's `END <step> exit=N`:
  - the Mac gauntlet (`~/lanes/cb19/mac-gauntlet.sh` behind the lock in a worktree pinned to the head: the head
    check, fmt, the python tests, the pty fixtures, the checked suite and its SKIP count, both builds and selftests,
    both binaries' goldens (at most three attempts on the floor), the pty rows without `sound-live` and
    `mute-key`, skipped by name, the score check, both gameplay gates, the memory gate): log
    `/Users/mfwolffe/lanes/cb19/gate/mac-gauntlet-<head>.log`, its last line `CB19_MAC_GAUNTLET_EXIT N`, marker
    `mac-gauntlet-<head>.exit` and pid file `mac-gauntlet-<head>.pid` beside it (`nohup`, disowned: macOS has no
    `setsid`);
  - hasu's (block B, the lane's image, `taskset -c 6-11` inside: the python tests, the pty fixtures,
    `.lair/tools/check-linux`, the native goldens, the score check, both gameplay gates, the memory gate, then
    `env LAIR_PERF_SLACK=1 tools/check-perf` inside the container, slack 1): log
    `/home/mfwolffe/lanes/cb19/gate-<head>.log`, its last line `CB19_LINUX_GAUNTLET_EXIT N`, marker
    `gate-<head>.exit`, pid file `gate-<head>.pid`.

## Done-when

- [x] cub#89 A: every foe's spawn out of every NPC's talk radius (R-cb19-1 A); the spacing census red at `c8669f2c`,
  green at the head, gated on both binaries; the censuses re-run and every moved row named; every changed golden
  "foe moved by the gap"; `wide.FOES_NEW_MIN`'s comment corrected.
- [x] cub#91 A and cub#50: an old save never stops the start; a too-old default save kept as `save.cubN-old` with the
  title's offer; every refusal a sentence; the pty rows red at `c8669f2c` and green at the head; a unit row per
  message.
- [x] R-cb18-3 B: the marten keeps its theft across rest, death, re-entry and reload; CUB 9 with its CUB 8
  migration; journey 8; the witness replay; both tiers' goldens of the carrying marten (R-cb19-2..4 A).
- [x] cub#90: `feel-controls` tick-paced; under the forced stall (eight loops on its CPU) trunk's row red 18 of 20.
- [ ] cub#90: the paced row as it stands green 20 of 20 under the same stall: `stress3-7fa6cfb1`, running at the
  hand-back.
- [x] The plant red by name, off the line (cub#92).
- [x] Test targets: the checked suite; both binaries' goldens; the generators against the base and the rule; the
  spacing, foe, hit, boss, fairness, new-foe, den-spacing, bend, spur, npc and world censuses compared; the old-save
  pty rows on both binaries; the theft witness and its replay; the stress runs.
- [ ] The full gauntlets at the final head, the Mac's and hasu's: running at the hand-back (the evidence index).

Closes #89, #90, #91 and #50 (by hand at the merge: the orchestrator's).

Ledger: cb19 | the three rulings | module | PR: this note's PR | plant #92 | final head: this PR's head.
