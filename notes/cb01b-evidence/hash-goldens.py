from pathlib import Path
import hashlib
import sys
root = Path(sys.argv[1])
h = hashlib.sha256()
# The engine writes one empty comparison log per case beside the output dirs.
for log in root.glob('*.diff'):
    assert log.stat().st_size == 0, f'nonempty golden diff: {log}'
files = sorted(p for p in root.rglob('*') if p.is_file() and p.suffix != '.diff')
for p in files:
    name = p.relative_to(root).as_posix()
    h.update(name.encode() + b'\0' + hashlib.sha256(p.read_bytes()).digest())
print(len(files), h.hexdigest())
