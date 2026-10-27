# cb04b — movement held and combat committed

_Materialised from the body of cub#55 at the merge (`3aa9736b`)._

Current publication head **3aa9736b93c13f25acb7ba7a08c72486bd8ffe24**. Fully gated source **c7bd48776ac7b0a66755c0f263b85d87e63bddcd**; only17 final evidence files follow it. Linux and Mac complete gates are green. Historical measurements remain below, followed by the integration receipts.

Held movement, Control sprint, committed directional combos, timed rally, growing HUD bars and the ruled roll. Rebased once onto95a4889d (cb04f, cb06 opening and cb05 seven-area forest); their slain masks, opening, Cinderwick, hazards and den drawings are retained. The five-section note is here for materialisation as `notes/cb04b-movement-and-combat.md`. The measurements and first gate receipts below are retained pre-integration evidence; the integration follow-up gives the new receipts.

## Prediction

`098fd3b1` committed `notes/cb04b-prediction.txt` before implementation; `a6a11f09` moved the engine pin separately before gameplay changes. The initial terrain instrument excluded the shore reeds; that window was corrected and rerun before tuning. The final instrument integrates60 production ticks per sampled cell, reanchoring position while retaining fractional residues to separate gait from collision. There are76,800 rows per run:50 seeds, fields80/200, both display tiers, present walkable terrain classes, eight headings and three gaits. It is not a claimed continuous playthrough.

| area | dry cardinal walk before → after, cells/s |
|---|---:|
| Shingle |8.7890625 →9.375|
| Bramblehold |8.7890625 →9.375|
| Larkmeadow |8.7890625 →9.375|
| Teeth |8.7890625 →9.375|
| Shallows, dry |8.7890625 →9.375|
| Gravehollow |8.7890625 →9.375|

Dry diagonal8.783592048→9.371926987; the remaining difference is finite trigonometric/fixed-point precision. Sneak4.3359375→4.6875; sprint14.0625→15. Visible shallow water halves walk/sprint:4.3359375→4.6875 and7.03125→7.5; sneak already uses half trot and is not halved again. Low-health normal-walk limp, turning and collisions retain their rules. No Bramblehold-specific cap was found. Warm Linux render means at80×24 rich: Bramblehold261.26→273.50µs, versus Shingle403.40→420.72; worst sampled full frame across all areas/sizes/tiers3546→3609µs. This does not reconstruct the unrecorded physical terminal's frame rate.

|14-tick continuous trial, cells|before|after|
|---|---:|---:|
|paw1 walk|4.1015625|4.375|
|paw1 sprint|6.5625|7|
|paw1 dodge/roll|3.1640625|10|
|paw10 walk|6.0703125|6.453125|
|paw10 sprint|9.6796875|10.28125|
|paw10 dodge/roll|3|13|

Old paw1's14-tick figure includes post-dodge walking. Clear cardinal rolls measure2560FP; diagonals±1810FP per axis, about9.99893 cells rather than√2 times the distance. Long-held pty chords measure at least30 actual ticks; their blocked travel is reported, not presented as clear-ground distance. The corrected combo has48 measured drawn offsets,8 aims×3 hits×2 tiers: first left, second right, third visibly forward. Rich uses signed subcell pixels, plain signed cell shifts; collision covers both drawings.

| boss | before wins by attempt | final wins by attempt | unparryable hits before→after |
|---|---|---|---:|
|boar|94 first,6 second|100 first|158→32|
|lynx|100 first|100 first|18→24|
|elk|100 first|96 first,2 second,2 fourth|2→2|
|alpha|100 first|100 first|0→0|

All400 worlds win within the unchanged five-budget limit, with zero arena breaches. Shortest observed parryable tells remain12/10/16/9 ticks. This is the expected-growth scripted fighter, not a human reaction-time claim; the accepted tactic correction is detailed below. The final113-script body census spans46,551 ticks; the100-world audit spans210,644. Both report overlap/contact-unreachable/foe-overlap0/0/0.


The controlled fox fixture starts at body contact and rolls inward, so escape distance cannot disguise timing. Before and after, at paw1 and10: false tell0, real windup16, strike28. No roll or an early roll at1 leaves health36/water1; a correctly timed roll at27 leaves52/2. The inward travel is intentionally body-blocked. The ordinary fox-feint journey is independently replayed by the gameplay gate.

