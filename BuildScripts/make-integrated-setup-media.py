"""Make a new ISO from CI's verified integrated SetupMedia.zip; requires pycdlib1.22.0."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import stat
import zipfile
import pycdlib


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--setup-zip', type=Path, required=True)
    parser.add_argument('--provenance', type=Path, required=True)
    parser.add_argument('--output-directory', type=Path, required=True)
    args = parser.parse_args()
    provenance = json.loads(args.provenance.read_text())
    data = args.setup_zip.read_bytes()
    if hashlib.sha256(data).hexdigest() != provenance['setup_media_sha256']:
        raise SystemExit('CI setup archive hash mismatch')
    files = {}
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        for name in archive.namelist():
            path = Path(name)
            if name.endswith('/'):
                continue
            if path.is_absolute() or '..' in path.parts or '\\' in name or stat.S_ISLNK(archive.getinfo(name).external_attr >> 16):
                raise SystemExit('Unsafe archive entry')
            if name in files:
                raise SystemExit('Duplicate archive entry')
            files[name] = archive.read(name)
    assert set(files) == set(provenance['files']) | {'payload.sha256'}
    for name, digest in provenance['files'].items():
        assert hashlib.sha256(files[name]).hexdigest() == digest, name
    args.output_directory.mkdir(parents=True, exist_ok=False)
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=3, joliet=3, vol_ident='HVSETUP')
    directories = {Path('.'): ''}
    wanted = {p for name in files for p in Path(name).parents if p != Path('.')}
    for index, directory in enumerate(sorted(wanted, key=lambda p: (len(p.parts), p.as_posix()))):
        parent = directories[directory.parent]
        location = parent + '/D' + str(index).zfill(7)
        iso.add_directory(iso_path=location, joliet_path='/' + directory.as_posix())
        directories[directory] = location
    streams = []
    for index, (name, value) in enumerate(sorted(files.items())):
        stream = io.BytesIO(value)
        streams.append(stream)
        location = directories[Path(name).parent] + '/F' + str(index).zfill(7) + '.BIN;1'
        iso.add_fp(stream, len(value), iso_path=location, joliet_path='/' + name)
    output = args.output_directory / 'IntegratedSetup.iso'
    iso.write(str(output))
    iso.close()
    check = pycdlib.PyCdlib()
    check.open(str(output))
    for name, expected in files.items():
        recovered = io.BytesIO()
        check.get_file_from_iso_fp(recovered, joliet_path='/' + name)
        assert recovered.getvalue() == expected, name
    check.close()
    result = {'iso_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
              'setup_source': provenance['setup_source'], 'files_verified': len(files),
              'verification': 'PASS: all ISO files match CI payload exactly',
              'runtime': 'Recovery seed persistence and clean installation still require runtime validation'}
    (args.output_directory / 'manifest.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
