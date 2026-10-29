#!/bin/bash
# cb17's Mac gauntlet, run inside maclock.sh (the shared lock held for the
# whole run, the 8 GiB floor read before it starts): tools/check's steps in
# order, each exit read directly, the pty rows without the two that play
# afplay aloud (rows.py says which and why). STOPS at the first nonzero step
# and prints every step's `END <step> exit=N`. The marker holds the exit.
#   nohup maclock.sh mac-gauntlet.sh > LOG 2>&1 & disown
set -u
lane=/Users/mfwolffe/lanes/cb17
marker=$lane/mac-gauntlet.exit
rm -f "$marker"
echo $$ >"$lane/mac-gauntlet.pid"
cd "$lane/cub" || { echo 2 >"$marker"; exit 2; }
echo "cb17 mac gauntlet source $(git rev-parse HEAD) branch $(git branch --show-current) $(date -u +%FT%TZ)"
mkdir -p target/test-home
export HOME="$lane/cub/target/test-home"
ROWS=$(python3 -I "$lane/rows.py" "$lane/cub") || { echo 2 >"$marker"; exit 2; }
echo "cb17 pty rows: $ROWS"
step() {
    name=$1
    shift
    started=$(date +%s)
    "$@"
    s=$?
    echo "END $name exit=$s elapsed=$(($(date +%s) - started))s $(date -u +%FT%TZ)"
    if [ "$s" != 0 ]; then
        echo "$s" >"$marker"
        echo "CB17_MAC_GAUNTLET_DONE exit=$s at $name $(date -u +%FT%TZ)"
        exit "$s"
    fi
}
step python-tests python3 -I -m unittest discover -s tests -p '*_test.py'
step prepare-pty python3 -I tools/prepare-pty
step check-fmt .lair/tools/check-fmt
step unit-tests .lair/tools/test
step build .lair/tools/build --all
step selftest target/release/cub --selftest
step goldens-release .lair/tools/goldens
step pty-rows python3 -I .lair/tools/pty --bin target/release/cub --rows "$ROWS"
step goldens-native .lair/tools/goldens --bin target/native/cub
step score-check python3 -I tools/score-check
step gameplay-native python3 -I tools/gameplay.py --bin target/native/cub
step gameplay-release python3 -I tools/gameplay.py --bin target/release/cub
step check-memory sh tools/check-memory target/release/cub
step perf .lair/tools/perf
step perf-idle python3 -I .lair/tools/perf-idle --bin target/release/cub
echo 0 >"$marker"
echo "CB17_MAC_GAUNTLET_DONE exit=0 $(date -u +%FT%TZ)"
