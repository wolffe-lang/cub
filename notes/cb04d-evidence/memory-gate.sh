#!/bin/bash
set -eu
export HOME=/Users/mfwolffe/lanes/cb04d/home
export TMPDIR=/Users/mfwolffe/lanes/cb04d/tmp
export CARGO_INCREMENTAL=0
mkdir -p "$HOME" "$TMPDIR"
while ! vm_stat | awk 'NR==1 {gsub(/[^0-9]/,"",$0); page=$0} /Pages free:|Pages inactive:|Pages speculative:/ {gsub(/[^0-9]/,"",$0); n+=$0} END {exit !(n*page >= 8*1024*1024*1024)}'; do
    printf '%s cb04d: waiting 180s for 8 GiB available memory\n' "$(date -u +%FT%TZ)"
    /bin/sleep 180
done
cd /Users/mfwolffe/lanes/cb04d/cub
exec "$@"
