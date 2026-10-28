#!/bin/bash
set -u
lane=/home/mfwolffe/lanes/cb11
repo="$lane/rebase-final"
echo $$ > "$lane/linux-rebase.pid"
echo "CB11_LINUX_REBASE_SOURCE $(git -C "$repo" rev-parse HEAD) START $(date -u +%FT%TZ)"
exec 9>/home/mfwolffe/lanes/kasumi-cores-4-7.lock
until flock -n 9; do
    echo "cb11 rebase waits for cores4-7 $(date -u +%FT%TZ)"
    sleep 30
done
export LAIR_CPUS=4-7 TMPDIR="$lane/tmp" CARGO_INCREMENTAL=0
run() {
    cd "$repo" || return 2
    .lair/tools/in-container tools/check-linux || return $?
    # in-container does not forward the caller's LAIR_PERF_SLACK.
    .lair/tools/in-container env LAIR_PERF_SLACK=1 tools/check-perf || return $?
}
run
status=$?
echo "CB11_LINUX_REBASE_EXIT $status $(date -u +%FT%TZ)"
echo "$status" > "$lane/linux-rebase.exit"
exit "$status"
