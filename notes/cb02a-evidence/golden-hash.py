from pathlib import Path
import hashlib
import sys
root = Path(sys.argv[1])
assert all(not p.read_bytes() for p in root.glob('*.diff')), 'a comparison log contains a difference'
files = sorted(p for p in root.rglob('*') if p.is_file() and p.suffix != '.diff')
h = hashlib.sha256()
for path in files:
    h.update(path.relative_to(root).as_posix().encode() + b'\0')
    h.update(path.read_bytes())
print(len(files), h.hexdigest())
