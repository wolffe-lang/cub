Footprint: module

# cb17 — the missing soundtracks: a part for every area

Every area of Thornmere has its own part now, and so do the end and three moments of the ground: fourteen original
parts in the part format (`score/*.part`, the engine's reader), the cue schedule taught the end, the lookout's reveal,
the Mere's crossing, the Howe's walk and the Hush's wait (R-cb17-1 A), each part's PCM golden, a cue-schedule
golden per trigger, a sound census over the real walk, and the memory gate's budget held with every part loaded
(the second playtest's item 15). Game code, game-owned tests, tools, docs and goldens only: no engine, pin or CI
change.

Ledger: cb17 — fourteen parts (the Teeth, the Shallows, the Hush, Cinderwick, the Stand, the Burn, the Mere, the
Underteeth, the Howe, Gravehollow, Moonford, the reveal, the crossing, the walk; 269 s of music, 25 parts in all);
the end plays Moonford, not the title; `score.moment_of` reads the reveal, the crossing, the walk and the Hush's wait
from the ground; a replay's mixer holds only its own cues (R-cb17-2 A) and the live prepare renders one part at a
time (R-cb17-3 A: peak 270 MB → 50 MB on nomad); `--score-scene` and fifteen scene goldens; `--sound-census` over
cb14's walk, and a second's settle between an area's part and its moment (R-cb17-7 A); module; plant #83; final source `92793546`; the Linux gauntlet green at `35e561af` (check-linux 2485 s, perf at slack 3), every pty row
and score row on both tiers; the final gauntlets on both hosts at the PR head run detached (their pids, logs and
markers in the hand-back and below).

## Prediction

`49a69b4e` committed `notes/cb17-prediction.txt` before the first change, at trunk `ed180ef5`. What it said and what
held:

1. **The gaps** held exactly: ten areas without a part (the Teeth `crags`, the Shallows `river`, the Hush `old-den`,
   Cinderwick `cinderwick`, `none` for the Stand, the Burn, the Mere, the Underteeth, the Howe and Gravehollow), the end
   playing the title (`scene_of` read every nonzero scene as the title), no cue for the lookout's reveal, the Mere's
   crossing or the Howe's walk: fourteen parts, twenty-five with cb03's eleven, twenty-six cues with the silence.
2. **The mixer's sixteen** held: `sound.mixer` refuses a bank over sixteen, so `replay_pcm` over the whole bank would
   have exited 2. R-cb17-2 A implemented; the six-second replay is byte-equal (`replay.pcm` unchanged, and the new
   `six` script renders its very bytes on both tiers).
3. **Byte-equal** held: the eleven parts' goldens (`--update` rewrote all twenty-five from the release binary and git
   saw no change to cb03's and cb06's), `replay.pcm`, every frame golden on both tiers, the censuses. Moved, named:
   the score list (25 parts and the 15 scripts), `tools/score-check`'s listing, the `sound-live` row's WAVs (12 → 26),
   `src/score_test.lu`'s count and area rows, the README's score sentence, `docs/SCORE.md`, `docs/DESIGN.md`.
4. **The numbers**: 269 s of music added (predicted about 270), every part 8–24 s; every loop's last tick under the
   seam bar (the highest, the Shallows, 241 of 256); the live prepare on nomad's release build 0.46 s → 1.05 s
   (predicted about 1.1 s), the WAVs while the game runs 35 MB → 89 MB (predicted about 90). The memory gate's two
   muted rows unchanged under 4096 bytes a tick; the sound-on row under it too (`score-memory`), and the prepare's
   peak lower, as predicted, by more than expected: 270 MB → 50 MB (`notes/cb17-evidence/prepare-peak.txt`).
5. **R-cb17-1 A, the motif, Moonford, the plant** held as written: the Hush silent from the Shallows' fade to its
   300th tick (`score-hush`: ticks 55–344 of its script peak 0), the motif D, E flat, D, A in the Hush, the Howe, the
   walk and Gravehollow, Moonford the title's call in D major; the plant (the walk dropped from the bank) red by name
   in its scene's cue schedule and in four unit rows. Not predicted: the sound census (added for the contract's
   "sound census" row), the reveal's hold (R-cb17-4 A), and what the census found at once: the walker's sway across
   the fourth stone's row cued walk, howe, walk within eight ticks (`sound-census-before-settle.txt`, ticks 9389,
   9391, 9397), so a change between an area's part and its moment now settles for a second (R-cb17-7 A).

