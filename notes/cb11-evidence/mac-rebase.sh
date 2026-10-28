#!/bin/bash
set -u
lane=/Users/mfwolffe/lanes/cb11
cd "$lane/cub" || exit 2
echo $$ > "$lane/mac-rebase.pid"
echo "CB11_MAC_REBASE_SOURCE $(git rev-parse HEAD) $(date -u +%FT%TZ)"
memory_wait() {
    while :; do
        bytes=$(vm_stat | awk '/Pages (free|inactive|speculative):/ {gsub("\\.", "", $NF); s+=$NF} END {printf "%.0f", s*16384}')
        if [ "$bytes" -ge 8589934592 ]; then
            echo "cb11 rebase floor clear $bytes $(date -u +%FT%TZ)"
            return 0
        fi
        echo "cb11 rebase waits for8GiB $bytes $(date -u +%FT%TZ)"
        sleep 30
    done
}
stage() {
    name=$1; shift
    for attempt in 1 2 3; do
        memory_wait
        echo "cb11 stage $name attempt $attempt START $(date -u +%FT%TZ)"
        if "$@"; then
            echo "cb11 stage $name GREEN $(date -u +%FT%TZ)"
            return 0
        else
            status=$?
        fi
        echo "cb11 stage $name END status=$status $(date -u +%FT%TZ)"
        if [ "$status" -ne 3 ]; then return "$status"; fi
    done
    echo "CB11_MAC_STAGE_MEMORY_REFUSED $name after3 attempts"
    return 3
}
run() {
    stage native-build sh .lair/tools/build --native || return $?
    stage release-build sh .lair/tools/build --release || return $?
    stage checked sh .lair/tools/test || return $?
    stage python python3 -I -m unittest discover -s tests -p '*_test.py' || return $?
    for backend in native release; do
        stage "$backend-combo" python3 -I tools/combo-timing.py --bin "target/$backend/cub" || return $?
        stage "$backend-reader" python3 -I .lair/tools/pty --bin "target/$backend/cub" --rows cb11-hand-reader,cb10-ghostty-repeat,cb07-strikes,cb08-whisper-flank --keep || return $?
    done
    echo "CB11_MAC_REBASED_BUILD_CHECKED_TARGETED_GREEN $(date -u +%FT%TZ)"
    native_green=0
    release_green=0
    # At most three full-golden stage attempts. A completed backend is never
    # rerun when a later backend meets the memory floor.
    for attempt in 1 2 3; do
        echo "cb11 full-golden stage attempt $attempt $(date -u +%FT%TZ)"
        if [ "$native_green" -eq 0 ]; then
            memory_wait
            if sh .lair/tools/goldens --bin target/native/cub; then
                native_green=1
            else
                status=$?
                [ "$status" -eq 3 ] || return "$status"
                echo "CB11_MAC_GOLDEN_MEMORY_REFUSED native attempt=$attempt"
                continue
            fi
        fi
        if [ "$release_green" -eq 0 ]; then
            memory_wait
            if sh .lair/tools/goldens --bin target/release/cub; then
                release_green=1
            else
                status=$?
                [ "$status" -eq 3 ] || return "$status"
                echo "CB11_MAC_GOLDEN_MEMORY_REFUSED release attempt=$attempt"
                continue
            fi
        fi
        echo "CB11_MAC_REBASED_GOLDENS_GREEN $(date -u +%FT%TZ)"
        return 0
    done
    echo 'CB11_MAC_THIRD_GOLDEN_MEMORY_REFUSAL: no completed sequence rerun; hand back to coordinator'
    return 3
}
run
status=$?
echo "CB11_MAC_REBASE_EXIT $status $(date -u +%FT%TZ)"
echo "$status" > "$lane/mac-rebase.exit"
exit "$status"
