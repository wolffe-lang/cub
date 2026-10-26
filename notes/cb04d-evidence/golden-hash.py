from pathlib import Path
import hashlib
import sys

root = Path(sys.argv[1])
files = sorted(p for p in (root / 'tests/goldens').rglob('*') if p.is_file())
hash = hashlib.sha256()
for path in files:
    relative = str(path.relative_to(root))
    hash.update(relative.encode() + b'\0' + path.read_bytes() + b'\0')
print('files', len(files), 'directories', len({p.parent for p in files}))
print('path-content-sha256', hash.hexdigest())
