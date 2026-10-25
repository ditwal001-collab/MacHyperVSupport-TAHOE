"""Capture an explicitly selected Hyper-V named pipe into unique local files.

Configure the target VM's COM1 separately. This tool changes no VM settings.
Use only one receiver per pipe; leave existing receivers running.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import time
import uuid


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pipe', required=True, help=r'Example: \\.\pipe\TahoeInstallTest')
    parser.add_argument('--output', required=True, type=Path, help='New capture directory')
    parser.add_argument('--wait-seconds', type=int, default=3600)
    args = parser.parse_args()
    if not args.pipe.startswith('\\\\.\\pipe\\'):
        parser.error('--pipe must be a local Windows named pipe')
    if args.wait_seconds <= 0:
        parser.error('--wait-seconds must be positive')
    args.output.mkdir(parents=True, exist_ok=False)
    ready = {'pid': os.getpid(), 'utc': datetime.now(timezone.utc).isoformat(),
             'state': 'waiting for selected COM1 pipe'}
    (args.output / 'capture-ready.json').write_text(json.dumps(ready, indent=2))
    deadline = time.monotonic() + args.wait_seconds
    while time.monotonic() < deadline:
        try:
            serial = open(args.pipe, 'rb', buffering=0)
        except OSError:
            time.sleep(0.25)
            continue
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        path = args.output / ('serial-' + stamp + '-' + uuid.uuid4().hex[:8] + '.log')
        print('Connected: ' + str(path), flush=True)
        with serial, path.open('xb', buffering=0) as logfile:
            while True:
                try:
                    data = serial.read(4096)
                except OSError:
                    break
                if not data:
                    break
                logfile.write(data)
        print('Disconnected; waiting for reconnect.', flush=True)
        deadline = time.monotonic() + args.wait_seconds
    print('Capture wait timeout reached.', flush=True)


if __name__ == '__main__':
    main()
