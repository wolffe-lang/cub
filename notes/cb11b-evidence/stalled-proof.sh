#!/bin/bash
set -eu
sh .lair/tools/build --release
python3 -I tests/combo_pty.py --observer-stall-ms 80 --bin target/release/cub
echo CB11B_STALLED_READER_GREEN