## Forbidden

Original game code and drawings only; no other game's code/assets/text/music. No engine source, compiler/runtime, CI workflow, planning repository or user-configuration edits; the two lair pins are explicit dependencies. No packages, labels, merges, tags, releases or issue actions; no attribution trailers. Signal witnesses use pty input bytes, not signal scripts. The coordinator owns full-matrix and CI watching.

Earlier Linux gates used4–7; final gates use the reassigned12–15 flock/taskset and existing `localhost/pack-ci:fbee7e864f7dbee6` container. Mac compiler/game gates use the scripted8GiB free+inactive floor,180-second retries, and lane HOME/TMPDIR. The first Mac candidate built successfully but its full gate exposed the engine capture-model gap; the second build was explicitly authorised after lr04. Its completed gameplay stage exposed the elk-counter timeout; a further accepted-candidate build was authorised after the scoped elk fix passed Linux. Both blocked logs/captures are retained. The five clean plant worktrees were removed individually; the play worktree remains.

Disclosures: one accidental rsync attempted `/home/nonexistent` on the Mac; it was not repeated and that path was verified absent. One fixed-string archive transfer used ssh bash-c rather than bash-s. These were not gauntlet runs and changed no other checkout.

## Inputs verified

Base1eb0ab8 includes cb04f. Engine initially74bf5781 for lr03's sessions, finally **74b89744e8f8a4ed01539b2fe814daf819b9abfc**, pinned separately in `897aa61c`. Wolf0.2.35/cf0c13d, lupin0.1.56 (version line294d626; release revision28547b4), std2386522eb059cca5a84108562c2c0a0e72345d34 unchanged. Complete archive pairs were fetcher-verified on both hosts; release digests were read twice and retained. Contracts, four verbatim playtests, RULES1–10, predecessor notes and named design/art/key/palette documents were read. README read, refreshed in separate commits, current.

Recommendations implemented, with the two later rulings distinguished:
- **R-cb04b-1 A:** Ctrl-held arrows sprint until release or exhaustion,12 stamina/sec; c only rolls. Enhanced Ctrl+C remains interrupt, never roll; releases never act. The inferred fallback and its limitations are documented.
- **R-cb04b-2:** WALK_PERCENT198→211,+6.5657%, for the requested small increase; derived foe speeds remain tied to that constant. `--pace N` (`25..300` percent) adjusts player locomotion for experiments and is recorded, off the title.
- **R-cb04b-3, ruled:** `max(10,ceil(2*14*trot_at(paw)/256))` cells:10 at paw1,13 at paw10. Eight travel ticks use cumulative `d*(16t-t*t)/64`; six recovery ticks follow. Iframes10 at paw1,+1 at paw5,+1 at paw10, cap12. **The first two recovery ticks are protected at paw1**; four at paw10. The last four/two are vulnerable. Input at age14 is accepted without a fifteenth locked tick. Stamina18; exhausted rolls refused; substeps prevent tunnelling and each axis clips independently.
- **R-cb04b-4 A:** no-arrow roll uses facing; held arrows latch all eight aims. Unlocked facing follows the roll, locked facing tracks the target. Exact holds survive area entry without changing cb04f's encounter logic.
- **R-cb04b-5, accepted:** the census hands a boss's first windup to its dedicated fighter instead of letting the generic route walker fight it. It replans obstructed close approaches and stages outside the four-cell engagement fringe. The five-attempt, nine-tick and zero-breach limits are unchanged. The chase witness uses Ctrl and waits for a moving target to remain within its snap's reach; it does not widen the catch/distance limits.

Combo costs12/14/18; recovery6/8/12 after3 windup/2 active ticks. First/second bodies move¼ cell forward and½ cell aim-left/right, settling sideways during recovery; third commits two cells forward. The camera holds at commitment, and the clipped landing head shake remains. Rally lasts45 ticks (1.5s), with a linearly shrinking lost-health pool and per-hit cap `floor(8*remaining/45)`, clamped to available/missing health; it expires at45. Health is red, regainable health grey stipple/dots, stamina green. Bars use10 points/cell, rounded-up length capped30; rows1/3, numbers5, water6, den hint7. Stat1/10/40 bar/rally goldens cover80×24 and120×40 on both tiers.

