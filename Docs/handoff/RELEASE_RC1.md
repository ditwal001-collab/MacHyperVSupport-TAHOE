# Clean combined release candidate RC1

Pinned source: `6c3568178ba21136b8c21dd45597476c74ec31d1`, branch
`release/tahoe-clean-rc1`. GitHub Actions run40189441511 completed successfully
on2026-10-25: Debug/Release package builds and both Clang analyses passed.
Coverity is upstream-owner-only and was skipped. This is a candidate build,
not a stable release designation or a public GitHub Release publication.

## Source content and attribution

The branch starts at the already compiled clean SynIC source c960997, rooted at
startergo's GraphicsBridge base c48fc5c. Three separate graphics commits are
cherry-picked: a76f66a (startergo refresh hunk, original author preserved),
ac18838 (33-ms refresh pacing),6c35681 (opt-in software cursor).
The CPU patch retains owner-CPU migration, scheduler switch, IRQ-protected CPU
verification, slot-clear/full fence/pending ordering, EOM and prior affinity
restoration. It retains fail-closed error guards and the pre10.6 fallback.

Compared with the tested instrumented c9eb980 source, only the extra diagnostic
code in ControllerInterrupts/VMBus is absent: duplicated TAHOE-SYNIC entry logs,
sampled trace variables, per-call EOM traces and VMBus enumeration/sleep traces.
No `TAHOE-SYNIC`/`TAHOE-DEBUG` strings remain in the new source or Release binaries.
Normal upstream logging and error messages remain. Choosing Release alone would
not have constituted this source cleanup; the clean branch is independently
reviewable. The optional software cursor still requires `-hvgfxfbswcursor`.

## Exact build provenance

Original Release ZIP SHA256:
`162f47670ef9f4640bdfdefd8ba9495b1a039ca6828a52f5ec4498e9d3cb5d6c`.
Release Monterey core:
`c97e29193de9bedf9e2f39b7da38a589347874f7f8ef8c0c8e24f92d7f76ca16`.
Release framebuffer:
`d8a079d47d61988aabe40cb788b015979c27384135b57339e854d5c017792122`.
Debug ZIP:
`fab4ca6d2c29319e0bb89dcfbb234b86161fa5ddde2170758fea19d307b070ff`.
All package and executable hashes match uploaded CI provenance, including both
the build outputs and their packaged copies. thread_block import is present.
See `evidence/ci/run-40189441511-verified.json` and original Provenance files.

Runner was macos15 image20260824.0482.1, macOS15.7.9/24G830, Xcode16.4/16F6,
Apple clang17.0.0. MacKernelSDK is pinned to
3f750085caa17ec3a7880f11c11bf4f48cd6a164, ocbuild to
020b14fa68a9825642e0c0fb643c2963bd679ae3 and Lilu1.7.2 Debug SDK is SHA-verified.
Hosted image/transitive bootstrap downloads still limit bit-identical rebuilds.

## Runtime validation plan and boundaries

The previous Debug pair survived an11h07 overnight run. That validates one long
instrumented session, not the clean Release. Its26 matching EOM calls are the
captured startup calls; uptime is not evidence of additional EOM sampling.

RC1 testing preserves that entire overnight disk pair and creates unique cold
EFI/system copies while Off/detached. Both copies must hash-equal their sources
before modification. Replace only the Monterey executable on the new EFI and
leave the configuration hash f2b8dce6... unchanged for the first comparison.

An initial preparation boot uses clean Release core with the previous Debug
framebuffer until the guarded guest Aux installation succeeds. Label it mixed,
not a full Release acceptance boot. The installer requires the exact existing
Debug framebuffer hash, keeps an exclusive backup, preserves all existing Aux
module IDs/other versions and root Boot/System hashes, and swaps only the new
framebuffer/Aux outputs. It does not change security settings or reboot itself.

After both Release components are installed, verify boot enumeration/storage,
normal GUI, mouse/cursor behavior, networking and sustained I/O, followed by
repeated starts and normal shutdown/restart. REPRODUCE.md's clean-Release target
is10 starts; do not claim that target was reached unless each attempt is logged.
Clean source has no per-call EOM traces, so those counters cannot be presented as
new live measurements in clean Release. Retain Debug evidence separately.

## Pre-test shutdown observation

Hyper-V's normal integration shutdown request returned0x80004005 while the guest
remained Running. The agent then selected normal macOS Shut Down from the Apple
menu. Serial recorded orderly driver poweroff, total2735ms; Hyper-V reached Off
at11:49 UTC without a hard reset or worker termination. The integration failure
is a separate open issue; a successful guest-menu shutdown does not fix it.

