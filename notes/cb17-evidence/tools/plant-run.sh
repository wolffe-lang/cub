#!/bin/bash
# cb17's plant witness on the Mac (run inside maclock.sh): the plant
# worktree's two builds (must be 0), then the two rows the break must turn
# red, each step's exit printed as `END <step> exit=N`. The build stops the
# run if it fails; the red rows are the evidence, so both run.
set -u
cd /Users/mfwolffe/lanes/cb17/plant || exit 2
echo "cb17 plant source $(git rev-parse HEAD) branch $(git branch --show-current)"
.lair/tools/build --all
s=$?
echo "END build exit=$s"
[ "$s" = 0 ] || exit "$s"
.wolf-bin/wolf test --deny-warnings --nocapture src/score_test.lu
s=$?
echo "END score-test exit=$s"
python3 -I tools/score-check
s=$?
echo "END score-check exit=$s"
