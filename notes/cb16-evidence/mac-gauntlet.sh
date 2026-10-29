#!/bin/bash
# cb16's Mac gauntlet, run inside heavy.sh (the lock held for the whole run,
# the 8 GiB floor checked at its start). Every step's exit is read directly
# and printed as END <step> exit=N; the first nonzero step stops the run. The
# full golden check is attempted at most three times when the engine's own
# floor refuses it (exit 3, the-rules.md's loaded-server rule). The pty rows
# run without sound-live and mute-key (the-rules.md since planning 46518b2:
# they start afplay aloud; CI's macOS job runs them).
set -u
want=$1
cd /Users/mfwolffe/lanes/cb16/cub || exit 2
step() {
    name=$1
    shift
    echo "START $name $(date -u +%FT%TZ)"
    "$@"
    status=$?
    echo "END $name exit=$status $(date -u +%FT%TZ)"
    if [ "$status" != 0 ]; then
        echo "CB16_MAC_GAUNTLET_EXIT $status at $name"
        exit "$status"
    fi
}
head_is() { [ "$(git rev-parse HEAD)" = "$want" ] && [ -z "$(git status --porcelain --untracked-files=no)" ]; }
goldens_try() {
    bin=$1
    n=1
    while [ "$n" -le 3 ]; do
        .lair/tools/goldens --bin "$bin" > "/Users/mfwolffe/lanes/cb16/gate/goldens-$(basename "$(dirname "$bin")").txt" 2>&1
        status=$?
        echo "goldens $bin attempt $n exit $status: $(grep -c ' ok$' "/Users/mfwolffe/lanes/cb16/gate/goldens-$(basename "$(dirname "$bin")").txt") ok, $(grep -c DIFFERS "/Users/mfwolffe/lanes/cb16/gate/goldens-$(basename "$(dirname "$bin")").txt") DIFFERS"
        if [ "$status" != 3 ]; then return "$status"; fi
        n=$((n + 1))
        echo "goldens refused by the floor; waiting 60 s"
        sleep 60
    done
    return 3
}
mkdir -p /Users/mfwolffe/lanes/cb16/gate target/test-home
export HOME=/Users/mfwolffe/lanes/cb16/cub/target/test-home
step head head_is
step fmt .lair/tools/check-fmt
step python-tests python3 -I -m unittest discover -s tests -p '*_test.py'
step test .lair/tools/test
step skips sh -c '[ "$(grep -c "^SKIP" target/test.log)" = 0 ]'
step build .lair/tools/build --all
step selftest-native target/native/cub --selftest
step selftest-release target/release/cub --selftest
step goldens-release goldens_try target/release/cub
step goldens-native goldens_try target/native/cub
step prepare-pty python3 -I tools/prepare-pty
step pty python3 -I .lair/tools/pty --bin target/release/cub --rows "$(python3 -I /Users/mfwolffe/lanes/cb16/tools-lane/pty-rows-without-sound.py)"
step npc-rows-native python3 -I -c "import runpy; runpy.run_path('tools/npc_checks.py')['check']('target/native/cub')"
step npc-rows-release python3 -I -c "import runpy; runpy.run_path('tools/npc_checks.py')['check']('target/release/cub')"
step hit-census sh -c 'target/release/cub --hit-census > /Users/mfwolffe/lanes/cb16/gate/hit-mac.csv && shasum -a 256 /Users/mfwolffe/lanes/cb16/gate/hit-mac.csv | grep -q ^53234a37bb94711dddbc1d4d84a0c6e5fa1579f96f45b0734a7e92931e340055'
echo "CB16_MAC_GAUNTLET_EXIT 0 at $(git rev-parse HEAD) $(date -u +%FT%TZ)"
