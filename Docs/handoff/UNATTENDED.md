# Current state before unattended continuation

## 2026-10-24 16:43 UTC: VM OFF, cold system copy IN PROGRESS

Guest `shutdown -h now` completed from idle Recovery; host confirmed Off.
Original system disk was detached from target SCSI 0:1. It remains preserved.
New copy and stage manifest:
`evidence/local-tests/system-boot-selection-20261024T164253Z/`.
Read context.json before any attachment or start. The copy must finish and both
SHA256 values must match before use. EFI test copy remains at SCSI 0:0.
Do NOT start the VM with its system disk absent or an incomplete copy.
Receiver PID 46464 must be rechecked before boot. No Preboot plist changed yet.

## 2026-10-24 16:42 UTC: isolated boot-selection experiment planned

Read-only guest inspection found a valid blessed APFS System snapshot, matching
Preboot boot.efi, no recovery-boot-mode or efi-boot-next NVRAM variable, and
normal NVRAM boot-args without -bsdmgroot. However, the selected Preboot group's
System/Library/CoreServices/com.apple.Boot.plist explicitly has Kernel Flags
`-bsdmgroot` and a BootKernelExtensions.kc path. The group's
Library/Preferences/SystemConfiguration/com.apple.Boot.plist has empty flags.
Serial confirms root image pivot into Recovery/BaseSystem.dmg and migration
mode on the Tahoe installer boot. APFS access alone is not a normal-system boot.
This identifies the source of the BaseSystem selection, NOT why migration failed
to finish or proof that skipping it is safe on the original system disk.

Next experiment is therefore restricted to a NEW full system-VHDX copy, after
guest graceful shutdown from idle Recovery, original disk detachment and verified
copy hashes. Preserve the original system disk as the unchanged cold recovery
point. No erasure, format, deletion or protected-backup use. Test candidate source
and EFI remain unchanged. Record all paths/hashes privately before changing any
copy, and preserve original plist bytes before a one-setting experiment.
As of this note shutdown/copy/configuration change have NOT yet occurred.

GitHub visibility independently verified PUBLIC at user request. Clean SynIC
run 40093339256 and speculative graphics run 40101047189 both SUCCESS. Graphics
variant remains uninstalled; do not conflate it with the boot-selection test.

## Live verification 2026-10-24 16:17 UTC (supersedes running-phase assumptions below)

Target VM remains Running. Its current console was actively verified, not merely
inferred from a stale thumbnail: opening Terminal and running `uname -a` returned
Darwin 24.4.0, Sequoia Recovery. The third Tahoe installer boot emitted
`OSInstaller: Triggering reboot` at 15:19:09, then orderly APFS unmount / MACH
Reboot. The receiver reconnected at 15:20:39 into a new, zero-byte serial file;
Python PID 46464 remains alive. Thus quiet serial currently does not establish
a frozen Tahoe kernel: the guest is responsive Recovery without new serial output.
The third log now contains 224796951 bytes and 23 EOM writes, all target=actual=0.
No panic/root-wait was found by the targeted search. No installed-system login
is proved. Recovery's on-disk installer log ends at the same 15:19:09 reboot.
A read-only error search shows efilogin-helper resource archive limits (1048 items)
and missing sound data; causality for Recovery fallback is UNKNOWN.
No lifecycle change, reinstall, format, or disk-image modification was performed
during this continuation. Local console evidence: frame-20261024T161548Z.png,
frame-20261024T161612Z.png and frame-20261024T161709Z.png in the existing test folder.
A Swiss keyboard pipe translation was wrong and produced a shell redirection;
the guest rejected it with Read-only file system. No output file was written.
Use simple commands without pipes until that key mapping has been verified.

Next investigation is the installer/boot-selection fallback, not another SynIC
or speculative graphics installation. Preserve the current responsive Recovery
and logs while collecting the specific installer error/boot target evidence.

