DELIVERY 2026-10-25 20:21 UTC: full fresh test/docs pushed at14d6ebf.
New Hyper-V-only maintainer archive evidence/packages/hyperv-maintainer-20261025T202025Z-cc97e0bc.zip
SHA256487034944f5c0356f00d35ccba066c0662f2c9662628eaa74cc4b8613b83fef7,
91 entries; patch reconstruction/CI binary/privacy/archive readback PASS.
Guide includes direct Recovery, observed setup recovery, KDK/first-install ISO
builder and precise validation limits. Existing local scratch files preserved.
Final prepared helper ISO: full-install-20261025-01/final-first-install-media/
FreshFramebuffer.iso (not attached; combined revised helper not rerun from blank).
Old guest Off; new guest Running; logger53008 remains active. No pending user input.
LATEST 2026-10-25 20:17 UTC: FIRST FULL FRESH TAHOE RELEASE DESKTOP CONFIRMED.
26.7.1/25G241, loaded core UUID7CAF03F1-3631-33A9-AAAF-581270B665B0 and
framebuffer UUID3C6D0CDD-D9E7-39C8-94FB-D97A47BE3CF6 match CI run40189441511
source6c35681. Canonical-path Aux repair completed; normal restart20:07:18,
UUID check20:12. New system originally BLANK; no old system migration.
HTTPS200/Safari and Finder/Downloads/mouse short smoke pass;14channels/software
cursor marker;198959-byte prefix SHA84248655... no panic/root-wait/cursor failure.
Exact hashes/limits: ci/fresh-install-full-release-20261025.json. Not repeat stability.
All4 temporary DVD volumes guest-ejected, new SCSI0:3-6 DVD devices removed;
only empty DVD0:2 remains. ISOs/backups preserved. New t_full_test Running,
old srv-maos-devs11 Off. Serial53008 active, current log200718Z-c7b68ed1.
Initial final-setup hang needed USER-APPROVED hard restart. Live kmutil load was
REJECTED/not executed; no security bypass. Final first-install script includes
private probe then canonical build; stages tested separately, combined second
blank installation not rerun. No generic EFI-from-scratch template yet.
LATEST 2026-10-25 20:03 UTC: first normal post-install framebuffer boot reached
desktop but kextstat shows NO loaded framebuffer. Aux still contains4modules,
framebuffer path points to private staging bundle; canonical-path hypothesis
is being tested via separate guarded Repair.command. Do NOT claim full success.
Manual live kmutil load was REJECTED by auto-review and NOT executed/retried.
Safer documented Aux/reboot path only. Repair backup HVFreshPathRepair.KdmrduY5y
(check exact name in console if needed); private build running at20:02.
New media HVFBPATH at SCSI0:5; earlier HVFRESHFB0:3, matching KDK0:4, empty0:2.
No security reduction. Old VM Off, serial53008 alive, current log195630Z-8d7014ce.
LATEST 2026-10-25 19:56 UTC: matching KDK installed successfully after rechecking
DMG SHA9045a521... and Apple package chain. First framebuffer installer succeeded:
FRESH_FRAMEBUFFER_INSTALLED /Users/Shared/HVFreshFramebuffer.RA6Ywuz3.
Release executable d8a079d4..., original3 Aux modules preserved plus FB0.9.10;
Boot/System SHA checks passed before/after, Aux/kcditto backups retained.
Normal guest sudo shutdown -r now requested for loaded UUID validation. Serial53008
active. DO NOT count full framebuffer boot until actual loaded UUID confirmed.
Fresh macOS26.7.1/25G241/core Release UUID verified; FileVault On. Old VM Off.
LATEST 2026-10-25 19:44 UTC: USER EXPLICITLY APPROVED HARD RESTART of
new t_full_test after final-setup stall. Restart-VM -Name t_full_test -Force
executed approx19:40:54 UTC. Old guest remains Off; no disk mount/backup change.
Logger53008 reconnected: serial-20261025T194054Z-443f3939.log.
FileVault preboot accepted local DPAPI test password after SLOW TypeText one
character/250ms (8-character fast chunks failed; no password exposed).
Normal Darwin boot now underway. Need desktop/sw_vers/core UUID/FileVault/Aux.
Pre-restart384171-byte prefix SHA5974663f02f5e691674a3da2ab7f611ade286e5a995a670eb7f930558d6945f0.
LATEST 2026-10-25 19:28 UTC: new test account created, Apple sign-in deferred
with empty field; FileVault Turn On selected/key protected by DPAPI. Setup stalls
on final Update Mac Automatically since approx19:11 UTC. Clock/mouse responsive,
no usable shell/desktop. Command-Q REJECTED by auto-review; NOT executed/retried.
Safer non-forced Msvm_ShutdownComponent request returned32768, serial confirms
shutdown daemon absent. NO force/reset/kill or security bypass performed.
New guest Running, old guest Off/preserved, receiver53008 alive. Keep logging.
Final sw_vers/core UUID/desktop/framebuffer FIRST install still UNVERIFIED.
See FRESH_INSTALL_TEST.md and ci/fresh-install-setup-stall-20261025.json.
Do not count fresh test PASS; resolve lifecycle blocker before another boot.
LATEST 2026-10-25 19:10 UTC: optional FileVault deferral was REJECTED by automatic
approval review as an unapproved security reduction. Do not retry/bypass it.
Safer path taken: Turn On FileVault. Recovery-key screen saved ONLY as ignored
local filevault-recovery-screen-private.dpapi; Windows DPAPI decrypt/hash round
trip verified, exact newly generated plaintext key screenshot removed after
verified encrypted backup. Account password likewise testadmin-private.clixml.
No recovery key, password or authentication image may enter Git/package.
Old encrypted VM unchanged/Off. New Setup now at appearance, English/Switzerland,
U.S keyboard, local testadmin, Apple account deferred while its field still empty.
No global security changes. Check FileVault progress after desktop; do not power
interrupt active encryption. Need version/core UUID/Aux inventory and framebuffer.
LATEST 2026-10-25 19:01 UTC: Following user's latest explicit return of control
('mach du weiter'), agent resumes setup. Apple sign-in remained completely empty;
no personal login was begun. Chose Sign in Later in Settings / Skip so optional
Apple authentication does not block driver validation. No credentials collected.
Use direct thumbnails for setup. Account testadmin created, DPAPI password local.
LOGGER CHECK 2026-10-25 18:57 UTC: new receiver PID53008 remains active and
fresh VM Running; old VM Off. Old receiver PID48800 is no longer present.
Old logs are preserved. Before any future old-VM start, restart its receiver
on its original pipe; do not assume old PID liveness from historical notes.
Apple-account UI remains user-owned; no additional screenshots or input issued.
LATEST 2026-10-25 18:52 UTC: local testadmin creation completed; Setup Assistant
now at Sign In to Your Apple Account with EMPTY email field. User explicitly
wants to sign in personally; informed user that page is ready. Automated input
AND screenshots paused until user signals completion. No personal Apple account
credentials collected, typed by agent or stored. Independent doc work may continue.
Test credential DPAPI file still local only. Current helper/script state in Git.
CORRECTION 2026-10-25 18:51 UTC: black PrintWindow captures DO NOT establish a
VMConnect rendering failure. User could clear local password fields interactively;
direct thumbnails show live Setup Assistant. Treat capture limitation/client
freshness as unverified, not as a new confirmed driver bug. User returned control;
agent refilled both test password fields and Continue shows Creating account.
No interactive diagnosis viewer was started; direct WMI thumbnails suffice.
LATEST 2026-10-25 18:47 UTC: user requested to sign into their Apple account.
ALL automated keyboard/mouse input and GUI captures paused to avoid conflict or
capturing authentication screens. Continue independent documentation only until
user indicates login done. Local testadmin fields were filled but Continue had
NOT yet been clicked by agent; actual current setup state must be rechecked later.
DPAPI credential stays local, never print password. Old VM remains Off.
LATEST fresh install 2026-10-25 18:41 UTC: normal installed APFS System boot at
18:35:27 reached ENGLISH SETUP ASSISTANT. No installer/restore/bsdmgroot args;
root snapshot xid723;14channels. VMConnect is BLACK but direct Hyper-V thumbnail
shows real usable setup (country Switzerland selected, now Set up as new).
Do NOT blindly reset. Use new read-only BuildScripts/capture-hyperv-thumbnail.ps1
via ScriptBlock, -VMName t_full_test -OutputPath NEW.png, to observe actual GUI.
Guest resolution1024x768, thumbnail1280x720 has active960x720 at x160: native
x=(thumbnailX-160)/0.9375, y=thumbnailY/0.9375. WMI input works, U.S keyboard.
Testadmin password generated in ignored test root/testadmin-private.clixml,
DPAPI encrypted. Never print it. It is NOT yet entered/created in the guest.
Serial root/serial/serial-20261025T183527Z-1b51154c.log, PID53008 active.
Read-only FreshTools-v2.iso prepared (not attached), with Inspect.command and
Release Framebuffer.zip. No new guest framebuffer installed yet. Old VM Off.
LATEST fresh install 2026-10-25 18:20 UTC: Apple18.381GB package downloaded and
extracted; automatic guest reboot18:19:08. New macOS Installer entry correctly
selected; Enter confirmed. Now Apple logo installation with29min estimate.
Current serial root/serial/serial-20261025T181908Z-c2f2f36d.log; PID53008 active.
Both Recovery and staged-installer boots enumerate14channels with no captured
panic/root-wait. NOT a normal desktop yet. Do not reset/stop/mount live disks.
Read ci/fresh-install-phase2-20261025.json, FRESH_INSTALL_TEST.md. Old VM Off.
LATEST TASK 2026-10-25 18:05 UTC: User explicitly authorized NEW VM t_full_test
for a direct Tahoe blank-disk installation and requested old VM shutdown.
Old srv-maos-devs11 user-shutdown confirmed Off; keep it Off and preserved.
Branch test/tahoe-fresh-install, local root evidence/local-tests/full-install-20261025-01.
New EFI copy: own identity, remove -nobsdmgroot, Apple Recovery26.6.2/25G83,
core clean Release6c35681/run40189441511. New400GiB System.blank.vhdx ONLY.
New VM first boot reached Tahoe Recovery/all14channels. New blank guest disk2
429.5GB was explicitly verified then APFS/GPT FullTest initialized. Installer
GUI now open. Installation NOT yet complete; do not interrupt it.
Serial independent PID53008, pipe t_full_test_serial; directory root/serial.
Old logger48800 preserved. Fresh keyboard target MUST be t_full_test, NOT oldVM.
Capture helper root/capture-console.py selects only t_full_test VMConnect.
Read Docs/handoff/FRESH_INSTALL_TEST.md and evidence/ci/fresh-install-preparation-20261025.json.
No old system clone, other VM changes or backup overwrite. Scope expansion comes
from the user's latest explicit request, superseding old one-VM-only restriction.
LATEST 2026-10-25 13:37 UTC: FULL RELEASE DESKTOP BOOT VERIFIED. Loaded core and
framebuffer UUIDs both match original run40189441511 Release binaries. User
reports faster/satisfactory operation. Read rc1-release-boot-20261025.json and
RELEASE_RC1.md. Current isolated Release pair stays Running, backups preserved.
One full Release success, NOT ten-start/stability acceptance. Serial receiver48800
continues; current serial-20261025T133215Z-a781464d.log. No per-call EOM traces.
Earlier prekernel shutdown/timeouts remain open, no authentication bypass.
LATEST 2026-10-25 13:23 UTC: guarded Release framebuffer installation SUCCEEDED,
marker and expected d8a079d4 executable hash observed. Four-module Aux preserved;
Boot/System hash checks OK. Backup /Users/Shared/HVReleaseRC1.s0ZkXpJy retained.
Normal Apple-menu restart initiated; inspect current console/serial and loaded
module identities. Both Release files now installed; runtime acceptance pending.
Older statements that framebuffer is still Debug are historical and superseded.
# Tahoe SynIC development handoff

