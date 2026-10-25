# Maintainer delivery and project map

This Hyper-V-only delivery includes clean source patches, original CI binary
ZIPs, anonymized VM/EFI setup and a technical test record. Start with this guide,
HYPERV_SETUP.md and RELEASE_RC1.md. Check each ZIP/hash, source, run and runtime
scope before installation. An11h07 Debug run is verified; clean Release build
success alone is not a stable-release acceptance claim.

A separate blank-disk installation now reached Tahoe26.7.1/25G241 desktop with
both exact clean Release UUIDs,14channels, software cursor, HTTPS/Safari and a
short Finder/input smoke test. It required recovery from a final Setup Assistant
stall and a canonical Aux bundle-path correction. Read FRESH_INSTALL_TEST.md and
TAHOE_INSTALL_STEP_BY_STEP_DE.md; this does not establish unattended installation,
repeat-boot reliability or a generic EFI template. The combined revised first
installer was assembled from stages exercised separately on that fresh guest;
it has not been rerun end to end on a second blank installation.

## Project structure and changed files

```text
MacHyperVSupport/
  Controller/HyperVController.hpp             remove obsolete preemption lock
  Controller/HyperVControllerInterrupts.cpp   CPU-local EOM functional correction
  VMBus/HyperVVMBus.cpp                       baseline restored in clean candidate
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

Use a fresh checkout at that base. The CURRENT bundle has five patches under
patches/:0001 clean SynIC CPU placement,0002 startergo full-frame refresh,
0003 refresh pacing,0004 optional software cursor,0005 CI/provenance. For each
in order run `git apply --check PATCH` then `git apply PATCH`. The exporter checks
application and reconstructs all nine changed source/build files byte-for-byte
after line-ending normalization against the clean candidate. The historical
instrumented four-patch exports described in older reports are separate variants;
do not apply them on top of this clean series.

The reference/ GraphicsBridge patch is attribution/history only: base c48fc5c
already contains it. Do not apply the reference patch again. Original base and
refresh-hunk attribution are preserved in ATTRIBUTION.txt.

Pinned source/run mapping:

| Variant | Source | Actions run | Runtime scope |
| --- | --- | --- | --- |
| Instrumented SynIC |0756f1d75601f0c24bce98ae4adf8c83ce6e3307|40090495930|recorded enumeration/GUI tests|
| Clean SynIC build |c960997 (clean-c48 branch)|40093339256|build only|
| Refresh backport |3d31e1107d097f2a3eee4683e89d7d8678a76708|40101047189|visible input restored; slow mouse|
|33-ms pacing |e17098263de44ac71251bcd31caea999e050221e|40124452997|user reports faster mouse|
| Combined optional cursor |c9eb980daab9598b1af6732217147490dacceb3e|40139181101|positive overnight11h07 Debug observation|
| Clean combined RC1 |6c3568178ba21136b8c21dd45597476c74ec31d1|40189441511|build/analyses passed; see RELEASE_RC1.md for actual runtime status|

The GitHub Actions workflow builds Debug/Release and runs both Clang analyses.
It uses macos-15-intel/Xcode16.4, pinned MacKernelSDK and ocbuild, and a
checksum-verified Lilu1.7.2 Debug SDK. Exact pins and dependency hashes are in
REPRODUCE.md, the workflow and each included Provenance directory. Hosted images
and remaining transitive downloads prevent a bit-identical rebuild guarantee.
To repeat the combined build in the existing repository:

```sh
gh workflow run main.yml --ref release/tahoe-clean-rc1
gh run view 40189441511
gh run download 40189441511 --dir downloaded-build
```

A new run has a new identity: verify its source and uploaded provenance anew.
The delivery contains original Debug/Release ZIPs in separate historical-reference
and clean-RC1 directories. Do not mix executables/provenance between them.
Overnight Debug core is803a3d24..., framebuffer310f155f... . Clean RC1 Release
core isc97e2919..., framebufferd8a079d4... . Exact hashes are in the manifest
and run-40189441511-verified.json. The profile/overnight evidence records which
configuration was actually booted.

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

The guest-specific guarded InstallAux-example.command derives from the tested
Aux-only procedure, pinned to this candidate's hashes. Its runtime installation
status is recorded in RELEASE_RC1.md. It refuses different build/module hashes
or a different Aux inventory. Inspect/adapt those preconditions for another
machine; full private EFI configurations, VM images and KDK payloads are omitted.

The lab's `-nobsdmgroot` flag bypassed a residual installer BaseSystem selection
on isolated copies. It is not part of the SynIC/cursor patch and is not a general
upgrade repair. The original disk remains preserved; original migration completion
is still unproven. Maintain that distinction when reviewing the reports.

## Acceptance boundary

The Debug tests show a usable Tahoe26.7.1 desktop, correct captured EOM placement,
a useful software-cursor workaround and one positive overnight session. The root
hardware-cursor cause and same-binary flag A/B remain unresolved; read RELEASE_RC1
for repeated-boot and clean-Release runtime status. No stable-release claim follows
from a long Debug session or a successful CI build. RESULTS_LOG covers failures,
rollbacks, host-finalization and integration-shutdown incidents. HYPERV_SETUP
separates recorded changes from pre-existing settings and unknown before-values.
Raw logs, personal GUI images, local names/IPs, original configurations, disk
images and the temporary fixed-target diagnostic viewer are excluded.
