#!/usr/bin/env python3
"""Hash relative paths and bytes, in stable path order, for both-host goldens."""
import hashlib
from pathlib import Path
import sys
root = Path(sys.argv[1])
h = hashlib.sha256()
n = 0
for path in sorted(root.rglob('*')):
    if path.is_file():
        h.update(path.relative_to(root).as_posix().encode() + b'\0' + path.read_bytes())
        n += 1
print(n, h.hexdigest())
