# Maintainer delivery and project map

This delivery includes source patches AND the original CI binary ZIPs. Do not
reconstruct provenance from a copied executable alone. Check each ZIP/hash,
source commit, run and configuration identity before installation. All binaries
are candidates; only the explicitly recorded Debug runs have runtime evidence.

## Project structure and changed files

```text
MacHyperVSupport/
  Controller/HyperVController.hpp             EOM affinity declarations/diagnostics
  Controller/HyperVControllerInterrupts.cpp   CPU-local EOM functional correction
  VMBus/HyperVVMBus.cpp                       enumeration instrumentation
  Graphics/HyperVGraphicsPrivate.cpp          separate startergo refresh hunk
  Graphics/HyperVGraphicsRegs.hpp             separate 33-ms pacing comparison
MacHyperVFramebuffer/
  HyperVGraphicsFramebuffer.cpp               optional software cursor capability
  HyperVGraphicsFramebuffer.hpp               per-instance comparison flag
.github/workflows/main.yml                    pinned build/provenance workflow
BuildScripts/record-provenance.sh             build inputs, ZIPs and binary hashes
BuildScripts/snapshot-serial-log.py           read-only live-log prefix snapshots
Docs/handoff/                                reports and operating handoff
evidence/ci/                                 curated anonymized test evidence
```

The exported patch files contain only the relevant changed source/CI files,
not a full duplicate checkout. Documentation and verification manifests are
provided separately. Original base is
`c48fc5ccade272ec79f633dcb23e45ba1c40d6cc`, the startergo GraphicsBridge fix;
preserve its original attribution and Qonfused credit. The refresh backport
also retains startergo attribution from3454a80 and source commit3d31e11.

## Reproduce source and builds

Use a fresh checkout at that base. Apply the CPU export's numbered0001-0004
patches in order with `git apply --check` followed by `git apply`. An alternative
clean functional patch excludes instrumentation; follow REPRODUCE.md rather than
applying both functional variants. Apply optional graphics0001-0003 separately
for the combined graphics/cursor comparison. Their scope excludes the CPU fix.
Every series was application-checked and reconstructed against the pinned source.

Pinned source/run mapping:

| Variant | Source | Actions run | Runtime scope |
| --- | --- | --- | --- |
| Instrumented SynIC |0756f1d75601f0c24bce98ae4adf8c83ce6e3307|40090495930|recorded enumeration/GUI tests|
| Clean SynIC build |c960997 (clean-c48 branch)|40093339256|build only|
| Refresh backport |3d31e1107d097f2a3eee4683e89d7d8678a76708|40101047189|visible input restored; slow mouse|
|33-ms pacing |e17098263de44ac71251bcd31caea999e050221e|40124452997|user reports faster mouse|
| Combined optional cursor |c9eb980daab9598b1af6732217147490dacceb3e|40139181101|one positive short Debug software-cursor test|

The GitHub Actions workflow builds Debug/Release and runs both Clang analyses.
It uses macos-15-intel/Xcode16.4, pinned MacKernelSDK and ocbuild, and a
checksum-verified Lilu1.7.2 Debug SDK. Exact pins and dependency hashes are in
REPRODUCE.md, the workflow and each included Provenance directory. Hosted images
and remaining transitive downloads prevent a bit-identical rebuild guarantee.
To repeat the combined build in the existing repository:

```sh
gh workflow run main.yml --ref test/tahoe-software-cursor
gh run view 40139181101
gh run download 40139181101 --dir downloaded-build
```

A new run has a new identity: verify its source and uploaded provenance anew.
The delivery contains original Debug/Release ZIPs for the tested instrumented
SynIC source and combined cursor source; do not mix their core executables.
The combined Debug core is803a3d24...; its separate framebuffer is310f155f... .

## Install, test and roll back

1. Inventory actual loaded modules, existing Aux contents, hashes and boot args.
   Keep an exclusive verified backup and a known bootable prior EFI image.
2. For the core, replace only the appropriate Monterey executable on a backed-up,
   Off/detached EFI TEST copy. Verify config and binary identity before attach.
3. The framebuffer is a separate /Library/Extensions component on this system.
   Follow CURSOR_WORKAROUND.md and the guarded guest procedure; do not enable
   unsupported injection or replace the entire package indiscriminately.
4. Preserve all existing Aux module IDs/other versions. The tested Aux procedure
   explicitly reads existing Boot/System collections and rebuilds only Aux.
   It does not unseal the system or change SIP/security settings.
5. Append `-hvgfxfbswcursor` only for the optional comparison. Verify the serial
   activation marker, loaded component and input behavior after boot. Test
   Downloads/Finder and Safari as reported, then longer sessions and repeat boots.
6. For rollback restore saved bundle/Aux and appropriate boot-cache state, verify
   hashes, and select the preserved EFI. Never overwrite backups or force a
   shutdown during an active installer. Review any failed cache build before reboot.

The guest-specific guarded InstallAux.command is included as a tested example.
It intentionally refuses different build/module hashes or a different Aux
inventory. Inspect/adapt those preconditions for another machine; no private
OpenCore configuration or VM image is supplied. KDK payloads are not redistributed.

The lab's `-nobsdmgroot` flag bypassed a residual installer BaseSystem selection
on isolated copies. It is not part of the SynIC/cursor patch and is not a general
upgrade repair. The original disk remains preserved; original migration completion
is still unproven. Maintain that distinction when reviewing the reports.

## Acceptance boundary

The latest prefix and user tests show a usable Tahoe26.7.1 desktop, correct
captured EOM CPU placement and a working software-cursor workaround. The root
hardware-cursor cause, same-binary flag A/B comparison, long sessions, repeated
boots and clean Release runtime acceptance remain open. No stable release claim
is made. Read RESULTS_LOG.md for failures, rollbacks and the host Stopping incident.
Raw logs, personal GUI images, local names/IPs, original configurations, disk
images and the temporary fixed-target diagnostic viewer are excluded.
