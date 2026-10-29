# The score

cub's music is original: twenty-five parts written for the game in the part format the engine reads (pax's
`notes/px32-format.md`; lair's `docs/SOUND.md`), committed as text under `score/` and carried inside the
binary (`tools/score-embed` writes `src/score/parts.lu`; `src/score_test.lu` holds the two equal). Nothing
is sampled, quoted or borrowed; no public-domain piece is used. The engine's mixer (lair, lr01) renders
every part to 48 kHz stereo PCM; the goldens under `tests/goldens/score/` pin the bytes on both hosts and
both compiler backends (`tools/score-check`).

| machine | how the music sounds | gate |
|---|---|---|
| macOS arm64 | each part rendered once to a WAV at start (`~/.cub/sound/`, about a second), the current cue's WAV played by `/usr/bin/afplay`, a child of the game ended when the cue changes | the `sound-live` pty row: afplay appears as the game's child and is gone with it |
| Linux x86-64 | the same WAVs; `paplay` where it is installed, else the refusal `player_missing: paplay` once on stderr before the terminal opens and a silent game | the `sound-live` row in the container (the WAVs are the sink), `sound-oss` names the OSS stub's refusal |
| PAX | the OSS stub (`oss_ioctl_unsupported`) until wolf-std grows an ioctl adapter; `/dev/dsp` is cb05's with gm01 | — |

## The parts

Every length is exact bars at the tempo, so a loop restarts on its own downbeat; the last beat of a loop
is a rest, so the release tails finish before the restart (`tools/score-check` holds the last tick under
-42 dBFS). `cub --score-list` prints the table's lengths from the parts themselves.

| cue | title | tempo and meter | length | parts | what it is |
|---|---|---|---|---|---|
| `title` | The Ford at Dawn | 72, 4/4, 6 bars | 20 s | horn, two strings, harp | The pack's call in D minor, a horn over sustained strings and a harp's eighths, lifting to F and settling back: the crossing's music until the first crack. |
| `shingle` | Gravel and Slack Water | 60, 4/4, 6 bars | 24 s, loops | flute, harp, two strings | A minor, open and slow: a harp ripple under a flute's two-note breaths, the strings a pedal that moves to G and F and home. The Shingle's part. |
| `bramblehold` | Under the Thorn | 100, 4/4, 10 bars | 24 s, loops | strings, clarinet, timpani, drum | D minor with a raised E flat: low tremolo strings, a clarinet that answers in short phrases, a timpani and a drum that never fall on the same beat. Bramblehold's part. |
| `larkmeadow` | Larks over Long Grass | 120, 3/4, 16 bars | 24 s, loops | oboe, strings, harp | F major, a lilt in three: an oboe line over strings and a harp that walks the triad, the second half answering the first. Larkmeadow's part. |
| `boss-boar` | Bristle | 120, 4/4, 8 bars | 16 s, loops | drum, timpani, trombone, strings | The boar of the thicket: a drum's charge under a trombone that barks on D and B flat, the strings a tremolo wall. cb04 wires it. |
| `boss-lynx` | Claw in the Scree | 150, 3/4, 10 bars | 12 s, loops | strings, flute, cymbal, timpani | The lynx of the crags: high tremolo strings in G minor sliding a semitone, a flute's short cries, a cymbal on the third beat. cb04 wires it. |
| `boss-elk` | The Ford Runs High | 96, 4/4, 8 bars | 20 s, loops | horn, strings, trombone, timpani | The elk of the river: a broad horn line in C minor over tremolo strings, a trombone and a timpani under the first beats. cb04 wires it. |
| `boss-alpha` | The Shadow at the Old Den | 60, 4/4, 6 bars | 24 s, loops | organ pedal, choir, organ, tam-tam | The shadow alpha: a pedal D under a choir's open fifth that darkens to E flat, an organ that answers the pack's call in fragments, a tam-tam once. cb04 wires it. |
| `den` | Embers | 72, 3/4, 4 bars | 10 s, loops | harp, flute, strings | A den's rest: a harp settling on D, a flute that enters on the second bar, strings beneath. Plays while the cub rests. |
| `death` | Fallen | 60, 4/4, 1 bar and two silent | 12 s, once | strings, tam-tam, flute | The sting: a struck chord falling to nothing over a tam-tam, a flute's last four notes down to D. Plays once at a fall; the area resumes when it has sounded. |

