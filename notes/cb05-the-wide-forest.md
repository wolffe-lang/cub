# cb05 — the wide forest

Bigger areas with smooth, shaped branches and a thicket with more ways through it; fewer, farther dens, the retired ones left standing as landmarks; Cinderwick, a burnt town between the Shingle and Bramblehold, with the Ashen in its lanes and yards; Larkmeadow filled; every dead end rewarded; the forest talking back in lore lines at its caches and marks. Game code, game-owned tests, witnesses, censuses, docs and goldens only: no engine, pin or CI change. `src/world/` is the engine's symlink and was not touched.

## Prediction

`9b706b77` committed `notes/cb05-prediction.txt` before the first implementation change, at trunk `7e2c6a77` (+ cb04d's note). The "before" rows were read on trunk's own generators by this lane's new instruments, run on hasu's container against the base (`notes/cb05-evidence/*-before.*`).

What the prediction said and what held:

- Seven areas, ten edges, per-area lengths 160/288/288/288/224/224/224 (R-cb05-2 A): held exactly.
- Dens 11 → 9, at most two an area, none within 110 route cells (R-cb05-3 A): held; the census walks the real tiles over fifty seeds and both fields: **least within an area 122, least onward 116** (predicted 110–140 within; the onward figure is the next area's first den from the previous area's last, through its portal). Dens 8, 9, 10 retired to landmarks, their ids kept in schema 4, a save whose last den is one of them wakes at the nearest kept den (the meadow's two both wake at the last warm hollow: at 288 rows both old rows lie nearer it than the grass nest; the prediction guessed one each).
- Foes per area (R-cb05-4 A): in every seed at both fields the Shingle 9 (unchanged), Cinderwick 16, Bramblehold 18, Larkmeadow 18, the Teeth 8, the Shallows 8, Gravehollow 9 (predicted 12–16 / 14–18 / 14–18 / 8–12 for the last three); every one at least 30 cells from a den (the world audit's `min_foe_cells` 30 over 700 rows).
- The bend census: the instrument postdates the generator it would have measured, so the sawtooth's "before" is cb04d's own per-ten figures and the maintainer's eye; after, **0 reversals** on every route and branch (fifty seeds, both fields; 7,676 counted turns, the town's lane 0). cb04d's per-ten jaggedness, which the prediction said would be no worse, fell in every area: Shingle 0.0895 → 0.0679, Bramblehold 0.1857 → 0.1046, Larkmeadow 0.1325 → 0.0572, the Teeth 0.1681 → 0.1000, the Shallows 0.1903 → 0.1028, Gravehollow 0.1699 → 0.1111; route width medians 7/9/9/7/9/9 → 7/9/9/7/9/11; the three worst routes 0.976/0.909/0.909 → 0.488/0.488/0.488 per ten.
- Generation under 50 ms an area at field 200: held on the Mac release build (the Shingle 17 ms, the thicket and the meadow 8, the Teeth, the Shallows and Gravehollow 3, the town 4; the native x86-64 build in hasu's container takes 63 ms on the Shingle, so the bar is held to the release build as the perf gate's are). Render means within +15 %: Mac release 174/164 µs at 80×24 rich/plain and 1264/1252 at 200×60 against cb04d's 182/174 and 1306/1296 (faster; the gate's own run under a loaded Mac read 254/242/1847/1733, inside the 1000/4000 bars at slack 1); latency median 11.9 ms, p90 33.5.
- Goldens: every in-level case moved; 23 new cases (the town's lanes at night at both sizes, fourteen landmarks, the four town witnesses); score goldens unchanged.

The prediction's one wrong guess beyond the meadow's wake: the town's lane. The prediction assumed the route meander would serve it; it cut house corners (the lane wanders five cells in a plot), and three censuses pull three ways on a street — the straight-run bar (no run over twelve), cb04d's jaggedness (no step out and back within three samples) and this lane's bends census (no opposite turns within eight cells). The lane that satisfies all three weaves on anchors every two plots, sits mid-cell at each apex, eases four rows into and out of it and slants straight between; the houses are placed by the lane's reach over their plot's rows, not by one row.

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

The whole Mac gate (`tools/check`) is **green, exit 0** at source head `cd7e5022` (`mac-final.log`, 2026-10-27T03:07Z–03:19Z): 292 checked tests (0 failed/rejected/unsupported, 0 SKIP lines), 530 golden case-tier rows and the art sheet, all 31 pty rows (the four new ones among them), the score check, both backends' gameplay/persistence/world/body/boss/den gates with the five wide censuses inside them, perf 254/242/1847/1733 µs under the 1000/4000 bars and the latency bars; the only SKIP is the Linux-only `/proc` idle metric. The engine's own memory floor refused the gate mid-run four times on a busy Mac (another lane's builds); each time it was rerun whole. The Linux gate in hasu's container at `cd7e5022` ran green through the same 292 tests, goldens, pty rows, score and both gameplay gates up to one assertion: the native (unoptimised) x86-64 build's generation of the Shingle at field 200 took 63 ms against the 50 ms bar (`linux-first.log`); the bar is the release build's, as the perf bars are, and the gate now says so; the rerun at the final head is `linux-final.log`.

Plants, each a draft PR on a `cb05-plant-*` branch, the fix and its test committed first:

- `cb05-plant-sawtooth`: a branch admitted with a sawtooth (a sixteen-row alternation summed onto the shape): `test_cb05_no_branch_or_route_reverses_within_eight_cells` and the bends census go red.
- `cb05-plant-dens`: the split roots moved to row 150, 47 rows from the briar hollow: `test_cb05_two_dens_an_area_at_least_a_den_spacing_apart` and `--den-spacing` go red.
- `cb05-plant-ashen`: `ashen_move` no longer refuses the step past the town's edge: `test_cb05_an_ashen_never_chases_past_the_towns_edge` goes red.

(Opened after the checkpoint; their PR numbers, heads and CI run ids are in the final hand-back.)

## Done-when

- [x] Bigger areas, per-area lengths, smooth shaped branches (a slow S, a hook, a loop, a 180° turn), Bramblehold's fork, second way to the boar's clearing and spurs; the bends, reachability, den, gate and doorway censuses over fifty seeds and both fields.
- [x] At most two dens an area, 110 route cells apart; retired dens as landmarks, their ids kept, the migration test.
- [x] Cinderwick between the Shingle and Bramblehold: the graph re-threaded, the Ashen, embers, single-file passages, yards with caches, the cold hearth.
- [x] Larkmeadow filled: landmarks, the burn, Quill's perch, foes in the band.
- [x] Every dead end rewards; the spur census.
- [x] Frame means hold; generation under 50 ms an area.
- [x] Tests, goldens at both tiers and sizes, the four pty rows, three plants, DESIGN/ART/PALETTE/KEYS, README in its own commit, this note, the lane audit.
- [ ] PR CI belongs to the orchestrator: read once, never waited on, never labelled.

Play (schema 4; add `--mute` for silence):

```sh
/Users/mfwolffe/lanes/cb05/cub-play-cd7e5022 --save /Users/mfwolffe/lanes/cb05/play.save --ghost-dir /Users/mfwolffe/lanes/cb05/play-ghosts
```

Mach-O arm64, SHA256 `3bfe3256d90d85520d4dee4bee0075b3dd4667b88941077611684c7b366276ed` (`play-binary.txt`); built from source head `cd7e5022`, every later commit docs, gates or evidence.

The lane audit and the PR are the final hand-back's. No engine requirement found: `lair` served every need (the pty, goldens, perf and container tools unchanged). Materialise this note on trunk after merge.
