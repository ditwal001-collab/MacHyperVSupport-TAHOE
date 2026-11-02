"""Run the original OpenCore macrecovery tool with a headless progress-width fallback."""
import argparse
import os
from pathlib import Path
import runpy
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--tool', required=True, type=Path)
parser.add_argument('--output', required=True, type=Path)
args = parser.parse_args()
if args.output.exists():
    parser.error('A new output directory is required')
original = os.get_terminal_size


def width(fd=1):
    try:
        return original(fd)
    except OSError:
        return os.terminal_size((100, 30))


os.get_terminal_size = width
sys.argv = [str(args.tool), '-b', 'Mac-CFF7D910A743CAAF', '-m', '00000000000000000',
            '-os', 'latest', '-o', str(args.output), 'download']
runpy.run_path(str(args.tool.resolve()), run_name='__main__')
