"""Read-only inventory of large local test files; never deletes or mounts disks."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--active-disks', required=True, type=Path,
                    help='Local-only JSON array of currently attached disk/optical paths')
parser.add_argument('--keep-file', action='append', default=[])
parser.add_argument('--output', required=True, type=Path)
args = parser.parse_args()
repo = Path(__file__).resolve().parents[1]
root = (repo / 'evidence/local-tests').resolve()
active = {str(Path(p).resolve()).casefold() for p in
          json.loads(args.active_disks.read_text(encoding='utf-8-sig')) if p}
keep = {str(Path(p).resolve()).casefold() for p in args.keep_file}
suffixes = {'.vhdx', '.vhd', '.iso', '.dmg', '.log', '.zip'}
records = []
for directory, directories, names in os.walk(root, followlinks=False):
    directories[:] = [name for name in directories if name != '.git'
                      and name != 'mount' and not (Path(directory) / name).is_symlink()]
    for name in names:
        path = Path(directory) / name
        if path.suffix.lower() not in suffixes or path.is_symlink():
            continue
        resolved = path.resolve()
        resolved.relative_to(root)
        stat = resolved.stat()
        key = str(resolved).casefold()
        records.append({'path': resolved.relative_to(repo).as_posix(),
                        'bytes': stat.st_size, 'mtime_ns': stat.st_mtime_ns,
                        'retention': 'active' if key in active else
                                     'explicit_keep' if key in keep else 'review_candidate'})
records.sort(key=lambda item: item['bytes'], reverse=True)
result = {'utc': datetime.now(timezone.utc).isoformat(), 'mode': 'read_only_inventory',
          'scope': 'Selected test-file extensions only; retained originals/backups outside this directory are not scanned',
          'files': records, 'selected_total_bytes': sum(v['bytes'] for v in records),
          'review_candidate_bytes': sum(v['bytes'] for v in records if v['retention'] == 'review_candidate')}
with args.output.open('x', encoding='utf-8') as output:
    json.dump(result, output, indent=2)
    output.write('\n')
print(json.dumps({key: value for key, value in result.items() if key != 'files'}, indent=2))
print(json.dumps(records[:12], indent=2))
