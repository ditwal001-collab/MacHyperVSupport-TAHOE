"""Create a standalone full-install delivery; never accesses Hyper-V or VM disks."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import uuid
import zipfile


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--redaction-file', required=True, type=Path)
    parser.add_argument('--setup-artifact-directory', required=True, type=Path)
    parser.add_argument('--setup-iso', required=True, type=Path)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    script = repo / 'BuildScripts/export-hyperv-maintainer.py'
    spec = importlib.util.spec_from_file_location('maintainer_export', script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    tokens = json.loads(args.redaction_file.read_text(encoding='utf-8-sig'))

    def git(*values):
        return subprocess.check_output(['git', *values], cwd=repo)

    head = git('rev-parse', 'HEAD').decode().strip()
    result = json.loads(subprocess.check_output([
        'py', '-3', str(script), '--redaction-file', str(args.redaction_file),
        '--setup-artifact-directory', str(args.setup_artifact_directory)
    ], cwd=repo, text=True))
    assert result['verification'] == 'PASS'
    original = repo / 'evidence/packages' / result['archive'].removesuffix('.zip')
    tag = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8]
    output = repo / 'evidence/packages' / ('Tahoe-FullInstall-Handoff-' + tag)
    output.mkdir(exist_ok=False)
    shutil.copytree(original, output / 'maintainer')
    shutil.copy2(original / 'documentation/TAHOE_INSTALL_STEP_BY_STEP_DE.md',
                 output / 'HOW_TO_TAHOE_DE.md')
    shutil.copy2(original / 'documentation/FULL_INSTALL_PACKAGE_MAP_DE.md',
                 output / 'WO_IST_WAS.md')

    sources = {}
    def add_source(path, source, data):
        destination = output / 'changed-files' / path
        if destination.exists():
            assert destination.read_bytes() == data, 'Conflicting source: ' + path
            return
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        sources[path] = {'source': source, 'sha256': digest(data)}

    # Actual final files, not only diff hunks. Preserve their original project paths.
    driver_paths = git('diff', '--name-only', module.BASE, module.RC).decode().splitlines()
    for path in driver_paths:
        source = head if path == '.github/workflows/main.yml' else module.RC
        add_source(path, source, git('show', source + ':' + path))
    for path in module.SETUP_PATHS:
        add_source(path, module.SETUP, git('show', module.SETUP + ':' + path))
    for path in module.TOOLS:
        add_source(path, head, (original / 'tools' / Path(path).name).read_bytes())
    for path in module.DOCS:
        if path == 'evidence/RESULTS_LOG.md':
            continue  # Local operational notes are supplied only as a redacted report.
        add_source(path, head, (original / 'documentation' / Path(path).name).read_bytes())

    installer = output / 'installer'
    installer.mkdir()
    setup_zip = original / 'integrated-setup/SetupMedia.zip'
    provenance = json.loads((original / 'integrated-setup/provenance.json').read_text())
    shutil.copy2(setup_zip, installer / 'SetupMedia.zip')
    shutil.copy2(original / 'integrated-setup/provenance.json', installer / 'provenance.json')
    with zipfile.ZipFile(setup_zip) as archive:
        for name in ('MacHyperVSetup.pkg',):
            data = archive.read(name)
            assert digest(data) == provenance['files'][name]
            (installer / name).write_bytes(data)
    # Read back every ISO payload against the unmodified CI ZIP, including file set.
    import pycdlib
    import io
    iso = pycdlib.PyCdlib()
    iso.open(str(args.setup_iso.resolve()))
    try:
        with zipfile.ZipFile(setup_zip) as archive:
            found = set()
            for directory, _, names in iso.walk(joliet_path='/'):
                for name in names:
                    path = directory.rstrip('/') + '/' + name
                    found.add(path.lstrip('/'))
            assert found == set(archive.namelist()), 'ISO has missing/extra payloads'
            for name in archive.namelist():
                actual = io.BytesIO()
                iso.get_file_from_iso_fp(actual, joliet_path='/' + name)
                assert actual.getvalue() == archive.read(name), 'ISO payload mismatch: ' + name
    finally:
        iso.close()
    shutil.copy2(args.setup_iso, installer / 'IntegratedSetup.iso')
    shutil.copytree(original / 'binaries/clean-rc1', output / 'drivers')

    (output / 'CHANGED_FILES.json').write_text(json.dumps({
        'base': module.BASE, 'driver_source': module.RC, 'setup_source': module.SETUP,
        'documentation_tools_source': head,
        'scope': 'Relevant final driver/setup/CI/tools/public documentation files only; '
                 'not a full checkout. Local operational notes and scratch backups excluded.',
        'files': dict(sorted(sources.items()))
    }, indent=2) + '\n', encoding='utf-8')
    # Nested original archives and reports already passed the maintainer export checks.
    for path in (output / 'changed-files').rglob('*'):
        if path.is_file():
            data = path.read_text(encoding='utf-8')
            for token in tokens:
                assert token.lower() not in data.lower(), 'Private token in ' + path.name
            assert not re.search(r'[A-Za-z]:\\|(?:\d{1,3}\.){3}\d{1,3}', data), path.name
    manifest = {'utc': datetime.now(timezone.utc).isoformat(), 'source': head,
                'maintainer_archive': result,
                'verification': 'PASS: source snapshots, pinned CI product, exact ISO readback, '
                                'maintainer patch checks, privacy and ZIP readback',
                'files_sha256': {p.relative_to(output).as_posix(): digest(p.read_bytes())
                                 for p in sorted(output.rglob('*')) if p.is_file()}}
    (output / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    with (output / 'SHA256SUMS.txt').open('w', encoding='utf-8') as handle:
        for name, value in manifest['files_sha256'].items():
            handle.write(value + '  ' + name + '\n')
    archive_path = output.with_suffix('.zip')
    with zipfile.ZipFile(archive_path, 'x', zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(output.rglob('*')):
            if path.is_file():
                archive.write(path, output.name + '/' + path.relative_to(output).as_posix())
    with zipfile.ZipFile(archive_path) as archive:
        assert archive.testzip() is None
        for name, value in manifest['files_sha256'].items():
            assert digest(archive.read(output.name + '/' + name)) == value
    print(json.dumps({'directory': output.name, 'archive': archive_path.name,
                      'sha256': digest(archive_path.read_bytes()),
                      'changed_files': len(sources), 'manifest_entries': len(manifest['files_sha256']),
                      'verification': 'PASS'}, indent=2))


if __name__ == '__main__':
    main()
