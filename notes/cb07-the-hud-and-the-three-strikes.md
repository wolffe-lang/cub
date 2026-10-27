# cb07 — the HUD and the three strikes (M-CB4)

The three strikes made visible, the HUD reduced to health, stamina and scent with the bars flush on the map
and the scent as a big number in the bottom right corner; the Ashen's health and blow (item 3) wait on the
rebase onto cb05 the orchestrator announces. Base cub#55's head `59c70201` (branch `cb04b`: cb04f + cb04b,
without cb05 and cb06). Game code, game-owned tests, witnesses, censuses, docs and goldens only: no engine,
pin or CI change. `Footprint: module`.

## Prediction

`fdf6d92e` committed `notes/cb07-prediction.txt` before the first change. The instruments came next
(`d0fcb015`: `--strike-census`, `--hud-census`, `art.draw_actor`, `art.render_bare`) and ran on the
unchanged game before anything moved (`e35b0f29`, `notes/cb07-evidence/strike-before.txt`,
`hud-before.txt`); the same two ran at the end (`8508e1ed`, `strike-after.txt`, `hud-after.txt`).

**The strikes** (the centroid of the cub's drawn pixels against the standing drawing at the commitment
point, in cells along the aim and to its left; the rich tier's braille and block cells decoded to pixels,
two across and four down a cell, the plain tier's cells the same way).

| hit, aim east | predicted before | measured before (rich) | predicted after | measured after (rich) |
|---|---|---|---|---|
| 1 at its peak | 0.5 forward 0.5 left, one tick | 0.50 forward 0.50 left at age 3 only; 0.50 and 0.00 at ages 4-6 | 1 forward 1 left, ages 3-6 | 1.04 forward 1.00 left at every age 3-6, easing 0.50/0.50 at 8, 0.00/0.00 at 10 |
| 2 at its peak | the mirror | 0.50 forward 0.50 right at age 3 only | 1 forward 1 right, ages 3-6 | 1.04 forward 1.00 right at ages 3-6, 0.00/0.00 at 12 |
| 3 at its peak | 1 forward at 3, 2 from 4, and stays | 1.00 at age 3, 2.00 from age 4 to 16 | 2 forward, ages 3-8, home by 16 | 2.04 forward at every age 3-8, 1.14 at 12, 0.00 at 16 |
| 3's head | a cell across for one tick at 5 and one at 6 | shake -1 at 5, +1 at 6 | left 5-6, right 7-8, left 9-10, right 11-12, the head a cell out | as predicted; the shaken drawing paints 1-4 cells beyond the body at every swing age, none at 4 or 13 |

On a diagonal aim (north-east) the rich tier measured 0.35 forward 0.35 left before and 1.08 forward 1.03 left
after (hit 1), 2.14 forward after (hit 3); the plain tier shows whole cells on both axes: 1.00/1.00 and
2.00 on the cardinals, 1.41/1.41 and 2.83 on a diagonal, exactly, before as after (the plain tier rounded
cb04b's quarter and half cells up to whole cells already, for one tick). 656 rows an instrument run (8 aims
x 3 hits x every age x 2 tiers); `--strike-census` exits 1 if any row breaks the contract and none does
(`strike-census rows=656 broken=0`). The windup (ages 0-2) does not move on either tier.

**The HUD** (cells of the frame that differ from the frame drawn without the HUD).

| frame | predicted before | measured before | predicted after | measured after |
|---|---|---|---|---|
| 80x24, stat 1, scent 0 | 360 | 360 (both tiers, day and night, every stat and scent) | about 51 rich | 51 rich, 57 plain |
| 200x60, stat 1, scent 0 | 600 | 600 | the same as 80x24 | 51 rich, 57 plain |
| 80x24, stat 40, scent 1234, a rally | — | 360 | never a stray cell | 100 rich, 117 plain, 0 stray |

192 rows (2 tiers x 2 fields x day and night x 4 scent values x 3 stat levels x with and without a rally),
`stray=0` on every one (`hud-census rows=192 stray=0`). The count no longer depends on the field; it is
the two labels (13), the bar cells (13 at stat 1, 47 at stat 40), the water line (14 after a spring, 23
before), the `scent` label (5) and the digits (6 for a 0 on the rich tier, 13 plain).

**The Ashen**: the census waits on the rebase (item 3); the prediction stands in `cb07-prediction.txt`.

## Forbidden

Original game code, drawings and text only; no other game's code, art or text; no engine (`lair`) change,
no pin, workflow or CI change; the planning repository and `~/.claude` untouched. No label on any PR, no
merge, tag, release, issue filed or closed; no attribution trailers. The maintainer's MLX server was never
stopped; every Mac job ran behind the 8 GiB `vm_stat` gate (`heavy.sh`), one at a time, under the lane's
HOME and TMPDIR. Kasumi's jobs ran on cores 4-7 under the lock. Nothing of cb05's (the town, the swarm
rule, the Ashen) or cb06's (the opening) is touched here: item 3 follows the rebase.

Not in this pass, by the contract: movement, the roll, the rally rule, the world, the town's plan, the
opening.

## Inputs, verified

Base `59c70201` fetched as `origin/cb04b` and read twice (`git rev-parse origin/cb04b` and the PR's
`headRefOid`, identical). Engine `74b89744e8f8a4ed01539b2fe814daf819b9abfc` (`lair.pin`, staged by
`tools/fetch-lair` on both hosts, `LAIR-REV` read); wolf 0.2.35 (cf0c13d) with lupin 0.1.56 (294d626) and std
`2386522e` through `.lair/tools/fetch-toolchain`. Read: the contract, the maintainer's notes, RULES §1-10,
design.md §1, §2, §8, §19, DESIGN.md, KEYS.md, ART.md, GLYPHS.md, the notes cb01, cb04d, cb05 (on its lane
worktree) and cub#55's body (cb04b's note until materialised), cb04b's lane scripts for the hosts' shape.

The maintainer's words, verbatim, drove the three items: "Attack combos STILL aren't rendering. It should
attack forwards-left, forwards-right, then straight forwards with a head shake." — "Let's make the hud:
health, stamina, scent only. Scent reporting should just be a number and it should be bigger, and it should
be in the bottom right hand corner." — "Have the health and stamina be flush against the map background."

What a person sees at play speed (thirty ticks a second), aim east, from the keyboard:

- **Hit 1.** Space: the cub crouches for a tenth of a second, then jumps a whole cell up-and-right (forward
  and to its left), jaws open, and hangs there for four ticks (130 ms) before sliding back over the next
  four. On the rich tier the slide is in pixels; on the plain tier the body sits a cell out for the whole
  recovery and snaps home on the last tick.
- **Hit 2.** The mirror: a jump a cell down-and-right, held, and back.
- **Hit 3.** A leap two cells straight ahead, held for six ticks (200 ms), the head flicking up, down, up,
  down a cell at a time, each flick held two ticks, then the body sliding home over the last eight ticks.
  The ears-back, open-jawed snap is the pose for every peak; the rest of the recovery is the standing cub.

The hit cone and the reach follow the body, and a bite also reaches from the commitment point
(`sim.strike_reaches`): a foe the cub is touching is bitten although the lunge carries the body a cell
across the aim (cb03a's dead-ahead contact rows, every direction, still land), and a foe a cell further on
is bitten where the drawn jaws are.

Rulings, recommended and implemented, never decided:

- **R-cb07-1** (the Ashen's numbers): after the rebase; the recommendation stays 20 health / 14 blow.
- **R-cb07-2** (the bars' rails): **A, no rails** — implemented: two bare bars with their labels on the
  map; the empty part of each bar is a dim `─` track so the bar's length reads without a cap.
- **R-cb07-3** (new; the water line): the maintainer said "health, stamina, scent only" and the contract
  keeps `draw_water` in the draw order. Implemented: the water line (`Water 2/2  w drink`) stays, flush on
  the map on row 5 under the stamina bar, counted as a label in the census, because the charges are a
  mechanic the player must read and the `w` hint is the only place the key is taught. (A) keep it so;
  (B) drop it to the `--hud` debug line and teach `w` elsewhere. Recommend A; the play build decides.
- **R-cb07-4** (new; the plain tier's digit rows): the contract's 3x5 `#` font is five rows tall, and the
  three-row cap at 80x24 cannot hold on the plain tier with `#` cells and a legible font (a three-row `#`
  font confuses 2, 3 and 5). Implemented: five rows on the plain tier (rows 19-23 at 80x24), three on the
  rich. (A) keep the 3x5 font at five rows on plain; (B) a three-row plain font from `_|` strokes.
  Recommend A: the plain tier is the VT's and PAX's, and legibility there matters more than two rows.
- **R-cb07-5** (new; the field's width at four digits): the label beside three digits covers twelve
  columns at 80x24 on the rich tier (the cap); four digits cover fourteen. (A) accept the growth past
  999 (the field grows leftward as the digits grow, as the contract says); (B) drop the label at four
  digits. Recommend A.

## Evidence index

- `fdf6d92e`: the prediction, before the first change.
- `d0fcb015`, `e35b0f29`: the strike census and the HUD census (`src/combatproof`), `art.draw_actor`,
  `art.render_bare`; their runs on the unchanged game (`notes/cb07-evidence/strike-before.txt`,
  `hud-before.txt`).
- `5991a134`: `sim.strike_offset`, `strike_hold`, `strike_peak`, `combo_motion` toward the offset's point,
  `head_shake` over ages 5-12, `shake_cells` across the committed aim.
- `3adfa1c9`: the snap pose (`silhouette.cub_posed` pose 5), `motionart.shifted_shaken`.
- `0ead62d5`: `src/digits/digits.lu`, the two new quadrant blocks in `sprites.rich_code_points` and
  `docs/GLYPHS.md`.
- `92a40780`: `art.hud_plan`, `hud_claims`, `draw_hud` flush on the map, `draw_water` on row 5,
  `scent_row`/`scent_col`, the plain snap rows, `pose_of` 5.
- `ccec6b04`: the head-out measure (`out`), the scent goldens in the art study, the help lines.
- `7dea1b03`: `sim.strike_reaches` (a bite reaches from the commitment point as well as the drawn jaws).
- `f1d63d7b`, `75713282`, `0dc3a1f4`: `src/strike_test.lu`, `src/hud_test.lu`; cb04b's rows moved to the
  new HUD (`combo_draw_test`, `posture_test`, `art_test`, `den_integration_test`); cb04b's first-bite row
  rewritten to the whole-cell lunge (`feel_test`); cb04c's stamina-edge rows (`look_test`,
  `tools/gameplay.py`, the `level-look-after-c` pty row) hold the edge free of lettering instead of empty;
  the checked rows held to the step budget, the native census strict.
- `82365e21`, `49c5a9d9`: the `cb07-strikes` pty row.
- `2f8bd7fa`, `d38acd50`, `3113609e`: DESIGN.md, ART.md, KEYS.md; the README in its own commit.
- `8508e1ed`: the censuses after (`notes/cb07-evidence/strike-after.txt`, `hud-after.txt`).
- Goldens: TODO.
- Gates: TODO (Mac, Linux, logs).
- Plants: TODO.

## Done-when

- [x] Item 1: the three strikes whole cells, held, eased back; the snap pose on both tiers; the strike
  census with its witness rows and the pty row; goldens for every age of every hit at both tiers.
- [x] Item 2: the HUD reduced to health, stamina, scent; the bars flush on the map; the big scent number;
  the frame census with no stray cell; the scent goldens at both fields, both tiers, day and night.
- [ ] Item 3: the Ashen's health and blow, after the rebase the orchestrator announces.
- [ ] Item 4: gates on both hosts, the plants, the audit, the PR — TODO.
- [ ] The checkpoint: the play build `~/lanes/cb07/cub-play-<sha>` for the maintainer's eye.
