# Current state before unattended continuation

## Guest now unlocked; local sudo authentication pending (23:04 UTC)

Guest is at desktop; read-only commands verified sw_vers macOS26.7.1 build25G241.
Loaded framebuffer fish.goldfish64.MacHyperVFramebuffer0.9.9, UUID
45B79D4F-3751-32EE-89A1-57CF056D4493. /Library/Extensions binary SHA256
51c9cd8c78ceb87f3e373882ea25cfe982f68c4a1e89c6d4ff6985b04038c1cf.
Current SIP is an existing Custom Configuration with Kext Signing disabled;
no protection settings were changed. sudo -n true requires a password.
Agent issued sudo -v: Terminal is now WAITING AT LOCAL PASSWORD PROMPT.
DO NOT inject further commands until prompt is gone: they would become password
input. Never request or type credentials in chat. This is authentication, not
an additional authorization request.

DVD now cursor-media-20261025-03/CursorTest.iso (same HVCURSORTEST label), SHA256
06543889CB20706653766BF6A71D44F9AEC2DEE40E732DA77186A2A01237D81D.
Adds guarded Install.command: checks guest build + old/new binary SHA, extracts
candidate, normalizes permissions, makes exclusive /Users/Shared backup and
verifies it, installs only framebuffer then kmutil install --volume-root / --update-all.
No automatic reboot/security changes. If cache update fails restores old bundle
and stops for review; must assess cache state before reboot.
Candidate still NOT installed. After successful sudo -v in same Terminal:
sudo -n bash /Volumes/HVCURSORTEST/Install.command
Use verified Swiss keyboard mapping y/z,Y/Z,/=>&, -=>/, _=>?, *=>#.
After success capture exact guest backup path and kmutil log, then graceful guest
shutdown, new Off/detached EFI copy with -hvgfxfbswcursor added, verify config/hash,
start with active serial and verify loaded0.9.10 + software marker before testing.
The 0.9.9->0.9.10 component change is an additional comparison variable; no isolated
release-fix claim. Existing core remains803a3d24..., config32be11... until that step.

## Current cursor work / local-unlock blocker, 2026-10-25 local

Candidate c9eb980 CI40139181101 SUCCESS: Debug/Release and both Clang analyses.
Independent verification: evidence/ci/run-40139181101-verified.json.
Debug framebuffer310f155f50aa2f5ffccd688ba0ef280e268335e209e616ae888f2f73d8133ef3;
Release framebufferd8a079d47d61988aabe40cb788b015979c27384135b57339e854d5c017792122.
Core binary is byte-identical to e170982 comparison; candidate not installed.

Target had returned Off with zero-byte serial-20261024T223540Z-477635b9.log;
cause unverified. Agent read only the system TEST copy offline: temporarily
detached, mounted ReadOnly/NoDriveLetter, restored SCSI0:1 in finally. 7-Zip22
cannot use the native APFS device paths tried; no filesystem writes, no original
disks touched. Do not repeat those unsuccessful native-path attempts blindly.

Agent restarted target on the same exact EFI/System copies with verified serial
PID48800. New capture serial-20261024T225535Z-cbaf6894.log is zero bytes while
the visible local pre-kernel password/unlock screen waits. No credential request
in chat, no guesses/security bypass. Guest module identification/install requires
local unlock; this is a real access blocker, not an approval question.

Read-only test media attached at new free SCSI0:2 DVD slot (no previous DVD):
local-tests/cursor-media-20261025-02/CursorTest.iso,
SHA25682E2655BAAF7FF36C9D3E0231D6618699C5C108287AD478A0516E12384FDDDF0.
Label HVCURSORTEST; Inspect.command runs sw_vers/kextstat/kmutil/show disk hashes,
no sudo/install/reboot. Actual compiled bundle ID fish.goldfish64.MacHyperVFramebuffer.
Framebuffer.zip contains only the verified candidate; its extracted executable
must retain/receive normal kext permissions when eventually installing. Root
ownership, existing backups, current security state and cache rebuild must be
verified in guest first. README/source explicitly require /Library/Extensions on
modern macOS; do not just enable the disabled OpenCore framebuffer entry.
DVD is not bootable; firmware boot order unchanged. No cursor fix claimed.

## Autonomous restart and separate cursor candidate, 2026-10-25 local

