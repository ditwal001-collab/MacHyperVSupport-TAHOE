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

At18:14:53 the Apple payload was mounted successfully; at18:16:04 extraction
reported succeeded and integrity validation began. The log reported a mobile
update trust-policy fallback to X509; no verification bypass was introduced.
At18:19:08 the guest restarted automatically. OpenCore correctly selected the
new macOS Installer entry; Enter confirmed that selection. Serial reconnected
without loss of the receiver process. The second boot again enumerated all14
channels and authenticated the staged installer root, reaching Apple-logo
installation progress with a29-minute estimate. This is still an installer,
not the installed normal system. See fresh-install-phase2-20261025.json.
The old source EFI was rehashed at18:18 and still exactly matches its cold-copy
source hash4313bb56..., confirming it was not edited during new-VM preparation.

For repeatability, new-tahoe-test-vm.ps1 captures the hardware commands as a
plan-by-default helper. PowerShell parsing passed, and a read-only invocation
against the existing running test VM correctly refused before any mutation.
The complete helper creation path has not itself been runtime-tested; the
actual VM was created with the corresponding individual commands above.

## First installed-system startup and interactive setup

The staged installer requested another restart at18:32:45. That boot used the
Apple -restore/x86_64SURamDisk environment, then itself requested a restart.
At18:35:27 the next boot had normal boot arguments, no installer-root or restore
arguments, and mounted the new APFS System snapshot xid723. All14 VMBus channels
were captured again. No -nobsdmgroot override was used in this fresh sequence.

Automated VMConnect PrintWindow captures were black, but a direct Hyper-V query at
18:38:41 showed the English Setup Assistant on the new system. This distinction
is essential: the guest is displaying usable setup despite black client captures.
The user later reported clearing the password fields interactively, consistent
with actual console access. A VMConnect rendering failure is therefore NOT
established by these automated captures; the capture mechanism may be the limit.
capture-hyperv-thumbnail.ps1 reproduces this read-only diagnostic and refuses
to overwrite an existing image. The previous working VM remains Off.

Country Switzerland, primary English(US), U.S. input and Set up as new were
selected. A separate local test account was prepared with an independently
generated strong password, stored only in an ignored Windows-DPAPI-encrypted
credential file. No existing user's password was requested or copied.
Account creation/login completion is not yet confirmed at this checkpoint.

See fresh-install-normal-boot-20261025.json for exact source, core/config hashes,
snapshot identity and evidence boundaries. The final sw_vers, loaded core UUID,
first normal desktop and first-time framebuffer installation still need checking.
AppleKeyStore/code-signature warnings occur in the log; absence of panic/root-wait
markers does not mean an error-free log. Raw images and credentials are not
included in the maintainer export.

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

### Setup checkpoint, 2026-10-25 19:28 UTC

The independent local test account was created. After the user returned control,
the optional Apple-account field was still empty, so sign-in was deferred; no
personal Apple credentials were entered or collected. English/U.S. input and
Zurich/Switzerland time zone were selected. FileVault was enabled through setup,
and the recovery-key screen was preserved only in verified Windows-DPAPI-encrypted
local storage. The resulting encryption state has not yet been queried in macOS.
Do not include that screen, the encrypted credential or raw images in a delivery.

At approximately19:11 UTC Continue was selected on Update Mac Automatically,
preserving automatic updates. At19:24 the page still showed its spinner and
disabled Continue button; the menu clock advanced and mouse movement was visible.
Neither an Apple-menu click nor the tested application-opening shortcuts opened
a usable diagnostic shell. No terminal command was typed blindly.

Automatic approval review rejected Command-Q because quitting setup could disrupt
installation/encryption. That command was not executed or retried. A safer,
non-forced Hyper-V guest shutdown request returned32768; serial explicitly reports
that the shutdown daemon is not running. No forced shutdown, reset, process kill,
security reduction or live VHDX mount was performed. The guest remains Running;
the original guest remains Off and preserved. Serial receiver53008 is active.

The19:26:36 bounded369479-byte serial prefix has SHA256
82e16488b668c35baa0fc0da1bb9f71ef744c73e6b69c71b4a6380af2d04c1f3.
It contains no captured panic/root-device-wait/cursor-conversion markers and no
per-call EOM traces. Its raw copy remains local under full-install/snapshots.
See ci/fresh-install-setup-stall-20261025.json for exact build/config provenance.

Confirmed result: blank-disk installation reached normal APFS-root Setup Assistant.
Open blocker: final setup does not complete, and a supported guest-controlled
shutdown is unavailable without its userspace daemon. A SynIC regression,
FileVault deadlock or graphics cause is NOT established by these observations.
Final sw_vers, loaded core UUID, desktop and first framebuffer install remain
unverified. Do not mark the fresh-install acceptance test PASS.

Record online install version, target-volume selection and progress. Do not
interrupt installation for repeated boot tests. Then verify sw_vers, loaded
Release core, synthetic storage/network/input and first desktop. Build and test
a guarded framebuffer FIRST installer against the new guest's actual Aux module
inventory, preserving original Boot/System collections and a cold rollback.
Only then count a full Release desktop with the optional software cursor.

Recovery is not a completed installation. Clean Release has no per-call EOM CPU
traces, so absent EOM trace lines are not new CPU-locality measurements.


## User-authorized restart and first fresh desktop, 2026-10-25 19:46 UTC

The user explicitly approved a hard restart after the final setup stall.
Restart-VM targeted only the new guest at19:40:54 UTC. Its new serial capture
reconnected automatically. Preboot FileVault accepted the independent test
credential when typed slowly, one character per250ms; fast chunked synthetic
input had failed. No personal credentials or recovery key were exposed.

At19:44:15 a normal Finder desktop was directly visible. This establishes the
fresh system desktop after one recovery restart, not a smooth unattended setup.
The read-only Inspect.command completed, confirming macOS26.7.1/build25G241,
x86_64 and loaded core UUID7CAF03F1-3631-33A9-AAAF-581270B665B0 matching Release
run40189441511/source6c35681. FileVault reports On. No framebuffer was loaded.
The inspection report remains in a new private guest HVFreshInspect directory.

The existing Aux has precisely AppleMobileDevice4.0, HighPointIOP4.4.5 and
HighPointRR4.22.1, without a framebuffer. The dedicated first-install helper
refuses another build/inventory or an already present framebuffer, backs up
Aux/Preboot, and builds its candidate before changing installed files. Its first
runtime invocation failed safely with Missing Developer Kit for25G241. The
PRIVATE_BUILD_FAILED marker confirms no active bundle/Aux change. Therefore a
matching KDK is a proven prerequisite for this tested fresh path, not merely an
assumption inherited from the upgrade experiment. Installation with the existing
Apple-signed matching KDK is the next step; loaded framebuffer still pending.

Hot replacement of the original read-only DVD was not immediately recognized.
After ejecting that guest volume, a new DVD at SCSI0:3 exposed HVFRESHFB. A Set
operation on the empty old DVD reported an object-not-found error; the system
remained running, old0:2 is empty, and new0:3 is confirmed mounted. No disk-image
write/mount or old-VM change was used to work around that media issue.
