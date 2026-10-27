#!/bin/bash
# cb07 Linux gate on kasumi cores 4-7 (the lock), the engine's container.
set -u
lane=/home/mfwolffe/lanes/cb07
cd "$lane/cub" || exit 2
rm -f "$lane/linux.exit"
echo $$ > "$lane/linux.pid"
git fetch -q origin cb07 && git checkout -q -B cb07 origin/cb07 || exit 2
echo "cb07 LINUX head=$(git rev-parse HEAD) start=$(date -u +%FT%TZ)"
tools/fetch-lair || exit 2
export LAIR_CPUS=4-7 CARGO_INCREMENTAL=0
flock /home/mfwolffe/lanes/kasumi-cores-4-7.lock taskset -c 4-7 nice -n 10 .lair/tools/in-container sh -ec '
    mkdir -p target/test-home
    export HOME=/work/target/test-home
    .lair/tools/fetch-toolchain
    .lair/tools/check-fmt
    .lair/tools/test
    .lair/tools/build --all
    target/native/cub --selftest
    target/release/cub --selftest
    target/release/cub --strike-census >target/strike-linux.txt
    target/native/cub --strike-census >target/strike-linux-native.txt
    cmp target/strike-linux.txt target/strike-linux-native.txt
    target/release/cub --hud-census >target/hud-linux.txt
    tail -1 target/strike-linux.txt
    tail -1 target/hud-linux.txt
    .lair/tools/goldens
    .lair/tools/goldens --bin target/native/cub
    python3 -I tools/score-check
    python3 -I .lair/tools/pty --bin target/release/cub
    python3 -I .lair/tools/pty --bin target/native/cub --rows cb07-strikes
    python3 -I tools/gameplay.py --bin target/native/cub
    python3 -I tools/gameplay.py --bin target/release/cub
    echo "linux: complete"
'
rc=$?
echo "LINUX_EXIT $rc $(date -u +%FT%TZ)"
echo "$rc" > "$lane/linux.exit"
exit "$rc"
