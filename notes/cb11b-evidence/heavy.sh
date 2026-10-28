#!/bin/bash
set -eu
lane=/Users/mfwolffe/lanes/cb11b
lock=/Users/mfwolffe/lanes/mac-build.lock
until mkdir "$lock" 2>/dev/null; do
    holder=$(cat "$lock/pid" 2>/dev/null || true)
    if [ -n "$holder" ] && ! kill -0 "$holder" 2>/dev/null; then
        rm -rf "$lock"
        continue
    fi
    echo "cb11b waits for Mac lock holder=$holder $(date -u +%FT%TZ)"
    sleep 30
done
echo $$ > "$lock/pid"
echo cb11b > "$lock/lane"
trap 'rm -rf "$lock"' EXIT
export TMPDIR="$lane/tmp" HOME="$lane/home" LAIR_LANE_HOST=nomad CARGO_INCREMENTAL=0
while :; do
    bytes=$(vm_stat | awk '/Pages (free|inactive|speculative):/ {gsub("\\.", "", $NF); s+=$NF} END {printf "%.0f", s*16384}')
    if [ "$bytes" -ge 8589934592 ]; then break; fi
    echo "cb11b waits for8GiB $bytes $(date -u +%FT%TZ)"
    sleep 30
done
echo "cb11b floor clear $bytes $(date -u +%FT%TZ)"
cd "$lane/cub"
"$@"