LATEST EVENT CHECK: Worker18508 confirms guest-requested shutdown at2026-10-25
12:09:22 UTC, after start18500 at12:03:53. It was not a host Stop/Reset and
occurred BEFORE obsolete-image cleanup12:18. New serial file still empty;
pre-kernel unlock timeout is only a hypothesis. No Release kernel boot claimed.
Agent will restart target once for local unlock; re-query actual current state.
No security setting or authentication bypass was introduced.

PACKAGE / CLEANUP CHECKPOINT 2026-10-25 12:18 UTC: Hyper-V-only package
evidence/packages/hyperv-maintainer-20261025T121628Z-40dd7327.zip,
SHA2564348d3bae44d04f8b52d14d7ff440cdfe74349b7a1b9fe313d3d82ce8eefaf33;
72 entries, source reconstruction, original CI hashes and privacy/scope PASS.
No application-setup content. See LOCAL_STORAGE_RETENTION.md (operational,
excluded from package). User-authorized cleanup removed ONLY five old inactive
experimental EFI images and duplicate host KDK DMG:6.23GB logical,6.228GB
observed free-space increase. No active/rollback/original/protected disk deleted.
All raw serial evidence and CI archives remain. Deleted image paths in older
historical notes are intentionally no longer current recovery inputs.
Current Release preparation still waits at local pre-kernel unlock; receiver
48800 active. Guarded framebuffer installation and full Release test not yet run.

