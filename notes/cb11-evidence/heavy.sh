#!/bin/bash
set -eu
lane=/Users/mfwolffe/lanes/cb11
lock=/Users/mfwolffe/lanes/mac-build.lock
until mkdir "$lock" 2>/dev/null; do
    holder=$(cat "$lock/pid" 2>/dev/null || true)
    if [ -n "$holder" ] && ! kill -0 "$holder" 2>/dev/null; then
        rm -rf "$lock"
        continue
    fi
    echo "cb11 waits for Mac lock holder=$holder $(date -u +%FT%TZ)"
    sleep 30
done
echo $$ > "$lock/pid"
echo cb11 > "$lock/lane"
trap 'rm -rf "$lock"' EXIT
export TMPDIR="$lane/tmp" HOME="$lane/home" LAIR_LANE_HOST=nomad CARGO_INCREMENTAL=0
while :; do
    bytes=$(vm_stat | awk '/Pages (free|inactive|speculative):/ {gsub("\\.", "", $NF); s+=$NF} END {printf "%.0f", s*16384}')
    if [ "$bytes" -ge 8589934592 ]; then
        echo "cb11 memory floor clear $bytes bytes $(date -u +%FT%TZ)"
        break
    fi
    echo "cb11 waits for 8 GiB $bytes bytes $(date -u +%FT%TZ)"
    sleep 30
done
cd "$lane/cub"
"$@"
