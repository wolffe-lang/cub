#!/bin/bash
set -u
lane=/home/mfwolffe/lanes/cb11
repo="$lane/cadence-final"
echo $$ > "$lane/linux-cadence.pid"
echo "CB11_LINUX_CADENCE_SOURCE $(git -C "$repo" rev-parse HEAD) START $(date -u +%FT%TZ)"
exec 9>/home/mfwolffe/lanes/kasumi-cores-4-7.lock
until flock -n 9; do
    echo "cb11 cadence waits for cores4-7 $(date -u +%FT%TZ)"
    sleep 30
done
export LAIR_CPUS=4-7 TMPDIR="$lane/tmp" CARGO_INCREMENTAL=0
run() {
    cd "$repo" || return 2
    .lair/tools/in-container tools/check-linux || return $?
    .lair/tools/in-container env LAIR_PERF_SLACK=1 tools/check-perf || return $?
}
run
status=$?
echo "CB11_LINUX_CADENCE_EXIT $status $(date -u +%FT%TZ)"
echo "$status" > "$lane/linux-cadence.exit"
exit "$status"
