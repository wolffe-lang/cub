#!/bin/bash
set -u
lane=/Users/mfwolffe/lanes/cb04b
cd "$lane/cub" || exit 2
rm -f "$lane/mac-contact-final.exit"
echo $$ > "$lane/mac-contact-final.pid"
head=$(git rev-parse HEAD)
echo "cb04b MAC_REBASE head=$head start=$(date -u +%FT%TZ)"
rows=$(python3 -I -c 'import runpy; print(",".join(k for k in runpy.run_path("tests/pty_rows.py")["ROWS"] if k.startswith("cb04b-") or k.endswith("save-resume")))')
run_gate() {
    test -z "$(git status --porcelain)" &&
    bash "$lane/heavy.sh" .lair/tools/check-fmt &&
    bash "$lane/heavy.sh" .lair/tools/test &&
    bash "$lane/heavy.sh" .wolf-bin/wolf test --deny-warnings --nocapture --no-native-fallback --filter cb04b_ src &&
    bash "$lane/heavy.sh" .lair/tools/build --all &&
    printf '%s\n' "$head" > target/cb04b-build-head.txt &&
    bash "$lane/heavy.sh" target/native/cub --selftest &&
    bash "$lane/heavy.sh" target/release/cub --selftest &&
    bash "$lane/heavy.sh" .lair/tools/goldens &&
    bash "$lane/heavy.sh" .lair/tools/goldens --bin target/native/cub &&
    bash "$lane/heavy.sh" python3 -I tools/score-check &&
    python3 -I -m unittest discover -s tests -p '*_test.py' &&
    bash "$lane/heavy.sh" python3 -I tools/prepare-pty &&
    bash "$lane/heavy.sh" python3 -I .lair/tools/pty --bin target/release/cub &&
    bash "$lane/heavy.sh" python3 -I .lair/tools/pty --bin target/native/cub --rows "$rows" &&
    bash "$lane/heavy.sh" python3 -I tools/gameplay.py --bin target/native/cub &&
    bash "$lane/heavy.sh" python3 -I tools/gameplay.py --bin target/release/cub &&
    bash "$lane/heavy.sh" target/release/cub --motion-census > "$lane/logs/motion-rebase-after-mac.txt" &&
    cmp "$lane/logs/motion-rebase-after-mac.txt" "$lane/logs/motion-rebase-after-linux.txt" &&
    bash "$lane/heavy.sh" target/release/cub --motion-render > "$lane/logs/render-rebase-after-mac.txt" &&
    bash "$lane/heavy.sh" target/release/cub --fox-roll-census > "$lane/logs/fox-rebase-after-mac.txt" &&
    bash "$lane/heavy.sh" env LAIR_PERF_SLACK=1 .lair/tools/perf --bin target/release/cub &&
    ! grep -q FAILED target/perf/summary.txt &&
    bash "$lane/heavy.sh" env LAIR_PERF_SLACK=1 python3 -I .lair/tools/perf-idle --bin target/release/cub
}
run_gate
rc=$?
if [ "$rc" = 0 ]; then
    shasum -a 256 target/release/cub || rc=$?
fi
echo "MAC_CONTACT_FINAL_EXIT $rc $(date -u +%FT%TZ)"
echo "$rc" > "$lane/mac-contact-final.exit"
exit "$rc"
