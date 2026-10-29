#!/bin/bash
# cb16's Linux gauntlet on kasumi (run under kasumi-run.sh: cores 8-11, the
# flock): the clone brought to the pushed head named, then the game's
# tools/check-linux in the engine's container (the python tests, prepare-pty,
# the engine's check-linux: fmt, the checked tests, both builds, the
# selftest, the goldens, the pty rows; the native goldens, the score check,
# gameplay on both backends with cb16's npc rows, the memory gate), the perf
# pass at slack 1 (a FAILED line fails it), the hit census against the base.
# Every step's exit is read directly and printed as END <step> exit=N; the
# first nonzero step stops the run.
set -u
want=$1
lane=/mnt/steamlib/lanes/cb16
cd "$lane/cub" || exit 2
step() {
    name=$1
    shift
    echo "START $name $(date -u +%FT%TZ)"
    "$@"
    status=$?
    echo "END $name exit=$status $(date -u +%FT%TZ)"
    if [ "$status" != 0 ]; then
        echo "CB16_LINUX_GAUNTLET_EXIT $status at $name"
        exit "$status"
    fi
}
sync_head() {
    git fetch -q origin cb16 && git checkout -q -B cb16 origin/cb16 && git reset -q --hard "$want" &&
        [ "$(git rev-parse HEAD)" = "$want" ] && [ -z "$(git status --porcelain --untracked-files=no)" ]
}
perf() {
    .lair/tools/in-container env LAIR_PERF_SLACK=1 tools/check-perf > "$lane/logs/perf.log" 2>&1
    status=$?
    grep -a 'perf' "$lane/logs/perf.log" | tail -8
    if grep -aq FAILED "$lane/logs/perf.log"; then grep -a FAILED "$lane/logs/perf.log"; return 1; fi
    return "$status"
}
hits() {
    .lair/tools/in-container target/release/cub --hit-census > "$lane/logs/hit-linux.csv" || return 1
    sha256sum "$lane/logs/hit-linux.csv"
    sha256sum "$lane/logs/hit-linux.csv" | grep -q ^53234a37bb94711dddbc1d4d84a0c6e5fa1579f96f45b0734a7e92931e340055
}
step head sync_head
step check-linux .lair/tools/in-container tools/check-linux
step perf-slack-1 perf
step hit-census hits
echo "CB16_LINUX_GAUNTLET_EXIT 0 at $(git rev-parse HEAD) $(date -u +%FT%TZ)"
