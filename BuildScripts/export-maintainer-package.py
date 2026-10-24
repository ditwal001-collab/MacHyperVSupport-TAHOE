"""Export curated patches without Git metadata writes, VM access or raw logs."""
import argparse
import difflib
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import uuid
import zipfile

ROOT = Path(__file__).resolve().parent.parent
BASE = 'cd66095f0d6c099f3498522fdf3edbd4825dbb81'
CI_BASE = '377c2b5a63efd5fab3ead497dc7256b99c74004e'
DEBUG_BASE = '9b80c5f39d67a5c9fd76a9765b8302092c2f250f'
SOURCE_PATHS = [
    'MacHyperVSupport/Controller/HyperVController.hpp',
    'MacHyperVSupport/Controller/HyperVControllerInterrupts.cpp',
]
WORKFLOW = '.github/workflows/main.yml'
PROVENANCE = 'BuildScripts/record-provenance.sh'
DOCS = [
    'CODEX_HANDOFF.md', 'PATCH_PLAN.md', 'REPRODUCE.md',
    'Docs/handoff/SYNIC_EOM_REPORT.md',
    'evidence/OBSERVATIONS.md', 'evidence/RESULTS_LOG.md',
    'Docs/handoff/RESTART.md',
    'evidence/ci/40087952850-compiler-error.md',
    'evidence/ci/run-40090495930.json',
    'evidence/ci/boot-01-0756f1d.json',
    'evidence/ci/boot-01-0756f1d-sanitized.txt',
    'evidence/ci/boot-01-observations.jsonl',
]


def git(*args, allowed=(0,)):
    result = subprocess.run(['git', *args], cwd=ROOT, capture_output=True)
    if result.returncode not in allowed:
        raise RuntimeError(result.stderr.decode('utf-8', errors='replace'))
    return result.stdout


