# Reproduce source, build and runtime checks

See [the technical report](Docs/handoff/SYNIC_EOM_REPORT.md) before applying.
The exported patch series uses base
`cd66095f0d6c099f3498522fdf3edbd4825dbb81`. It already includes the credited
GraphicsBridge commit `c48fc5ccade272ec79f633dcb23e45ba1c40d6cc`.

Run `BuildScripts/export-maintainer-package.ps1` in PowerShell. It creates a new
timestamped directory under `evidence/packages`, refuses to overwrite one,
exports source-only patches and a manifest, and verifies patch application in
an isolated temporary source tree. It never accesses a VM or disk image.
The functional patch is relative to the instrumented baseline; apply the
separate diagnostic prerequisite first. Any uncommitted source/CI follow-ups
are recorded in the manifest. Review before committing.
If host policy requires signed PowerShell scripts, leave that policy intact
and invoke the Python entry point directly:
`py -3 BuildScripts/export-maintainer-package.py`.

The ZIP also includes `synic-functional-clean.patch`, an alternative source-only
patch against the same base with the diagnostic code removed. Apply this patch
alone instead of 0002/0003 for the clean candidate. CI patches are independent.
The exporter verifies this variant separately; it has not been compiled or
tested in a VM.

On a fresh clone checked out at the pinned base:

```text
git apply --check 0001-existing-ci.patch
git apply 0001-existing-ci.patch
git apply 0002-existing-diagnostics.patch
git apply 0003-synic-functional.patch
git apply 0004-ci-provenance.patch
```

Patch 0004 also adds the provenance script. It pins MacKernelSDK and ocbuild,
uses the checksum-verified Lilu 1.7.2 Debug SDK, and records environment and
binary hashes. This adaptation passed in run `40090495930`. Hosted runner images,
action version tags and transitive legacy tool downloads remain reproducibility
limits; this is not a bit-for-bit build guarantee.

After repository/network permissions permit, commit follow-ups separately,
push the functional branch to remote `tahoe`, and inspect the run for that exact
SHA. The workflow's push trigger starts the build; do not create a release.
Use `gh run view RUN --repo ditwal001-collab/MacHyperVSupport-TAHOE --log-failed`
for failures. Download `Artifacts` and `Provenance` into a new directory, record
artifact digest, ZIP SHA256 and the Monterey kext executable SHA256 for each
configuration. Confirm source SHA, branch and successful build before proposing
installation. Windows local syntax/patch checks cannot replace Xcode builds.

The user explicitly authorized autonomous tests on `srv-maos-devs11` after
restart and required serial capture. This authorization remains limited to
that VM. Check current upgrade health before lifecycle changes. Disk work
requires VM Off, detached target disks and verified unique backups.
Record an EFI configuration hash without publishing identifying configuration.
Start serial capture before each approved boot. Keep CPU topology, OpenCore,
ACPI, other kexts and storage layout constant.

The first test uses a separate EFI copy, leaving the original EFI unchanged.
Its original kext is backed up separately; only the candidate executable differs
after replacement. Before starting the VM, ensure the test EFI is host-unmounted,
attached in the original SCSI slot and the receiver is running. Use
`BuildScripts/capture-test-serial.py --output NEW_DIRECTORY`; it refuses an
existing ready-file, creates unique log files and reconnects across guest
restarts. Raw logs, EFI copies and downloaded binaries live in ignored
`evidence/local-tests/`; they must not be added to Git. Do not delete an EFI
test copy while it remains attached to the VM. An active upgrade takes priority
over repeated-boot trials.

| Variant | Minimum attempts | Required evidence |
|---|---:|---|
| Identical instrumentation, original EOM | 5 | Every failure and success, storage/root outcome |
| Identical instrumentation, corrected EOM | 10 | Every EOM target matches sampled actual CPU; scan, SCSI, APFS root, login |
| Final release with diagnostic changes removed | 10 | Equivalent boot success, network, sustained I/O, authorized restart/shutdown |

Do not deliberately reproduce a known graphics panic on the upgrade VM.
Inspect existing panic evidence instead. Release without diagnostics must be
built from a separately reviewed source state: merely choosing Release disables
HVDBGLOG output but does not remove every diagnostic code change.
