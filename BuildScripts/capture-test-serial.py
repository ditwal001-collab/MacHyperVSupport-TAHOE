"""Capture the Tahoe test VM's existing serial pipe without overwriting logs."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import time
import uuid


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    parser.add_argument('--wait-seconds', type=int, default=600)
    args = parser.parse_args()
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    ready = output / 'capture-ready.json'
    with ready.open('x', encoding='utf-8') as stream:
        json.dump({'pid': os.getpid(), 'utc': datetime.now(timezone.utc).isoformat(),
                   'state': 'waiting for existing COM1 pipe'}, stream)
    pipe = r'\\.\pipe\macos-tahoe-debug'
    deadline = time.monotonic() + args.wait_seconds
    while time.monotonic() < deadline:
        try:
            serial = open(pipe, 'rb', buffering=0)
        except OSError:
            time.sleep(0.25)
            continue
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        path = output / ('serial-' + stamp + '-' + uuid.uuid4().hex[:8] + '.log')
        print('Connected; preserving capture in ' + str(path), flush=True)
        with serial, path.open('xb', buffering=0) as logfile:
            while True:
                try:
                    data = serial.read(4096)
                except OSError:
                    break
                if not data:
                    break
                logfile.write(data)
        print('Serial connection ended; receiver remains ready for reconnect.', flush=True)
        deadline = time.monotonic() + args.wait_seconds
    print('Capture wait timeout reached.', flush=True)


if __name__ == '__main__':
    main()
