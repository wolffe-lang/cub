# cb05 — the wide forest

Bigger areas with smooth, shaped branches and a thicket with more ways through it; fewer, farther dens, the retired ones left standing as landmarks; Cinderwick, a burnt town between the Shingle and Bramblehold, with the Ashen in its lanes and yards; Larkmeadow filled; every dead end rewarded; the forest talking back in lore lines at its caches and marks. Game code, game-owned tests, witnesses, censuses, docs and goldens only: no engine, pin or CI change. `src/world/` is the engine's symlink and was not touched.

**The overhaul stands as built; the maintainer never reached it.** His play of `cd7e5022` died repeatedly in Cinderwick, the second area, so the lengthened areas, the reshaped branches, Bramblehold's fork, the filled meadow and the nine dens were never seen in play. Item 8 (below, "The second pass") is the town's answer: the swarm, the width and the hitbox, each measured before and after; nothing of the forest beyond the town moved for it.

## The second pass (item 8)

The maintainer's words: "We'll have to make the town area enemies easier. They swarm and i've died repeatedly ... I was hoping the town map would be more rectangular, that is take up more width of the screen ... The town enemies hitboxes might be too small as well." Three parts, each with its instrument on the branch (`cub --crossing-census`, `--hitbox-audit`, `--town-map`), measured before (the town of `cd7e5022`) and after.

