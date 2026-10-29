#!/bin/bash
# cb16 lane tooling: the censuses the NPCs must not move, base against head,
# both native builds on nomad (run inside heavy.sh). Each pair is diffed byte
# for byte; the summary line names every census and whether it is equal.
set -u
out=/Users/mfwolffe/lanes/cb16/gate/census
mkdir -p "$out"
base=/Users/mfwolffe/lanes/cb16/base-bin/cub-ed180ef5-native
head=/Users/mfwolffe/lanes/cb16/cub/target/native/cub
for c in --world-audit --foe-census --den-spacing --bends-audit --spurs-audit; do
    name=${c#--}
    "$base" "$c" > "$out/$name-base.txt" 2>&1
    b=$?
    "$head" "$c" > "$out/$name-head.txt" 2>&1
    h=$?
    if cmp -s "$out/$name-base.txt" "$out/$name-head.txt"; then same=equal; else same=DIFFERS; fi
    echo "census $name base_exit=$b head_exit=$h $same $(shasum -a 256 "$out/$name-head.txt" | cut -c1-16)"
done
echo CB16_CENSUS_DONE
