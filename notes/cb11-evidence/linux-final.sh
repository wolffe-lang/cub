#!/bin/bash
set -u
lane=/home/mfwolffe/lanes/cb11
repo="$lane/final"
echo $$ > "$lane/linux-final.pid"
echo "cb11 Linux source $(git -C "$repo" rev-parse HEAD) START $(date -u +%FT%TZ)"
exec 9>/home/mfwolffe/lanes/kasumi-cores-4-7.lock
until flock -n 9; do
    echo "cb11 waiting for cores 4-7 $(date -u +%FT%TZ)"
    sleep 30
done
export LAIR_CPUS=4-7 TMPDIR="$lane/tmp" CARGO_INCREMENTAL=0 LAIR_PERF_SLACK=1
run() {
    cd "$repo" || return 2
    .lair/tools/in-container tools/check-linux || return $?
    .lair/tools/in-container tools/check-perf || return $?
}
run
status=$?
echo "CB11_LINUX_FINAL_EXIT $status $(date -u +%FT%TZ)"
echo "$status" > "$lane/linux-final.exit"
exit "$status"