**(a) The swarm — R-cb05-5, recommended A and implemented.** At most two Ashen pursue at once (`ASHEN_PURSUERS`; a third that hears the cub keeps its post, turned toward it, until one of the two is parried, loses the cub or dies: `Foe.chasing`), their hearing 16 → **10** cells (`ASHEN_HEARING`) and 4 → **2** sneaking (`ASHEN_HEARING_SNEAK`), the lane's first third (80 of 240 rows) carries one pair (row 40; the next at 88, 160, 204), groups of three nowhere (the far yards keep their two). The fox's and the bosses' numbers untouched. The crossing census (`src/cross/cross.lu`): a fresh cub with the Shingle's heart (52 health) and no flask, placed at the thorn throat, walked by the test walker to the cold hearth with Book-II play (walk, bite what is in reach, parry an Ashen's windup two ticks before the blow, never roll), ten seeds at both fields. Before (`crossing-before.txt`): 10 of 10 arrived at both fields, health 48–52, 1–4 Ashen beaten on the way. After the rule on the narrow town (`crossing-after-rule.txt`): 10 of 10, the same. After the block plan (`crossing-after.txt`): **10 of 10 at both fields**, no death anywhere, the bar nine of ten. The instrument says the scripted cub was never in danger: it bites with a locked aim every tick a body is in reach and parries in the window; the maintainer's deaths were a human's, in a swarm that heard him sixteen cells off and came four at a time. The rule caps what comes and how far it hears; the walker's margin is the gate row (`tools/world_checks.py::wide`, `--crossing-census` green, at least nine of ten, no death on the lane).

**(b) The width.** Before: the town was the lane and its plots, ±36 cells of the field's ±48 at 80 columns (73 of 97), the same 73 at 200 (of 217), 288 rows long. After (`town-map-80-after.txt`, `town-map-200-after.txt`): a rectangle — the lane with its 14 plots a side, two cross streets of 8 rows after plots 2 and 10 running the whole width, the square (plots 6 and 7) open across it, a side street each way at x = ±44 from the first cross street to the last so every street loops, every passage row running on behind the yards to the side street; **94 of 97 cells at 80**; at 200 a second row of plots faces the side streets' outer sides and a ring at ±80 closes the blocks, **166 of 217** (more blocks, never wider streets). The length shrank 288 → **240** to pay for it (the hearth at rows 124..127, the den spacing's least onward 116 kept, the 110 bar). The lane is unchanged, so the bends (0 reversals), jaggedness and straight-run (10) censuses hold; the world audit's 700 rows reach every cache, den and portal with every foe 30 cells and more from a den (the cache yards moved to plots 2, 4, 9, 12 and the marks to 3, 10 for it); spurs green; generation 4 ms (80) / 9 ms (200) for the town. The rectangle row: `test_cb05_the_town_is_a_rectangle_across_the_field` (the cross streets open across the width, the side streets open end to end, the wood closed three cells past the edge, both fields, three seeds).

**(c) The hitbox.** The audit (`hitbox-before.txt`, `hitbox-after.txt`) bites an Ashen standing still from each of the eight aims, the cub's body touching it and then a cell off (the bite's reach is two), and records the cub's cell, the bodies' gap, whether the Ashen's anchor and its nearest body cell lie in the bite's ninety-degree cone, and whether the bite lands. **All sixteen land, before and after**: the hit test was already the whole body (`sim.in_reach` measures the gap between the drawn bodies, cb02c; the cone test on the anchor passes from every touching or one-off position because the anchor sits a cell inside the body along the aim). The Ashen's own blow and the parry use the same body test. Nothing changed for it; what it was is on record. The hitbox row: `--hitbox-audit` green in the gate.



## Prediction

`9b706b77` committed `notes/cb05-prediction.txt` before the first implementation change, at trunk `7e2c6a77` (+ cb04d's note). The "before" rows were read on trunk's own generators by this lane's new instruments, run on hasu's container against the base (`notes/cb05-evidence/*-before.*`).

What the prediction said and what held:

- Seven areas, ten edges, per-area lengths 160/288/288/288/224/224/224 (R-cb05-2 A): held exactly.
- Dens 11 → 9, at most two an area, none within 110 route cells (R-cb05-3 A): held; the census walks the real tiles over fifty seeds and both fields: **least within an area 122, least onward 116** (predicted 110–140 within; the onward figure is the next area's first den from the previous area's last, through its portal). Dens 8, 9, 10 retired to landmarks, their ids kept in schema 4, a save whose last den is one of them wakes at the nearest kept den (the meadow's two both wake at the last warm hollow: at 288 rows both old rows lie nearer it than the grass nest; the prediction guessed one each).
- Foes per area (R-cb05-4 A): in every seed at both fields the Shingle 9 (unchanged), Cinderwick 16, Bramblehold 18, Larkmeadow 18, the Teeth 8, the Shallows 8, Gravehollow 9 (predicted 12–16 / 14–18 / 14–18 / 8–12 for the last three); every one at least 30 cells from a den (the world audit's `min_foe_cells` 30 over 700 rows).
- The bend census: the instrument postdates the generator it would have measured, so the sawtooth's "before" is cb04d's own per-ten figures and the maintainer's eye; after, **0 reversals** on every route and branch (fifty seeds, both fields; 7,676 counted turns, the town's lane 0). cb04d's per-ten jaggedness, which the prediction said would be no worse, fell in every area: Shingle 0.0895 → 0.0679, Bramblehold 0.1857 → 0.1046, Larkmeadow 0.1325 → 0.0572, the Teeth 0.1681 → 0.1000, the Shallows 0.1903 → 0.1028, Gravehollow 0.1699 → 0.1111; route width medians 7/9/9/7/9/9 → 7/9/9/7/9/11; the three worst routes 0.976/0.909/0.909 → 0.488/0.488/0.488 per ten.
- Generation under 50 ms an area at field 200: held on the Mac release build (the Shingle 17 ms, the thicket and the meadow 8, the Teeth, the Shallows and Gravehollow 3, the town 4; the native x86-64 build in hasu's container takes 63 ms on the Shingle, so the bar is held to the release build as the perf gate's are). Render means within +15 %: Mac release 173/164 µs at 80×24 rich/plain and 1260/1290 at 200×60 against cb04d's 182/174 and 1306/1296 (the gate's own run read 196/183/1351/1301, inside the 1000/4000 bars at slack 1); latency median 11.5 ms, p90 33.5.
- Goldens: every in-level case moved; 23 new cases (the town's lanes at night at both sizes, fourteen landmarks, the four town witnesses); score goldens unchanged.

The prediction's one wrong guess beyond the meadow's wake: the town's lane. The prediction assumed the route meander would serve it; it cut house corners (the lane wanders five cells in a plot), and three censuses pull three ways on a street — the straight-run bar (no run over twelve), cb04d's jaggedness (no step out and back within three samples) and this lane's bends census (no opposite turns within eight cells). The lane that satisfies all three weaves on anchors every two plots, sits mid-cell at each apex, eases four rows into and out of it and slants straight between; the houses are placed by the lane's reach over their plot's rows, not by one row.

**Rebased onto trunk at cb06's merge (`58969722`: cb04f's dens rule, save schema 5 and the centred ledger; cb06's opening).** Conflicts were the appended docs sections (DESIGN, PALETTE, README, the pty rows: both kept, trunk's first), the sim's `area_foes` doc beside cb04f's slain code (both kept), and the regenerated goldens (mine, regenerated again on the rebased tree). cb04f's behaviour is kept exactly: `enter_area` restores foes from the slain masks, the rest menu and the ledger untouched; schema 5 now carries **a slain mask an area, seven** (`journey`: 63 words, `SNAPSHOT` 37; `controls`: an appended `saved-36` slot, `EV_COUNT` 49), and the migration check expects seven empty masks. cb04f's witnesses moved under the wide forest without changing what they witness: the slain-survive test bites its first Shingle foe by the walker's ordinary keys (the Shingle's curve moved under the hand-recorded ones), the den-memory case crosses the thorn gate to Cinderwick and the Shingle's own log mouth to Bramblehold (two returns as before; its live row gets a minute: the case is 1,233 ticks). cb06's opening shares nothing with this lane beyond the goldens its sprites moved, regenerated.

## Forbidden

Original code, art and text only; no other game's code, art, text or names. No engine (`lair`) change; no pin, workflow or CI change; no change to movement, attacks, the roll (cb04b), the foe-reset rule in `sim.enter_area` or the rest menu (cb04f), or Old Snag (cb04e); `area_foes` keeps its shape. No ruling decided here: R-cb05-1 (the town's name, the Ashen, the den's name, the lore lines) is proposed in the checkpoint for the maintainer; R-cb05-2/3/4 recommend A and implement A. Never labelled a PR, merged, tagged, created or closed an issue, edited `~/.claude` or the planning repo, installed a package. No attribution or co-author trailers.

Mac heavy jobs ran through `/Users/mfwolffe/lanes/cb05/heavy.sh` (an 8 GB `vm_stat` free+inactive+speculative gate, retried every 180 s, the lane's own HOME and TMPDIR); the engine's own `require_memory` refused twice mid-gate on a busy Mac and the gate was simply rerun. hasu jobs ran under `flock /home/mfwolffe/lanes/hasu-block-A.lock` with `taskset -c 0-5` inside the rootless podman container, caches under the lane dir; nothing of the maintainer's touched; no process group signalled. Scratch under `/Users/mfwolffe/lanes/cb05/`, never `/private/tmp`.

## Inputs verified

Toolchain pinned in `.wolf-bin/`: wolf 0.2.35 (pin cf0c13d) paired with lupin 0.1.56 (pin 294d626); the engine at `.lair/` as trunk pins it. Contract, the maintainer's notes, design.md (§1, §2, §8, §16, §19), DESIGN.md's world table and the notes cb02, cb02a, cb02b, cb03a, cb04, cb04a, cb04c, cb04d read before the first change. README refreshed in its own commit (`df88d83c`).

Rulings recommended, none decided:

- **R-cb05-1** (to the maintainer): the town **Cinderwick**, its dead **the Ashen**, its den **the cold hearth**; the Ashen's look (four pixels across, twelve down; the head, the shoulders, a long thin body, the legs; grey on the night's black) and tell (the arms rise slowly beside the head over thirty ticks, the blow thrusts one arm out, a stagger splits the body); the ten lore lines in `src/lore/lore.lu`.
- **R-cb05-2 A**: 288 for Bramblehold, Cinderwick and Larkmeadow; 224 for the Teeth, the Shallows and Gravehollow; the Shingle's 160 untouched (the tutorial's lengths and its proofs stand).
- **R-cb05-3 A**: at most two dens an area, at least 110 route cells between them; the retired dens become landmarks (the coal roots, the low embers, the ash shelter).
- **R-cb05-4 A**: twelve to eighteen foes in each big area (the town 16, Bramblehold 18, Larkmeadow 18), eight to twelve in the later three, the Shingle's nine unchanged.

