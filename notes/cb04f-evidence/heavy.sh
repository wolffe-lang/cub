#!/bin/bash
set -eu
export HOME=/Users/mfwolffe/lanes/cb04f/home TMPDIR=/Users/mfwolffe/lanes/cb04f/tmp
export LAIR_LANE_HOST=nomad CARGO_INCREMENTAL=0 CARGO_BUILD_JOBS=4
while :; do
    bytes=$(vm_stat | awk '/page size of/ {gsub("[^0-9]", "", $8); page=$8} /Pages (free|inactive):/ {gsub("\\.", "", $NF); sum+=$NF} END {printf "%.0f",sum*page}')
    echo "cb04f memory free+inactive=$bytes at $(date -u +%FT%TZ)"
    if [ "$bytes" -ge 8589934592 ]; then break; fi
    /bin/sleep 180
done
exec "$@"