LATEST 2026-10-25 12:07 UTC: overnight Debug run verified11h07, no captured
EOM CPU mismatch/cursor conversion/panic/rootwait. Clean combined RC1 source
6c3568178ba21136b8c21dd45597476c74ec31d1 on release/tahoe-clean-rc1 passed
CI40189441511 Debug/Release and Clang. Read RELEASE_RC1.md and HYPERV_SETUP.md.
Root branch maintainer/hyperv-release-delivery intentionally excludes application
setup commits; their separate branch remains preserved. New Hyper-V-only exporter
reconstructs five clean patches and checks original CI binaries/privacy/scope.

Current VM is Running at LOCAL PRE-KERNEL UNLOCK, no new kernel output. Do not
send shell commands into that password field. New isolated disks:
local-tests/release-rc1-test-20261025-01/EFI.release-rc1.vhdx and
System.release-rc1.vhdx at SCSI0:0/0:1. Full cold hashes match Debug sources;
old overnight pair is detached/preserved. New EFI core isc97e2919..., config
f2b8dce6... unchanged. Framebuffer is STILL Debug310f155f... until guarded
guest install from read-only HVRELRC1 DVD0:10. This preparation boot is not a
complete Release test. Serial PID48800 alive, current log
serial-20261025T120334Z-e3581efd.log empty by actual handle read at12:07:56.

