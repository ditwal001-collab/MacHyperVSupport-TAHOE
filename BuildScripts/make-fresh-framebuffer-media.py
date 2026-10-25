"""Create new, read-back-verified first-install ISO from the pinned CI Release ZIP.

Requires pycdlib==1.22.0. Does not access Hyper-V, disks, credentials or network.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import zipfile

import pycdlib

RELEASE = '162f47670ef9f4640bdfdefd8ba9495b1a039ca6828a52f5ec4498e9d3cb5d6c'
FRAMEBUFFER = 'd8a079d47d61988aabe40cb788b015979c27384135b57339e854d5c017792122'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release-zip', required=True, type=Path)
    parser.add_argument('--output-directory', required=True, type=Path)
    args = parser.parse_args()
    release = args.release_zip.read_bytes()
    if sha(release) != RELEASE:
        raise SystemExit('Unexpected Release ZIP; use verified run40189441511')
    framebuffer = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(release)) as source:
        with zipfile.ZipFile(framebuffer, 'w', zipfile.ZIP_DEFLATED) as target:
            for name in source.namelist():
                if 'MacHyperVFramebuffer.kext/' in name and not name.endswith('/'):
                    suffix = name.split('MacHyperVFramebuffer.kext/', 1)[1]
                    if '..' in Path(suffix).parts or suffix.startswith('/'):
                        raise SystemExit('Unsafe bundle member')
                    target.writestr('MacHyperVFramebuffer.kext/' + suffix, source.read(name))
    with zipfile.ZipFile(io.BytesIO(framebuffer.getvalue())) as bundle:
        executable = bundle.read('MacHyperVFramebuffer.kext/Contents/MacOS/MacHyperVFramebuffer')
        if sha(executable) != FRAMEBUFFER:
            raise SystemExit('Unexpected framebuffer executable')
    scripts = Path(__file__).resolve().parent
    files = {'Install.command': (scripts / 'install-fresh-framebuffer-25G241.command').read_bytes().replace(b'\r\n', b'\n'),
             'Inspect.command': (scripts / 'inspect-fresh-tahoe.command').read_bytes().replace(b'\r\n', b'\n'),
             'Framebuffer.zip': framebuffer.getvalue()}
    args.output_directory.mkdir(parents=True, exist_ok=False)
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=3, joliet=3, vol_ident='HVFRESHFB')
    streams = []
    for index, (name, data) in enumerate(files.items()):
        (args.output_directory / name).write_bytes(data)
        stream = io.BytesIO(data)
        streams.append(stream)
        iso.add_fp(stream, len(data), iso_path=f'/FILE{index}.DAT;1', joliet_path='/' + name)
    output = args.output_directory / 'FreshFramebuffer.iso'
    iso.write(str(output))
    iso.close()
    check = pycdlib.PyCdlib()
    check.open(str(output))
    for name, expected in files.items():
        recovered = io.BytesIO()
        check.get_file_from_iso_fp(recovered, joliet_path='/' + name)
        if recovered.getvalue() != expected:
            raise RuntimeError('ISO read-back mismatch: ' + name)
    check.close()
    manifest = {'source': '6c3568178ba21136b8c21dd45597476c74ec31d1', 'run': 40189441511,
                'release_zip_sha256': RELEASE, 'framebuffer_sha256': FRAMEBUFFER,
                'iso_sha256': sha(output.read_bytes()), 'files': {name: sha(data) for name, data in files.items()},
                'verification': 'PASS: pinned executable and all ISO files read back exactly',
                'scope': 'Only observed Intel25G241 three-module Aux inventory; no EFI, KDK or credentials'}
    (args.output_directory / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
