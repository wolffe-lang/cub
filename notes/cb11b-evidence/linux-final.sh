#!/bin/bash
set -u
lane=/home/mfwolffe/lanes/cb11b
repo="$lane/cub"
echo $$ > "$lane/linux-final.pid"
echo "CB11B_LINUX_SOURCE $(git -C "$repo" rev-parse HEAD) START $(date -u +%FT%TZ)"
exec 9>/home/mfwolffe/lanes/kasumi-cores-4-7.lock
until flock -n 9; do
    echo "cb11b waits for cores4-7 $(date -u +%FT%TZ)"
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
echo "CB11B_LINUX_EXIT $status $(date -u +%FT%TZ)"
echo "$status" > "$lane/linux-final.exit"
exit "$status"
