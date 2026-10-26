Footprint: cross-cutting

# Note — cb04, the bosses and the ghosts

M-CB4 on cub trunk `0bcfd0cb` (cb02c's merge), rebased at the end onto cb03's trunk `3c17348` (the
score; the engine re-pinned by cb03 to lair `57870143`): the Teeth, the Shallows and Gravehollow; Old
Snag, Whisper, Alder and Ashgrim; ghosts from the death archives; the title with its demo; the end. The
numbers come from two instruments, `cub --boss-census` (fifty seeds at both sizes, the scripted real-key
fighter) and the goldens' `final.state`; the frames, the census, two fight traces and both hosts' gate
logs are under `notes/cb04-evidence/`. The prediction is `notes/cb04-prediction.txt`, committed before
the first change (`3cee557`).

## Prediction

Written before any change (`notes/cb04-prediction.txt`); read against the result:

1. **The ghost reader.** Held. A `.pk` carries keys and numeric events only, so a ghost needs the game's
   own words for its positions: the death archive gains a trailer of `ghost-x`, `ghost-y`, `ghost-face`,
   `ghost-pose`, `ghost-area` a tick for the last 90 ticks and `ghost-death N`, merged in tick order; the
   engine's `replay.from_text` and `replay.args_at` read it back and nothing in the sim runs for a ghost.
   The engine lacked nothing; `args_at` is linear in the events, so a ghost's frames are read once at load.
   The gate (`tools/gameplay.py`, `ghosts`) compares the trailer with the sim's trace frame for frame: 90
   frames, 0 differing, both tiers.
2. **Attempts to win** (100 worlds a boss, five lives each): predicted boar ≥ 90 first-attempt wins and
   never above 2, lynx mostly 1, elk ≥ 95, alpha 1–2 at most 3, none unwon. Measured: boar 1: 78, 2: 10,
   3: 10, 5: 2 at cb02c's pace (wider than predicted: the charge in the clearing's mouth, see below) and
   1: 86, 2: 12, 3: 2 at the final head on cb03's pace; lynx 1: 100; elk 1: 100; alpha 1: 100 (narrower:
   the mirror is read by the parry); none unwon. The boar's spread is the one miss; it stays inside the
   contract's bound (a win within five lives in every world).
3. **Telegraphs ≥ 9 by construction.** Held: shortest observed by attack, boar 12 / 24 / 12, lynx 10 / 12 /
   15, elk 16 / 24 / 18, alpha 9 / 12 / — (the howl, phase two only, never rolled in the census). The
   unparryable attack was predicted to land 0 hits; it landed 134 (boar), 14 (lynx), 2 (elk), 0 (alpha)
   at the final head (180 / 26 / 6 / 0 before the rebase): the boar's charge from the clearing's mouth,
   where the branch leaves no room to step aside, is the whole of the boar's count; the fighter now
   enters the arena before it fights, and probes the ground before it picks a side, and the hits are what
   remain.