Schema5 stays unchanged. Exact/modifier/release replay words are additive; after cb05's seventh area mask, numeric pace/witness events append at49/50 (48/49 in the pre-rebase six-area build), guarded by a slot-identity test covering all37 snapshot fields. The explicit empty-arena `--combat-witness` setup is recorded and disclosed; live/replay equality includes pace150. Physical-terminal key and glyph measurements remain unclaimed.

## Evidence index

- `6d43463e`: opt-in sessions and exact held input.
- `554cb566`, `7bf754b7`: pace/roll/rally and signed combat drawing.
- `1a537d94`, `d85ec66e`, `4fbe1c59`: live chords, schema/tick boundaries, fixed-point bars and clipped head shake.
- `53f6e0ca`, `ec0f4f43`: witnessed fighter/chase adaptation without relaxing limits.
- `7afd1788`, `1869387f`: regenerated playable journeys and frame goldens.
- `1edbce4f`: both blocked host logs, before the engine repair.
- `c28864a3`, `8dba5ae1`, `400c5dd1`: enhanced Control-C checked/pty red, repair, both-binary green and unchanged model-blocker evidence.
- `897aa61c`: repaired capture-model pin; no unknown-control assertion was weakened.
- `5466d801`, `f7af28cd`: approved elk-only alignment guard, named red/green regression, exact400-row comparison and before/after frames.

Tracked evidence is under `notes/cb04b-evidence/`: integrated `motion-before/after.txt.gz` and summaries, before/after area rendering and fox timing,48 `drawn-offsets`, golden added/removed paths, toolchain metadata, plant reds and host scripts/logs. The older `motion-before-native.txt.gz` is the historical one-tick probe, not the final integrated instrument. The unmodified-game baseline was c51a834 plus measurement-only code; its native/release outputs match.

Goldens: **4699 files,228 directories**;1720 paths added and216 removed relative to cb04f trunk, both sets retained. Path+NUL+bytes+NUL SHA256 **91cfd564404d2017a16e3d164fb17fad22a6c6eba68d4a82fee0961dbe291d2e**. Every combo age/aim, every straight/diagonal roll age and the scaled/rally bars are included. Fixed-width golden text intentionally keeps trailing cell padding; source whitespace and formatter checks are separate.

### Elk counter follow-up

The failed candidate897aa61c left elk15 unwon at both fields. All five2500-tick budgets expired with the player at88/88 health and the elk at358HP: a scripted-player stall, not a death or iframe/charge balance failure. The fighter is paw3 (a10-cell roll), not paw10. R4's latched eight-way facing exposed its blind forward-lunge assumption: at tick449 x latched aim64 while the target bearing was160; later misses aimed96/224. The correctly aligned lunge at978 was its sole42-point hit.

The approved correction is only the elk's stagger-counter choice: require the existing inclusive45-degree forward cone before x; otherwise use the existing held-direction bite or approach/turn. A real player must turn before a forward lunge too. Tick449 now chooses a bite aimed160, using the unchanged riposte rule. The player wins on the fourth budget at tick8667, health73. No roll, damage, timing, seed or limit changes. Before/after action449 and timeout/victory frames are under `elk-before-actions`, `elk-after-actions`, `elk-before-frames`, `elk-after-frames`; diagnostic instrumentation reproduced the original400 rows unchanged.

All300 non-elk rows remain byte-identical. Every other elk world's win-attempt count is unchanged; the coordinator accepted changed durations/hits from the general elk tactic. The74 changed rows are below. Duration is the successful budget's ticks;0 before means no win, not zero simulated time. Hits are the three attack counters.

