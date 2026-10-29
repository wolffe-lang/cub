#!/bin/bash
# cb17's Linux gauntlet on kasumi, cores 4-7 under their flock (a printing
# wait, never a kill): the clone brought to origin/cb17's head, then CI's
# Linux leg in the engine's container (tools/check-linux: the python tests,
# the pty fixtures, the engine's check-linux with fmt, the checked tests,
# both builds, the selftest, the goldens and every pty row, the native
# goldens, score-check with its scene schedules and sound-on memory row,
# gameplay on both backends, the memory gate), then CI's perf job
# (tools/check-perf at slack 3, its default, passed inside the container).
# The wrapper STOPS at the first nonzero step and prints every step's
# `END <step> exit=N`; a perf line saying FAILED fails the perf step even
# when the tool exits 0. The marker holds the gauntlet's exit.
#   setsid -f bash kasumi-gauntlet.sh   (pid file, log and marker below)
set -u
lane=/mnt/steamlib/lanes/cb17
logs=$lane/logs
marker=$lane/gauntlet.exit
mkdir -p "$logs" "$lane/tmp"
rm -f "$marker"
echo $$ >"$lane/gauntlet.pid"
echo "cb17 gauntlet start $(date -u +%FT%TZ) pid $$"
exec 9>/home/mfwolffe/lanes/kasumi-cores-4-7.lock
until flock -n 9; do
    echo "cb17 waits for cores 4-7 $(date -u +%FT%TZ)"
    sleep 30
done
echo "cb17 holds cores 4-7 $(date -u +%FT%TZ)"
export LAIR_CPUS=4-7 TMPDIR="$lane/tmp" CARGO_INCREMENTAL=0
cd "$lane/cub" || { echo 2 >"$marker"; exit 2; }
git fetch -q origin cb17 || { echo 2 >"$marker"; exit 2; }
git checkout -q --detach FETCH_HEAD || { echo 2 >"$marker"; exit 2; }
echo "cb17 source $(git rev-parse HEAD)"
sh tools/fetch-lair >"$logs/fetch-lair.log" 2>&1 || { echo 2 >"$marker"; exit 2; }
step() {
    name=$1
    shift
    started=$(date +%s)
    "$@" >"$logs/$name.log" 2>&1
    s=$?
    if [ "$name" = perf ] && [ "$s" = 0 ] && grep -aq FAILED "$logs/$name.log"; then
        grep -a FAILED "$logs/$name.log" | cut -c1-200
        s=1
    fi
    echo "END $name exit=$s elapsed=$(($(date +%s) - started))s $(date -u +%FT%TZ) | $(tail -1 "$logs/$name.log" | cut -c1-150)"
    if [ "$s" != 0 ]; then
        echo "$s" >"$marker"
        echo "CB17_LINUX_GAUNTLET_DONE exit=$s at $name $(date -u +%FT%TZ)"
        exit "$s"
    fi
}
step prepare-pty .lair/tools/in-container python3 -I tools/prepare-pty
step check-linux .lair/tools/in-container tools/check-linux
step perf .lair/tools/in-container env LAIR_PERF_SLACK=3 tools/check-perf
echo 0 >"$marker"
echo "CB17_LINUX_GAUNTLET_DONE exit=0 $(date -u +%FT%TZ)"
