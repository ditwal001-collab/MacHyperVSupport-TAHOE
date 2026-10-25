# Direct Tahoe installation on a new blank system disk

Status: IN PROGRESS, 2026-10-25. This test does not yet prove installation
completion. User explicitly expanded the VM scope to one new fresh-install VM
and requested that the existing working VM be shut down. That existing VM was
shut down by the user and independently confirmed Off. Its disk attachments and
backups remain preserved. No other existing VM is part of this test.

## Reproducible steps completed

1. Create a separate branch, test/tahoe-fresh-install, preserving all local files.
2. Create a unique local test directory and record the working EFI source hash.
   With the old VM Off, copy only EFI into a new file and verify matching hashes.
   Do not clone the old system disk: the new target is genuinely empty.
3. Download official OpenCore macrecovery.py, boards.json and README from pinned
   commit78d5ff824992d5b227f842e34d8221eb8f31baf1. Request Apple Recovery with
   board Mac-CFF7D910A743CAAF, dummy MLB00000000000000000 and OS latest.
   Upstream downloader verifies the image against the signed chunklist.
4. Read SystemVersion.plist from the downloaded DMG using7-Zip: the Recovery
   environment is Tahoe26.6.2/build25G83. This is not a claim about the version
   the online installer will ultimately install.
5. Mount only the new unassigned EFI copy. Preserve its original configuration
   privately; generate a fresh iMac20,1 serial/MLB with macserial1.0.6, new UUID
   and new locally administered ROM. The utility reported arc4random unavailable;
   these identifiers are not credentials or a cryptographic security claim.
   Remove only -nobsdmgroot for authentic Recovery boot, show auxiliary picker
   entries and set15-second picker timeout. Preserve existing security settings.
6. Replace the inherited com.apple.recovery.boot directory in the new copy with
   the verified Apple files, preserving the inherited directory outside the image.
   ocvalidate1.0.6 reports no schema issues. Unmount on the host before attachment.
7. Create one Generation2 VM:8vCPU, fixed24GiB, new dynamic400GiB VHDX with
   512-byte logical/4096-byte physical sectors. EFI at SCSI0:0, blank system at
   SCSI0:1. Reuse only the existing designated external switch. Use EFI first in
   firmware, maximum1920x1080, no automatic checkpoints, no nested virtualization.
   New VM Secure Boot matches the existing Off profile; host security unchanged.
8. Set a separate COM1 named pipe. Start capture-hyperv-serial.py as a hidden,
   independent receiver BEFORE boot. Do not replace the old VM receiver.
9. First boot reaches all14 VMBus channels and the normal Tahoe Recovery GUI.
   Menu explicitly says Reinstall macOS Tahoe. No Sequoia prerequisite is used.
10. In Recovery Terminal run diskutil list. Recovery is disk0, EFI disk1/about5GB,
    and the only other physical disk is unpartitioned disk2/429.5GB. Recheck host
    attachments against the new System.blank.vhdx before initializing ONLY disk2:
    diskutil eraseDisk APFS FullTest GPT disk2. Completion was observed on screen.
11. Quit Terminal and select Reinstall macOS Tahoe, then Continue. Installer
    phase, final version and first complete desktop still require observation.

At18:09 UTC the installer accepted FullTest as the target and started downloading
one Apple InstallAssistant.macOSTahoe package, reported18.381GB. By18:13 UTC the
new VHDX had grown to13.93GB. This establishes download/write activity, not a
percentage of completed OS installation. Initial GUI estimate3h20 is not a promise.
The old VM was independently rechecked Off at18:10. No installer restart/reset
was performed. A separate read-only inspection ISO is being prepared for the
first desktop; it has not yet been attached or used to change guest kexts.

## Verified inputs and evidence

Core source6c3568178ba21136b8c21dd45597476c74ec31d1, Release/run40189441511;
SHA256c97e29193de9bedf9e2f39b7da38a589347874f7f8ef8c0c8e24f92d7f76ca16.
New EFI config SHA2563c08709ccdb0fa227c614c7799cee0c156eda8ca7fba8d540909ea732ac5dc52.
Recovery DMG SHA256edddd0d5869caaa12e29e6996a04f11590280580976a119dbd42c24fa62fe18e;
chunklist06f7c498f856341f467ba1faedf2717fb2c172ae0aff4658a1467cbf46b711f9.
See evidence/ci/fresh-install-preparation-20261025.json for the bounded serial
prefix and anonymized results. Raw console images, IDs and original configuration
remain only in the ignored local test directory.

The new disk initialization is specifically authorized by the fresh-install
request. This does not authorize formatting an existing guest or its backups.
The copied EFI retains the tested configuration ancestry; this is not a clean
EFI reconstruction from Sample.plist. No generic EFI template or framebuffer
first-install success has yet been delivered by this checkpoint.

## Next acceptance steps

Record online install version, target-volume selection and progress. Do not
interrupt installation for repeated boot tests. Then verify sw_vers, loaded
Release core, synthetic storage/network/input and first desktop. Build and test
a guarded framebuffer FIRST installer against the new guest's actual Aux module
inventory, preserving original Boot/System collections and a cold rollback.
Only then count a full Release desktop with the optional software cursor.

Recovery is not a completed installation. Clean Release has no per-call EOM CPU
traces, so absent EOM trace lines are not new CPU-locality measurements.