| seed | field | attempts before→after | duration before→after | hits before→after |
|---:|---:|---:|---:|---|
|0|80|1→1|1007→840|0/0/0→0/0/0|
|0|200|1→1|1007→840|0/0/0→0/0/0|
|3|80|1→1|1151→834|1/0/0→0/0/0|
|3|200|1→1|1151→834|1/0/0→0/0/0|
|4|80|1→1|1222→968|0/0/0→0/0/0|
|4|200|1→1|1222→968|0/0/0→0/0/0|
|5|80|1→1|1513→1058|1/0/0→0/0/0|
|5|200|1→1|1513→1058|1/0/0→0/0/0|
|6|80|1→1|1290→1277|0/0/0→0/0/0|
|6|200|1→1|1290→1277|0/0/0→0/0/0|
|7|80|1→1|1413→1091|4/0/0→1/0/0|
|7|200|1→1|1413→1091|4/0/0→1/0/0|
|8|80|1→1|849→1068|1/0/0→0/0/0|
|8|200|1→1|849→1068|1/0/0→0/0/0|
|9|80|1→1|1615→888|0/0/0→0/0/0|
|9|200|1→1|1615→888|0/0/0→0/0/0|
|10|80|1→1|1099→713|3/0/1→1/0/0|
|10|200|1→1|1099→713|3/0/1→1/0/0|
|11|80|1→1|1086→671|1/0/0→0/0/0|
|11|200|1→1|1086→671|1/0/0→0/0/0|
|12|80|1→1|938→1157|0/0/0→0/0/0|
|12|200|1→1|938→1157|0/0/0→0/0/0|
|14|80|1→1|1180→1064|0/0/0→0/0/0|
|14|200|1→1|1180→1064|0/0/0→0/0/0|
|15|80|0→4|0→745|0/0/0→1/0/0|
|15|200|0→4|0→745|0/0/0→1/0/0|
|16|80|1→1|1268→767|1/0/0→0/0/0|
|16|200|1→1|1268→767|1/0/0→0/0/0|
|17|80|1→1|1370→940|0/0/0→0/0/0|
|17|200|1→1|1370→940|0/0/0→0/0/0|
|19|80|1→1|908→886|0/0/0→0/0/0|
|19|200|1→1|908→886|0/0/0→0/0/0|
|20|80|1→1|1920→1316|0/1/0→0/0/0|
|20|200|1→1|1920→1316|0/1/0→0/0/0|
|21|80|1→1|1423→1102|0/0/0→0/0/0|
|21|200|1→1|1423→1102|0/0/0→0/0/0|
|23|80|1→1|1618→1010|0/0/0→0/1/0|
|23|200|1→1|1618→1010|0/0/0→0/1/0|
|24|80|1→1|932→933|1/0/0→1/0/0|
|24|200|1→1|932→933|1/0/0→1/0/0|
|25|80|1→1|889→841|1/0/0→1/0/0|
|25|200|1→1|889→841|1/0/0→1/0/0|
|27|80|1→1|1118→1197|0/0/0→1/0/1|
|27|200|1→1|1118→1197|0/0/0→1/0/1|
|28|80|1→1|1243→842|0/0/0→1/0/0|
|28|200|1→1|1243→842|0/0/0→1/0/0|
|29|80|1→1|1050→980|1/0/0→0/0/0|
|29|200|1→1|1050→980|1/0/0→0/0/0|
|30|80|1→1|1859→1092|0/0/0→0/0/0|
|30|200|1→1|1859→1092|0/0/0→0/0/0|
|31|80|2→2|881→720|0/0/0→0/0/0|
|31|200|2→2|881→720|0/0/0→0/0/0|
|32|80|1→1|1191→1042|0/0/0→0/0/0|
|32|200|1→1|1191→1042|0/0/0→0/0/0|
|33|80|1→1|1218→790|1/0/0→0/0/0|
|33|200|1→1|1218→790|1/0/0→0/0/0|
|35|80|1→1|1576→751|0/0/0→0/0/0|
|35|200|1→1|1576→751|0/0/0→0/0/0|
|38|80|1→1|1065→880|1/0/0→0/0/0|
|38|200|1→1|1065→880|1/0/0→0/0/0|
|39|80|1→1|841→821|0/0/0→0/0/0|
|39|200|1→1|841→821|0/0/0→0/0/0|
|40|80|1→1|852→688|0/0/0→0/0/0|
|40|200|1→1|852→688|0/0/0→0/0/0|
|42|80|1→1|1354→933|1/0/0→0/0/0|
|42|200|1→1|1354→933|1/0/0→0/0/0|
|44|80|1→1|1468→1157|0/0/0→0/0/0|
|44|200|1→1|1468→1157|0/0/0→0/0/0|
|46|80|1→1|1461→850|1/0/0→0/0/0|
|46|200|1→1|1461→850|1/0/0→0/0/0|
|47|80|1→1|1163→1230|3/1/1→1/0/1|
|47|200|1→1|1163→1230|3/1/1→1/0/1|
|48|80|1→1|1559→1130|0/0/0→0/0/0|
|48|200|1→1|1559→1130|0/0/0→0/0/0|

