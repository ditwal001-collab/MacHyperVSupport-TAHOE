# Maintainer delivery and project map

Start with **HOW_TO_TAHOE_DE.md** in the full-install delivery root. It is the
single end-user installation guide, assuming Hyper-V is already installed and
working. It covers a fresh512-GiB installation, all downloads, EFI requirements,
VM settings, serial capture, setup product and final acceptance checks. It does
not require reading historical test reports to follow the installation steps.

The full-install delivery additionally contains changed-files/ with actual source
files in project layout, installer/ with the original setup product and verified
DVD image, drivers/ with the original Release archive, and maintainer/ with
patches, provenance and technical evidence. WO_IST_WAS.md explains these paths.
No private EFI, VM disks, account secrets or development environment is included.

The final fresh installation passed desktop, exact Release UUIDs, automatic
1920x1080 and a further normal reboot. The user personally confirmed Apple login.
Final Match Settings required a regular guest shutdown/start; account metadata
and time zone needed correction. This is qualified acceptance, not a fully
unattended or universal blank-VM installer. A usable personalized EFI remains an
external prerequisite. See final-setup-acceptance-result-20261026.json for the
bounded final result. Historical technical evidence is retained separately for
review; it is not part of the installation instructions.

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
Tools/Setup/                                  optional native first-login setup
BuildScripts/build-integrated-setup.py         separate pinned setup product build
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

The exporter can additionally include the exact setup CI artifact with
`--setup-artifact-directory PATH`. This produces a separate integrated-setup/
folder and optional patch0006 against the clean driver candidate. The five
driver patches and their original binary hashes remain unchanged. The optional
patch reconstructs six setup/build files, not an entire replacement project;
upstream shutdown daemon sources already exist in the baseline. The original
setup-only GitHub workflow remains available at its pinned source commit.
Failed Recovery Seed is excluded from this optional source subset and media.

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