User explicitly authorized automatic starts. After user shutdown, target Off was
verified; log serial-20261024T222131Z-ebab9d12.log ends CPU halted / PowerOff.
It has 22 matching-CPU EOM writes, 161 cursor conversion failures, no panic/root
wait marker; SHA256989B68C0637AA2651628AF79F8A6B0B6AB93809989EBAEDDF8613DA402F58DFC.
Agent started ONLY target with the SAME expected two working-copy disks after
checking serial PID48800. No EFI/config/binary/disk modification was performed.
This start is still e170982/run40124452997, NOT the new cursor candidate.

Separate branch test/tahoe-software-cursor, c9eb980daab9598b1af6732217147490dacceb3e,
adds an opt-in -hvgfxfbswcursor boot flag in the framebuffer, advertising no
hardware cursor only when requested. Existing flushCursor hides host cursor;
IOFramebuffer supplies software drawing. Default behavior stays unchanged.
Build40139181101 started; query actual status. Candidate NOT installed, NOT
runtime validated. Need loaded framebuffer identity before installation; core
binary replacement alone does not install this change. Never bypass kext security.
User also requests remote-access alternatives if VMConnect remains unreliable;
Jump Desktop Connect/Fluid is first comparison, AnyDesk or Apple Screen Sharing
with VNC alternatives. No remote-access service configured by agent.

## User-initiated restart, 2026-10-24 22:21 UTC

User announced restart; host uptime reset and target is Running. No restart was
issued by the agent. Target console now shows local pre-kernel password/unlock.
Receiver PID48800 remained alive and reconnected automatically to a new capture
serial-20261024T222131Z-ebab9d12.log (empty at this checkpoint).
IMPORTANT correction to immediately preceding empty-log observation: previous
serial-20261024T205403Z-a56bdd2a.log is now populated (493656 bytes), contains
Darwin25.6 boot through clean MACH Reboot, 22 matching-CPU EOM writes, zero
wrong-CPU writes, 59 cursor conversion failures, no panic/root-wait marker.
Reason for delayed file visibility/output is not established. Do not claim a
permanent capture gap. Current restart's kernel validation still pending unlock.
Snapshot SHA256 EC4A3A10FE147CE49835CD827190D823DDB803AD7132DB0EE90CD222645CBEC5.
No disk/config/code changes. Pointer disappearance remains unresolved.

## Latest observation, 2026-10-25 local (22:20 UTC previous day)

Target Running; read-only target VMConnect screenshot shows a full macOS desktop.
User reports fast movement but black pointer disappears after a short time.
This supersedes the earlier pending-unlock/off state below. Preserve the active
interactive session; no restart or guest input was performed for this check.
Serial receiver PID48800 verified alive, but newest log remains zero bytes.
Current-boot SynIC validation is unavailable; do not claim logging coverage.
See GRAPHICS_REFRESH_REPORT.md for source-based cursor hypothesis and evidence limits.

## User-requested restart, 2026-10-24: VM RUNNING for local mouse test

The user explicitly requested start to test the prepared pacing comparison.
Host confirmed Running on the same two working copies; no disk/config change.
Source e170982/run40124452997, interval33ms, executable803a3d24f6312ce53f1b7385321c37e1a14e28d5c413620634243f821e60c888,
config32be11f98247242f8e1534076817825cae2fa79b235ce289b179ec59e39caf8f.
Old serial PID46464 had ended while the VM was Off. A fresh independent hidden
receiver is verified PID48800; COM1 pipe unchanged. Exclusive new capture folder:
evidence/local-tests/display-pacing-test-20261024-01/serial-start-20261024T205328Z-cc486be1/.
Exact start UTC is in the latest local user-start-*.json; serial-start-record
also preserves readiness before boot. Existing target console retained, or a
visible target console opened if absent. Local unlock and runtime mouse result
still pending at the start checkpoint. Original disks/backups remain preserved.

## Latest verified state: target VM OFF; pacing runtime still unvalidated

At the final state check after the local-unlock wait, host reported Off. The
latest kernel capture remains zero bytes. Cause of the intervening poweroff is
NOT established; do not attribute it to the pacing kext which had not produced
any kernel evidence. Current snapshot time: evidence/ci/display-02-pacing-pending.json.
Keep this Off state intact. Runtime comparison needs a local start/unlock and
receiver-liveness check first; never obtain the password in chat or bypass it.
Attached copies remain EFI.refresh-pacing.vhdx at SCSI0:0 and System.test.vhdx at
SCSI0:1. Original system/EFI and every test variant/backup remain preserved.
Source e170982/run40124452997 successfully built and hashes checked; NO mouse
improvement or release-stability claim is established. All source/documentation
is saved; kernel/GUI validation is blocked on the local unlock/start boundary.