Final complete gates ran at **f7af28cd051061c28f95c4925637bbfed20f5d90**; subsequent changes are accepted-evidence files only. Linux exited0 at2026-10-27T04:59:07Z; Mac exited0 at05:38:00Z. Logs are `linux-final.log` and `mac-final.log` in the evidence directory. Both hosts pass335 checked tests (zero failures/rejections/unsupported/SKIP),31 additional strict checked cb04b tests, both builds/selftests, all4699 golden files on both backends, PCM score,50 full release pty rows plus22 native cb04b rows, BOTH complete gameplay stages, all world/den/door/body/boss checks, and slack1 performance. The original agree-rich/agree-plain model blocker now passes without relaxing its assertion. Mac's release integrated motion census is byte-identical to Linux's.

Render means inµs,80×24 rich/plain and200×60 rich/plain: Linux292/279 and2068/2091; Mac168/158 and1170/1159. Direct latency median/p90: Linux14.1/33.4ms, Mac33.0/33.5ms, against40/70ms. Linux idle301 switches/10s; Mac loudly skips only the Linux `/proc` idle counter, twice. Mac memory waits remained180 seconds at the8GiB floor; none was bypassed. The final log records completion of release gameplay and performance after those waits.


Required draft plants (fixes/tests committed first; all local reds are named `FAILED (trap(assert))`, not compile rejection/unsupported rows):
- #41,c06ba595: `test_cb04b_release_resumes_held_direction`.
- #42,d9339d85: `test_cb04b_drawn_combo_north` (third leap).
- #43,471b0040: `test_cb04b_rally_expires_at_window_end`.
- #44,d0fc495c: `test_cb04b_roll_latches_held_direction_all_eight`.
- #45,4c40603d: `test_cb04b_roll_iframe_last_tick_misses_then_hit_lands`.

Each immediate plant CI lookup returned[]; the coordinator owns CI receipts and unmerged closure. No label or CI wait by this lane.

### cb05/cb06 integration and mute witness

Rebased once onto95a4889d. Kept cb05's Cinderwick thorn face, den silhouettes, ember hazards and seventh saved mask, cb06's complete opening and all their terminal rows. The held doorway regression now expects Cinderwick; a duplicate replay import introduced by the merge was removed. The first checked preflight recorded one failed assertion and one rejected file; the repaired full preflight passed361 tests, zero unsupported/rejected/failures/SKIP, both builds/selftests and complete frame regeneration. Those red/green logs remain under `notes/cb04b-evidence/rebase-preflight-*`.

The movement instrument, not gameplay, also needed integration: its old boolean table ended at terrain8, so cb05's ash9 caused a real bounds trap. It now collects kind ids as data and scans `forest.length(area)`, not the former160-row constant. A bounded three-row slice around a guaranteed town ember exercises that collector on the checked machine; the first whole-town checked test exhausted fuel and was not counted as passing. The full release command still covers50 seeds, both fields, both tiers, all eight headings and three gaits. All100,800 rows have blocked0; town gravel/ash/embers are covered, and every area's dry northward walk is4800FP over60 ticks (9.375 cells/s). The six continuous14-tick walk/sprint/roll distances are unchanged. `59965bc6` is the instrument/test repair; no speed, hazard, boss tactic or census limit changed.

Current goldens:5463 files in394 directories, no case directory added or removed relative to95a4889d;1792 files added and284 removed, both path sets retained. Path+NUL+bytes+NUL SHA256 `b349d614a61b7a0fa2b4200e678f4ae791fc01dab349991eefd4b327dd95cfcb`. The grown bars and town-lane frame were inspected after generation.

