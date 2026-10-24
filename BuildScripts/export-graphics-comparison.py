"""Export separate graphics patches; never access a VM or disk image."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import uuid
import zipfile

BASE = 'c48fc5ccade272ec79f633dcb23e45ba1c40d6cc'
REFRESH = '3d31e1107d097f2a3eee4683e89d7d8678a76708'
PACING = 'e17098263de44ac71251bcd31caea999e050221e'
FILES = ('MacHyperVSupport/Graphics/HyperVGraphicsPrivate.cpp',
         'MacHyperVSupport/Graphics/HyperVGraphicsRegs.hpp')
DOCS = ('Docs/handoff/GRAPHICS_REFRESH_REPORT.md',
        'evidence/ci/display-01-3d31e11.json',
        'evidence/ci/display-02-pacing-pending.json',
        'evidence/ci/run-40101047189-verified.json',
        'evidence/ci/run-40124452997-verified.json')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--private-vm-name', default=None)
    args = parser.parse_args()
    repo = args.repo.resolve()

    def git(*arguments):
        return subprocess.check_output(['git', *arguments], cwd=repo, stderr=subprocess.PIPE)

    tag = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8]
    package = repo / 'evidence/packages' / ('graphics-' + tag)
    package.mkdir(parents=True, exist_ok=False)
    verify = repo / 'evidence/local-tests' / ('graphics-export-check-' + tag)
    verify.mkdir(parents=True, exist_ok=False)
    for name in FILES:
        target = verify / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as output:
            output.write(git('show', BASE + ':' + name))
    messages = []
    for old, new, names, patch_name in (
        (BASE, REFRESH, (FILES[0],), '0001-startergo-refresh.patch'),
        (REFRESH, PACING, (FILES[1],), '0002-pacing-experiment.patch'),
    ):
        patch = package / patch_name
        with patch.open('xb') as output:
            output.write(git('diff', '--binary', old, new, '--', *names))
        directory = '--directory=' + verify.relative_to(repo).as_posix()
        git('apply', '--check', directory, str(patch))
        git('apply', directory, str(patch))
        for name in names:
            assert (verify / name).read_bytes().replace(b'\r\n', b'\n') == git('show', new + ':' + name).replace(b'\r\n', b'\n'), name
        messages.append(patch_name + ': apply/check/reconstruction PASS')
    for name in FILES:
        assert (verify / name).read_bytes().replace(b'\r\n', b'\n') == git('show', PACING + ':' + name).replace(b'\r\n', b'\n'), name
    for name in DOCS:
        target = package / 'documentation' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        content = (repo / name).read_text(encoding='utf-8')
        if args.private_vm_name:
            content = content.replace(args.private_vm_name, '<test-vm>')
        target.write_text(content, encoding='utf-8')
    tools = package / 'tools'
    tools.mkdir()
    (tools / Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    (package / 'README.txt').write_text(
        'OPTIONAL GRAPHICS COMPARISON; NOT A SYNIC PATCH REPLACEMENT.\n'
        'Base: ' + BASE + '. Apply 0001 alongside the separate SynIC source series.\n'
        '0001 is ONLY the refresh-timer hunk from startergo 3454a80ef6d6e26a3afcdd38a512c559586bd2ba.\n'
        'Original author startergo and author date retained in source commit ' + REFRESH + '.\n'
        'The credited c48fc5c GraphicsBridge baseline is preserved.\n'
        '0002 is a separate 10 -> 33 ms experiment; runtime improvement NOT established.\n'
        'Builds contain the SynIC candidate; these two patches themselves do not add it.\n'
        'Refresh build 40101047189: user confirmed restored visible input; slow pointer remains.\n'
        'Pacing build 40124452997: build/hash checks PASS; runtime needs local start/unlock.\n'
        'No raw logs, login images, configuration or disk images included.\n'
        'To regenerate using bundled tool: python tools/export-graphics-comparison.py --repo REPO_PATH\n',
        encoding='utf-8')
    (package / 'VERIFICATION.txt').write_text('\n'.join(messages) + '\n', encoding='utf-8')
    manifest = dict(base=BASE, refresh_source=REFRESH, pacing_source=PACING,
                    created_utc=datetime.now(timezone.utc).isoformat(),
                    refresh_run=40101047189, pacing_run=40124452997,
                    pacing_runtime='NOT VALIDATED; LOCAL UNLOCK REQUIRED',
                    files_sha256={p.relative_to(package).as_posix(): digest(p.read_bytes())
                                  for p in sorted(package.rglob('*')) if p.is_file()})
    (package / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    archive = package.with_suffix('.zip')
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as output:
        for path in sorted(package.rglob('*')):
            if path.is_file():
                output.write(path, path.relative_to(package).as_posix())
    print(archive)
    print('SHA256: ' + digest(archive.read_bytes()))
    print('\n'.join(messages))


if __name__ == '__main__':
    main()
