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
