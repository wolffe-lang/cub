#!/bin/bash
set +e
python3 -I /Users/mfwolffe/lanes/cb11b/plant/tests/combo_pty.py --observer-stall-ms 80 --bin /Users/mfwolffe/lanes/cb11b/cub/target/release/cub
status=$?
echo "CB11B_PLANT_EXIT $status"
[ "$status" -eq 1 ]
