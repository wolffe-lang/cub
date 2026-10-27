#!/bin/bash
set -eu
lane=/Users/mfwolffe/lanes/cb07
export HOME="$lane/home" TMPDIR="$lane/tmp" CARGO_INCREMENTAL=0 LAIR_LANE_HOST=nomad
export WOLF_STD="$lane/cub/.wolf-bin/std"
mkdir -p "$HOME" "$TMPDIR"
while ! vm_stat | awk 'NR==1 {gsub(/[^0-9]/,"",$0); page=$0} /Pages free:|Pages inactive:/ {gsub(/[^0-9]/,"",$0); n+=$0} END {exit !(n*page >= 8*1024*1024*1024)}'; do
    printf '%s cb07: wait180s for8GiB free+inactive\n' "$(date -u +%FT%TZ)" >&2
    /bin/sleep 180
done
printf '%s cb07:8GiB gate passed: %s\n' "$(date -u +%FT%TZ)" "$1" >&2
cd "$lane/cub"
exec "$@"
