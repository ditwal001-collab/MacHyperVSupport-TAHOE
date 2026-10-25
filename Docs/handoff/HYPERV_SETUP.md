# Hyper-V setup and configuration audit

This report describes one authorized Generation2 test VM. All names, VM IDs,
addresses, switch names, pipe names, platform serials and local disk paths are
omitted. The machine-readable current profile is
`evidence/ci/hyperv-profile-20261025.json`. Settings are observations, not a
universal VM creation recipe or proof that each value was changed by this work.

## Observed host and VM

The original handoff reports Windows11 Hyper-V on Intel Core i9-12900HX.
The current Hyper-V query confirms Generation2, configuration version11.0,
8 virtual processors and fixed24GiB memory (dynamic memory disabled). The initial
handoff already recorded8vCPUs/static24GiB, so these are pre-existing settings;
no CPU/RAM tuning was introduced by the SynIC patch.

| Setting | Current observed value | Change attribution |
| --- | --- | --- |
| Nested virtualization | False | No change recorded; initial value not independently captured |
| CPU migration/legacy compatibility | False/False | No change recorded; initial values unknown |
| CPU maximum/reserve/weight |100%/0%/100|Current snapshot only|
| Firmware Secure Boot |Off|Current snapshot only; not disabled by this patch/install procedure|
| Network boot protocol |IPv4|Current snapshot only|
| Display |Maximum1920x1080|Initial handoff already reports1920x1080; no resolution change recorded|
| Synthetic network |One adapter, External switch|External switch reported in initial handoff too; no switch/host networking changes recorded|
| MAC spoofing/DHCP guard/router guard |Off/Off/Off|Current snapshot only|
| Automatic checkpoints |Disabled|Current snapshot only; no checkpoint/restore performed by this workflow|
| Automatic start/stop |StartIfRunning/Save|Current snapshot only; no host-wide lifecycle policy change recorded|
| COM1 |Named pipe configured|Already present in original handoff; receiver restarted/reconnected without changing port|
| COM2 |Not configured|Current snapshot only|

The guest-service interface is disabled; heartbeat/shutdown/time-sync are enabled.
KVP and VSS are enabled but reported No Contact at collection time. This is a
status observation, not proof that all userspace integration daemons are running.
No host-wide CPU settings, ACLs, execution policy or security protections were
changed by this procedure.

## Storage and lifecycle changes actually performed

Original layout was SCSI0:0 EFI VHDX and SCSI0:1 system VHDX. During investigation
the agent selected isolated working copies in those same slots. Original system,
original EFI and the separate working Sequoia backup remain preserved. Current
working EFI is a dynamic VHDX of5367677440 virtual bytes; the system disk is a
dynamic400GiB VHDX. Both report512-byte logical/4096-byte physical sectors.
These sizes describe the current disks; no resize or format was performed.

Each EFI modification used a unique copy while the VM was Off and the edited
image detached. Hash checks verified the cold copy before replacing only the
intended core executable or boot-argument entry. The test EFI was unmounted on
the host before attaching it back at0:0; firmware first-boot selection was set
to the test EFI where necessary. No existing backup was overwritten.

Read-only optical media carried inspection/guarded installer content and the
matching Apple KDK; optical slots are transient laboratory details, not boot
requirements. They are not distributed as VM disk images. COM1's existing pipe
was retained; a separate host receiver captures continuously across reconnects.

A previous guest shutdown finished but Hyper-V remained Stopping. After verifying
the guest's completion and uniquely matching its worker, only that worker was
terminated; Hyper-V restarted the VM automatically, then normal target-only
poweroff reached Off. This was an exceptional host-finalization recovery, not
a recommended normal reboot procedure or evidence of clean shutdown stability.
No other VM or global Hyper-V service was operated on.

On2026-10-25 the Debug overnight run ended with a normal macOS-menu shutdown:
Hyper-V integration shutdown first returned0x80004005, but the menu path logged
orderly driver poweroff and reached Off without a hard reset. A new full system
and EFI pair was cold-copied and hash-verified for clean Release testing. The
overnight pair remains the retained full rollback point. This current shutdown
observation does not retroactively turn the earlier host incident into a clean
shutdown or resolve the integration error.

## EFI/OpenCore profile and audited changes

Initial saved configuration SHA256:
`430d1f347fa0b5271cd212e1c35692013b252361eccc8ba5f0ff6c3ec95368eb`.
The overnight working profile SHA256:
`f2b8dce68e686e349940192cb0f4a53a299e2f5f3b870ab2ceb6acec238fdc81`.
The corresponding summaries omit all platform identity. The latter was rebuilt
in memory from the saved before-cursor file and the recorded single append;
its byte hash matches the recorded installation audit. It is not a new live
mount/read of an attached VHDX.

Verified changes on test copies:

1. Replace the Monterey core executable with the pinned candidate build. The first
   audit showed only that executable changed and configuration unchanged.
2. Append `-nobsdmgroot` for a residual installer BaseSystem boot selection on the
   working system copy. This is a lab boot-profile workaround, not an upgrade
   migration fix or part of the SynIC source correction.
3. Remove only `-hvstormsgdbg` from that test profile to avoid the extreme storage
   packet-log flood. Other diagnostic arguments and serial output were retained.
4. Select graphics refresh/pacing builds on later EFI copies.
5. Append `-hvgfxfbswcursor` to opt into software cursor rendering. Compared with
   the immediately preceding configuration, this was the only semantic change.
   The separate framebuffer component was updated in the guest Aux collection.

Pre-existing EFI settings retained unchanged include ProvideCurrentCpuInfo=true,
CPUID data55060a00000000000000000000000000 and mask
ffffffff000000000000000000000000, and custom csr-active-config03000000.
Three enabled ACPI tables are present in the saved order:
SSDT-HV-DEV, SSDT-HV-PLUG, SSDT-HV-VMBUS. This records the tested order; the upstream
README recommends VMBUS/DEV/PLUG. No ACPI reorder was part of this investigation,
and this report does not silently prescribe one for the tested guest.

Lilu/VirtualSMC are enabled. The legacy core applies through kernel20.99.99;
Monterey core starts at21.0.0. Framebuffer injection is disabled in OpenCore:
the framebuffer is installed separately in `/Library/Extensions` with an Aux-only
rebuild as described in CURSOR_WORKAROUND.md. Do not enable injection as a shortcut.
Existing SIP configuration was queried and preserved, not weakened further.

## Reproduction and rollback

Use a dedicated test VM and separate EFI/system working copies. Inventory its
actual settings and original Aux modules first. Start serial capture before
boot. Keep CPU topology, ACPI and unrelated kexts constant while comparing builds.
For the core replace only the matching binary on a detached EFI copy, preserving
the original. For framebuffer use a verified backup and a private Aux-only build
that retains all existing module IDs/other versions; never blindly rebuild only
one third-party module. Preserve root Boot/System collections and security state.

Restore the preserved disk selection and previous framebuffer/Aux backup for
rollback; validate hashes before boot. Never host-mount or edit an attached live
disk, overwrite backups, format volumes, or power off during an active installer.
The read-only profile collector takes an explicit VM name and refuses to overwrite
its output; it exports no identifying values and performs no configuration change.