## 2026-10-24 19:44 UTC: local pre-kernel unlock required (current blocker)

The 33-ms candidate is installed on new EFI.refresh-pacing.vhdx and the VM is
RUNNING, but a native macOS pre-kernel password/unlock screen is waiting for
local user entry. It has a Lake background and Recovery help text; no new kernel
serial bytes were captured. Do not infer a successful new kernel boot or a mouse
improvement. Actual FileVault state has not been re-queried, so do not claim its
configuration changed merely from the appearance of this screen.
Active EFI:SCSI0:0=evidence/local-tests/display-pacing-test-20261024-01/EFI.refresh-pacing.vhdx.
Active system:SCSI0:1=existing System.test.vhdx. Original disks remain detached.
Source e170982/run40124452997 SUCCESS; Debug hash803a3d24f6312ce53f1b7385321c37e1a14e28d5c413620634243f821e60c888.
Config unchanged32be11f98247242f8e1534076817825cae2fa79b235ce289b179ec59e39caf8f.
Receiver PID46464 preserved. User was informed local unlock is necessary; no
password requested in chat. Evidence:ci/display-02-pacing-pending.json.
Once local unlock occurs, verify the new serial capture and actual GUI before
claiming the pacing comparison ran. Keep the current waiting VM intact.

## 2026-10-24 19:39 UTC: pacing comparison starting

Run40124452997 fully SUCCESS, Debug/Release and analyses. Package and executable
hashes verified in evidence/ci/run-40124452997-verified.json. Source e17098263de44ac71251bcd31caea999e050221e.
Only source difference vs 3d31e11: refresh timer10 ->33ms, unchanged SynIC/mouse/cursor.
Guest remained in a processing Setup Assistant pane with disabled Continue;
Back/regular quit/lock/quit-dialog attempts did not provide a graceful exit.
The user-authorized diagnostic was interrupted by hard stop ONLY after confirming
both disks were working copies and the original cold recovery point was preserved.
Record is local display-pacing-test-20261024-01/stop-context.json. This is NOT a
normal shutdown or proof of completed setup; journal replay/state confound tests.

New exclusive EFI copy, hash-verified before editing, edited only detached/Off,
host-unmounted before attachment:
evidence/local-tests/display-pacing-test-20261024-01/EFI.refresh-pacing.vhdx at SCSI0:0.
Same System.test.vhdx remains SCSI0:1. All older EFI variants preserved.
New Debug executable SHA256:803a3d24f6312ce53f1b7385321c37e1a14e28d5c413620634243f821e60c888.
Config unchanged:32be11f98247242f8e1534076817825cae2fa79b235ce289b179ec59e39caf8f.
PID46464 checked before boot. Exact boot UTC in local boot-plan.json.
Next: inspect newest serial reconnect and actual GUI. Mouse improvement is still
UNPROVEN; hardware cursor conversion issue remains a distinct unresolved finding.

## 2026-10-24 19:20 UTC: refresh fix observed; mouse-performance comparison building

User reports input now working after separate graphics refresh binary installed;
VMConnect screenshot shows post-login Setup Assistant (Analytics). Latest capture
serial-20261024T190640Z-8fa4ff79.log: Darwin 25.6.0, 14 channels, 15 parseable EOM
writes, zero mismatches, no captured panic/root wait. Evidence:
evidence/ci/display-01-3d31e11.json and GRAPHICS_REFRESH_REPORT.md.
Active new EFI remains display-refresh-test-20261024-01/EFI.display-refresh.vhdx.
System working copy unchanged attachment; original disks remain preserved.

User then reports slow mouse movement. Actual guest resolution now 1920x1080x32;
VM CPUUsage sampled 13%; hardware cursor conversion errors captured. Current
full-frame timer is 10 ms, up to 100 requests/sec. Cause not yet established.
Separate experimental branch fix/tahoe-refresh-pacing, source
e17098263de44ac71251bcd31caea999e050221e, changes only interval 10 -> 33 ms.
Worktree evidence/local-tests/display-pacing-worktree. Run40124452997 building;
Clang analysis passed, Build pending at last check. NOT installed. Do not change
mouse speed/global host settings or claim a mouse fix before runtime comparison.
Current VM stays running while CI finishes. Receiver PID46464 still alive.