After LOCAL unlock, verify desktop/root context and run the guarded installer
files/InstallAux.command from the Release test root via its DVD. It requires
normal local sudo authentication, preserves all four Aux IDs/other versions
and root Boot/System hashes. Then normal reboot; verify BOTH Release core
c97e2919... and framebufferd8a079d4... before acceptance. Target10 clean boots;
none counted yet. No password stored. Do not use broad kmutil --update-all.

Normal Hyper-V shutdown first failed0x80004005. macOS-menu shutdown succeeded
and Off was verified11:49 without reset/worker kill. All source disks detached
before cold copying. User requests obsolete test/media cleanup AFTER package
verification; inventory saved locally, not a deletion approval for active disks,
originals, protected backup or current Debug rollback pair. Do not delete those.

LATEST SUCCESS CHECKPOINT 2026-10-25 00:28 UTC: software cursor workaround active
on isolated test copies. c9eb980/run40139181101 framebuffer0.9.10 installed through
guarded four-module Aux rebuild; core803a3d24... unchanged. Fresh Off/detached EFI
copy enables -hvgfxfbswcursor; configf2b8dce6... . VM RUNNING, desktop visible in
VMConnect; serial activation marker1,26 matching EOM writes,0 cursor conversion
failures/panic/root wait in bounded prefix. User reports Safari, Downloads and
mouse working so far. Read CURSOR_WORKAROUND.md and latest UNATTENDED.md; older
password/rollback notices below are superseded. Sustained/repeated/Release pending.

