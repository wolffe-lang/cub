#!/bin/bash
set -eu
lane=/home/mfwolffe/lanes/cb04f
cd "$lane/cub"
echo $$ > "$lane/linux-gate.pid"
trap 'rc=$?; echo "LINUX_GATE_EXIT $rc $(date -u +%FT%TZ)"; echo "$rc" > "$lane/linux-gate.exit"' EXIT
echo "cb04f source ledger-final $(date -u +%FT%TZ)"
export LAIR_CPUS=8-11 CARGO_INCREMENTAL=0
flock /home/mfwolffe/lanes/kasumi-cores-8-11.lock taskset -c 8-11 .lair/tools/in-container sh -ec '
.lair/tools/check-fmt
.lair/tools/test
.lair/tools/build --all
target/release/cub --selftest
.lair/tools/goldens --update
.lair/tools/goldens --bin target/native/cub
python3 -I tools/score-check
python3 -I .lair/tools/pty --bin target/release/cub
nice -n 10 python3 -I tools/gameplay.py --bin target/native/cub
nice -n 10 python3 -I tools/gameplay.py --bin target/release/cub
LAIR_PERF_SLACK=1 .lair/tools/perf
LAIR_PERF_SLACK=1 python3 -I .lair/tools/perf-idle --bin target/release/cub
'