def normalized(data):
    return data.replace(b'\r\n', b'\n')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-root', default='evidence/packages')
    parser.add_argument('--build-run')
    parser.add_argument('--tested-sha')
    parser.add_argument('--build-conclusion', default='UNKNOWN',
                        choices=['UNKNOWN', 'success', 'failure', 'in_progress'])
    args = parser.parse_args()
    if args.build_conclusion == 'success' and not (args.build_run and args.tested_sha):
        parser.error('A successful build requires --build-run and --tested-sha')
    output_root = (ROOT / args.output_root).resolve()
    # All generated data, including the verification tree, stays in this checkout.
    output_root.relative_to(ROOT)
    package = output_root / (
        datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8]
    )
    package.mkdir(parents=True, exist_ok=False)
    patches = [
        ('0001-existing-ci.patch', git('diff', '--binary', BASE, CI_BASE, '--', WORKFLOW)),
        ('0002-existing-diagnostics.patch', git('diff', '--binary', CI_BASE, DEBUG_BASE, '--',
            'MacHyperVSupport/Controller/HyperVControllerInterrupts.cpp',
            'MacHyperVSupport/VMBus/HyperVVMBus.cpp')),
        ('0003-synic-functional.patch', git('diff', '--binary', DEBUG_BASE, '--', *SOURCE_PATHS)),
        ('0004-ci-provenance.patch', git('diff', '--binary', CI_BASE, '--', WORKFLOW, '.gitignore')
            + git('diff', '--no-index', '--', '/dev/null', PROVENANCE, allowed=(1,))),
    ]
    for name, data in patches:
        if not data:
            raise RuntimeError('Empty patch: ' + name)
        (package / name).write_bytes(data)

    # Populate only affected base files. git apply never receives --index.
    verify = package / 'verified-source'
    affected = [WORKFLOW, '.gitignore', *SOURCE_PATHS, 'MacHyperVSupport/VMBus/HyperVVMBus.cpp']
    for path in affected:
        target = verify / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(git('show', BASE + ':' + path))
    relative_verify = verify.relative_to(ROOT).as_posix()
    verification = []
    for name, _ in patches:
        patch = str(package / name)
        git('apply', '--check', '--directory=' + relative_verify, patch)
        git('apply', '--directory=' + relative_verify, patch)
        verification.append(name + ': apply check and application PASS')
    hashes = {}
    for path in [*affected, PROVENANCE]:
        actual = normalized((verify / path).read_bytes())
        expected = normalized((ROOT / path).read_bytes())
        if actual != expected:
            raise RuntimeError('Patched source differs from working tree: ' + path)
        hashes[path] = digest(actual)
    verification.append('Patched files equal normalized working-tree content: PASS')
    # Also offer a source-only alternative with no diagnostic prerequisites.
    # The exact removals deliberately fail if instrumentation changes shape.
    clean_sources = {path: normalized((ROOT / path).read_bytes()) for path in SOURCE_PATHS}
    controller_path = SOURCE_PATHS[1]
    controller = clean_sources[controller_path].decode('utf-8')
    diagnostic_blocks = [
        '  UInt32 currentCpu = cpu_number();\n'
        '  bool pending = _cpuData[cpu].messages[kVMBusInterruptMessage].flags.messagePending;\n\n'
        '  HVDBGLOG("TAHOE-SYNIC: targetCPU=%u currentCPU=%u pending=%u",\n'
        '           cpu, currentCpu, pending ? 1U : 0U);\n\n'
        '  HVDBGLOG("TAHOE-SYNIC: targetCPU=%u currentCPU=%u pending=%u",\n'
        '           cpu, currentCpu, pending ? 1U : 0U);\n',
        '  UInt32 actualCpu = cpu_number();\n',
        '  HVDBGLOG("TAHOE-SYNIC: Writing EOM targetCPU=%u actualCPU=%u",\n'
        '           cpu, actualCpu);\n',
    ]
    for block in diagnostic_blocks:
        if controller.count(block) != 1:
            raise RuntimeError('Diagnostic source changed; review clean export manually')
        controller = controller.replace(block, '')
    clean_sources[controller_path] = controller.encode('utf-8')
    clean_diff = ''
    clean_verify = package / 'verified-clean-source'
    for path, data in clean_sources.items():
        original = git('show', BASE + ':' + path)
        target = clean_verify / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(original)
        clean_diff += 'diff --git a/' + path + ' b/' + path + '\n'
        clean_diff += ''.join(difflib.unified_diff(
            original.decode('utf-8').splitlines(True), data.decode('utf-8').splitlines(True),
            fromfile='a/' + path, tofile='b/' + path))
    clean_patch = package / 'synic-functional-clean.patch'
    clean_patch.write_bytes(clean_diff.encode('utf-8'))
    clean_directory = clean_verify.relative_to(ROOT).as_posix()
    git('apply', '--check', '--directory=' + clean_directory, str(clean_patch))
    git('apply', '--directory=' + clean_directory, str(clean_patch))
    for path, data in clean_sources.items():
        if normalized((clean_verify / path).read_bytes()) != data:
            raise RuntimeError('Clean patch reconstruction failed: ' + path)
    verification.append('Clean source-only patch on pinned base: apply and content PASS')
    (package / 'VERIFICATION.txt').write_text('\n'.join(verification) + '\n', encoding='utf-8')
    for path in DOCS:
        target = package / 'documentation' / path
        target.parent.mkdir(parents=True, exist_ok=True)
        curated = (ROOT / path).read_text(encoding='utf-8')
        curated = curated.replace('srv-maos-devs11', '<test-vm>')
        target.write_bytes(curated.encode('utf-8'))
    (package / 'README.txt').write_text(
        'EXPERIMENTAL SOURCE PACKAGE. NO CONFIRMED RUNTIME FIX.\n'
        'Apply numbered patches in order to base ' + BASE + '.\n'
        '0003 is relative to diagnostic baseline ' + DEBUG_BASE + '.\n'
        'Source/CI working-tree differences, if any, are recorded in manifest.json.\n'
        'Alternative: apply ONLY synic-functional-clean.patch for the source fix\n'
        'without diagnostics on the same base (CI patches can be added separately).\n'
        'Read documentation/REPRODUCE.md and SYNIC_EOM_REPORT.md before building.\n'
        'No raw logs, machine configuration, credentials or Git author metadata included.\n',
        encoding='utf-8')
    manifest = {
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'base': BASE,
        'diagnostic_base': DEBUG_BASE,
        'head': git('rev-parse', 'HEAD').decode().strip(),
        'branch': git('branch', '--show-current').decode().strip(),
        'working_tree_followups_included': bool(git('diff', '--name-only', 'HEAD', '--',
            *SOURCE_PATHS, WORKFLOW, '.gitignore', PROVENANCE).strip()),
        'candidate_run': args.build_run,
        'candidate_run_tested_sha': args.tested_sha,
        'candidate_run_conclusion': args.build_conclusion,
        'vm_test': 'NOT RUN',
        'normalized_source_sha256': hashes,
        'files_sha256': {
            path.relative_to(package).as_posix(): digest(path.read_bytes())
            for path in sorted(package.rglob('*')) if path.is_file()
        },
    }
    (package / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    archive = package.with_suffix('.zip')
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as output:
        for path in sorted(package.rglob('*')):
            if path.is_file():
                output.write(path, path.relative_to(package).as_posix())
    print(package)
    print('ZIP: ' + str(archive))
    print('ZIP SHA256: ' + digest(archive.read_bytes()))
    print('\n'.join(verification))


if __name__ == '__main__':
    main()
