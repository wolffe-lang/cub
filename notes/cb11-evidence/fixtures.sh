#!/bin/bash
set -eu
lane=/home/mfwolffe/lanes/cb11
exec 9>/home/mfwolffe/lanes/kasumi-cores-4-7.lock
until flock -n 9; do echo "cb11 fixtures wait $(date -u +%FT%TZ)"; sleep 30; done
export LAIR_CPUS=4-7 TMPDIR="$lane/tmp"
cd "$lane/cub"
.lair/tools/in-container target/release/cub --make-den-memory target/cb11-den-memory.pk
.lair/tools/in-container target/release/cub --make-world-proof target/cb11-world-proof
cp target/cb11-den-memory.pk tests/cases/den-memory.pk
cp target/cb11-world-proof/*.pk tests/cases/
.lair/tools/in-container .lair/tools/goldens --update
.lair/tools/in-container python3 -u -I tools/gameplay.py --bin target/release/cub
echo CB11_FIXTURE_SEMANTICS_GREEN
