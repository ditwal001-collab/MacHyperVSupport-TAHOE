"""Assemble verified CI ZIPs and source exports; no VM or disk-image access."""
import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import uuid
import zipfile


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cpu-package', required=True, type=Path)
    parser.add_argument('--graphics-package', required=True, type=Path)
    parser.add_argument('--private-token', action='append', default=[])
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    tag = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8]
    output = repo / 'evidence/packages' / ('maintainer-' + tag)
    output.mkdir(parents=True, exist_ok=False)
    for label, source in [('synic-source', args.cpu_package), ('optional-graphics-source', args.graphics_package)]:
        with zipfile.ZipFile(source) as archive:
            manifest = json.loads(archive.read('manifest.json'))
            assert manifest['base'] == 'c48fc5ccade272ec79f633dcb23e45ba1c40d6cc'
            for name, expected in manifest['files_sha256'].items():
                assert sha(archive.read(name)) == expected, name
        shutil.copyfile(source, output / (label + '.zip'))
    variants = [
        ('synic-instrumented', 'run-40090495930-artifacts', 40090495930,
         '0756f1d75601f0c24bce98ae4adf8c83ce6e3307'),
        ('combined-cursor', 'run-40139181101-cursor-artifacts', 40139181101,
         'c9eb980daab9598b1af6732217147490dacceb3e'),
    ]
    build_records = []
    for label, folder, run, source in variants:
        artifact = repo / 'evidence/local-tests' / folder
        provenance = artifact / 'Provenance'
        environment = (provenance / 'environment.txt').read_text()
        assert 'source=' + source in environment and 'run=' + str(run) + ' ' in environment
        expected = {}
        for line in (provenance / 'build-sha256.txt').read_text().splitlines():
            digest, name = line.split(None, 1)
            expected[name.strip()] = digest
        target = output / 'binaries' / label
        target.mkdir(parents=True)
        packages = {}
        for configuration in ('Debug', 'Release'):
            archive = next((artifact / 'Artifacts' / configuration).glob('MacHyperVSupport-*.zip'))
            data = archive.read_bytes()
            digest = sha(data)
            assert digest == expected['build/' + configuration + '/' + archive.name]
            with zipfile.ZipFile(io.BytesIO(data)) as package:
                for name in package.namelist():
                    if '/Contents/MacOS/' in name and not name.endswith('/'):
                        relative = name.split('Kexts/', 1)[-1]
                        key = 'build/' + configuration + '/' + relative
                        if key not in expected:
                            matches = [k for k in expected if k.startswith('build/' + configuration + '/') and k.endswith(relative)]
                            assert matches, name
                            key = matches[0]
                        assert sha(package.read(name)) == expected[key], name
            shutil.copyfile(archive, target / archive.name)
            packages[configuration] = digest
        shutil.copytree(provenance, target / 'Provenance')
        build_records.append({'variant': label, 'source': source, 'run': run,
                              'packages_sha256': packages, 'runtime': 'Debug observations only; Release not runtime validated'})
    docs = output / 'documentation'
    docs.mkdir()
    for name in ('Docs/handoff/MAINTAINER_DELIVERY.md', 'Docs/handoff/CURSOR_WORKAROUND.md',
                 'Docs/handoff/SYNIC_EOM_REPORT.md', 'REPRODUCE.md', 'evidence/RESULTS_LOG.md'):
        text = (repo / name).read_text(encoding='utf-8')
        for token in args.private_token:
            text = text.replace(token, '<redacted>')
        (docs / Path(name).name).write_text(text, encoding='utf-8')
    tools = output / 'tools'
    tools.mkdir()
    for name in ('BuildScripts/export-tested-delivery.py', 'BuildScripts/snapshot-serial-log.py'):
        shutil.copyfile(repo / name, tools / Path(name).name)
    installer = repo / 'evidence/local-tests/cursor-aux-install-20261025-01/files/InstallAux.command'
    shutil.copyfile(installer, tools / installer.name)
    shutil.copyfile(repo / 'LICENSE.txt', output / 'LICENSE.txt')
    changed = subprocess.check_output(['git', 'diff', '--name-status',
        'c48fc5ccade272ec79f633dcb23e45ba1c40d6cc', 'c9eb980daab9598b1af6732217147490dacceb3e', '--',
        'MacHyperVSupport', 'MacHyperVFramebuffer', '.github/workflows/main.yml', 'BuildScripts/record-provenance.sh'], cwd=repo)
    (output / 'CHANGED_FILES.txt').write_bytes(changed)
    (output / 'README.txt').write_text(
        'Start with documentation/MAINTAINER_DELIVERY.md.\n'
        'Source-only SynIC patches and separate optional graphics/cursor patches.\n'
        'Original CI Debug/Release ZIPs plus provenance; verify manifest hashes.\n'
        'Combined software cursor: one positive short Debug run, not stable Release acceptance.\n'
        'InstallAux.command is a guarded guest-specific example, not a universal installer.\n'
        'No raw logs, personal images, config, VM disks or Apple KDK payload.\n', encoding='utf-8')

    def check_private(data):
        for token in args.private_token:
            assert token.lower().encode() not in data.lower(), 'Private token found in delivery'
        if data.startswith(b'PK\x03\x04'):
            with zipfile.ZipFile(io.BytesIO(data)) as nested:
                for entry in nested.namelist():
                    if not entry.endswith('/'):
                        check_private(nested.read(entry))

    for path in output.rglob('*'):
        if path.is_file():
            check_private(path.read_bytes())
    manifest = {'created_utc': datetime.now(timezone.utc).isoformat(),
                'documentation_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo).decode().strip(),
                'builds': build_records, 'nested_hashes_and_privacy_checks': 'PASS',
                'files_sha256': {p.relative_to(output).as_posix(): sha(p.read_bytes())
                                 for p in sorted(output.rglob('*')) if p.is_file()}}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    archive = output.with_suffix('.zip')
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED) as package:
        for path in sorted(output.rglob('*')):
            if path.is_file():
                package.write(path, path.relative_to(output).as_posix())
    with zipfile.ZipFile(archive) as package:
        for name, digest in manifest['files_sha256'].items():
            assert sha(package.read(name)) == digest, name
    record = {'archive': archive.name, 'sha256': sha(archive.read_bytes()),
              'manifest_entries': len(manifest['files_sha256']), 'verification': 'PASS'}
    archive.with_suffix('.delivery.json').write_text(json.dumps(record, indent=2))
    print(archive)
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