The first post-detach copy call found invalidated disk-object Path properties
and did not start copying. The retry used the immutable path snapshot saved
before shutdown and explicit stop-on-error checks. Sources were detached/Off;
new files were created without overwriting any existing disk or backup.

## Cold-copy verification and preparation boot

Both cold copies matched their sources before editing. EFI image SHA256:
`2e6fe24d9918c20c8c2e0539c84c6e566213d6b42fdc7cdfdfab3e48340b6f48`;
system image SHA256:
`4e07f7ce61e39377d9c9f2a58400838e73677b2aea2ff26dd91817ce2473679d`.
The prior entire Debug pair remains detached and preserved. The new EFI audit
confirmed only the Monterey executable changed; configuration remains exactly
`f2b8dce68e686e349940192cb0f4a53a299e2f5f3b870ab2ceb6acec238fdc81`.
The host unmounted the new EFI before attaching either Release test disk.

Preparation start at approximately12:03:54 UTC reached the pre-kernel local
unlock screen. At12:07:56 the receiver was alive but its actual opened log had
zero bytes. Therefore no clean-core kernel boot, CPU behavior or final Release
runtime success is claimed yet. Local unlock is required before the guarded
framebuffer installation. No credentials are stored or embedded in the package.
The initial preparation profile is Release core plus preserved Debug framebuffer;
it must never be counted as a complete Release acceptance run.

Once local access is available, verify current module identity, run the guarded
Aux installer on the NEW system copy, then reboot normally and validate both
Release components. The old pair supports full rollback by disk selection.
Update this report with actual boot evidence before claiming Release acceptance.

At12:09:22 UTC Hyper-V Worker event18508 reports a guest-requested shutdown.
The earlier successful start is event18500 at12:03:53 UTC. No host stop/reset
was issued after that start, and the new serial file remained empty. A preboot
unlock timeout is plausible but not established. This event occurred before the
obsolete-image cleanup at12:18 and must not be attributed to that cleanup.
No clean Release kernel execution or SynIC regression is inferred from it.

## Release framebuffer installation 2026-10-25 13:23 UTC

The guarded installer completed after local sudo authentication. Console evidence
vmconnect-20261025T132316516368Z-0.png shows RELEASE_RC1_FRAMEBUFFER_INSTALLED,
the expected framebuffer SHA256 d8a079d47d61988aabe40cb788b015979c27384135b57339e854d5c017792122,
and Aux SHA256 51d86e9db1092774f5830fe769b69608e657d4d860535d9f135563506a416e25.
Boot/System collection hash checks passed before and after the Aux replacement;
all four Aux module IDs and other versions passed the script checks. Backup is
retained inside the guest under /Users/Shared/HVReleaseRC1.s0ZkXpJy.
The macOS restart notice is expected; it alone would not prove success.
A normal Apple-menu restart was requested after the successful marker. Full
Release loaded identity and runtime validation remain pending after that restart.

## First complete Release desktop boot, 2026-10-25 13:37 UTC

Source6c3568178ba21136b8c21dd45597476c74ec31d1/run40189441511.
Verified loaded core UUID7CAF03F1-3631-33A9-AAAF-581270B665B0 and framebuffer
UUID3C6D0CDD-D9E7-39C8-94FB-D97A47BE3CF6 against LC_UUID in the original CI
Release binaries. Executable/config SHA256 values are recorded in
 evidence/ci/rc1-release-boot-20261025.json. Desktop is visible and the user
reports faster, satisfactory operation. This is one complete Release success.
A bounded204960-byte serial prefix SHA256aa15150cadd5346248af4635b8fb828f652fb7c1ac3ee8ce8637bee8ba414d2b
shows enumeration through channel14, SCSI/APFS root and software-cursor activation;
no captured panic, root wait or cursor conversion failure. Some concurrent boot
lines are interleaved. No per-call EOM traces exist in clean Release: zero trace
lines are not new target/actual CPU validation. SRB STATUS84 messages remain in
the raw capture and are not classified here; do not claim an error-free log.
The preceding restart had no kernel output and guest-requested shutdown18508 at
13:29:32 UTC; preboot timeout remains a hypothesis. A subsequent start at13:32
reached this desktop. Ten-start and sustained Release validation remain open.
Raw console/prefix evidence stays local under the Release test directory.

Latest clean-install evidence, 2026-10-26: the unchanged original clean driver binaries were installed automatically by the separate00f70ee setup product during a full APFS erase installation. Correct loaded UUIDs, actualFBhash,1920desktop and persistence after another normal reboot passed. FinalAppleSetupwait still required a regular guest shutdown/start; previous native approval may persist with sameVMfirmware. This is not a new kernel build, ten-start acceptance, fresh per-call EOM CPU measurement or long-term Release soak. See INTEGRATED_SETUP.md and curated integrated-product-v2-result-20261026.json.
