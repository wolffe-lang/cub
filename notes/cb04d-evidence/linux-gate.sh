#!/bin/bash
set -u
lane=/home/mfwolffe/lanes/cb04d
cd "$lane/cub"
echo $$ > "$lane/linux-final.pid"
echo "cb04d source 389848a start $(date -u +%FT%TZ)"
export LAIR_CPUS=4-7 CARGO_INCREMENTAL=0
flock /home/mfwolffe/lanes/kasumi-cores-4-7.lock taskset -c 4-7 .lair/tools/in-container sh -ec '
    .lair/tools/check-fmt
    .lair/tools/test
    .lair/tools/build --all
    target/release/cub --selftest
    .lair/tools/goldens
    .lair/tools/goldens --bin target/native/cub
    python3 -I tools/score-check
    python3 -I .lair/tools/pty --bin target/release/cub
    python3 -I tools/gameplay.py --bin target/native/cub
    python3 -I tools/gameplay.py --bin target/release/cub
    LAIR_PERF_SLACK=1 .lair/tools/perf
    LAIR_PERF_SLACK=1 python3 -I .lair/tools/perf-idle --bin target/release/cub
'
status=$?
echo "LINUX_FINAL_EXIT $status $(date -u +%FT%TZ)"
echo "$status" > "$lane/linux-final.exit"
exit "$status"
