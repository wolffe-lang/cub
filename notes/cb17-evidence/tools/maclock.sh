#!/bin/bash
# cb17's Mac runner: take the shared build lock (the directory
# /Users/mfwolffe/lanes/mac-build.lock, mkdir; a holder whose pid is dead is
# removed and retried at once, else a printed line and 30 s), write pid and
# lane inside, wait in a printing loop for the 8 GiB vm_stat floor (free +
# inactive + speculative pages x 16384), run the command, release the lock.
# The command's exit is this script's exit.
#   maclock.sh CMD ARGS...
set -u
LOCK=/Users/mfwolffe/lanes/mac-build.lock
FLOOR=$((8 * 1024 * 1024 * 1024))
until mkdir "$LOCK" 2>/dev/null; do
    holder=$(cat "$LOCK/pid" 2>/dev/null || echo "")
    lane=$(cat "$LOCK/lane" 2>/dev/null || echo "?")
    if [ -n "$holder" ] && ! kill -0 "$holder" 2>/dev/null; then
        echo "cb17 maclock: holder pid $holder ($lane) is dead; removing $(date -u +%FT%TZ)"
        rm -rf "$LOCK"
        continue
    fi
    echo "cb17 maclock: waits for $lane (pid ${holder:-none}) $(date -u +%FT%TZ)"
    sleep 30
done
echo $$ >"$LOCK/pid"
echo cb17 >"$LOCK/lane"
trap 'rm -rf "$LOCK"' EXIT
free_bytes() {
    vm_stat | awk '/Pages free/ {f=$3} /Pages inactive/ {i=$3} /Pages speculative/ {s=$3} END {gsub(/\./,"",f); gsub(/\./,"",i); gsub(/\./,"",s); printf "%d\n", (f+i+s)*16384}'
}
while :; do
    have=$(free_bytes)
    if [ "$have" -ge "$FLOOR" ]; then
        echo "cb17 maclock: holds the lock; floor clear at $((have / 1048576)) MiB $(date -u +%FT%TZ)"
        break
    fi
    echo "cb17 maclock: floor short, $((have / 1048576)) MiB < 8192 MiB; waiting $(date -u +%FT%TZ)"
    sleep 30
done
"$@"
status=$?
echo "cb17 maclock: END exit=$status $(date -u +%FT%TZ)"
exit "$status"