CI run40457618218's mute-key capture records both m keys at0/20 and starts1/stops2: the first key suppresses the initial cue before score.step, not a lost-key or restart defect. A controlled real-pty query-time injection reproduces those exact ticks and counts. The row now prepares an opening-complete save and waits for a complete playing trace after score.step. Original starts2 and0.6-second child-stop/restart checks remain; initial afplay, two ordered postzero m records and a stable playing scene are additionally required. The accepted pre-rebase binary passed the fixed row and a two-second delayed-launch driver. A driver withholding the second m fails the same starts2 assertion; this is not claimed as a score.restart code mutation. All captures, records and logs are retained under `notes/cb04b-evidence/mute-key/`.

The first complete regates at8e9acad6562fdb4b7ace251b6b8b993e04722d89 stopped in terminal rows before gameplay/performance; the failure and its repair are below. Linux uses the newly reassigned4–7 flock/taskset; only the lane's12–15 waiter834608 was stopped, never its holder. Mac remains behind8GiB free+inactive with180-second retries.

### Fresh fixtures and predecessor saves

Linux den-keys loaded a valid six-mask CUB5 fixture written by the pre-cb05 gate at04:47:01Z; it exited2 before entering the terminal. Reuse had stayed green while all writers used the same six-area shape, and a fresh CI checkout had no old save. Mac had the same stale engine.save and other shared test saves. Three retained real-pty reproductions show the EIO cause: save_corrupt exits2, then quit/ctrl-c's first write gets errno5; the trap row also exits2. No tools/pty helpers remained, and none was killed. The merged decoder is byte-identical to95a4889d.

`3d0d5a4c` gives fresh-journey rows separate save paths and archives the engine's fixed-name fixture before full gates; old saves and captures are preserved. Two unit tests verify archival bytes, unique missing save paths and artifact-readable permissions. Every original row assertion remains. No game, decoder, engine or CI workflow changed. The formerly failing rows passed on both hosts against the unchanged binaries.

Separate resume rows load actual saves written through a short pty journey by the supplied95a4889d and4a7cd345 binaries. Their binary and fixture hashes are in `tests/saves/provenance.json`; captures and writer logs are retained. Both fixtures pass both native/release backends on Linux and Mac, preserving seed137, played ticks, seen opening and all seven masks. Fixture isolation therefore does not replace compatibility coverage. The first resume probe correctly rejected an explicitly conflicting --seed7; the corrected normal resume command omits that flag.

Both complete reruns atd30823519944f300b340364ea1a857cfad0d4db5 passed the repaired terminal stage and then failed the unchanged ordinary parry assertion (Mac10:39:16Z; Linux10:39:20Z). Linux was reassigned0–3 after4–7 became occupied; only the lane's waiter1042371 was stopped.

### Defensive fixture contact and release latency

The widened approach leaves an isolated inferred Right alive after the newer Left expires. The generator then supplied ten empty-input ticks, which are not an immediate stop: the cub drifted out of the strike's reach. Both parry and unanswered-hit fixtures therefore witnessed a miss. The original trace applies Right at157, expires it at169, moves5FP at173, and stops at174. This is the designed fallback latency, not a permanently held key.

`e5f1e664` adds `src/inferred_stop_test.lu::test_cb04b_inferred_release_stops_after_last_repeat_within_eleven_ticks`. On the strict checked machine it pins exact expiry and speed-zero timing at default paw1 full-speed walk: at most11 ticks after a recognized inferred repeat,17 after a lone tap, followed by eight stationary ticks with zero obstacle stops. The inferred window is interval+1, maximum6 ticks, or12 for a lone tap; braking takes6 updates. A gap longer than13 ticks is classified as a new tap, so17 ticks is the general default-walk bound after the last legacy arrow byte. The pinned engine's `test_a_repeat_run_releases_one_interval_after_the_last_press` separately covers interval expiry. KEYS now states these simulation-tick bounds.

`64fb68b4` repairs only the fixture generator: ordinary aim arrows stay refreshed during the same10/16-tick waits. No numeric state injection, seed change, damage change, altered parry window, longer wait or relaxed assertion. Generation now rejects a missing stagger, damaged dodge or unanswered strike that misses. Both new defensive checked rows were first seen failing by name, then passed with zero rejection/unsupported. The complete ordinary gameplay check passes both backends. Only parry/dodge/weasel-retreat replays and their18 golden files changed. At177 the parry has health52 and foe phase4; the unanswered strike health32 and foe phase3; the roll health52. All5463 golden paths and394 directories remain, hash now `dca10a371a2eeb8b1e66ba22e237ecde999993af099dfd7c9db08f54a49e2921`.

