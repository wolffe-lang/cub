# The score

cub's music is original: eleven parts written for the game in the part format the engine reads (pax's
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

Named slots for cb04's areas, silent until their parts exist (the schedule cues the silence for them):
`crags`, `river`, `old-den` (`score.area_part` 3, 4, 5). The bank holds at most sixteen cues (the
engine's bound): eleven parts, the silence and three slots leave one.

## The cue schedule (`src/score/score.lu`)

One schedule, two sinks. Each tick the game reads a scene (`score.scene_of`: the opening, a fall, the
den, the boss, the area) and the schedule answers the cue to start, if any:

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
python3 -I tools/score-check         the goldens, the seams, the WAV header, the refusal, both backends
python3 -I tools/score-check --update   write the goldens afresh (the release binary)
```

The goldens are a sha256 and length per part with the part's first second of PCM (R-cb03-4 B: a whole
bank is about 26 MB), and the whole replay's PCM.
