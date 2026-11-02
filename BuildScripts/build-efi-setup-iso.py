"""Prepare a per-VM EFI tree and combine its FAT boot image with verified setup media."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import plistlib
import secrets
import shutil
import subprocess
import uuid
import zipfile


def sha(data):
    return hashlib.sha256(data).hexdigest()


def file_sha(path):
    with path.open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def prepare(args):
    source = args.source
    config = plistlib.loads((source / 'OC/config.plist').read_bytes())
    assert config['PlatformInfo']['Automatic']
    assert not config['Misc']['Security']['EnablePassword']
    old = dict(config['PlatformInfo']['Generic'])
    model = old['SystemProductName']
    pair = subprocess.check_output([str(args.macserial), '-m', model, '-n', '1'], text=True).strip().split('|')
    assert len(pair) == 2
    generic = config['PlatformInfo']['Generic']
    generic.update(SystemSerialNumber=pair[0].strip(), MLB=pair[1].strip(),
                   SystemUUID=str(uuid.uuid4()).upper(), ROM=b'\x02' + secrets.token_bytes(5))
    if args.identity_from:
        generic.update(plistlib.loads(args.identity_from.read_bytes())['PlatformInfo']['Generic'])
    config['Misc']['Security'].update(PasswordHash=b'', PasswordSalt=b'')
    config['Misc']['Boot'].update(ShowPicker=True, HideAuxiliary=False, PickerMode='Builtin',
                                 LauncherOption='Disabled', Timeout=10)
    config['Misc']['Entries'] = []
    config['Misc']['Tools'] = []
    # Optical media are read-only: keep console + serial logs, never EFI file logs.
    config['Misc']['Debug']['Target'] = 0x0B
    nvram = config['NVRAM']['Add']['7C436110-AB2A-4BBB-A880-FE41995C9F82']
    nvram['boot-args'] = '-v keepsyms=1 debug=0x12a serial=5 msgbuf=1048576 -hvgfxfbswcursor'
    nvram['prev-lang:kbd'] = b'en-US:0'
    config['Misc']['Security']['ScanPolicy'] = 0
    config['Kernel']['Add'] = [v for v in config['Kernel']['Add']
                               if v['Enabled'] and v['BundlePath'] in
                               ('Lilu.kext', 'VirtualSMC.kext', 'MacHyperVSupportMonterey.kext')]
    assert {v['BundlePath'] for v in config['Kernel']['Add']} == {
        'Lilu.kext', 'VirtualSMC.kext', 'MacHyperVSupportMonterey.kext'}
    config['UEFI']['Drivers'] = [v for v in config['UEFI']['Drivers']
                                 if v['Enabled'] and v['Path'] != 'ResetNvramEntry.efi']
    args.output.mkdir(parents=True, exist_ok=False)
    destination = args.output / 'EFI'
    (destination / 'BOOT').mkdir(parents=True)
    (destination / 'OC').mkdir()
    shutil.copy2(source / 'BOOT/BOOTx64.efi', destination / 'BOOT/BOOTx64.efi')
    shutil.copy2(source / 'OC/OpenCore.efi', destination / 'OC/OpenCore.efi')
    # Do not offer the bootloader itself as an OS entry and recurse on timeout.
    (destination / 'BOOT/.contentVisibility').write_text('Disabled', encoding='ascii')
    (destination / 'OC/.contentVisibility').write_text('Disabled', encoding='ascii')
    for section, directory, field in [(config['ACPI']['Add'], 'ACPI', 'Path'),
                                       (config['UEFI']['Drivers'], 'Drivers', 'Path'),
                                       (config['Kernel']['Add'], 'Kexts', 'BundlePath')]:
        for entry in section:
            if not entry['Enabled']:
                continue
            relative = Path(entry[field])
            assert not relative.is_absolute() and '..' not in relative.parts
            path = source / 'OC' / directory / relative
            target = destination / 'OC' / directory / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if path.is_dir():
                shutil.copytree(path, target)
            else:
                shutil.copy2(path, target)
    new = plistlib.dumps(config, sort_keys=False)
    for field in ('SystemSerialNumber', 'MLB', 'SystemUUID'):
        assert generic[field] != old[field] and old[field].encode() not in new
    (destination / 'OC/config.plist').write_bytes(new)
    core = destination / 'OC/Kexts/MacHyperVSupportMonterey.kext/Contents/MacOS/MacHyperVSupportMonterey'
    assert sha(core.read_bytes()) == 'c97e29193de9bedf9e2f39b7da38a589347874f7f8ef8c0c8e24f92d7f76ca16'
    subprocess.run([str(args.ocvalidate), str(destination / 'OC/config.plist')], check=True)
    result = {'model': model, 'identity': 'new randomly generated per-VM identity; no original identifiers',
              'config_sha256': sha(new), 'core_sha256': sha(core.read_bytes()),
              'ocvalidate': 'PASS', 'files_sha256': {
                  p.relative_to(args.output).as_posix(): sha(p.read_bytes())
                  for p in sorted(destination.rglob('*')) if p.is_file()}}
    (args.output / 'efi-manifest.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'files_sha256'}, indent=2))


def make_iso(args):
    import pycdlib
    provenance = json.loads(args.provenance.read_text())
    assert sha(args.setup_zip.read_bytes()) == provenance['setup_media_sha256']
    files = {}
    with zipfile.ZipFile(args.setup_zip) as archive:
        for name in archive.namelist():
            assert not name.startswith('/') and '..' not in Path(name).parts and '\\' not in name
            files[name] = archive.read(name)
    assert set(files) == set(provenance['files']) | {'payload.sha256'}
    for name, expected in provenance['files'].items():
        assert sha(files[name]) == expected
    if args.recovery_only:
        files = {}
    with args.boot_image.open('rb') as handle:
        boot_header = handle.read(512)
    boot_hash = file_sha(args.boot_image)
    assert boot_header[510:512] == b'\x55\xaa' and boot_header[82:90] == b'FAT32   '
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=3, joliet=3, vol_ident='APPLETAHOE' if args.recovery_only else 'HVSETUP')
    streams = []
    locations = {Path('.'): ''}
    for index, path in enumerate(sorted({p for n in files for p in Path(n).parents if p != Path('.')},
                                         key=lambda p: (len(p.parts), p.as_posix()))):
        location = locations[path.parent] + '/D' + str(index).zfill(7)
        iso.add_directory(iso_path=location, joliet_path='/' + path.as_posix())
        locations[path] = location
    for index, (name, data) in enumerate(sorted(files.items())):
        fp = io.BytesIO(data); streams.append(fp)
        iso.add_fp(fp, len(data), iso_path=locations[Path(name).parent] + '/F' + str(index).zfill(7) + '.BIN;1',
                   joliet_path='/' + name)
    iso.add_file(str(args.boot_image), iso_path='/EFIBOOT.IMG;1', joliet_path='/EFIBOOT.IMG')
    iso.add_eltorito('/EFIBOOT.IMG;1', platform_id=0xEF, efi=True, boot_load_size=1)
    assert not args.output.exists()
    iso.write(str(args.output)); iso.close()
    check = pycdlib.PyCdlib(); check.open(str(args.output))
    try:
        for name, expected in files.items():
            recovered = io.BytesIO(); check.get_file_from_iso_fp(recovered, joliet_path='/' + name)
            assert recovered.getvalue() == expected, name
        class HashSink:
            def __init__(self):
                self.hash = hashlib.sha256()
            def write(self, value):
                self.hash.update(value)
                return len(value)
        sink = HashSink()
        check.get_file_from_iso_fp(sink, joliet_path='/EFIBOOT.IMG')
        assert sink.hash.hexdigest() == boot_hash
        assert check.eltorito_boot_catalog is not None
    finally:
        check.close()
    result = {'iso': args.output.name, 'sha256': file_sha(args.output), 'bytes': args.output.stat().st_size,
              'boot': 'UEFI El Torito platform EF, FAT32 boot image', 'payload_files_verified': len(files),
              'setup_source': provenance['setup_source'], 'driver_source': provenance['driver_source'],
              'apple_recovery_included': args.recovery_only, 'static_verification': 'PASS; every setup and FAT image byte read back',
              'runtime': 'not yet boot-tested; no full-install acceptance claimed'}
    args.output.with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


def make_fat(args):
    from pyfatfs.PyFat import PyFat
    from pyfatfs.PyFatFS import PyFatFS
    with args.output.open('xb'):
        pass
    fat = PyFat()
    fat.mkfs(str(args.output), fat_type=PyFat.FAT_TYPE_FAT32,
             size=args.size_mib * 1024 * 1024, label='APPLETAHOE' if args.size_mib > 128 else 'HVBOOT')
    fat.close()
    with PyFatFS(str(args.output)) as fs:
        for path in sorted(args.tree.rglob('*'), key=lambda p: (len(p.parts), p.as_posix())):
            relative = path.relative_to(args.tree).as_posix()
            if path.is_dir():
                fs.makedirs(relative, recreate=True)
            elif path.is_file():
                fs.writebytes(relative, path.read_bytes())
    with PyFatFS(str(args.output), read_only=True) as fs:
        for path in args.tree.rglob('*'):
            if path.is_file():
                assert fs.readbytes(path.relative_to(args.tree).as_posix()) == path.read_bytes()
    print(json.dumps({'fat_image': args.output.name, 'sha256': file_sha(args.output),
                      'verification': 'PASS: every EFI file read back through FAT32 parser; file-only creation'}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='mode', required=True)
    prepare_parser = sub.add_parser('prepare')
    for name in ('source', 'output', 'macserial', 'ocvalidate'):
        prepare_parser.add_argument('--' + name, required=True, type=Path)
    prepare_parser.add_argument('--identity-from', type=Path)
    iso_parser = sub.add_parser('iso')
    for name in ('boot-image', 'setup-zip', 'provenance', 'output'):
        iso_parser.add_argument('--' + name, required=True, type=Path)
    iso_parser.add_argument('--recovery-only', action='store_true')
    fat_parser = sub.add_parser('fat')
    fat_parser.add_argument('--tree', required=True, type=Path)
    fat_parser.add_argument('--output', required=True, type=Path)
    fat_parser.add_argument('--size-mib', type=int, default=128)
    args = parser.parse_args()
    {'prepare': prepare, 'fat': make_fat, 'iso': make_iso}[args.mode](args)


if __name__ == '__main__':
    main()
