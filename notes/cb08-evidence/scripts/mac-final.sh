#!/bin/bash
set -u
lane=/Users/mfwolffe/lanes/cb08
cd "$lane/cub" || exit 2
echo $$ >"$lane/mac-final.pid"
echo "cb08 Mac final HEAD $(git rev-parse HEAD) start $(date -u +%FT%TZ)"
export TMPDIR="$lane/tmp" LAIR_LANE_HOST=nomad CARGO_INCREMENTAL=0
mkdir -p target/test-home
export HOME="$PWD/target/test-home"
wait_memory() {
    while :; do
        bytes=$(vm_stat | awk '/Pages (free|inactive|speculative):/ {gsub("\\.", "", $NF); s+=$NF} END {printf "%.0f", s*16384}')
        if [ "$bytes" -ge 8589934592 ] && ! ps -Ao comm= | grep -qE '/wolf$'; then
            echo "Mac memory gate clear: $bytes bytes $(date -u +%FT%TZ)"
            return 0
        fi
        echo "cb08 Mac final waits for 8 GiB and one build: $bytes bytes $(date -u +%FT%TZ)"
        sleep 30
    done
}
run() {
    for tier in native release; do
        while :; do
            wait_memory
            .lair/tools/build "--$tier"
            status=$?
            [ "$status" -eq 3 ] || break
        done
        [ "$status" -eq 0 ] || return "$status"
        "target/$tier/cub" --selftest || return $?
        wait_memory
        .lair/tools/goldens --bin "target/$tier/cub" >"target/cb08-mac-final-$tier-goldens.log" 2>&1 || return $?
        echo "Mac $tier goldens green $(date -u +%FT%TZ)"
    done
    python3 -I tools/prepare-pty || return $?
    python3 -I .lair/tools/pty --bin target/release/cub --rows cb08-diagonal-live || return $?
    python3 -I .lair/tools/pty --bin target/release/cub --rows cb08-whisper-flank || return $?
    sha=$(git rev-parse --short=8 HEAD)
    cp target/release/cub "$lane/cub-play-$sha" || return $?
    echo "play $lane/cub-play-$sha"
    shasum -a 256 "$lane/cub-play-$sha"
    shasum -a 256 "$lane/cub-play-$sha"
}
run
rc=$?
echo "MAC_FINAL_EXIT $rc $(date -u +%FT%TZ)"
echo "$rc" >"$lane/mac-final.exit"
exit "$rc"
