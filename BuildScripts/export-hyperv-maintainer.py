"""Export Hyper-V-only source patches, verified CI binaries and curated reports."""
import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import uuid
import zipfile

BASE = 'c48fc5ccade272ec79f633dcb23e45ba1c40d6cc'
RC = '6c3568178ba21136b8c21dd45597476c74ec31d1'
SETUP = '00f70ee358e4d9ddad2fccca39bc19ede1d55365'
SETUP_RUN = 40269870810
SETUP_PATHS = ('Tools/Setup/HyperVSetup.m', 'Tools/Setup/bootstrap.command',
               'Tools/Setup/postinstall', 'BuildScripts/build-integrated-setup.py',
               'BuildScripts/make-integrated-setup-media.py',
               'BuildScripts/install-fresh-framebuffer-25G241.command')
CPU = ('MacHyperVSupport/Controller/HyperVController.hpp',
       'MacHyperVSupport/Controller/HyperVControllerInterrupts.cpp')
GRAPHICS = ('MacHyperVSupport/Graphics/HyperVGraphicsPrivate.cpp',
            'MacHyperVSupport/Graphics/HyperVGraphicsRegs.hpp')
FB = ('MacHyperVFramebuffer/HyperVGraphicsFramebuffer.cpp',
      'MacHyperVFramebuffer/HyperVGraphicsFramebuffer.hpp')
BUILD = ('.github/workflows/main.yml', '.gitignore', 'BuildScripts/record-provenance.sh')
DOCS = ('Docs/handoff/MAINTAINER_DELIVERY.md', 'Docs/handoff/HYPERV_SETUP.md',
        'Docs/handoff/RELEASE_RC1.md', 'Docs/handoff/CURSOR_WORKAROUND.md',
        'Docs/handoff/SYNIC_EOM_REPORT.md', 'Docs/handoff/GRAPHICS_REFRESH_REPORT.md',
        'Docs/handoff/TAHOE_BOOT_RESULT.md', 'Docs/handoff/TAHOE_INSTALL_STEP_BY_STEP_DE.md',
        'Docs/handoff/FRESH_INSTALL_TEST.md', 'Docs/handoff/SRV_CLEAN_INSTALL_512G.md',
        'Docs/handoff/INTEGRATED_SETUP.md', 'Docs/handoff/INTEGRATED_SETUP_REPRODUCE.md',
        'Docs/handoff/APPLE_ACCOUNT_EFI.md', 'Docs/handoff/FULL_INSTALL_PACKAGE_MAP_DE.md',
        'REPRODUCE.md', 'evidence/RESULTS_LOG.md')
