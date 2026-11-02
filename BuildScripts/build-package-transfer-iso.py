"""Temporary optical transport: avoid unsupported multi-extent files in Recovery."""
import argparse
from pathlib import Path
import pycdlib

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('package', type=Path)
p.add_argument('parts', type=Path)
p.add_argument('output', type=Path)
a = p.parse_args()
if a.parts.exists() or a.output.exists():
    p.error('Refusing to overwrite previous transport files')
a.parts.mkdir()
iso = pycdlib.PyCdlib()
iso.new(interchange_level=3, joliet=3, vol_ident='APPLEPARTS')
with a.package.open('rb') as source:
    n = 0
    while True:
        chunk = source.read(1024 * 1024 * 1024)
        if not chunk:
            break
        part = a.parts / f'part{n:02d}'
        with part.open('xb') as out:
            out.write(chunk)
        iso.add_file(str(part), iso_path=f'/PART{n:02d}.;1', joliet_path=f'/part{n:02d}')
        n += 1
iso.write(str(a.output))
iso.close()
print(f'{n} parts, {a.output.stat().st_size} ISO bytes; data transport only, NOT bootable')