## 2026-10-24 19:06 UTC: separate graphics candidate boot (current state)

User independently reports unreadable/stale VMConnect display and apparently
nonworking keyboard/mouse focus. Reconnect refreshed the client once, then it
stayed at 11:57 while the direct Hyper-V framebuffer reached 12:01 and showed
changed masked input / a working power menu. Thus prior WMI login-screen/clock
evidence did NOT establish a usable live VMConnect console. Scope correction:
input reached the guest while its visible client image did not refresh reliably.
The desktop-capture helper also required per-process DPI awareness; it now uses
physical pixel dimensions. No global host DPI/keyboard/security settings changed.

Guest was gracefully shut down using the live WMI-observed macOS login power
menu. Host Off confirmed; no hard stop in this graphics experiment.
Separate branch fix/tahoe-display-refresh, source 3d31e1107d097f2a3eee4683e89d7d8678a76708,
run 40101047189 SUCCESS. Only diff versus 0756f1d is the seven-line startergo
refresh-timer hunk (one markFullScreenDirty() call plus original comments).
SynIC Controller/VMBus source unchanged. New Debug Monterey executable SHA256:
39219543142986a6485ea2ae05a15a4c34e017946a45f40a2106466520a840a8.
Config unchanged: 32be11f98247242f8e1534076817825cae2fa79b235ce289b179ec59e39caf8f.

VM now starts with a NEW EFI at SCSI 0:0:
evidence/local-tests/display-refresh-test-20261024-01/EFI.display-refresh.vhdx.
Same system working copy remains SCSI 0:1. New EFI was exclusively copied,
hash-verified, edited only detached/Off, host-unmounted before attachment.
Only executable content changed; Info.plist equal; previous executable and all
EFI images preserved. Context, installation verification and boot plan are in
the new ignored experiment directory. PID 46464 checked before boot.
Next: confirm SynIC counters, then actual VMConnect clock/menu/input redraws
against direct WMI images. A static WMI login screenshot alone is insufficient.

## 2026-10-24 17:22 UTC: CONFIRMED LIVE NORMAL TAHOE LOGIN SCREEN

Successful copy-only boot using EFI.no-storage-packets.vhdx + System.test.vhdx.
Normal password login screen independently viewed at 17:19:29 UTC and 17:22:06;
clock advanced 10:19 -> 10:22. No Recovery controls. Darwin 25.6.0; System version
previously read as 26.7.1 / 25G241. Personal account login / runtime sw_vers NOT run.
All 14 channels, 24 fully parseable EOM writes, ZERO CPU mismatches, no captured
panic/root wait or BaseSystem pivot. PID 46464 verified alive at final checks.
Same 0756f1d/run40090495930 binary; config hash 32be11f9...e39caf8f (full hash below).
Read TAHOE_BOOT_RESULT.md and evidence/ci/boot-05-tahoe-login.json for provenance.
Keep the VM running at its login screen; do not request the absent user's password.
Do not promote the bypass profile to the original system: migration completion
and clean Release stability are NOT established. Original system/EFI/backups
remain preserved. Active ignored test disks MUST NOT be moved/deleted/cleaned.
Graphics-hypothesis binary remains UNINSTALLED; live GUI refresh works without it.
PrintWindow VMConnect capture produced a garbled client image while the separate
Hyper-V thumbnail showed a valid live login GUI; neither capture path alone is
a sufficient basis to diagnose graphics failure from an anomalous image.

## 2026-10-24 17:18 UTC: low-packet comparison RUNNING (current state)

After >20 minutes without confirmed GUI, graceful shutdown was unavailable
(missing hvshutdownd). The user-authorized copy-only diagnostic run was therefore
HARD STOPPED at 17:15:09 UTC, with explicit guards proving only the two test copies
were attached and the hash-verified cold original was detached. No forced stop
of the original disk, other VM, deletion or formatting occurred. The prior full
raw capture is preserved; this interruption is not an OS crash or a successful boot.