TOOLS = ('BuildScripts/export-hyperv-maintainer.py', 'BuildScripts/export-full-install-handoff.py', 'BuildScripts/verify-ci-delivery.py',
         'BuildScripts/collect-hyperv-profile.ps1', 'BuildScripts/summarize-efi-profile.py',
         'BuildScripts/snapshot-serial-log.py', 'BuildScripts/capture-hyperv-serial.py',
         'BuildScripts/capture-hyperv-thumbnail.ps1', 'BuildScripts/new-tahoe-test-vm.ps1',
         'BuildScripts/prepare-tahoe-efi.ps1', 'BuildScripts/enable-tahoe-iservices-patch.py',
         'BuildScripts/inspect-fresh-tahoe.command',
         'BuildScripts/install-fresh-framebuffer-25G241.command',
         'BuildScripts/repair-fresh-framebuffer-path-25G241.command',
         'BuildScripts/make-fresh-framebuffer-media.py')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--redaction-file', required=True, type=Path,
                        help='Local-only JSON array of identifying strings')
    parser.add_argument('--setup-artifact-directory', type=Path,
                        help='Optional verified IntegratedSetup CI artifact (ZIP and provenance)')
    args = parser.parse_args()
    tokens = json.loads(args.redaction_file.read_text(encoding='utf-8-sig'))
    assert isinstance(tokens, list) and all(isinstance(v, str) and v for v in tokens)
    repo = Path(__file__).resolve().parents[1]

    def git(*values):
        return subprocess.check_output(['git', *values], cwd=repo, stderr=subprocess.PIPE)

    def redact(data):
        text = data.decode('utf-8')
        for token in sorted(tokens, key=len, reverse=True):
            text = re.sub(re.escape(token), '<redacted>', text, flags=re.I)
        return text.encode('utf-8')

    tag = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8]
    output = repo / 'evidence/packages' / ('hyperv-maintainer-' + tag)
    output.mkdir(parents=True, exist_ok=False)
    verify = repo / 'evidence/local-tests' / ('release-export-check-' + tag)
    verify.mkdir(parents=True, exist_ok=False)
    base_files = set(git('ls-tree', '-r', '--name-only', BASE).decode().splitlines())
    all_paths = (*CPU, *GRAPHICS, *FB, *BUILD)
    assert set(git('diff', '--name-only', BASE, RC).decode().splitlines()) == set(all_paths)
    for name in all_paths:
        if name in base_files:
            target = verify / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(git('show', BASE + ':' + name))
    patches = output / 'patches'
    patches.mkdir()
    directory = '--directory=' + verify.relative_to(repo).as_posix()
    steps = (
        ('0001-synic-owning-cpu.patch', BASE, RC, CPU),
        ('0002-startergo-refresh.patch', BASE, RC, (GRAPHICS[0],)),
        ('0003-refresh-pacing.patch', BASE, RC, (GRAPHICS[1],)),
        ('0004-opt-in-software-cursor.patch', BASE, RC, FB),
        ('0005-build-provenance.patch', BASE, RC, BUILD),
    )
    for name, old, new, paths in steps:
        patch = patches / name
        patch.write_bytes(git('diff', '--binary', old, new, '--', *paths))
        git('apply', '--check', directory, str(patch))
        git('apply', directory, str(patch))
    for name in all_paths:
        actual = (verify / name).read_bytes().replace(b'\r\n', b'\n')
        expected = git('show', RC + ':' + name).replace(b'\r\n', b'\n')
        assert actual == expected, name
    (output / 'CHANGED_FILES.txt').write_bytes(git('diff', '--name-status', BASE, RC))
    (output / 'ATTRIBUTION.txt').write_text(
        'Base ' + BASE + ' is startergo GraphicsBridge ordering fix; preserve Qonfused credit.\n'
        'Refresh hunk: startergo 3454a80ef6d6e26a3afcdd38a512c559586bd2ba, partial backport.\n'
        'Clean SynIC correction: 7a3b98a on base c48fc5c; CI/provenance c960997.\n'
        'Pacing and opt-in software cursor are separate changes, not the CPU fix.\n'
        'No development-machine application setup is part of this source series.\n', encoding='utf-8')
    reference = output / 'reference'
    reference.mkdir()
    (reference / 'startergo-graphicsbridge-base.patch').write_bytes(
        git('diff', '--binary', BASE + '^', BASE, '--',
            'MacHyperVSupport/GraphicsBridge/HyperVGraphicsBridge.cpp'))
    (reference / 'README.txt').write_text(
        'Historical attribution/reference only. The numbered series starts AT c48fc5c.\n'
        'Do not apply this reference patch on top of that base.\n', encoding='utf-8')
    docs = output / 'documentation'
    docs.mkdir()
    for name in DOCS:
        (docs / Path(name).name).write_bytes(redact((repo / name).read_bytes()))
    evidence = output / 'evidence'
    evidence.mkdir()
    for path in sorted((repo / 'evidence/ci').iterdir()):
        if path.is_file() and path.suffix in ('.json', '.jsonl', '.txt', '.md'):
            assert 'dev-environment' not in path.name
            (evidence / path.name).write_bytes(redact(path.read_bytes()))
    tools = output / 'tools'
    tools.mkdir()
    for name in TOOLS:
        (tools / Path(name).name).write_bytes((repo / name).read_bytes())
    installer = repo / 'evidence/local-tests/release-rc1-test-20261025-01/files/InstallAux.command'
    (tools / 'InstallAux-example.command').write_bytes(installer.read_bytes())
    shutil.copyfile(repo / 'LICENSE.txt', output / 'LICENSE.txt')
    builds = []
    for label, folder, source, run in (
        ('instrumented-synic-reference', 'run-40090495930-artifacts',
         '0756f1d75601f0c24bce98ae4adf8c83ce6e3307', 40090495930),
        ('overnight-instrumented-reference', 'run-40139181101-cursor-artifacts',
         'c9eb980daab9598b1af6732217147490dacceb3e', 40139181101),
        ('clean-rc1', 'run-40189441511-clean-rc1-artifacts', RC, 40189441511),
    ):
        root = repo / 'evidence/local-tests' / folder
        prov = root / 'Provenance'
        env = (prov / 'environment.txt').read_text()
        assert 'source=' + source + '\n' in env and 'run=' + str(run) + ' ' in env
        hashes = dict()
        for line in (prov / 'build-sha256.txt').read_text().splitlines():
            digest, name = line.split(None, 1)
            hashes[name.strip()] = digest
        destination = output / 'binaries' / label
        destination.mkdir(parents=True)
        records = {}
        for config in ('Debug', 'Release'):
            archive = next((root / 'Artifacts' / config).glob('MacHyperVSupport-*.zip'))
            assert sha(archive.read_bytes()) == hashes['build/' + config + '/' + archive.name]
            with zipfile.ZipFile(archive) as package:
                for name in package.namelist():
                    if '/Contents/MacOS/' in name and not name.endswith('/'):
                        suffix = name.split('Kexts/', 1)[-1]
                        matches = [key for key in hashes if key.startswith('build/' + config + '/')
                                   and key.endswith(suffix)]
                        assert matches and all(sha(package.read(name)) == hashes[key] for key in matches)
            shutil.copyfile(archive, destination / archive.name)
            records[config] = sha(archive.read_bytes())
        shutil.copytree(prov, destination / 'Provenance')
        builds.append({'variant': label, 'source': source, 'run': run, 'packages_sha256': records})
    integrated = None
    if args.setup_artifact_directory:
        source_artifact = args.setup_artifact_directory
        provenance_bytes = (source_artifact / 'provenance.json').read_bytes()
        provenance = json.loads(provenance_bytes)
        assert provenance['setup_source'] == SETUP
        assert provenance['driver_source'] == RC and provenance['driver_run'] == 40189441511
        assert str(provenance['run']) == str(SETUP_RUN)
        setup_zip = (source_artifact / 'SetupMedia.zip').read_bytes()
        assert sha(setup_zip) == provenance['setup_media_sha256']
        with zipfile.ZipFile(io.BytesIO(setup_zip)) as media:
            names = media.namelist()
            assert len(names) == len(set(names))
            assert set(names) == set(provenance['files']) | {'payload.sha256'}
            for name, expected in provenance['files'].items():
                assert sha(media.read(name)) == expected, name
            assert 'Seed.command' not in names
        setup = output / 'integrated-setup'
        setup.mkdir()
        (setup / 'SetupMedia.zip').write_bytes(setup_zip)
        (setup / 'provenance.json').write_bytes(provenance_bytes)
        patch = setup / '0006-integrated-setup-optional.patch'
        patch.write_bytes(git('diff', '--binary', RC, SETUP, '--', *SETUP_PATHS))
        # Verify this separate add-on AFTER the unchanged five driver patches.
        rc_paths = set(git('ls-tree', '-r', '--name-only', RC).decode().splitlines())
        for name in SETUP_PATHS:
            if name in rc_paths and not (verify / name).exists():
                target = verify / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(git('show', RC + ':' + name))
        git('apply', '--check', directory, str(patch))
        git('apply', directory, str(patch))
        for name in SETUP_PATHS:
            assert (verify / name).read_bytes().replace(b'\r\n', b'\n') == git(
                'show', SETUP + ':' + name).replace(b'\r\n', b'\n'), name
        (setup / 'CHANGED_FILES.txt').write_bytes(git('diff', '--name-status', RC, SETUP, '--', *SETUP_PATHS))
        (setup / 'README.txt').write_text(
            'OPTIONAL guest installation tooling; not part of the five driver patches.\n'
            'Apply 0006 only after 0001-0005, or to clean candidate ' + RC + '.\n'
            'Six setup/build files reconstruct the tested source subset at ' + SETUP + '.\n'
            'The GitHub setup-only workflow is available in that original commit;\n'
            'it is deliberately not mixed into the driver CI patch.\n'
            'For a local macOS build run: python3 BuildScripts/build-integrated-setup.py\n'
            '  --release-zip ORIGINAL_CI_RELEASE_ZIP --output-directory NEW_DIRECTORY\n'
            'Requires existing upstream Tools/Daemons and Shutdown user-client header,\n'
            'both already present at the driver baseline. Record any new build identity.\n'
            'Original CI SetupMedia.zip and provenance are unmodified. Read current\n'
            'INTEGRATED_SETUP and INTEGRATED_SETUP_REPRODUCE before use.\n'
            'Qualified fresh-APFS pass: automatic drivers/display plus reboot persistence;\n'
            'final Apple Setup wait still required regular shutdown/start. Previous\n'
            'native extension approval may persist with the retained VM firmware.\n'
            'No failed Recovery Seed, Apple payload, private EFI or credentials shipped.\n', encoding='utf-8')
        integrated = {'source': SETUP, 'run': SETUP_RUN,
                      'setup_media_sha256': sha(setup_zip),
                      'product_sha256': provenance['files']['MacHyperVSetup.pkg'],
                      'source_subset': list(SETUP_PATHS),
                      'verification': 'Exact CI payload hashes and optional patch reconstruction PASS'}
    (output / 'README.txt').write_text(
        'Read documentation/MAINTAINER_DELIVERY.md, HYPERV_SETUP.md and RELEASE_RC1.md.\n'
        'Numbered clean source series applies to ' + BASE + '.\n'
        'Historical instrumented binaries are references; runtime scope is in the reports.\n'
        'Original CI archives are unmodified. Verify hashes before choosing a candidate.\n'
        'InstallAux-example is a guarded guest-specific example, not a universal installer.\n'
        'Optional integrated-setup/ contains separately pinned setup tooling when requested.\n'
        'No VM disks, full EFI configs, raw logs, personal screenshots or Apple KDK payload.\n', encoding='utf-8')
    forbidden = (b'DEV_ENVIRONMENT', b'IOSDevSmoke', b'csdevkit', b'10.0.402',
                 b'1.143.1', b'setup-dev-environment.command', b'verify-ios-simulator.command')

    def check(data):
        for token in tokens:
            assert token.encode().lower() not in data.lower(), 'Private token in delivery'
        assert all(token.lower() not in data.lower() for token in forbidden), 'Out-of-scope setup content'
        if data.startswith(b'PK\x03\x04'):
            with zipfile.ZipFile(io.BytesIO(data)) as nested:
                for entry in nested.namelist():
                    if not entry.endswith('/'):
                        check(nested.read(entry))

    for path in output.rglob('*'):
        if path.is_file():
            # The exporter contains its own exclusion vocabulary; it is code,
            # not application setup content. All other files are strictly scanned.
            data = path.read_bytes()
            if path == tools / Path(__file__).name:
                for token in tokens:
                    assert token.encode().lower() not in data.lower()
            else:
                check(data)
    manifest = {'created_utc': datetime.now(timezone.utc).isoformat(),
                'base': BASE, 'clean_candidate': RC, 'builds': builds,
                'integrated_setup': integrated,
                'documentation_head': git('rev-parse', 'HEAD').decode().strip(),
                'verification': 'Patch application/reconstruction, CI hashes, privacy and scope checks PASS',
                'files_sha256': {p.relative_to(output).as_posix(): sha(p.read_bytes())
                                 for p in sorted(output.rglob('*')) if p.is_file()}}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    archive = output.with_suffix('.zip')
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED) as package:
        for path in sorted(output.rglob('*')):
            if path.is_file():
                package.write(path, path.relative_to(output).as_posix())
    with zipfile.ZipFile(archive) as package:
        for name, digest in manifest['files_sha256'].items():
            assert sha(package.read(name)) == digest, name
    result = {'archive': archive.name, 'sha256': sha(archive.read_bytes()),
              'manifest_entries': len(manifest['files_sha256']), 'verification': 'PASS'}
    archive.with_suffix('.delivery.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
