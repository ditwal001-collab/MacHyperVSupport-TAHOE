# Tested opt-in software cursor workaround

The user reproduced pointer disappearance by clicking Downloads in Finder.
Three or four fast mouse movements restored it briefly. Earlier boots recorded
59 and 161 hardware cursor conversion failures. The source advertises a 32x32
hardware cursor descriptor; exceeding it is a hypothesis, not the proven cause.

Branch `test/tahoe-software-cursor`, source
`c9eb980daab9598b1af6732217147490dacceb3e`, adds only a framebuffer-local bool,
boot-argument check and hardware-cursor capability selection. With
`-hvgfxfbswcursor`, `getAttribute(kIOHardwareCursorAttribute)` returns zero and
IOFramebuffer supplies software cursor rendering. Without the argument the
existing hardware path stays enabled. No cursor packet-size increase or SynIC
change is part of this patch. Existing `flushCursor` hides the host cursor.

CI run40139181101 passed Debug/Release builds and both Clang analyses. Downloaded
ZIP/binary hashes matched uploaded provenance. Debug framebuffer SHA256:
`310f155f50aa2f5ffccd688ba0ef280e268335e209e616ae888f2f73d8133ef3`.
The combined Debug core is byte-identical to the e170982 pacing build:
`803a3d24f6312ce53f1b7385321c37e1a14e28d5c413620634243f821e60c888`.

## Observed runtime result

Test boot began 2026-10-25 00:25:35 UTC on isolated working-copy disks, with
config SHA256 `f2b8dce68e686e349940192cb0f4a53a299e2f5f3b870ab2ceb6acec238fdc81`.
Compared with the preceding config, only the software-cursor boot argument changed
semantically. The new framebuffer0.9.10 was installed in /Library/Extensions.
Serial records its software-mode activation message. A bounded 302283-byte prefix
at00:28:22 contains26 matching-CPU EOM writes,0 cursor conversion failures,0 panic
and0 root-wait markers. Its SHA256 is in evidence/ci/display-03-software-cursor.json.
VMConnect displays the desktop again. The user reports moving the mouse, opening
Safari and opening Downloads successfully, with no disappearance so far.

The initial short Debug result was followed by an11h07 overnight run, confirmed
on2026-10-25 at11:32 UTC: VM Running, receiver alive,26 matching startup EOMs,
zero cursor conversion/panic/root-wait markers in a5432111-byte prefix. See
evidence/ci/overnight-20261025.json. This extends sustained Debug evidence in one
boot; it does not establish repeated-boot stability or clean Release acceptance. Existing
framebuffer0.9.9 was upgraded to0.9.10 together with enabling software rendering;
the version change is another variable. An A/B test with the same0.9.10 binary,
only toggling the argument, remains necessary to isolate its effect. Do not claim
the underlying hardware cursor bug or original installer migration is fixed.

## Tested installation path and rollback

Read the actual loaded module and its on-disk hash first. This guest used
fish.goldfish64.MacHyperVFramebuffer0.9.9 from /Library/Extensions, hash
`51c9cd8c78ceb87f3e373882ea25cfe982f68c4a1e89c6d4ff6985b04038c1cf`.
Replacing only the EFI core cannot update that separate framebuffer component.
Do not enable unsupported framebuffer bootloader injection or weaken security.
The guest's existing custom SIP configuration was retained unchanged.

Two initial guarded installs backed up and restored the old module when the broad
`kmutil install --update-all` failed. Do not repeat that broad command: it tried
unneeded kernel variants and writes to the read-only system volume.

A matching Apple-signed KDK25G241 was installed in the test guest after checking
its signature chain to Apple Root CA. Source: dortania/KdkSupportPkg release25G241,
asset Kernel_Debug_Kit_26.7.1_build_25G241.dmg, SHA256
`9045a521c8ae362d4cb2cc54701b03462686e0069518a0b66cfe2028f87dfe9b`.
Do not redistribute the KDK inside this handoff. Whether the final Aux-only
procedure needed an installed KDK was initially untested. The subsequent fresh
25G241 installation was tested without it: the private Aux build explicitly
failed with Missing Developer Kit before any active bundle/collection change.
This establishes the matching KDK prerequisite for that fresh tested system.

The successful procedure used a new private output file and:

```sh
kmutil create -n aux -V release -a x86_64 -x \
  -p /Library/Extensions/MacHyperVFramebuffer.kext \
  -p /Library/Extensions/HighPointIOP.kext \
  -p /Library/Extensions/HighPointRR.kext \
  -p /Library/Apple/System/Library/Extensions/AppleMobileDevice.kext \
  -B /System/Library/KernelCollections/BootKernelExtensions.kc \
  -S /System/Library/KernelCollections/SystemKernelExtensions.kc \
  -A PRIVATE_CANDIDATE_AUX_PATH
```

Those four paths are the tested guest's actual inventory, not a universal list.
Inspect the existing Aux collection first and preserve every existing bundle ID
and every other module version. Do not deploy the earlier one-module probe.
Back up and hash-verify the old bundle and Aux collection in an exclusive new
directory. Normalize candidate root:wheel ownership, directories755, files644,
executable755. Verify the candidate executable hash before writing the active path.

The guarded installer verified the full four-module list, built the private Aux,
confirmed other versions unchanged, atomically replaced only the Data-volume Aux,
ran the existing Apple kcditto staging helper and rechecked the original read-only
Boot/System collection hashes. All checks passed. Original module and collection
backups remain preserved. This procedural reproduction is Intel/Tahoe-specific;
inspect installed tool help and local layout rather than copying paths blindly.

Rollback restores the saved old bundle and old Aux collection and verifies their
hashes; resynchronize the appropriate boot cache before reboot. Remove the optional
argument only from an Off/detached/backed-up EFI test image. Never overwrite backups.

Guest shutdown completed but Hyper-V stuck at Stopping. Stop-VM returned InvalidState;
only the verified test VM's worker was terminated. Hyper-V automatically restarted
it, after which normal target-only TurnOff reached Off. This is a host finalization
incident, not a clean repeated-boot success or evidence of a SynIC regression.
The fresh EFI was prepared only after confirmed Off, source detach and copy/hash
verification. No original VM disk, protected backup or other VM was modified.

## Evidence reading

Windows directory enumeration may show a stale zero size for an open log. Use
`BuildScripts/snapshot-serial-log.py` to preserve a bounded handle-read prefix.
Do not infer a capture gap from Get-ChildItem.Length alone. Local WMI thumbnails
were useful when VMConnect went black; a temporary local viewer is operational
diagnostics only and its cursor behavior is not driver validation.