Both integration gates at9a8ff80d97734ed57bfc469cb91368ba31d0e646 advanced through every boss/den/path/chase check, then failed cb05's first-bite audit. Those third-red logs are retained.

### First-bite audit input

The audit's last column is actual damage landed; gap and cone columns describe the pre-action stand, but its printed cub coordinates are post-action. It supplied `(-sin(h), cos(h))`: arrows away from the target, then Lock+Bite. The diagnostic proves every committed aim was h+128. That previously relied on lock overriding arrows, contrary to the accepted R4 held-direction contract.

`e2ab1f41` changes the audit input to `(sin(h), -cos(h))` and explicitly requires the committed aim to equal h. Changing only that input made all16 original touching/gap-one stands land. No placement, jaws, lean, hitbox geometry, damage, timing or gameplay code changed; cb08's independent placement work is untouched. The normal command still runs all16. Its strict checked regression is two complete eight-aim groups; the first unsharded test exhausted fuel after14 rows and was not counted as passing.

`5daed87f` independently requires exactly16 distinct aim/gap pairs and every landed value true, rather than trusting only the green marker. Missing, duplicated, missed and empty synthetic outputs all fail. All six Python tests pass. Both backends pass the full16-row command and every remaining world check; the raw opposite-aim/one-variable/checked receipts are under `notes/cb04b-evidence/hitbox-input/`. Goldens remain unchanged at hash `dca10a371a2eeb8b1e66ba22e237ecde999993af099dfd7c9db08f54a49e2921`.

### Final integration receipts

Both complete gates passed sourcec7bd48776ac7b0a66755c0f263b85d87e63bddcd: **Linux exit0 at2026-10-27T12:29:41Z**, **Mac exit0 at12:22:32Z**. Each passes367 tests with zero failures/rejections/unsupported/SKIP,37 additional strict checked cb04b tests, six Python tests, both builds/selftests, all frame and score goldens,74 full release pty rows plus24 native rows, both complete gameplay stages, all world audits including the complete16-contact matrix, and slack1 performance. No prior red was called a pass. Logs, scripts and a machine-readable summary are under `notes/cb04b-evidence/rebased-final/`.

The final body census covers196 scripts/111,519 ticks; the100-world audit covers230,700 ticks. Both retain overlap/contact-unreachable/foe-overlap0/0/0. In the seven-area world, boar wins98 first/2 second; lynx, elk and alpha100 first each. All400 worlds win inside the unchanged five-budget limit with zero breaches. Unparryable hits are70/36/4/0; shortest parryable tells12/10/16/9. These are the new world's results, not a claim that the pre-cb05 geometry's300 non-elk rows stayed identical through a world expansion. The four complete boss-census outputs (two backends/two hosts) are byte-identical, SHA256 `321eacf0c9ba42e66c2bdfa246fecf03a509e7cf19ed79e021ef9044ee9fb171`.

The final100,800-row motion outputs are byte-identical across hosts, SHA256 `4cc33353717b8915a0d6c50d35681df9c95059b4da48c71bc602ae2d83e0facb`. Final goldens remain5463 files/394 directories (196 cases×2 tiers, art, score), hash `dca10a371a2eeb8b1e66ba22e237ecde999993af099dfd7c9db08f54a49e2921`; the final gate did not change them.

Render averages inµs at80×24 rich/plain and200×60 rich/plain: Linux306/285 and2155/2138; Mac174/164 and1249/1233, all under the unchanged1000/4000µs bars. Final direct latency median/p90: Linux13.6/33.8ms, Mac32.3/34.4ms, below40/70ms. Linux idle301 switches/10s is within240–360. Mac loudly skips only the Linux /proc idle counter; its latency runs pass. All Mac compiler/game gates kept the8GiB free+inactive floor and180-second retries.

