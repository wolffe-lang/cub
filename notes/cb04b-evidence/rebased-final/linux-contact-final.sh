#!/bin/bash
set -u
lane=/home/mfwolffe/lanes/cb04b
cd "$lane/cub" || exit 2
echo $$ > "$lane/linux-contact-final.pid"
echo "cb04b LINUX_REBASE head=$(git rev-parse HEAD) start=$(date -u +%FT%TZ)"
export LAIR_CPUS=0-3 CARGO_INCREMENTAL=0
flock /home/mfwolffe/lanes/kasumi-cores-0-3.lock taskset -c 0-3 .lair/tools/in-container sh -ec '
    tools/check-linux
    target/native/cub --selftest
    .wolf-bin/wolf test --deny-warnings --nocapture --no-native-fallback --filter cb04b_ src
    rows=$(python3 -I -c '\''import runpy; print(",".join(k for k in runpy.run_path("tests/pty_rows.py")["ROWS"] if k.startswith("cb04b-") or k.endswith("save-resume")))'\'')
    python3 -I .lair/tools/pty --bin target/native/cub --rows "$rows"
    target/release/cub --motion-census > target/cb04b-motion-after-linux.txt
    target/release/cub --motion-render > target/cb04b-render-after-linux.txt
    target/release/cub --fox-roll-census > target/cb04b-fox-after-linux.txt
    LAIR_PERF_SLACK=1 .lair/tools/perf --bin target/release/cub
    ! grep -q FAILED target/perf/summary.txt
    LAIR_PERF_SLACK=1 python3 -I .lair/tools/perf-idle --bin target/release/cub
'
rc=$?
echo "LINUX_CONTACT_FINAL_EXIT $rc $(date -u +%FT%TZ)"
echo "$rc" > "$lane/linux-contact-final.exit"
exit "$rc"