IMPORTANT live-log correction: Windows directory listings reported stale zero
sizes for the open capture. Actual handle-based read confirms current boot data:
16 matching-CPU EOM writes,7 cursor conversion failures, no panic/root-wait in
bounded prefix. Use BuildScripts/snapshot-serial-log.py, not Get-ChildItem Length
as liveness proof. Guest Tahoe26.7.1/25G241 is verified. Cursor installer rolled
back safely because KDK missing; matching Apple-signed KDK now verified/mounted,
but local sudo auth expired and sudo -s waits for LOCAL password. No commands
while password prompt. Read latest UNATTENDED.md; no cursor fix claimed.

LATEST cursor work: candidate c9eb980 on test/tahoe-software-cursor passed
CI40139181101 Debug/Release and analyses; downloaded binary/ZIP hashes verified
in evidence/ci/run-40139181101-verified.json. NOT installed or runtime validated.
Target restarted on unchanged e170982 copies for guest module inspection; local
pre-kernel unlock is the current blocker. Read-only HVCURSORTEST ISO attached at
SCSI0:2 (Inspect.command plus candidate ZIP), no automatic installer/security
changes. See latest UNATTENDED.md. Do not confuse candidate availability with fix.

LATEST 2026-10-25 local: VM Running and full macOS desktop visible in target
VMConnect. User reports fast mouse movement but disappearing black pointer.
Prior OFF/unlock notices below are historical. Preserve interactive session.
PID48800 receiver is alive but current log zero bytes: current-boot SynIC evidence
is unavailable. See UNATTENDED.md and GRAPHICS_REFRESH_REPORT.md latest entries.

FINAL STATE CHECK: VM is now Off after waiting at local pre-kernel unlock; cause
of the poweroff is unverified, new kernel log still empty. Do not auto-restart
or claim the pacing candidate ran. Local start/unlock is required for runtime
comparison. See latest UNATTENDED.md and ci/display-02-pacing-pending.json.

CURRENT BLOCKER (2026-10-24 19:44 UTC): 33-ms pacing candidate e170982/run40124452997
passed all build/analysis/hash checks and is staged on another EFI copy, but VM
waits at a local pre-kernel unlock screen. No new kernel output/mouse improvement
is proved. Local password entry in the VM is necessary; do not request it in chat.
Read latest UNATTENDED.md and GRAPHICS_REFRESH_REPORT.md. Earlier 3d31e11 restored
visible input but mouse movement was slow; no stable mouse fix is established.

LATEST (2026-10-24 19:20 UTC): user testing exposed frozen VMConnect output despite
fresh WMI previews. Separate startergo refresh backport 3d31e11/run40101047189 is
now installed on another EFI copy and user confirms input working; Setup Assistant
is visible. Mouse movement is slow. Separate 10 -> 33 ms pacing experiment e170982
is building in run40124452997 and is NOT yet installed. Read GRAPHICS_REFRESH_REPORT.md
and latest UNATTENDED.md first. SynIC source is unchanged; original disks preserved.

CURRENT RESULT (2026-10-24 17:22 UTC): the VM has reached a live normal Tahoe
password login screen on isolated system/EFI copies, using the 0756f1d binary.
All 14 channels and 24 matching-CPU EOM writes observed. Read
[TAHOE_BOOT_RESULT.md](Docs/handoff/TAHOE_BOOT_RESULT.md) and
[UNATTENDED.md](Docs/handoff/UNATTENDED.md) FIRST; they supersede older operational
status below. Original system is detached/preserved. Active disks are ignored
local test files: never delete/move them or clean that directory while attached.
Personal account login, original migration completion and release stability
remain unverified. No password prompt to the absent user is required.

Read [the technical report](Docs/handoff/SYNIC_EOM_REPORT.md),
[observations](evidence/OBSERVATIONS.md), [results](evidence/RESULTS_LOG.md),
[patch plan](PATCH_PLAN.md), and [reproduction procedure](REPRODUCE.md).

