#!/usr/bin/env python3
"""cb14 (lane tooling): the inherited final.states. For every golden
directory both trunk feb57572 and the working tree hold, compare final.state
(the simulation's end: the trace line and the foes); and for every directory
cb14's pre-rebase tree (51ecc07d) also holds, the fields that moved between
it and the working tree.

    python3 -I final-states.py <repo> <out file>
"""
import pathlib
import subprocess
import sys

repo, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])


def show(rev, path):
    p = subprocess.run(['git', '-C', str(repo), 'show', '%s:%s' % (rev, path)], capture_output=True, text=True)
    return p.stdout if p.returncode == 0 else None


def fields(text):
    first = text.splitlines()[0].split()
    return dict(zip(first[::2], first[1::2])), text.splitlines()[1:]


dirs = sorted(p.parent.name for p in (repo / 'tests/goldens').glob('*/final.state'))
lines = []
same_t = changed_t = 0
moved_fields = {}
for d in dirs:
    path = 'tests/goldens/%s/final.state' % d
    now = (repo / path).read_text()
    trunk = show('feb57572', path)
    before = show('51ecc07d', path)
    if trunk is not None:
        if trunk == now:
            same_t += 1
        else:
            changed_t += 1
            lines.append('vs trunk changed %s' % d)
    if before is not None and before != now:
        a, af = fields(before)
        b, bf = fields(now)
        moved = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
        foes = 'foes moved' if af != bf else 'foes same'
        lines.append('vs cb14-before changed %s: %s; %s' % (d, ' '.join('%s %s->%s' % (k, a.get(k), b.get(k)) for k in moved), foes))
        for k in moved:
            moved_fields[k] = moved_fields.get(k, 0) + 1
summary = ['final.states in both trunk and now: %d byte-identical, %d changed' % (same_t, changed_t),
           'fields moved against cb14-before: ' + ' '.join('%s:%d' % kv for kv in sorted(moved_fields.items()))]
out.write_text('\n'.join(summary + lines) + '\n')
print('\n'.join(summary))
