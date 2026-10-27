#!/bin/bash
# cb07 Mac gate: the whole local gate behind the 8 GiB vm_stat gate, one job at a time.
set -u
lane=/Users/mfwolffe/lanes/cb07
cd "$lane/cub" || exit 2
rm -f "$lane/mac-final.exit"
echo $$ > "$lane/mac-final.pid"
head=$(git rev-parse HEAD)
echo "cb07 MAC head=$head start=$(date -u +%FT%TZ)"
run_gate() {
    test -z "$(git status --porcelain)" &&
    bash "$lane/heavy.sh" .lair/tools/check-fmt &&
    bash "$lane/heavy.sh" .lair/tools/test &&
    bash "$lane/heavy.sh" .lair/tools/build --all &&
    printf '%s\n' "$head" > target/cb07-build-head.txt &&
    bash "$lane/heavy.sh" target/native/cub --selftest &&
    bash "$lane/heavy.sh" target/release/cub --selftest &&
    bash "$lane/heavy.sh" target/release/cub --strike-census > "$lane/logs/strike-mac-release.txt" &&
    bash "$lane/heavy.sh" target/native/cub --strike-census > "$lane/logs/strike-mac-native.txt" &&
    cmp "$lane/logs/strike-mac-release.txt" "$lane/logs/strike-mac-native.txt" &&
    bash "$lane/heavy.sh" target/release/cub --hud-census > "$lane/logs/hud-mac-release.txt" &&
    bash "$lane/heavy.sh" .lair/tools/goldens &&
    bash "$lane/heavy.sh" .lair/tools/goldens --bin target/native/cub &&
    bash "$lane/heavy.sh" python3 -I tools/score-check &&
    bash "$lane/heavy.sh" python3 -I .lair/tools/pty --bin target/release/cub &&
    bash "$lane/heavy.sh" python3 -I .lair/tools/pty --bin target/native/cub --rows cb07-strikes &&
    bash "$lane/heavy.sh" python3 -I tools/gameplay.py --bin target/native/cub &&
    bash "$lane/heavy.sh" python3 -I tools/gameplay.py --bin target/release/cub &&
    bash "$lane/heavy.sh" env LAIR_PERF_SLACK=1 .lair/tools/perf --bin target/release/cub &&
    ! grep -q FAILED target/perf/summary.txt &&
    bash "$lane/heavy.sh" env LAIR_PERF_SLACK=1 python3 -I .lair/tools/perf-idle --bin target/release/cub
}
run_gate
rc=$?
if [ "$rc" = 0 ]; then shasum -a 256 target/release/cub || rc=$?; fi
echo "MAC_FINAL_EXIT $rc $(date -u +%FT%TZ)"
echo "$rc" > "$lane/mac-final.exit"
exit "$rc"