Date: 2026-10-24. Read AGENTS.md, CODEX_HANDOFF.md and the actual Git status.
The user authorizes autonomous Git, GitHub and target-VM work without repeated
confirmation questions. Target remains exclusively srv-maos-devs11. Preserve
all existing backups, especially the protected Sequoia export. No public
publication, erase/reformat, or blind reinstall is part of the current plan.

The VM is RUNNING, using the unchanged instrumented SynIC candidate 0756f1d,
run 40090495930. Third captured boot began after a graceful guest reboot from
Recovery around 13:53 UTC. It is Darwin 25.6.0 (Tahoe), with 23 matching-CPU EOM
writes, all 14 channels, completed scan, SCSI and APFS root. WindowServer and
OSInstaller run. User reports Apple-logo screen appeared. No full installation
completion or installed-system login has been proved. Do not interrupt this
active phase merely to install a speculative graphics change.

Recovery was separately identified as Darwin 24.4.0 / Sequoia, using a
BaseSystem disk-image root. It is NOT a second Tahoe-system boot. From its
Terminal, OSMAIN/System/Library/CoreServices/SystemVersion.plist was read:
ProductVersion 26.7.1, build 25G241. The APFS System volume is sealed and the
Data volume is mounted. This proves files/version on disk, not completed setup.
The Data volume has a Unicode dash in its name; /Volumes/OSMAIN*Data resolves
it. A .install-failure.log exists; the read tail ends with OSInstaller triggering
a reboot, and a targeted OSInstaller.*fail search gave no match. The filename
alone does not establish the failure cause. No reinstall/repair/erase occurred.

The independent hidden serial receiver is Python PID 46464, with ready-file
under evidence/local-tests/vm-test-0756f1d-20261024-01/serial-reconnect-02/.
It has survived assistant turns and automatically reconnected across reboots.
Check the actual PID and file growth. Earlier foreground capture had a documented
gap 12:34:13.99–12:36:24.48 UTC. Keep all raw logs local and excluded from Git.

The active EFI is the test COPY under that local test directory, attached at
SCSI 0:0. Never delete/move it while attached. Original EFI at the VM's original
host path remains unchanged (verified hash in local test-context.json). System
disk is SCSI 0:1. No host-side system-VHDX write or protected-backup change has
been performed. Firmware currently has Network, system disk, then test EFI
in its boot order; it was read, not modified. Escape left PXE during the last
reboot. Do not infer default boot selection from user reports alone.

Correct clean SynIC branch: test/synic-eom-clean-c48fc5c, source 7a3b98a,
CI head c960997, Actions run 40093339256 SUCCESS. Downloaded artifacts are under
evidence/local-tests/run-40093339256-clean-artifacts; hash verification remains
to be completed. Wrong-base branch test/synic-eom-clean-20261024 is superseded.
The actual project baseline is c48fc5c, not cd66095f.

Separate GRAPHICS hypothesis branch: fix/tahoe-display-refresh, 3d31e11,
Actions run 40101047189 (last queried in progress). It applies ONLY the seven-line
refreshTimer dirty-marking hunk from startergo 3454a80, with original author and
date preserved. No VRAM-reporting hunks included; it is NOT installed in the VM.
User's actual console shows more current graphics than WMI thumbnails, which
have returned stale/black images; do not treat thumbnail staleness alone as proof
of a graphics defect or install the speculative variant during active upgrade.

Host WMI console access works: target VM's related Msvm_SyntheticMouse,
Msvm_Keyboard, and GetVirtualSystemThumbnailImage. Explicit mouse button-down,
150–200 ms wait, button-up works; ClickButton was too fast. Terminal uses Swiss
German QWERTZ; host TypeText US key translation requires y/z swap and punctuation
mapping. Already used read-only commands successfully. Screenshots are local.

Next: preserve/commit newer observations, monitor current Tahoe boot with serial,
wait for real installer/setup completion or an actual error; verify normal GUI
and sw_vers when possible. If genuine installer/graphics trouble remains, collect
specific evidence, ensure a consistent fresh backup before another variant, and
test one change at a time. Never count Recovery GUI as completed Tahoe install.
Document any blocker and stop that action safely rather than waiting for the
absent user or manufacturing a successful outcome.