| `crack` | A Footstep Too Light | 144, 4/4, 3 bars | 5 s, once | timpani, strings, harp | A low struck C/G-flat chord, a thinning string hold, then eighths quickening into sixteenths; ends as the cub drops. Original, not the death sting's notes. |
| `cinderwick` | The Cold Hearths | 72, 3/4, 8 bars | 20 s, loops | clarinet, harp, strings, bells | G Dorian: a clarinet's tune over a harp in three and low strings, a cracked bell struck twice. Cinderwick's part, the burnt town. cb17. |
| `stand` | Wind in the Pines | 60, 4/4, 6 bars | 24 s, loops | two strings, horn, flute | C Mixolydian: the wind in the strings, a tremolo swelling and falling every bar; the pack's call far off on a horn; a flute above the ridge. The Stand's part. cb17. |
| `burn` | Ash and a Single Reed | 80, 4/4, 7 bars | 21 s, loops | clarinet, drum, timpani | D Aeolian, dry: a clarinet alone with long rests, embers ticking in a drum, a charred trunk's timpani. The Burn's part. cb17. |
| `teeth` | The Marked Stones | 90, 4/4, 6 bars | 16 s, loops | two strings, timpani, horn, cymbal | A Phrygian: staccato strings on the ledge's edge, the pack's call worn into the stone on a horn (A, E, C, B flat, A), a high tremolo, scree on a cymbal. The Teeth's part. cb17. |
| `underteeth` | Drip | 50, 4/4, 5 bars | 24 s, loops | pedal, bells, harp, strings | D Aeolian, sparse and dripping: single drops on bells and a harp at uneven places in the bar, one echoed, the pedal's deep stone, wet stone held in the strings. The Underteeth's part. cb17. |
| `mere` | Still Water | 60, 4/4, 6 bars | 24 s, loops | harp, choir, strings, voice | B flat Lydian, still: the ripple's beat on a harp, a note a second as the ripple row moves a cell a second; voices in the mist; a pedal of black water. The Mere's part. cb17. |
| `shallows` | Grey Water Running | 108, 3/4, 12 bars | 20 s, loops | harp, two strings, horn | F major: the Ashwater's current in a harp's eighths under a long string line; in the second half a horn for the elk. The Shallows' part. cb17. |
| `hush` | The Hush | 60, 4/4, 6 bars | 24 s, loops | strings, choir, clarinet | D minor darkening to E flat: low strings, voices on an open fifth, the shadows' motif on a low clarinet. The Hush's part, after its wait. cb17. |
| `howe` | The Barrows | 72, 3/4, 8 bars | 20 s, loops | horn, choir, strings, bells, flute | D minor in three, an elegy: the shadows' motif on a horn for the alphas under the mounds, a standing stone's bell, a wisp's flute. The Howe's part to its fourth standing stone. cb17. |
| `gravehollow` | Under the Fallen Oak | 60, 4/4, 5 bars | 20 s, loops | strings, choir, organ, bells | D minor: the shadows' motif slowed on an organ over the roots' tremolo, voices on the fifth, a bell tolling twice. Gravehollow outside the fight. cb17. |
| `moonford` | Moonford at Dawn | 72, 4/4, 6 bars | 20 s, loops | horn, two strings, harp, choir, bells | The title's call returning in D major (D, A, F sharp, E, D), the harmony lifting through B minor and G to A; the pack's voices, a bell at dawn. The end's frames and its card. cb17. |
| `reveal` | The Whole of Thornmere | 90, 4/4, 3 bars | 8 s, once | strings, harp, horn, timpani, cymbal | F major: the strings rising in tremolo out of the Stand's wind, a harp's sweep, the pack's call whole on a horn as the names fade in. The lookout's reveal, held to its end. cb17. |
| `crossing` | Stone by Stone | 60, 4/4, 3 bars | 12 s, loops | harp, timpani, clarinet, strings | The Mere's key with the stones' beat: a staccato timpani each second (a stone sinks a beat after the step), the ripple doubled to eighths, a low reed, the ice's tritone in tremolo. The Mere between its causeways. cb17. |
| `walk` | To the Stone Mouth | 60, 4/4, 4 bars | 16 s, loops | drum, timpani, trombone, choir, strings | D minor: a slow tread on a muffled drum, the shadows' motif low in a trombone, voices rising toward the mouth. The Howe from its fourth standing stone to the stone mouth. cb17. |

**The key and the motif (cb17).** The bible's shared key is the one signature of B flat: the areas are its
modes (F major, D Aeolian, G Dorian, A Phrygian, C Mixolydian, B flat Lydian) beside cb03's A minor
Shingle; the boss themes are in the minor (D, G, C, D); Moonford is the title's D minor call turned to D
major. The shadows' motif, D, E flat, D and the A below, is the pack's call (D rising to A) turned down
through a darkened second; the Hush gives it to a clarinet, the Howe to a horn, the walk to a trombone,
Gravehollow to an organ at half speed, and the alpha's theme (cb03) darkens its choir's fifth to the same
E flat. The area parts sit at -38 to -42 dBFS RMS like cb03's (the Hush and the Underteeth the quietest).

**The bank (R-cb17-2 A).** The engine's mixer holds at most sixteen cues (`sound.mixer`); twenty-five
parts and the silence are twenty-six. The live sink plays WAVs and needs no mixer: it writes every part
(below). The deterministic sink builds each replay's mixer from the cues that replay's own scenes reach
(`score.scene_bank_with`; refused by name over sixteen): the mixer reads only cued slots, so the
six-second replay's bytes are what the whole bank made (`replay.pcm` unchanged). B, a lair change raising
the bound, moves the engine pin. **The prepare (R-cb17-3 A).** `score.write_wavs` reads every part first
(a part that does not parse writes nothing), then renders, writes and drops one part at a time in its own
region, so the start's peak is one part's PCM, not the bank's.

