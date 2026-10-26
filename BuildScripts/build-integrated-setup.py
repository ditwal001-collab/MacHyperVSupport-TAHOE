"""Build the integrated Intel25G241 first-boot setup from a pinned Release ZIP.

Run on macOS with Xcode command-line tools. Never operates on a VM or disk image.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import plistlib
import shutil
import subprocess
import zipfile

RELEASE_SHA = '162f47670ef9f4640bdfdefd8ba9495b1a039ca6828a52f5ec4498e9d3cb5d6c'
FB_SHA = 'd8a079d47d61988aabe40cb788b015979c27384135b57339e854d5c017792122'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release-zip', type=Path, required=True)
    parser.add_argument('--output-directory', type=Path, required=True)
    args = parser.parse_args()
    if digest(args.release_zip.read_bytes()) != RELEASE_SHA:
        raise SystemExit('Unexpected driver Release ZIP')
    repo = Path(__file__).resolve().parents[1]
    output = args.output_directory.resolve()
    output.mkdir(parents=True, exist_ok=False)
    stage = output / 'media'
    payload = stage / 'Payload'
    payload.mkdir(parents=True)
    with zipfile.ZipFile(args.release_zip) as release:
        with zipfile.ZipFile(payload / 'Framebuffer.zip', 'x', zipfile.ZIP_DEFLATED) as target:
            for name in release.namelist():
                if 'MacHyperVFramebuffer.kext/' in name and not name.endswith('/'):
                    suffix = name.split('MacHyperVFramebuffer.kext/', 1)[1]
                    if '..' in Path(suffix).parts or suffix.startswith('/'):
                        raise SystemExit('Unsafe bundle member')
                    data = release.read(name)
                    if suffix == 'Contents/MacOS/MacHyperVFramebuffer' and digest(data) != FB_SHA:
                        raise SystemExit('Unexpected framebuffer executable')
                    info = zipfile.ZipInfo('MacHyperVFramebuffer.kext/' + suffix, (1980, 1, 1, 0, 0, 0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    target.writestr(info, data)
    with zipfile.ZipFile(payload / 'Framebuffer.zip') as bundle:
        assert digest(bundle.read('MacHyperVFramebuffer.kext/Contents/MacOS/MacHyperVFramebuffer')) == FB_SHA
    (payload / 'Install.command').write_bytes((repo / 'BuildScripts/install-fresh-framebuffer-25G241.command').read_bytes().replace(b'\r\n', b'\n'))
    for name in ('bootstrap.command', 'Seed.command'):
        (stage / name).write_bytes((repo / 'Tools/Setup' / name).read_bytes().replace(b'\r\n', b'\n'))
        (stage / name).chmod(0o755)
    app = stage / 'MacHyperVSetup.app/Contents'
    (app / 'MacOS').mkdir(parents=True)
    (app / 'Info.plist').write_bytes(plistlib.dumps({
        'CFBundleIdentifier': 'fish.goldfish64.MacHyperVSetup',
        'CFBundleExecutable': 'MacHyperVSetup', 'CFBundleName': 'Hyper-V Setup',
        'CFBundlePackageType': 'APPL', 'CFBundleShortVersionString': '1.0',
        'CFBundleVersion': '1', 'LSMinimumSystemVersion': '12.0',
        'NSHighResolutionCapable': True,
    }))
    subprocess.run(['clang', '-arch', 'x86_64', '-fobjc-arc', '-mmacosx-version-min=12.0',
                    '-framework', 'Cocoa', '-framework', 'CoreGraphics',
                    str(repo / 'Tools/Setup/HyperVSetup.m'), '-o', str(app / 'MacOS/MacHyperVSetup')], check=True)
    subprocess.run(['codesign', '--force', '--sign', '-', '--timestamp=none', str(app.parent)], check=True)
    subprocess.run(['codesign', '--verify', '--deep', '--strict', str(app.parent)], check=True)
    subprocess.run([str(app / 'MacOS/MacHyperVSetup'), '--help'], check=True)
    daemon = stage / 'hvshutdownd'
    subprocess.run(['clang', '-arch', 'x86_64', '-std=gnu11', '-mmacosx-version-min=12.0',
                    '-include', 'stdarg.h', '-include', 'unistd.h',
                    '-include', 'CoreFoundation/CoreFoundation.h',
                    '-I' + str(repo / 'Tools/Daemons'),
                    '-I' + str(repo / 'MacHyperVSupport/IntegrationComponents/Shutdown'),
                    str(repo / 'Tools/Daemons/hvshutdownd/hvshutdownd.c'),
                    str(repo / 'Tools/Daemons/hviokit.c'),
                    '-framework', 'IOKit', '-framework', 'CoreFoundation', '-o', str(daemon)], check=True)
    subprocess.run(['codesign', '--force', '--sign', '-', '--timestamp=none', str(daemon)], check=True)
    shutil.copyfile(repo / 'Tools/Daemons/hvshutdownd/fish.goldfish64.hvshutdownd.plist',
                    stage / 'fish.goldfish64.hvshutdownd.plist')
    plists = {
        'fish.goldfish64.hyperv-setup': {
            'ProgramArguments': ['/bin/bash', '/Library/Application Support/MacHyperVSetup/bootstrap.command'],
            'RunAtLoad': True, 'StartInterval': 60,
        },
        'fish.goldfish64.hyperv-setup-ui': {
            'ProgramArguments': ['/Applications/MacHyperVSetup.app/Contents/MacOS/MacHyperVSetup'],
            'RunAtLoad': True, 'LimitLoadToSessionType': 'Aqua',
        },
    }
    for label, properties in plists.items():
        (stage / (label + '.plist')).write_bytes(plistlib.dumps({'Label': label, **properties}))
    source = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo, text=True).strip()
    provenance = {'setup_source': source, 'driver_source': '6c3568178ba21136b8c21dd45597476c74ec31d1',
                  'driver_run': 40189441511, 'driver_release_sha256': RELEASE_SHA,
                  'framebuffer_sha256': FB_SHA, 'target_build': '25G241',
                  'target_resolution': [1920, 1080], 'run': os.environ.get('GITHUB_RUN_ID'),
                  'xcode': subprocess.check_output(['xcodebuild', '-version'], text=True).strip(),
                  'sdk': subprocess.check_output(['xcrun', '--show-sdk-version'], text=True).strip()}
    for binary in (app / 'MacOS/MacHyperVSetup', daemon):
        assert subprocess.check_output(['lipo', '-archs', str(binary)], text=True).strip() == 'x86_64'
    (stage / 'provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
    files = {p.relative_to(stage).as_posix(): digest(p.read_bytes())
             for p in sorted(stage.rglob('*')) if p.is_file()}
    (stage / 'payload.sha256').write_text(''.join(value + '  ' + name + '\n' for name, value in files.items()))
    with zipfile.ZipFile(output / 'SetupMedia.zip', 'x', zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(stage.rglob('*')):
            if path.is_file():
                archive.write(path, path.relative_to(stage).as_posix())
    (output / 'provenance.json').write_text(json.dumps({**provenance,
        'setup_media_sha256': digest((output / 'SetupMedia.zip').read_bytes()), 'files': files}, indent=2) + '\n')


if __name__ == '__main__':
    main()
