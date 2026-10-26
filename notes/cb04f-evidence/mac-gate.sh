#!/bin/bash
set -eu
lane=/Users/mfwolffe/lanes/cb04f
cd "$lane/cub"
echo $$ > "$lane/mac-gate.pid"
trap 'rc=$?; echo "MAC_GATE_EXIT $rc $(date -u +%FT%TZ)"; echo "$rc" > "$lane/mac-gate.exit"' EXIT
sha=$(git rev-parse --short=8 HEAD)
echo "cb04f Mac final source $(git rev-parse HEAD) start $(date -u +%FT%TZ)"
export HOME="$lane/home" TMPDIR="$lane/tmp" CARGO_INCREMENTAL=0 CARGO_BUILD_JOBS=4 LAIR_LANE_HOST=nomad
heavy() { bash "$lane/heavy.sh" "$@"; }
heavy .lair/tools/check-fmt
heavy .lair/tools/test
heavy .lair/tools/build --all
heavy target/release/cub --selftest
heavy .lair/tools/goldens
heavy .lair/tools/goldens --bin target/native/cub
heavy python3 -I tools/score-check
heavy python3 -I .lair/tools/pty --bin target/release/cub
heavy python3 -I tools/gameplay.py --bin target/native/cub
heavy python3 -I tools/gameplay.py --bin target/release/cub
heavy env LAIR_PERF_SLACK=1 .lair/tools/perf
heavy env LAIR_PERF_SLACK=1 python3 -I .lair/tools/perf-idle --bin target/release/cub
cp target/release/cub "$lane/cub-play-$sha"
echo "$lane/cub-play-$sha --save $lane/play.save --ghost-dir $lane/play-ghosts"