Current accepted Mac binary: `/Users/mfwolffe/lanes/cb04b/cub-play-c7bd4877`, SHA256 `cddf36e40127026c123a25e1ca71a4ee66496ff5756604a483662f4a32612f55`, verified against the completed gate and copied without replacing older candidates. For a fresh journey:

```sh
HOME=/Users/mfwolffe/lanes/cb04b/home TMPDIR=/Users/mfwolffe/lanes/cb04b/tmp /Users/mfwolffe/lanes/cb04b/cub-play-c7bd4877 --save /Users/mfwolffe/lanes/cb04b/play-seven.save --ghost-dir /Users/mfwolffe/lanes/cb04b/play-ghosts-seven
```

Existing seven-area saves written by95a4889d or4a7cd345 resume as independently witnessed above. The earlier six-mask test fixtures remain preserved, not silently rewritten. Publication/CI/audit receipts follow at closeout.

## Done-when

- [x] Exact held resumption/diagonals, fallback documentation, modifier sprint and all eight attack/roll aims.
- [x] Before/after area/terrain/heading/gait census, recorded debug pace, retained foe/overlap limits.
- [x] Physical left/right/forward combo, distinct costs/recoveries, measured drawn offsets and every-age goldens.
- [x] Time-bounded rally, grey regain bar, fixed-point stat-scaled bars, status/water clear ordering.
- [x] Ruled roll distance/profile, latched chords, wall/body stops, exact iframe and action-recovery boundaries, both-tier animation.
- [x] Five deliberate plants, enhanced-Control-C red/green, documented rulings and README.
- [x] Complete Linux and Mac final gates, both gameplay stages and performance; accepted Mac binary and unchanged cross-host goldens.
- [x] Elk15 timeout corrected within the unchanged census limits; all300 non-elk rows and other elk attempt counts retained.
- [ ] PR CI/full-matrix, final audit holds and merge belong to the coordinator; no label and no CI wait.

Pre-rebase candidate, retained for historical comparison:

```sh
HOME=/Users/mfwolffe/lanes/cb04b/home TMPDIR=/Users/mfwolffe/lanes/cb04b/tmp /Users/mfwolffe/lanes/cb04b/cub-play-f7af28cd --save /Users/mfwolffe/lanes/cb04b/play.save --ghost-dir /Users/mfwolffe/lanes/cb04b/play-ghosts
```

Mach-O arm64, built once at the accepted source headf7af28cd. SHA256 `ccad864728d57c62f854afc25bc437f430a61649b8850a3d69772bd5d9ef955b`. Add `--mute` for silence. Both full gate exit markers are0; a build stamp alone was not treated as gate completion.


No new issue to file beyond the repaired lair#22. The once-only final audit and immediate one-time CI result are reported at hand-back. Keep the Mac play binary/worktree for acceptance; retain target/pty and the blocked captures.


Pre-rebase publication head **59c7020116a2fc31e9dc903619e704ff3e2b0705**; its difference from the fully gated source headf7af28cd is accepted evidence only. The immediate, once-only CI read found run **40457072094**, `in_progress`; no CI wait or label followed.

Pre-rebase audit run once, direct exit1, last line **`AUDIT FAIL (footprint: cross-cutting)`**. All ancestry, footprint, attribution, five-section, cited-sha, head and orphan checks pass. Holds are CI still in progress/no green tier yet, the coordinator-owned full-matrix label, and the deliberately retained play worktree. Log: `/Users/mfwolffe/lanes/cb04b/logs/final-audit.log`.

### Current publication

Final head **3aa9736b93c13f25acb7ba7a08c72486bd8ffe24** was pushed with an explicit lease on the previous59c70201 head. Its only difference from fully gated sourcec7bd4877 is the17 final evidence files. The immediate, once-only CI lookup found **40506133165**, `queued`: https://github.com/wolffe-lang/cub/actions/runs/40506133165 . No CI wait or label followed. The current audit ran once, direct exit1; last line **`AUDIT FAIL (footprint: cross-cutting)`**. Ancestry, footprint, attribution, five sections, cited SHAs, PR head and orphan checks pass; the full-matrix label is present. Holds are the still-in-progress CI run/no completed green tier and the deliberately retained play worktree. Log: `/Users/mfwolffe/lanes/cb04b/logs/rebased-final-audit.log`. No audit rerun, label or CI wait followed.