4. **Golden directories.** Predicted all 95 moved plus about 26 new (121). Measured: 68 cases + art =
   137 directories; the existing ones moved in `final.state` only (the trace's `bosses end arena played
   lost` and the foes' `attack poise`), none in a frame; 21 new cases (12 boss, `end`, `ghost-death`,
   `ghost`, `crags`, `river`, `old-den`, `demo`, `title`, `title-demo`) at both tiers, and the art
   sheet gained `boss-rich/plain` and `wolf-rich/plain`. The rebase onto cb03 moved every golden again
   (its posture HUD and pace); they were regenerated at the final head on kasumi.
5. **Save schema 3.** Held: `bosses N end N played N lost N` added, 53 words, the bounds as predicted, a
   schema-2 file `save_version` by name, `journey 2` with `saved-0` .. `saved-28`; every save in the
   world checks under 512 bytes.
6. **The censuses over six areas.** Held: 600 rows green (`--world-audit`, flat run ≤ 2, textured ≥ 90 %,
   `path_off` 0, reach = required, nearest foe ≥ 30), with the stone of the Teeth held to the flat-fill
   rule.
7. **Render cost.** The perf gate holds (`tools/check-perf`, kasumi, container: render avg 305 us, latency
   median 13.6 ms p90 33.4 ms at 80×24; the pre-rebase log is `linux-gate-pre-rebase.log`).

## Forbidden

Original work only: pack's `src/sim/` was read for the shape of a telegraph (windup, active, recovery
as counted ticks) and nothing else; every boss, its moves, the arenas, the areas, the ghost trailer, the
title and the end are cub's own; no other game's code, assets, text or music. No `lair` change (the engine
moved only with cb03's pin, taken at the rebase); no workflow, planning-repo or `~/.claude` edit. No
merge, label, tag, release or issue action; the three plants are draft PRs on `cb04-plant-*` branches and
nothing else. No attribution or co-author trailer on any commit or PR. Rulings are recommendations the
lane implemented (R-cb04-1 A, R-cb04-2 A, R-cb04-3 A, R-cb04-4 A; the new R-cb04-5 below), none decided.
Signal witnesses are the pty rows' bytes; no trap or kill script. The Mac held the worktree for git and
one play build at the final head behind the memory gate; every golden, soak and test loop ran on kasumi's
cores 8–11 under the shared lock, inside the engine container.

## Inputs verified

- Base trunk `0bcfd0cbc6a6226d76c82b365c5ecabb8a42bdfb`; rebased onto `3c17348` (cb03, the score);
  engine `aa6c4dc0` then cb03's `57870143` (`tools/fetch-lair` on kasumi, the staged `LAIR-REV` read);
  wolf 0.2.35 and lupin 0.1.56 staged by the fetcher.
- The contract, the campaign, `notes/cb02c-the-gait.md`, `cb02b-the-grove.md`, `cb02a-the-coast.md`,
  `cb01b-the-feel.md`, `docs/`, lair's `docs/REPLAY.md`, `sprints/RULES.md` §1–§10 and the guide read;
  pack's sim read for the telegraph vocabulary's shape; cb03's `docs/SCORE.md` for the cue slots
  (`boss-boar` .. `boss-alpha`, `title`, the silent `crags`, `river`, `old-den`).
- The contract names "the title card (cb01's)": nothing in the tree is a title card (cub starts in play);
  the title here is built from nothing, a correction for the planning repo.
- R-cb04-3 A says a rest "keeps its phase": implemented as a heal to full, which is phase one again (phase
  two is under half health by definition); the beaten state alone survives a rest.
- The coordinator's words during the lane: cb03a works on the existing areas, the combat and the HUD
  beside this lane; the save stays its own (no cb03a schema); den ids 4..7 are this lane's (4 the
  Teeth, 5 the Shallows, 6 Gravehollow, 7 spare), 8..15 cb03a's; schema 3 as the contract says, since the
  53-word checked format has no optional field. Seams with cb03a named: the stamina model (the
  fighter's reserve reads `s.stamina` and `s.exhausted`; the alpha's hop and guard read the cub's
  actions), the foe body rules (`push_out` gained a boss clause), the den code (`forest.DENS` 7, the
  den tables, `journey.lu`'s `last_den` 0..6 and `lit_dens` 1..127 to widen for 8..15), the HUD's row 1
  (the boss bar), and `src/forest/forest.lu`, rewritten for six areas: the three existing generators
  keep their rules but the file is one body now.
- cb03's `sim.boss_theme` slot (`s.boss`) is set here: the engaged boss's index while engaged, −1 on
  disengagement and when beaten; the title scene plays cb03's `title` part (`scene != 0`), and so does the
  end (the pack's call: the `howl` cue hook stands beside it).

## Evidence index

Commits, each its own chunk (`git log origin/trunk..`): the prediction `3cee557`; the areas `3e42ba3`,
`b373073`, `c55c068`, `e7da459`, `8371597`, `e04fb11`; the save `8339902`, `2e4ec7f`, `243dcfc`; the
bosses `39b7d13`, `dd0e38d`, `5b99891`, `0237fbe`, `ff7bb36`, `633ff21`, `7f5887e`; the ghosts
`517bd56`, `a887eba`, `9c72493`; the title, the demo and the end `6cd2391`, `1d7be9c`, `8fe87f8`,
`351e755`; the fighter and the census `9def98b`, `4dbcf72`, `889b87e`, `93b8493`; the witnesses and
goldens `b7c8d54`, `8060f7c`, `6d46164`, `27dcdbe`, `576cff1`, `954797a`; the gates `5f23d07`,
`3f42341`; the rebase onto cb03 `4a8a234`, `ca83e9e`; the docs `618b379` .. `aedf733`; the regenerated
goldens at the final head and this note follow.

Files under `notes/cb04-evidence/`:
- `boss-census.txt`: the census at the pre-rebase head (400 world rows, four `fairness` lines).
- `boss-census-final.txt`: the census at the final head (`tools/gameplay.py`'s copy).
- `fight-trace-alpha-seed1.txt`, `fight-trace-boar-seed6.txt`: `--fight-trace`, one line a tick.
- `linux-gate-pre-rebase.log`: `tools/check-linux` and `tools/check-perf` in the container on kasumi's
  cores 8–11 at `3f42341` (pre-rebase): `check-linux: green`, `cub check-linux: green`, perf green.
- `linux-gate-final.log`: the same at the final code head `3dd03c9` (681 lines: `check-linux: green`,
  `score-check: green`, `gameplay: green (0 skips)` on both binaries, `cub check-linux: green`, perf
  green, `GATE-EXIT 0`).
- `gameplay-final.log`, `pty-final.log`: the gameplay gate and the pty rows at the final code head
  (the engine's rows and cub's, `title` and `title-demo` among them).
- `plants.md`: the three plants, their branches, heads, PR numbers, run ids and the rows they turn red.

Gates and what they hold:
- `src/areas_test.lu` (8), `src/bosses_test.lu` (10), `src/ghost_test.lu` (5), the schema tests: the
  checked machine, every test within its step budget (sampled where a whole area would exhaust it).
- `tools/gameplay.py`: `bosses` (every parryable windup that reached its strike ≥ 9 on the beaten
  scripts, phase two under half health, the beaten bit and shortcut, the end's card and `r`, the three
  areas' foes, the title), `ghosts` (the trailer against the sim frame for frame; the archive drawn, an
  empty archive and another world's not; the sim unchanged by ghosts), `fairness` (the census on the
  shipping binary, exit 0, `unwon:0`, `arena_breaches 0`).
- `--boss-census` itself exits 1 on a world unwon, a parryable tell under 9 or a boss tick outside its
  arena (the plants' rows).
- The goldens: 137 directories, 21 new cases.
- The pty rows: `title` (the title drawn, a key begins the opening, `--no-title` skips it) and
  `title-demo` (no demo before ten seconds, the demo after); every other row starts past the title.

## Done-when

- [x] The Teeth, the Shallows and Gravehollow generated by seed with the grove's rules; dens 4..6; edges
      4..8 with the shortcuts home (bits 4 and 8, the log's bit 1 for the boar); the censuses over six areas.
- [x] Four bosses as big bodies on cb02c's rules, each in a bounded arena it never leaves (every move and
      yield checked; the census counts breaches: 0), two or three telegraphed attacks every parryable one
      ≥ 9 ticks, one unparryable beaten by the dodge, phase two at half health, poise, the alpha's mirror.
- [x] The bar only for a boss (R-cb04-2 A), drawn while engaged; a rest heals an unbeaten boss to full
      (R-cb04-3 A); the beaten state saved, the shortcut opened, the scent dropped.
- [x] Ghosts: the last five deaths fading (R-cb04-1 A), the trailer read by the engine's reader, the
      replay within eight cells; another world's death skipped (R-cb04-5, proposed).
- [x] The title with the four silhouettes lit when beaten, the keys, the demo after ten idle seconds
      (committed `demo.pk`, embedded); the end: the ford crossed as a wolf one size larger, the `howl` cue,
      the card, `r` keeps playing (R-cb04-4 A); the save records it.
- [x] Fairness: every world won within five lives (boar 1: 86, 2: 12, 3: 2; lynx, elk, alpha 100
      first-attempt), every parryable telegraph ≥ 9, the unparryable dodged (0 alpha, 2 elk, 14 lynx, 134
      boar hits in 100 fights each).
- [x] Tests, goldens (21 new cases at both tiers, the art sheets), the gameplay gate's boss, ghost and
      fairness rows, pty rows `title` and `title-demo`, docs (DESIGN, ART, KEYS, REPLAY, PALETTE, README),
      this note.
- [x] Three plants as draft PRs (#27, #28, #29) red by name in their own runs (`plants.md`).
- [ ] CI at the final head (`tier pr` green; `tier full` is the orchestrator's label); the lane audit's last
      line quoted in the hand-back.
