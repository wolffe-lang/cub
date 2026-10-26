#!/bin/bash
set -u
lane=/Users/mfwolffe/lanes/cb04d
cd "$lane/cub"
echo $$ > "$lane/mac-final.pid"
echo "cb04d Mac source 389848a start $(date -u +%FT%TZ)"
run_gate() {
    bash "$lane/heavy.sh" .lair/tools/check-fmt &&
    bash "$lane/heavy.sh" .lair/tools/test &&
    bash "$lane/heavy.sh" .lair/tools/build --all &&
    printf '389848a\n' > target/cb04d-build-head.txt &&
    bash "$lane/heavy.sh" target/release/cub --selftest &&
    bash "$lane/heavy.sh" .lair/tools/goldens &&
    bash "$lane/heavy.sh" .lair/tools/goldens --bin target/native/cub &&
    bash "$lane/heavy.sh" python3 -I tools/score-check &&
    bash "$lane/heavy.sh" python3 -I .lair/tools/pty --bin target/release/cub &&
    bash "$lane/heavy.sh" python3 -I tools/gameplay.py --bin target/native/cub &&
    bash "$lane/heavy.sh" python3 -I tools/gameplay.py --bin target/release/cub &&
    bash "$lane/heavy.sh" env LAIR_PERF_SLACK=1 .lair/tools/perf --bin target/release/cub &&
    bash "$lane/heavy.sh" env LAIR_PERF_SLACK=1 python3 -I .lair/tools/perf-idle --bin target/release/cub
}
run_gate
status=$?
echo "MAC_FINAL_EXIT $status $(date -u +%FT%TZ)"
echo "$status" > "$lane/mac-final.exit"
exit "$status"
