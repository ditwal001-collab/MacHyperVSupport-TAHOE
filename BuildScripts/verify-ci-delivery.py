"""Verify downloaded CI packages against their pinned provenance, read-only."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--artifacts', required=True, type=Path)
parser.add_argument('--source', required=True)
parser.add_argument('--run', required=True, type=int)
parser.add_argument('--output', required=True, type=Path)
args = parser.parse_args()
root = args.artifacts.resolve()
environment = (root / 'Provenance/environment.txt').read_text()
assert 'source=' + args.source + '\n' in environment
assert 'run=' + str(args.run) + ' ' in environment
expected = {}
for line in (root / 'Provenance/build-sha256.txt').read_text().splitlines():
    digest, name = line.split(None, 1)
    expected[name.strip()] = digest
packages = {}
for configuration in ('Debug', 'Release'):
    archives = list((root / 'Artifacts' / configuration).glob('MacHyperVSupport-*.zip'))
    assert len(archives) == 1
    archive = archives[0]
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    assert digest == expected['build/' + configuration + '/' + archive.name]
    binaries = {}
    with zipfile.ZipFile(archive) as package:
        for name in package.namelist():
            if '/Contents/MacOS/' not in name or name.endswith('/'):
                continue
            relative = name.split('Kexts/', 1)[-1]
            matches = [key for key in expected if key.startswith('build/' + configuration + '/')
                       and key.endswith(relative)]
            assert matches, name
            data = package.read(name)
            binary_digest = hashlib.sha256(data).hexdigest()
            # Provenance records both build output and its packaged copy.
            assert all(binary_digest == expected[key] for key in matches), name
            if configuration == 'Release':
                assert b'TAHOE-SYNIC' not in data and b'TAHOE-DEBUG' not in data
            binaries[relative] = binary_digest
    assert len(binaries) == 3
    packages[configuration] = {'file': archive.name, 'sha256': digest, 'binaries': binaries}
imports = (root / 'Provenance/monterey-imports.txt').read_text()
assert '_thread_block' in imports
result = {
    'source': args.source, 'run': args.run,
    'verification': 'Original CI ZIPs and all kext executables match uploaded SHA256 provenance',
    'thread_block_import_present': True,
    'release_tahoe_trace_strings_absent': True,
    'packages': packages,
    'runtime': 'Not established by this verification; see independent boot evidence',
}
with args.output.open('x', encoding='utf-8') as output:
    json.dump(result, output, indent=2)
    output.write('\n')
print(json.dumps(result, indent=2))