Development branch: `fix/synic-eom-cpu-affinity`.
Functional candidate: `670b352156c0cdd044e9f211577741c1d0f7dfcc`.
Run `40087952850` FAILED: OSMemoryBarrier was undeclared (see the sanitized
diagnostic in evidence/ci). Header repair `ad9a0b3` was pushed and started run
`40090195466`. Separate CI/provenance commit `91a5eb7` was pushed and started
run `40090291711`. Both follow-up runs FAILED with the same undeclared barrier.
Compiler full-fence repair `0756f1d` replaces the unavailable API with
`__sync_synchronize()` and started run `40090495930`, now SUCCESS for both
Debug/Release builds and analyses. Downloaded package and kext hashes match
CI provenance; see evidence/ci/run-40090495930.json.
Git/network operations work through targeted escalations after the restart.
The user authorized Git/gh development commands without repeated questions.
Documentation/export baseline `c3d417b` is committed and pushed; inspect the
actual Git status for newer observations. Existing .bak files must not be staged.

The original handoff was found in the sibling `../HANDOFF` directory, not in
`docs/handoff`. Its reported boot observations have not been independently
reproduced. Private machine paths and raw logs were not imported.

The user explicitly authorized autonomous Hyper-V/VM test steps after restart
and required serial logging. This authorization is confined to srv-maos-devs11.
The VM was Off. A new, hash-verified EFI copy was created in
`evidence/local-tests/vm-test-0756f1d-20261024-01/EFI.test.vhdx`; only its Monterey
executable was replaced, with original kext backed up. The original EFI VHDX
and protected Sequoia backup are unchanged. The test image is now attached at
SCSI 0:0 and the VM is RUNNING. Do not delete/move this ignored image while
attached. No direct offline write was made to the system VHDX.
The original foreground receiver (exec session 51796) ended. There is a serial
coverage gap from 12:34:13.99 to 12:36:24.48 UTC; do not claim complete upgrade
coverage or absence of errors during that interval. A separate hidden process
was started via Start-Process; Python PID 46464 is recorded in the local test
directory's serial-reconnect-02/capture-ready.json. It is connected and writing
new data. Inspect actual process/file liveness rather than assuming that a
foreground tool session survives a completed assistant turn.
Both directories preserve unique files and support reconnects. The first boot passed enumeration and APFS root
with 21 matching-CPU EOM writes. Installer/login completion remains pending;
do not interrupt an active upgrade for repeated-boot testing.
At 12:27 UTC the same boot was still emitting serial storage traffic, with
about 79 MiB captured, no new boot, and no SynIC/root-wait/panic failure.
Upgrade completion remains UNKNOWN; do not infer completion from installer UI
process activity or treat active I/O alone as a progress percentage.

Next: keep capturing serial and observe installer/login progress without
interrupting an active upgrade; document the outcome, commit documentation
separately, then perform repeated and clean-release tests when safe. No stable
runtime fix is established by this one instrumented pass.

The first clean source branch `test/synic-eom-clean-20261024` (b9a9719/da2bd1b)
is SUPERSEDED: it mistakenly used cd66095f rather than the actual c48fc5c base
of the tested development line. Its worktree remains preserved under
`evidence/local-tests/clean-worktree`; do not use it for an isolated comparison.
The exporter is corrected to c48fc5c and checks for unexported baseline changes.
Earlier package ZIPs declaring cd66095f as base are superseded. None of this
changes the active VM's instrumented binary or its source provenance.
Corrected clean branch `test/synic-eom-clean-c48fc5c` is pushed: functional
commit `7a3b98a`, CI head `c960997`. Worktree is
`evidence/local-tests/clean-c48-worktree`. Its CI conclusion is unverified.
Graphics/framebuffer/packaging match the instrumented tested baseline exactly.

Second captured boot: new serial connection at 13:21:34 UTC after the user
reported booting. By 13:24 UTC it again enumerated all 14 channels, completed
scan, started SCSI and resolved APFS root; 16 logged EOM writes matched CPU 0,
with no captured panic/root wait. WindowServer was spawned. Receiver PID 46464
automatically reconnected into a new file under serial-reconnect-02. See
evidence/ci/boot-02-0756f1d.json. Full installer/login completion is still not
established; two observed passes do not establish release stability.
IMPORTANT environment correction: the second boot is Sequoia Recovery,
Darwin 24.4.0; user sees "Reinstall macOS Sequoia". The first was Darwin
25.6.0 in Tahoe's installer environment. Do not count the Recovery boot as a
second Tahoe boot or an upgrade success. Do not choose Sequoia reinstall.
