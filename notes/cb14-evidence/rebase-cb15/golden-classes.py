#!/usr/bin/env python3
"""cb14 (lane tooling): the goldens' key sets and every changed key's cause,
against trunk feb57572. Trees: B the base both lanes started from (f20650d4),
T trunk (feb57572: cb11b, cb13, cb15 over B), P cb14 before this rebase
(51ecc07d: cb14 over B), N the working tree (cb14 over T, regenerated).

    python3 -I golden-classes.py <repo> <out dir>
"""
import collections
import pathlib
import subprocess
import sys

repo, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
B, T, P = 'f20650d4', 'feb57572', '51ecc07d'


def tree(rev):
    text = subprocess.run(['git', '-C', str(repo), 'ls-tree', '-r', rev, 'tests/goldens'],
                          capture_output=True, text=True, check=True).stdout
    keys = {}
    for line in text.splitlines():
        meta, path = line.split('\t', 1)
        keys[path] = meta.split()[2]
    return keys


def work():
    paths = sorted(str(p.relative_to(repo)) for p in (repo / 'tests/goldens').rglob('*') if p.is_file())
    blobs = subprocess.run(['git', '-C', str(repo), 'hash-object', '--stdin-paths'], input='\n'.join(paths) + '\n',
                           capture_output=True, text=True, check=True).stdout.split()
    return dict(zip(paths, blobs))


b, t, p, n = tree(B), tree(T), tree(P), work()
missing = sorted(set(t) - set(n))
extra = sorted(set(n) - set(t))
changed = sorted(k for k in set(t) & set(n) if t[k] != n[k])
same = sorted(k for k in set(t) & set(n) if t[k] == n[k])


def directory(k):
    return k.split('/')[2]


classes = collections.OrderedDict()


def put(cls, key):
    classes.setdefault(cls, []).append(key)


for k in changed:
    if k in p and n[k] == p[k] and p[k] != t[k]:
        put('map: as cb14 wrote it before the rebase (P), trunk had not changed it (T = B)' if t.get(k) == b.get(k)
            else 'map: as cb14 wrote it before the rebase (P); trunk had changed it (T != B), cb14 replaces it', k)
    elif k in p and p.get(k) != b.get(k) and t.get(k) != b.get(k):
        put('map over cb15: both lanes changed it from B; N is cb14\'s world under trunk\'s drawing', k)
    elif k in p and p.get(k) != b.get(k):
        put('map: cb14 changed it from B, trunk did not; N differs from P', k)
    elif t.get(k) != b.get(k):
        put('trunk changed it from B, cb14 had not before the rebase; N differs from T', k)
    else:
        put('neither lane changed it from B before the rebase; N differs', k)
for k in missing:
    put('missing: ' + ('cb14 removed it before the rebase (absent from P)' if k not in p else 'present in P'), k)
for k in extra:
    put('extra: ' + ('cb14 added it before the rebase (in P)' if k in p else 'new to the rebase (not in P)'), k)

with open(out / 'golden-classes.txt', 'w') as f:
    f.write('base %s trunk %s cb14-before %s; trunk keys %d, new keys %d, missing %d, extra %d, changed %d, unchanged %d\n'
            % (B, T, P, len(t), len(n), len(missing), len(extra), len(changed), len(same)))
    for cls, keys in classes.items():
        dirs = sorted({directory(k) for k in keys})
        f.write('\n%s: %d keys in %d directories\n' % (cls, len(keys), len(dirs)))
        f.write('  ' + ' '.join(dirs) + '\n')
with open(out / 'golden-keys.txt', 'w') as f:
    for cls, keys in classes.items():
        for k in keys:
            f.write('%s\t%s\n' % (cls, k))
print(open(out / 'golden-classes.txt').read())
