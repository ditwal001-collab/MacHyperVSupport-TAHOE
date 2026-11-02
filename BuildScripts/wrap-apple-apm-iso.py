"""Add an ISO9660 descriptor view inside verified unused APM space.

Experimental optical compatibility wrapper. Preserves APM partition records and
every Apple_HFS byte. Never modifies the source. Requires a separate boot test.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import struct
import pycdlib

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--source', type=Path, required=True)
p.add_argument('--source-sha256', required=True)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args()
receipt = a.output.with_suffix('.wrapper.json')
if a.output.exists() or receipt.exists() or a.source.stat().st_size % 2048:
    p.error('Existing output or source length not sector aligned')
size = a.source.stat().st_size
with a.source.open('rb') as source:
    header = source.read(512)
    assert header[:2] == b'ER' and struct.unpack('>H', header[2:4])[0] == 512
    source.seek(512)
    entry = source.read(512)
    count = struct.unpack('>I', entry[4:8])[0]
    assert 1 <= count <= 63
    partitions = []
    for i in range(count):
        source.seek((i + 1) * 512)
        entry = source.read(512)
        assert entry[:2] == b'PM'
        start, blocks = struct.unpack('>II', entry[8:16])
        partitions.append((start * 512, (start + blocks) * 512,
                           entry[48:80].split(b'\0')[0].decode('ascii')))
iso = pycdlib.PyCdlib()
iso.new(interchange_level=3, joliet=3, vol_ident='APPLETAHOE')
memory = io.BytesIO()
iso.write_fp(memory)
iso.close()
metadata = bytearray(memory.getvalue())
start, end = 16 * 2048, len(metadata)
assert any(kind == 'Apple_Free' and first <= start < end <= last
           for first, last, kind in partitions)
assert not any(kind != 'Apple_Free' and start < last and end > first
               for first, last, kind in partitions)
# Describe the full optical volume in both primary and supplementary descriptors.
for offset in range(start, end, 2048):
    if metadata[offset + 1:offset + 6] != b'CD001':
        break
    if metadata[offset] in (1, 2):
        metadata[offset + 80:offset + 88] = struct.pack('<I', size // 2048) + struct.pack('>I', size // 2048)
    if metadata[offset] == 255:
        break
sha = hashlib.sha256()
with a.source.open('rb') as source, a.output.open('xb') as output:
    while True:
        data = source.read(8 * 1024 * 1024)
        if not data:
            break
        sha.update(data)
        output.write(data)
    if sha.hexdigest().lower() != a.source_sha256.lower():
        raise SystemExit('Source hash mismatch; candidate preserved, DO NOT USE')
    output.seek(start)
    output.write(metadata[start:end])
check = pycdlib.PyCdlib()
check.open(str(a.output))
check.close()
with a.output.open('rb') as output:
    wrapped_sha = hashlib.file_digest(output, 'sha256').hexdigest()
result = {'source_sha256': sha.hexdigest(), 'sha256': wrapped_sha,
          'bytes': size, 'changed_range': [start, end], 'partitions': partitions,
          'verification': 'ISO parser PASS; only verified Apple_Free bytes replaced',
          'runtime': 'EXPERIMENTAL, Hyper-V acceptance and OpenCore boot not yet tested'}
with receipt.open('x', encoding='utf-8') as output:
    json.dump(result, output, indent=2)
print(json.dumps(result))