## Forbidden

Original music only: every part is written for cub in the engine's part format — nothing played, sampled, quoted or
borrowed, no public-domain piece; the motif and Moonford's call grow from cb03's own title. No engine (`lair`) change,
no pin, workflow, `.github/` or `tools/check*` change (the sound-on memory row lives in `tools/score-check` and
`tools/memory-probe.py`'s new `--sound-backend`, so `tools/check-memory` and the muted gate are untouched). No other
lane's file: cb16's and cb18's areas are read, never written (`score` reads `sim`, `forest` and `lands`; the census
drives `fight` and `walker` as cb14's walk does). No ruling decided: R-cb17-1 .. R-cb17-7 are recommendations the
lane implemented. Never labelled a PR, merged, tagged, created or closed an issue, edited `~/.claude` or the
planning repo, installed a package. No attribution or co-author trailers. **No audio played aloud on the Mac:**
every render went to a file; the sound-on runs used the OSS stub (it refuses by name and starts no player); the Mac
gauntlet ran every pty row but `sound-live` and `mute-key`, the two that start `afplay` on macOS (Linux and CI's
macOS leg run them).

The Mac worked under `~/lanes/cb17/` behind the shared lock (`/Users/mfwolffe/lanes/mac-build.lock`, `mkdir`, the
holder's pid checked, the 8 GiB `vm_stat` floor inside it: `notes/cb17-evidence/tools/maclock.sh`); the
maintainer's MLX server never touched. kasumi ran the Linux gauntlet on cores 4–7 under
`/home/mfwolffe/lanes/kasumi-cores-4-7.lock` (a printing wait, never a kill) in the engine's container
(`.lair/tools/in-container`, the cached `localhost/pack-ci:fbee7e864f7dbee6`), from a fresh clone under
`/mnt/steamlib/lanes/cb17/`, launched `setsid -f` with a pid file and a marker; no process group signalled.

## Inputs verified

Base cub trunk `ed180ef5` (cb14's note); the worktree `~/lanes/cb17/cub` on branch `cb17`; engine `74b89744` as
`lair.pin` names it (staged by `tools/fetch-lair`, `LAIR-REV` read); wolf 0.2.35 and std `2386522e` staged by
`.lair/tools/fetch-toolchain` on both hosts. Read before the first change: the contract and its 2026-10-29 addendum,
`the-rules.md`, the maintainer's notes (item 15), `the-proposals.md` §3 and §5, the bible §1, §2, §12, §14, §16,
`docs/SCORE.md`, `DESIGN.md`, `REPLAY.md`, every `score/*.part`, lair's `docs/SOUND.md` and `src/sound/` (the
mixer's bound), the notes cb03, cb06 and cb14, `sprints/RULES.md` §1–§10. README read and refreshed in its own
commit (`b0615273`).

**Rulings, recommended and implemented:**

- **R-cb17-1 A** (the contract's): the Hush's entry is the silence for 300 ticks while its cold den (den 6) is unlit,
  then the shadows' motif; once the den is lit, the motif at once (`score.MOMENT_HUSH_WAIT`, `HUSH_WAIT`). The
  journey's "first entry" is read from the den's lit bit, so it needs no new save field and holds across a resume. B,
  the motif at once, loses the Hush's one quiet entrance.
- **R-cb17-2 A** (new): a replay's mixer holds only the cues its own scenes reach (`score.scene_bank_with`, refused by
  name over sixteen); the live sink writes every part's WAV and needs no mixer. B, raising the engine's bound, moves
  the pin (cross-cutting); the lair need is below.
- **R-cb17-3 A** (new): `score.write_wavs` parses every part first (a bad part writes nothing), then renders,
  writes and drops one part at a time in its own region: the peak one part's PCM, not the bank's (270 MB → 50 MB). B,
  the bank held whole, scales with the music: about 650 MB at twenty-six cues (270 MB for 191 s; here 462 s).
- **R-cb17-4 A** (new): the reveal holds its eight seconds to the end like the sting (`score.holds`), only a fall
  cutting it; B, cut when the reveal's 60 ticks end, would need a two-second part or a cut mid-phrase.
- **R-cb17-5 A** (new): the walk is the Howe from its fourth standing stone (local row 150) to the stone mouth, about
  eight seconds at the trot; B, from the fifth stone (row 190), leaves four.
- **R-cb17-6 A** (new): the crossing is the whole water between the Mere's causeways (local rows 61..163), islands
  included; B, the stone rows only, would restart the part at every island.
- **R-cb17-7 A** (new, the census's finding): a change between an area's ground parts (the Mere's part and the
  crossing, the Howe's and the walk) sounds once it has held 30 ticks (`score.SETTLE`); an area change, a den, a
  boss, a fall, the reveal and the Hush's wait stay immediate. B, no settle, restarts a part whenever the cub
  sways across the line.

## The parts

One line each: what it is for, what it does. Lengths in ticks (30 a second); the motif is the shadows' (D, E flat, D,
the A below) unless named otherwise.

| part | for | length | what it does |
|---|---|---|---|
| `cinderwick` The Cold Hearths | Cinderwick, the burnt town | 600 | G Dorian in three at 72: a clarinet's tune over a harp's waltz bass and low strings, a cracked bell struck at bars 1 and 5. |
| `stand` Wind in the Pines | the Stand | 720 | C Mixolydian at 60: tremolo strings swell and fall every bar (the wind), the pack's call far off on a horn (C, G, E, D, C), a flute above. |
| `burn` Ash and a Single Reed | the Burn | 630 | D Aeolian at 80, dry: one clarinet with long rests, embers ticking as staccato drum taps, a charred trunk's timpani twice. |
| `teeth` The Marked Stones | the Teeth | 480 | A Phrygian at 90: a staccato string ostinato on A and B flat, the pack's call worn into stone on a horn (A, E, C, B flat, A), a high tremolo, scree on a cymbal. |
| `underteeth` Drip | the Underteeth | 720 | D Aeolian at 50, sparse and dripping: single drops on bells and harp at uneven places, one echoed, a low pedal, wet stone held in the strings. |
| `mere` Still Water | the Mere's causeways | 720 | B flat Lydian at 60: the ripple's beat on a harp, a note a second (the ripple row moves a cell a second), choir in the mist, a pedal of black water. |
| `shallows` Grey Water Running | the Shallows | 600 | F major in three at 108: the Ashwater's current in harp eighths under a long string line; a horn for the elk in the second half. |
| `hush` The Hush | the Hush, after its wait | 720 | D minor darkening to E flat at 60: low strings, voices on an open fifth, the motif on a low clarinet, then rising to F and back. |
| `howe` The Barrows | the Howe to its fourth stone | 600 | D minor in three at 72, an elegy: the motif on a horn for the alphas under the mounds, a standing stone's bell, a wisp's flute flicker. |
| `walk` To the Stone Mouth | the Howe's walk to the gate | 480 | D minor at 60: a slow tread on a muffled drum, the motif low in a trombone, voices rising toward the mouth. |
| `gravehollow` Under the Fallen Oak | Gravehollow outside the fight | 600 | D minor at 60: the motif at half speed on an organ over the roots' tremolo, voices on the fifth, a bell tolling twice; the alpha's theme replaces it in the fight. |
| `moonford` Moonford at Dawn | the end, the ford at dawn | 600 | The title's call in D major at 72 (D, A, F sharp, E, D), D–Bm–G–A–G A7–D under it, the pack's voices, a bell at dawn; loops under the frames and the card. |
| `reveal` The Whole of Thornmere | the lookout's reveal | 240, once | F major at 90: strings rising in tremolo out of the Stand's wind, a harp's sweep up five octaves, the pack's call whole on a horn as the names fade in; held to its end. |
| `crossing` Stone by Stone | the Mere between its causeways | 360 | The Mere's key at 60 with the stones' beat: a staccato timpani each second (a stone sinks a beat after the step), the ripple doubled to eighths, a low reed, the ice's tritone in tremolo. |

Levels: the area parts sit at −37 to −42 dBFS RMS beside cb03's −38 (the Hush and the Underteeth quietest, Moonford
and the reveal at the title's −34): `notes/cb17-evidence/levels.txt`. The shared key is B flat's signature (the
areas are its modes beside cb03's A minor Shingle); the bosses stay in the minor; Moonford turns the title's D minor
to D major.

## Evidence index

Commits, each its own chunk: `49a69b4e` the prediction; the fourteen parts one commit each (`59227291`'s successors,
`Add score/<name>.part: <title>`); `c057adb9` the embed; `ace68187` the score module (the parts, the moments, the
scene scripts, the per-scene bank, the one-at-a-time prepare); `45657ee2` `--score-scene` and the listing;
`222d4ded` the unit rows; `07ef26e5` the probe's `--sound-backend`; `e4a7b880` and `35e561af` score-check's rows;
`f8b61bdc` the `sound-live` WAVs; `bfa84c54` the goldens; `4e91c0b4` SCORE.md; `b0615273` README only; `e7e71a66`
DESIGN.md; `034852a4` the census; `5370f7e6` the settle; `1faa0637` its rows; `adf576bb` the crossing's and the walk's
scene goldens moved by it; `0b7e9385` the census in score-check; `3ce5e5bc` the docs; `92793546` README only; this
note and its evidence.

- **The rows.** `cub --score-list` prints every part with its length and every scene script with its ticks.
  `tools/score-check` on both tiers: the fifteen scene scripts' cue schedules and PCM first (`scene-<name>.cues`, a
  `tick T cue NAME` line a cue; `scene-<name>.sha256`), the Hush's silence (`score-hush`), the listing, every part's
  sha256, length and first second (`<name>.sha256`, `<name>.head.pcm`; 14 new, 2.7 MB), every loop's seam, the
  replay and `six` = `replay.pcm`, the WAV header, the refusal, then `score-memory`: the memory probe over the
  release binary's real loop with every part prepared (`CUB_SOUND_BACKEND=oss`, silent), seed 7, 4096 bytes a tick.
  The renders are byte-exact on both platforms and both backends: the Mac's goldens were written by the release
  binary and checked by the native one, kasumi's container checks the same files on both tiers
  (`gates/linux-35e561af-check-linux.log:2385..2501`, every part and scene `ok`).
- **The cue schedules per trigger** (`tests/goldens/score/scene-*.cues`): an area's entry (`cinderwick`, `stand`,
  `burn`, `teeth`, `underteeth`, `mere`, `shallows`, `howe`: the neighbour's part, then the area's at tick 45);
  `reveal` (stand, the reveal at 30, the Stand's loop again at 270: held past the reveal's 60 ticks); `crossing`
  (mere; the crossing at 75 and the Mere's part again at 165, each change settled 30 ticks); `hush` (shallows; the silence at 45, 105 … 285; the motif at 345; the den's
  rest at 405; the motif at once on leaving it lit at 450: the den's fade); `walk` (howe, the walk settled in at 75, gravehollow
  through the mouth at once at 135: the gate); `gravehollow` (walk, gravehollow, boss-alpha at 120, gravehollow at 180);
  `moonford` (gravehollow, moonford at 30); `six` (cb03's six seconds, unchanged).
- **The sound census** (`cub --sound-census`, `notes/cb17-evidence/sound-census.txt`, run by score-check): cb14's walk
  (its fixture, the way on Cinderwick … the Howe, with the Stand's lookout and the stone mouth into Gravehollow),
  9751 ticks, recorded and replayed through the schedule: `entries 12 ok, cues 30, reveal 1 crossing 2 walk 1`, every
  area's part on the tick it is entered (Cinderwick 548, Bramblehold 1645, the Stand 2808, Larkmeadow 3810, the Burn
  4671, the Teeth 5385, the Mere 6421, the Shallows 7290, the Howe 8918, Gravehollow 9661), the reveal at the lookout
  (3431, the Stand's loop again at 3671), the crossing over the water (6699, the Mere's part at 7126), the Hush silent
  from 8133 and its motif at 8433 (300 ticks), the walk from 9427 to the mouth. Before the settle the same census
  read `walk 2` with the chatter above.
- **The prepare** (`notes/cb17-evidence/prepare-peak.txt`): base `ed180ef5` peak 270,041,088 bytes, 0.47 s; cb17 peak
  50,151,424 bytes, 1.07 s, twenty-six WAVs, the OSS stub silent.
- **The plant** (draft #83, branch `cb17-plant-missing-part`, `e15fe924`: the walk dropped from
  `score.names`, base + a break the fix never contains): on the Mac, `notes/cb17-evidence/plant-mac.log:49`
  `AssertionError: score-scene walk/release FAILED: the cue schedule differs at line 2: 'tick 45 cue silence', golden
  'tick 45 cue walk'` (`END score-check exit=1`), and `wolf test: 17 passed; 4 failed` (`:27`):
  `test_cb17_every_area_and_moment_has_a_part_in_the_bank`, `test_cb17_every_scene_script_fits_the_mixer_and_cues_its_part`,
  `test_cb17_the_trigger_scripts_cue_in_order`, `test_cb03_every_part_parses_at_its_written_length`. No CI run
  dispatched for it (RULES §7, module).
- **The gauntlets.** At `35e561af` (every part, scene, test and tool but the census and the settle): Linux on kasumi
  cores 4–7 green (`gates/linux-35e561af-gauntlet.log`: prepare-pty, check-linux 2485 s — fmt, `wolf test: 570
  passed; 0 failed` (`check-linux.log:741`), both builds, the selftest, the goldens and every pty row with
  `sound-live` (26 WAVs, `:1266`) and `mute-key`, native goldens, score-check with `score-hush`, `score-memory` 300.1
  bytes a tick, gameplay on both backends, the memory gate — then perf at slack 3, latency median 13.5 ms).
  The Mac's run then (`gates/mac-pre-census.log`, every step `exit=0`, the pty rows but the two audible ones) was on
  a tree with the census half-written, so it is a signal, not the gate. The final gauntlets at the PR head, both
  detached, the wrappers stopping at the first nonzero step: Linux `/mnt/steamlib/lanes/cb17/logs/gauntlet.log`,
  marker `/mnt/steamlib/lanes/cb17/gauntlet.exit`, pid file `gauntlet.pid` beside it; the Mac
  `/Users/mfwolffe/lanes/cb17/mac-gauntlet.log`, marker `mac-gauntlet.exit`, pid file `mac-gauntlet.pid` beside it.
- **Tools** (scratch, kept for the record, never run by a gate): `notes/cb17-evidence/tools/` — `audition.lu` (the
  engine's reader and mixer over a part file, byte-equal to the binary's renders for all twenty-five), `analyze.py`
  (levels and seams), `setgain.py`, `peak.py`, `maclock.sh`, `mac-gauntlet.sh`, `rows.py`, `kasumi-gauntlet.sh`,
  `plant-run.sh`.

**Hooks named, not added** (the addendum: a cue needing another lane's hook is named here): **cb16**'s Ferryman poles
the cub across the Mere for 60 scent; if the raft moves the cub along the Mere's rows the crossing sounds by itself
(`score.moment_of` reads the row); if it carries the cub without moving it, a `sim` flag for the poled crossing is
the hook `moment_of` would read. **cb18**'s sentries at the stone mouth fight inside the walk's rows: the walk plays
over them (they are no boss), which is the design; a sentry theme would be a part and a `sim.boss_theme`-like hook.
**lair**: the mixer's sixteen-cue bound (`sound.mixer`) and the WAV sink's cut where the mixer fades (R-cb03-1 B) —
a streaming sink or a larger bound is lr02's.

**Issues to file** (not filed): cub — CI's macOS leg runs no `tools/score-check`, so the Mac's byte-exact score
goldens are only a local row (a `.github/` change, cross-cutting); cub — `tools/check` on macOS plays `afplay` aloud in
`sound-live` and `mute-key`, which the rule against audio on the Mac forbids a lane to run (a `--rows` filter or an
`afplay` volume flag in the row, the-rules.md to say which).

## Done-when

- [x] The gaps listed: ten areas, the end, three triggers (Prediction 1).
- [x] One original part per gap, in the shared key, the motif shared by the Hush, the Howe, the walk and Gravehollow,
      the Underteeth sparse and dripping, the Mere still with the ripple's beat, the Burn dry with a single reed, the
      Stand's wind in the strings, Moonford the title's call in the major; lengths, dynamics, the format's
      instruments.
- [x] The triggers wired: area entry, the gate (the walk to the stone mouth), the den's fade, the reveal, the
      crossing, the Hush's wait (R-cb17-1 A), the end; a `--score-scene` row for each part.
- [x] `--score-list` with every length; the PCM goldens byte-exact on both platforms and tiers; a cue-schedule golden
      per trigger; the sound census; the memory gate green with the new parts loaded.
- [x] The note, the plant red by name (#83), the census and its finding fixed (R-cb17-7 A).
- [ ] The full gauntlet on both hosts at the PR head: running detached at hand-back (Linux green at `35e561af`).
