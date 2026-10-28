#!/bin/bash
set -eu
sh .lair/tools/goldens --bin target/native/cub
sh .lair/tools/goldens --bin target/release/cub
python3 -I tools/combo-timing.py --bin target/release/cub
python3 -I .lair/tools/pty --bin target/release/cub --rows cb08-whisper-flank --keep
echo CB11_MAC_FINAL_VISUAL_GREEN
