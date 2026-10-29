#!/bin/bash
# cb17 dev step (inside maclock.sh): build both tiers, the score's unit rows
# and the opening's, then score-check (with --update when asked), each
# step's `END <step> exit=N`, stopping at the first nonzero.
set -u
cd /Users/mfwolffe/lanes/cb17/cub || exit 2
step() {
    name=$1
    shift
    "$@"
    s=$?
    echo "END $name exit=$s $(date -u +%FT%TZ)"
    [ "$s" = 0 ] || exit "$s"
}
step build .lair/tools/build --all
step score-tests .wolf-bin/wolf test --deny-warnings --nocapture src/score_test.lu src/opening_test.lu
step score-check python3 -I tools/score-check "$@"
