"""Receive an exact-size public installer image from the isolated test guest.

Use only after verifying the guest address and file size. No listener or firewall
change is made on the Windows host. Existing files are never overwritten.
"""
import argparse
import hashlib
import json
from pathlib import Path
import socket

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--host', required=True)
p.add_argument('--port', type=int, default=8080)
p.add_argument('--bytes', type=int, required=True)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args()
partial = a.output.with_name(a.output.name + '.partial')
receipt = a.output.with_name(a.output.name + '.json')
if a.bytes <= 0 or a.output.exists() or partial.exists() or receipt.exists():
    p.error('Invalid length or output already exists')
sha = hashlib.sha256()
total = 0
with socket.create_connection((a.host, a.port), timeout=30) as connection:
    connection.settimeout(120)
    with partial.open('xb') as out:
        while total < a.bytes:
            chunk = connection.recv(min(8 * 1024 * 1024, a.bytes - total))
            if not chunk:
                raise RuntimeError(f'Short transfer: {total}/{a.bytes}; partial preserved')
            out.write(chunk)
            sha.update(chunk)
            total += len(chunk)
partial.rename(a.output)
result = {'bytes': total, 'sha256': sha.hexdigest(),
          'validation': 'Exact-size TCP transfer only; boot and payload verification separate'}
with receipt.open('x', encoding='utf-8') as out:
    json.dump(result, out, indent=2)
print(json.dumps(result))
