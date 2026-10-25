# Original guest: clean Tahoe reinstall on512GiB

User requested a clean installation of the original guest after the separate
fresh-install test, explicitly selecting512GiB with other hardware unchanged.
The user subsequently deleted the separate test VM; no recreation/operation on
that deleted VM is part of this task. Its existing test evidence is preserved.

The original guest was independently confirmed Off. Its working Release EFI and
system files were hashed, detached and preserved without modification. Only a
new EFI copy and a genuinely blank512GiB dynamic512/4096 system disk were attached
to the original SCSI0:0/0:1 locations.8vCPU,24GiB fixed RAM, network, original COM1
pipe and other VM settings were retained. The existing main SMBIOS identity and
security configuration were preserved. Original Sequoia backups were untouched.

The new EFI was host-mounted only while unassigned, validated and unmounted
before attachment. Installer-only changes remove-nobsdmgroot, expose auxiliary
picker entries/15-second timeout and replace the new copy's inherited recovery
payload with the previously verified original Apple files. Original recovery
material is retained separately. Run40189441511/source6c35681 and original Release
ZIP hash were rechecked. See ci/srv-clean-install-512g-preparation-20261025.json
for exact core/config/image/rollback hashes and bounded serial evidence.

Serial receiver25588 started before boot on the unchanged original guest pipe.
Recovery started21:34:58 and reached the English Reinstall macOS Tahoe screen,
all14channels, storage and keyboard/mouse. Guest diskutil list showed only a
blank549.8GB disk2 beside Recovery, EFI and a read-only tooling DVD; host
attachments were independently rechecked before initializing that NEW disk.
Inherited Swiss German input mapped quotes incorrectly in the volume name.
Selecting ABC input and renaming only the new APFS volume corrected Macintosh HD.
No second erase, original disk write or backup overwrite was needed.

A Command-Q shortcut was conservatively rejected by auto-review. It was not
executed. Safer explicit navigation closed the idle Terminal window, verified
the labelled Terminal menu and selected Quit Terminal, returning to Recovery.
The Apple installer was not yet started at that point; no active setup was quit.

At21:43 the installer accepted the new Macintosh HD target and began its online
installation. The3h20 initial GUI estimate is not a completion promise. Final
build, account creation, clean first framebuffer installer and loaded UUID checks
remain pending. User-provided account details are held only in local encrypted/
private files; none are reproduced in this public report or CI JSON.

## Evidence boundary

This is installation progress, not a normal desktop success. No panic/root-wait
marker was captured in the bounded Recovery prefix, but SRB STATUS84 and other
warnings exist. Clean Release contains no per-call EOM CPU traces; their absence
is not a new CPU-affinity measurement. Do not reset while installation progresses.


## Staged installer, 2026-10-25 21:55 UTC

The online stage requested an automatic guest restart at21:53:05. The intended
macOS Installer entry started without manual picker input. Serial25588 reconnected
and again captured channel14/storage; the screen shows Apple-logo installation.
Cryptex patch progress52percent is only a phase counter, not overall completion.
No captured panic/root-device-wait appears in the bounded prefixes. Exact source,
core/config hashes and both prefix hashes are in ci/srv-clean-install-512g-staged-
20261025.json. No forced reset, host disk mount or old disk change was performed.
Final normal system and the combined first framebuffer installer remain pending.


## Normal APFS root, 2026-10-25 22:13 UTC

Automatic guest starts occurred22:08:48 (Apple restore),22:10:22 (APFS bootstrap
with Apple's-bsdmgroot argument), then22:11:17 (normal APFS disk2s4). The bootstrap
log ends in orderly unmount and MACH Reboot. The normal boot has no installer,
restore or rootdmg arguments and captures all14channels. loginwindow is active;
AppleKeyStore warnings exist, but no captured panic/root-wait in the bounded
150824-byte prefix SHA078cdcb96cd4fa9f9fe7d9a12594be27f744e636ed3a2a1256f465f1dd3570c2.
The thumbnail still shows initial verbose text at this checkpoint; no new GUI
failure is inferred. Setup/account, final sw_vers, loaded UUIDs and framebuffer
first installation remain pending. See ci/srv-clean-install-512g-normal-root-
20261025.json. No host reset or live disk mount was performed.


## Setup and private authentication checkpoint, 2026-10-25 22:27 UTC

The normal-root boot reached English Setup Assistant; Switzerland and Set up as
new were selected, without migration. User-specified local account creation
completed. Names, account ID, password and raw account images remain private.
At the optional Apple sign-in page, a previously empty field subsequently
contained user-entered authentication data. Automated inputs and GUI captures
were immediately paused; no personal Apple credentials were supplied by the
agent. The incidental existing auth screenshot was protected with verified
Windows DPAPI encryption and its exact plaintext copy removed. Authentication
values are excluded from Git/maintainer evidence. Serial logging continues.
Final setup, FileVault/time zone, sw_vers and first framebuffer installation
remain pending; no completed main-guest desktop result is claimed yet.
