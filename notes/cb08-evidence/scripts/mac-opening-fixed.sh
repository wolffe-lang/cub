#!/bin/bash
set -u
lane=/Users/mfwolffe/lanes/cb08
cd "$lane/cub" || exit 2
echo $$ >"$lane/mac-opening-fixed.pid"
export TMPDIR="$lane/tmp" LAIR_LANE_HOST=nomad HOME="$PWD/target/test-home"
echo "Mac opening fixed head $(git rev-parse HEAD) $(date -u +%FT%TZ)"
while :; do
    bytes=$(vm_stat | awk '/Pages (free|inactive|speculative):/ {gsub("\\.", "", $NF); s+=$NF} END {printf "%.0f", s*16384}')
    [ "$bytes" -ge 8589934592 ] && break
    echo "Mac opening waits for 8 GiB: $bytes $(date -u +%FT%TZ)"
    sleep 30
done
echo "Mac memory gate clear: $bytes bytes"
run() {
    python3 -I .lair/tools/pty --bin target/release/cub --rows opening-skip-00 || return $?
    python3 -I .lair/tools/pty --bin target/release/cub --rows opening-complete,opening-skip-00,opening-skip-01,opening-skip-02,opening-skip-03,opening-skip-04,opening-skip-05,opening-skip-06,opening-skip-07,opening-skip-08,opening-skip-09,opening-skip-10,opening-skip-11,opening-skip-12,opening-skip-13,opening-skip-14,opening-skip-15,opening-quit-due
}
run
rc=$?
echo "MAC_OPENING_FIXED_EXIT $rc $(date -u +%FT%TZ)"
echo "$rc" >"$lane/mac-opening-fixed.exit"
exit "$rc"
