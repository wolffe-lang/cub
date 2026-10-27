#!/usr/bin/env python3
"""Attribute runner wall time from the two jobs' timestamped logs, not test guesses."""
from datetime import datetime
from pathlib import Path
import re
import sys


def boundaries(path):
    rows = []
    for line in Path(path).read_text().splitlines():
        m = re.search(r'(2026-\S+Z) (.*)', line)
        if m:
            rows.append((datetime.fromisoformat(m[1].replace('Z', '+00:00')), m[2]))
    def times(marker):
        return [t for t, text in rows if marker in text]
    def first(marker):
        return times(marker)[0]
    art = times('goldens: art ok')
    gameplay = times('gameplay: green (0 skips)')
    return {
        'start': first('##[group]Run .lair/tools/in-container tools/check-linux'),
        'image': first('#8 DONE'),
        'fmt': first('check-fmt: canonical'),
        'checked': first('test: 0 SKIP lines'),
        'native': first('build: target/native/cub'),
        'release': first('build: target/release/cub'),
        'release_goldens': art[0],
        'pty': first('check-linux: green'),
        'native_goldens': art[1],
        'score': first('score-check: green'),
        'native_gameplay': gameplay[0] if gameplay else None,
        'release_gameplay': gameplay[1] if len(gameplay) > 1 else None,
    }


old, new = map(boundaries, sys.argv[1:3])
stages = [
    ('container provisioning', 'start', 'image'),
    ('Python fixtures + fmt', 'image', 'fmt'),
    ('checked tier', 'fmt', 'checked'),
    ('native build', 'checked', 'native'),
    ('release build', 'native', 'release'),
    ('release selftest + goldens', 'release', 'release_goldens'),
    ('pty rows', 'release_goldens', 'pty'),
    ('native goldens', 'pty', 'native_goldens'),
    ('score check', 'native_goldens', 'score'),
    ('native gameplay', 'score', 'native_gameplay'),
    ('release gameplay', 'native_gameplay', 'release_gameplay'),
]
print('stage\tcb07 start/end UTC\tcb07 seconds\tcb08 start/end UTC\tcb08 seconds\tdelta seconds')
for label, start, end in stages:
    cells = [label]
    durations = []
    for result in (old, new):
        a, b = result[start], result[end]
        if a is None or b is None:
            cells.extend(['not completed', '-'])
            durations.append(None)
        else:
            cells.extend([a.strftime('%H:%M:%S.%f') + '/' + b.strftime('%H:%M:%S.%f'), f'{(b-a).total_seconds():.3f}'])
            durations.append((b-a).total_seconds())
    cells.append('-' if None in durations else f'{durations[1]-durations[0]:+.3f}')
    print('\t'.join(cells))
old_to_score = (old['score'] - old['start']).total_seconds()
new_to_score = (new['score'] - new['start']).total_seconds()
print(f'container-start to score: cb07={old_to_score:.3f}s cb08={new_to_score:.3f}s delta={new_to_score-old_to_score:+.3f}s')
