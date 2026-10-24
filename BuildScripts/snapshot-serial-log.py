"""Preserve and summarize a bounded prefix of a live serial capture.

On Windows a directory listing can report a stale size for an open writer.
Measure the opened file instead; never use directory size as capture liveness.
This script does not open the serial pipe or operate on a VM.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import uuid


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    name = 'serial-prefix-' + now.strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8]
    snapshot = args.output / (name + '.log')
    digest = hashlib.sha256()
    with args.input.open('rb', buffering=0) as source:
        length = source.seek(0, os.SEEK_END)
        source.seek(0)
        remaining = length
        with snapshot.open('xb') as output:
            while remaining:
                chunk = source.read(min(65536, remaining))
                if not chunk:
                    raise RuntimeError('Capture was truncated during snapshot; preserve partial file for review')
                output.write(chunk)
                digest.update(chunk)
                remaining -= len(chunk)
    data = snapshot.read_bytes()
    # Count only complete lines, not an unfinished final serial write.
    complete = data[:data.rfind(b'\n') + 1].decode('utf-8', errors='replace')
    writes = re.findall(r'Writing EOM targetCPU=(\d+) actualCPU=(\d+)\r*\n', complete)
    result = {
        'utc': now.isoformat(), 'source_log_name': args.input.name,
        'snapshot_name': snapshot.name, 'prefix_bytes': length,
        'snapshot_sha256': digest.hexdigest(),
        'complete_eom_writes': len(writes),
        'mismatched_eom_writes': sum(target != actual for target, actual in writes),
        'cursor_conversion_failures': complete.count('Failed to convert hardware cursor image'),
        'panic_markers': complete.count('panic('),
        'root_wait_markers': complete.count('Still waiting for root device'),
        'software_cursor_activation_markers': complete.count('Software cursor comparison enabled by boot arg'),
        'scope': 'bounded captured prefix; absence of a marker is not stability proof',
    }
    with (args.output / (name + '.json')).open('x', encoding='utf-8') as output:
        json.dump(result, output, indent=2)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