New EFI copy EFI.no-storage-packets.vhdx was exclusively copied/hash-verified
from the prior EFI, mounted only detached/Off, and changed ONLY by removing
`-hvstormsgdbg`. Serial, SynIC diagnostics, -nobsdmgroot and the same 0756f1d Debug
binary are retained. Other plist values compare equal. New config SHA256:
`32be11f98247242f8e1534076817825cae2fa79b235ce289b179ec59e39caf8f`.
Host unmounted before attachment. VM now runs this new EFI at SCSI 0:0 and the
same System.test.vhdx at SCSI 0:1. All earlier EFI variants remain preserved.
Receiver PID 46464 checked before start; inspect newest reconnect log for path.
See copy-only-hard-stop.json, quiet-efi-context.json, quiet-config-change.json,
quiet-boot-plan.json locally. Original system remains detached and unchanged.
The working system copy has already booted and may replay its journal; cold-copy
CF92... describes initial equality before first use, not its current file hash.
Timing is confounded by warmed caches/state and journal replay: a faster boot
alone cannot prove packet logging was the only original installer problem.

## 2026-10-24 17:12 UTC: normal-mode attempt still RUNNING; graceful shutdown unavailable

Same copy-only boot remains active. It reached normal launchd early-boot completion,
mounted Data/Cryptexes and started coreservicesd plus additional system services.
No confirmed GUI/login, BaseSystem pivot, migration-mode marker, panic or root wait.
Dense storage traffic persists (246575 of 249442 lines at one checkpoint), with
15-second APFS iterator limits, long transaction/flush times and kernelmanagerd
registry-busy timeouts. Logging overhead is a plausible contributor, not proven
as the sole cause. Source confirms -hvstormsgdbg enables the RAW packet IOLog flood;
removing just this argument would retain controller/SynIC diagnostics.

Host Stop-VM was attempted ONLY as graceful guest shutdown, without Force/TurnOff.
It FAILED 0x80004005. Serial explicitly states HyperVShutdown::checkShutdown():
"Unable to request shutdown (shutdown daemon is not running)". Host rechecked
Running state and both test-copy attachments. No forced stop/reset occurred.
Do not assume an integration-service status of OK proves hvshutdownd is running.
The lower-packet-verbosity comparison is NOT started. Continue observing current
boot or use a genuinely available guest shutdown path before another disk change.

Existing VMConnect window can now be read directly via a scoped local helper,
evidence/local-tests/capture-target-vmconnect.py. It captures only windows whose
title contains the authorized VM. At 17:03 the real window still showed the early
kernel console, matching WMI; stale display cannot currently be blamed on WMI alone.
These private images include host window titles and MUST remain excluded from Git.

## 2026-10-24 16:51 UTC: isolated copy boot RUNNING (current state)

Full system copy passed SHA256 equality:
`CF92F837363108774D5E507966625A472C0FD315282F1B18B04074C6E81DE9B1`.
Original system VHDX is DETACHED and unchanged since graceful shutdown.
VM now uses BOTH new copies from
`evidence/local-tests/system-boot-selection-20261024T164253Z/`:
EFI.boot-selection.vhdx at SCSI 0:0, System.test.vhdx at SCSI 0:1.
Do not move/delete either while attached. Previous EFI test image and original
host EFI remain detached/preserved. New EFI was separately copied/hash-verified,
then host-mounted only while VM Off and detached. Original config bytes backed
up exclusively. Only boot-args gained `-nobsdmgroot`; semantic plist comparison
confirms all other values equal. Kext hash remains 38bf5d6d...f4ffec9.
New config SHA256: `b8384af04dad0aabb71048d9b0f35242e6f3bd413d096cfa5bf74b568e53bff1`.
The new EFI was host-unmounted before attachment; target UEFI FirstBootDevice
was set to this verified EFI, avoiding its previous Network-first priority.
This boot-selection change is separate from the SynIC patch/runtime comparison.

Serial receiver PID 46464 automatically reconnected. New capture:
serial-reconnect-02/serial-20261024T165127Z-221c41db.log in the original test dir.
Darwin 25.6.0 boot and CPU-local EOM writes observed; later root/login outcome
PENDING. WMI thumbnail still showed OpenCore menu while serial already showed
kernel/device boot: remember thumbnails can be stale. Do not send blind keys.

XNU bsd_init.c confirms `-nobsdmgroot` overrides `-bsdmgroot` in
bsdmgroot_bootable(). This is an isolated attempt to bypass BaseSystem pivot,
not proof of completed installation or a proposed production migration fix.
Source: https://github.com/apple-oss-distributions/xnu/blob/main/bsd/kern/bsd_init.c
Private cold-copy, EFI/config/attachment/boot provenance is in context.json,
efi-context.json, config-change.json, attached-copies.json and boot-plan.json.

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