## The cue schedule (`src/score/score.lu`)

One schedule, two sinks. Each tick the game reads a scene (`score.scene_of`: the opening, a fall, the
end, the den, the boss, a moment of the area's ground, the area) and the schedule answers the cue to start,
if any; a fall wins over everything, then the opening, the end, the title, the den, a boss, a moment
(`score.moment_of`, cb17), the area:

| moment | cue |
|---|---|
| opening ticks 0–209 | `title`, continuing from the title screen when already playing |
| first crack, tick 210 | `crack` replaces the title on this same simulation tick; one-tick mixer fade (the shortest supported), live a cut |
| fall, ticks 360–509 | `silence`; the sting has ended, the river takes the cub |
| waking, tick 510 onward | `shingle`, through the blinks and into play |
| opening skipped | the area's cue immediately; `crack` is interruptible, unlike `death` |
| in an area | its part, looping: restarted when its length is up |
| an area change | the new area's part at once; in the mixer the old slot fades out as the new fades in (the part's `cue replace fade N`, 9 ticks for the areas), live a cut |
| a boss (`sim.boss_theme`, cb04) | its theme replaces the area's loop (the engine's replace fade is the duck); the area's loop returns when the boss falls |
| a fall | `death`, at once; it plays once and is never cut short, so the area's loop resumes at the den when it has sounded |
| the den (`r`) | `den`, looping while the cub rests; the area's loop on leaving |
| the end (`sim.SCENE_END`, the ford at dawn) | `moonford`, looping under the three frames and the card (the title's part before cb17) |
| the lookout's reveal (the Stand, `sim.revealing`, 60 ticks) | `reveal` at once; it plays its eight seconds to the end, held like the sting (only a fall cuts it), then the Stand's loop |
| the Mere between its causeways (local rows 61–163) | `crossing`, looping; the Mere's part on either causeway |
| the Howe from its fourth standing stone (local row 150) to the stone mouth | `walk`, looping; Gravehollow's part through the mouth |
| the Hush's entry while its cold den (den 6) is unlit | the silence for 300 ticks, then `hush` (R-cb17-1 A); once the den is lit, `hush` at once |
| `m` | the music off (the player's child ended); `m` again cues the scene's part afresh |

The first crack strikes at tick 210, the hold lasts through the freeze,
and the harp begins near the rapid-spread transition. The live sink's
usual cut is intentional here: the title must not soften the shock. The
mixer uses its minimum supported fade, one tick (33 ms); no engine change.
Mute and `CUB_SOUND=0` still prepare and play nothing. The new part's full
PCM digest, byte length and one-second PCM head are pinned on both hosts.

The deterministic sink is the engine's mixer: `cub --score-replay OUT` runs a fixed six-second scene
replay (the title, the Shingle, a den, the Shingle, the boar, a fall, the wake) through `sound.cue` and
`sound.tick`; `tests/goldens/score/replay.pcm` pins every fade and the sting's hold. The audible sink plays
WAVs: lr01's engine mixes prepared PCM but streams none, so a live transition is a cut where the mixer has a
fade (R-cb03-1 B). The lair follow-on that closes the gap is a streaming sink (lr02) or a cancel on
`sound.Output`.

## Off

`cub --mute`, or `CUB_SOUND=0` in the environment, renders nothing and starts no player. Replays and the
headless runs are silent. `CUB_SOUND_BACKEND` names a backend (`macos`, `linux`, `oss`); unset, afplay's
presence chooses. A missing player or the OSS stub refuses by name, once, before the terminal is entered,
and the game plays on without music. The closing line reports `sound on|off backend B answers 0|1
prepared N us starts K stops L cue NAME`.

## Evidence

```
cub --score-list                     every part, its length, whether it plays once
cub --score-render NAME OUT.pcm      a part's PCM at its own length (stereo S16_LE, 48 kHz)
cub --score-wav NAME OUT.wav         the same bytes in a WAV
cub --score-replay OUT.pcm           the schedule through the mixer, 180 ticks
cub --score-scene NAME OUT.pcm       a scene script through the mixer; its cues on stdout (cb17)
python3 -I tools/score-check         the goldens, the seams, the WAV header, the refusal, both backends
python3 -I tools/score-check --update   write the goldens afresh (the release binary)
```

The goldens are a sha256 and length per part with the part's first second of PCM (R-cb03-4 B: a whole
bank is about 26 MB), and the whole replay's PCM. cb17 added a script for every new part
(`score.scene_names`: its trigger from the scene before it, through the real schedule): each pins its cue
schedule as text (`scene-NAME.cues`, a `tick T cue NAME` line a cue) and its mixer's PCM by sha256 and
length (`scene-NAME.sha256`); `six` is the replay and renders `replay.pcm`'s bytes; the Hush's script is
silent from the Shallows' fade to its 300th tick. A part dropped from the bank turns its scene's cue into
the silence, a red golden by name. `score-check` also runs the memory probe over the real loop with every
part prepared (the OSS stub's silent backend), under the memory gate's 4096 bytes a tick.