## Evidence index

- `9b706b77`: the prediction.
- `10fc1718`, `d978749c`, `df456dfe`, `e27955eb`, `cc008c18`, `787347e0`, `abf0a8cf`: terrain, the town, the lore, the forest (seven areas, shaped branches, the fork, pockets, landmarks, the burn), the sim (the Ashen, the embers, the foe groups, the retired dens' wake), the save, the art.
- `132e9e04`, `fad45ae6`, `b95c0d17`: the instruments, the five new censuses, the proof through Cinderwick.
- `43326020`, `d164a9c3`: routes zero-ended by their anchors, one curve per route, the loop entered tangentially, the fork eased.
- `04d4832e`, `4deeaefd`: the switchback's way in (a smoothstep, then straight: the bends census caught the smoothstep).
- `458efbb2`, `0d39d14a`, `c64af06d`, `f6ac5dd2`: the lane, four times (each census in turn).
- `58f7faaf`, `b64287a0`, `238ee598`: an ember burns the body, yard guards keep their posts, lane Ashen at open embers.
- `b00c5806`: the ten cb05 tests. `70d0bf2e`, `dad75c44`: the four town witnesses, the lanes at night, the landmarks. `bf0f1a21`: the four pty rows.
- `d0b63d0b`: the grass nest at the meadow's entry in the doorway's line (cb04d's doorway-edge row holds).
- `e6c26155`, `65b40ffb`: the gates (the journey through Cinderwick, the census totals, the wide censuses; the generation bar on the release build).
- `854f0349`, `433a9c6a`, `6b561f78`, `cd7e5022`, `df88d83c`: DESIGN, ART/PALETTE, KEYS, README (its own commit).
- `7a0061d0`, `14bd4391`, `eaf362c5`, `e5d8e2e2`: cases, goldens and the embedded demo, regenerated after each generator change.

Evidence lives under `notes/cb05-evidence/`: the before censuses (`world-before.txt`, `paths-before.csv`, `paths-before-summary.txt`, `feel-before.txt`, `bench-before.txt`, hasu's container on trunk), the after censuses (`world-after.txt`, `den-spacing-after.txt`, `foe-census-after.txt`, `bends-after.txt`, `spurs-after.txt`, `gen-bench-after.txt`, `paths-after.csv`, `paths-after-summary.txt`, `feel-after.txt`, `den-census-after.txt`, `look-after.txt`, `bench-after.txt`), the gate logs (`mac-final.log`, `linux-final.log`) and the play binary's hash (`play-binary.txt`).

The whole Mac gate (`tools/check`) is **green, exit 0** at the final source head `4a7cd345` (rebased onto trunk `58969722`; `mac-final.log`, 2026-10-27T06:44Z–06:58Z): 317 checked tests (0 failed/rejected/unsupported, 0 SKIP lines), every golden case-tier row and the art sheet, every pty row (the four town rows, cb04f's den-world-memory row with its minute, cb06's opening rows), the score check, both backends' gameplay/persistence/world/body/boss/den/den-memory gates with the seven wide censuses inside them, perf 175/173/1308/1294 µs under the 1000/4000 bars and the latency bars; the only SKIP is the Linux-only `/proc` idle metric. The engine's own memory floor refused earlier runs mid-way on a busy Mac; each was rerun whole. The Linux gate in hasu's container is **green, exit 0** at the same head (`linux-final.log`, `check-linux exit 0 2026-10-27T07:05:03Z`): the same tests, goldens, pty rows, score, both gameplay gates and the censuses. Render means (release, quiet; `bench-after.txt`): Mac 173/162 µs at 80×24 rich/plain, 1262/1257 at 200×60 (cb04d 182/174, 1306/1296); Linux 258/243 and 1802/1798 (`bench-linux-after.txt`; cb04d 297/278, 2142/2138). Earlier heads' gates are kept beside: `linux-00278a5a.log`, `linux-first.log` (cd7e5022), `linux-final-c79544f4.log` lives on hasu; the Mac gates of those heads were green in their turn.

Plants, each a draft PR on a `cb05-plant-*` branch, the fix and its test committed first:

- cub#51 `cb05-plant-sawtooth` (ac5c54c2): a two-cell sawtooth every eight cells summed onto every branch shape: `test_cb05_no_branch_or_route_reverses_within_eight_cells` FAILED (trap(assert)); `--bends-audit` RED 350 reversals within 8 cells.
- cub#52 `cb05-plant-dens` (22e8a543): the split roots moved to row 150, fifty rows from the briar hollow: `test_cb05_two_dens_an_area_at_least_a_den_spacing_apart` FAILED (trap(assert)); `--den-spacing` RED seed 0 field 80 area 1.
- cub#53 `cb05-plant-ashen` (2c98cf3f): `ashen_move` no longer refuses the step outside `forest.in_town`: `test_cb05_an_ashen_never_chases_past_the_towns_edge` FAILED (trap(assert)).

All three are `FAILED (trap(assert))` locally by their named test (RULES §7, a module lane: the local red is the evidence; no CI dispatch); the orchestrator closes the drafts.

## Done-when

- [x] Bigger areas, per-area lengths, smooth shaped branches (a slow S, a hook, a loop, a 180° turn), Bramblehold's fork, second way to the boar's clearing and spurs; the bends, reachability, den, gate and doorway censuses over fifty seeds and both fields.
- [x] At most two dens an area, 110 route cells apart; retired dens as landmarks, their ids kept, the migration test.
- [x] Cinderwick between the Shingle and Bramblehold: the graph re-threaded, the Ashen, embers, single-file passages, yards with caches, the cold hearth.
- [x] Larkmeadow filled: landmarks, the burn, Quill's perch, foes in the band.
- [x] Every dead end rewards; the spur census.
- [x] Frame means hold; generation under 50 ms an area.
- [x] Item 8: R-cb05-5 (two pursuers, hearing 10/2, one pair in the first third) with the crossing census ten of ten at both fields; the block plan (94 of 97 cells at 80, 166 of 217 at 200, length 240, every census holding); the hitbox audit (sixteen of sixteen land, the body already the test); rows for all three; the pass in this note.
- [x] Tests, goldens at both tiers and sizes, the four pty rows, three plants, DESIGN/ART/PALETTE/KEYS, README in its own commit, this note, the lane audit.
- [ ] PR CI belongs to the orchestrator: read once, never waited on, never labelled.

Play (schema 4; add `--mute` for silence):

```sh
/Users/mfwolffe/lanes/cb05/cub-play-4a7cd345 --save /Users/mfwolffe/lanes/cb05/play.save --ghost-dir /Users/mfwolffe/lanes/cb05/play-ghosts
```

Mach-O arm64, SHA256 `08b40f93095773024c7469f50ac5b2020882d33a40740548d39f0fdb7d6645b2` (`play-binary.txt`); built from source head `4a7cd345` (the second pass, rebased onto cb04f and cb06: schema 5, the dens rule, the centred ledger, the opening), every later commit docs or evidence. The acceptance candidate. The earlier builds, `cub-play-cd7e5022` (the one the maintainer played) and `cub-play-c79544f4`, are kept beside it.

The lane audit and the PR are the final hand-back's. No engine requirement found: `lair` served every need (the pty, goldens, perf and container tools unchanged). Materialise this note on trunk after merge.
