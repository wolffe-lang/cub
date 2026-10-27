#!/bin/bash
set -u
lane=/home/mfwolffe/lanes/cb04b
cd "$lane/cub" || exit 2
rm -f "$lane/linux-final.exit"
echo $$ > "$lane/linux-final.pid"
echo "cb04b LINUX head=$(git rev-parse HEAD) start=$(date -u +%FT%TZ)"
export LAIR_CPUS=12-15 CARGO_INCREMENTAL=0
flock /home/mfwolffe/lanes/kasumi-cores-12-15.lock taskset -c 12-15 .lair/tools/in-container sh -ec '
    tools/check-linux
    .wolf-bin/wolf test --deny-warnings --nocapture --no-native-fallback --filter cb04b_ src
    rows=$(python3 -I -c '\''import runpy; print(",".join(k for k in runpy.run_path("tests/pty_rows.py")["ROWS"] if k.startswith("cb04b-")))'\'')
    python3 -I .lair/tools/pty --bin target/native/cub --rows "$rows"
    LAIR_PERF_SLACK=1 .lair/tools/perf --bin target/release/cub
    ! grep -q FAILED target/perf/summary.txt
    LAIR_PERF_SLACK=1 python3 -I .lair/tools/perf-idle --bin target/release/cub
'
rc=$?
echo "LINUX_FINAL_EXIT $rc $(date -u +%FT%TZ)"
echo "$rc" > "$lane/linux-final.exit"
exit "$rc"
