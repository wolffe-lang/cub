#!/usr/bin/env python3
"""Write src/demo/demo.lu from tests/cases/demo.pk: the title's recorded demo,
embedded in the binary as the replay's own lines, so the title needs no file
beside it. A test holds the module to the case."""
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
case = (ROOT / 'tests/cases/demo.pk').read_text().splitlines()
lines = [l for l in case if l.strip() and not l.startswith('#')]
out = ['//! demo — the title\'s recorded demo (cb04): tests/cases/demo.pk, the',
       '//! real-key script the proof generates, embedded line by line so the title',
       '//! plays it from the binary alone. Written by tools/embed-demo.py; a test',
       '//! holds it to the case file.',
       '',
       'use controls',
       'use replay',
       '',
       '/// The demo\'s `.pk` lines.',
       'pub fn lines() -> List[str] {',
       '    var out = List[str]()']
for l in lines:
    out.append('    (mut out).push("%s")' % l.replace('"', '\\"'))
out += ['    out', '}', '',
        '/// The demo as a replay (`parse` cannot happen: the lines are a committed case).',
        'pub fn load() -> replay.Replay {',
        '    var text = ""',
        '    for l in lines() { text += l + "\\n" }',
        '    replay.from_text(text, controls.vocab()) else replay.new(1, 1, 80, 24)',
        '}', '']
(ROOT / 'src/demo/demo.lu').write_text('\n'.join(out))
print('demo.lu:', len(lines), 'lines')
