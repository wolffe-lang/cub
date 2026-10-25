#!/bin/sh
# heavy.sh — cb02b's wrapper for every heavy job on nomad (RULES §4): the
# script itself reads vm_stat and proceeds only with 8 GB free+inactive+
# speculative, waiting three minutes and retrying when short; then execs
# the command so no shell outlives it.
set -u
export TMPDIR=/Users/mfwolffe/lanes/cb02b/tmp
export LAIR_LANE_HOST=nomad
export CARGO_INCREMENTAL=0
mkdir -p "$TMPDIR"
attempt=0
while :; do
    free=$(vm_stat | awk '/page size of/ {gsub("[^0-9]","",$8); page=$8} /Pages (free|inactive|speculative)/ {gsub("\\.","",$NF); s+=$NF} END {printf "%d", s*page/1073741824}')
    if [ "$free" -ge 8 ]; then
        echo "heavy.sh: $(date '+%H:%M:%S') ${free} GB free+inactive+speculative; running: $*"
        exec "$@"
    fi
    attempt=$((attempt + 1))
    echo "heavy.sh: $(date '+%H:%M:%S') ${free} GB short of the 8 GB floor (attempt $attempt); waiting 180 s"
    sleep 180
done
