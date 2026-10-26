# Integrated clean setup validation

The user requires framebuffer support and1920x1080 as part of the installation,
without a separate manual driver/display repair. The current installation was
explicitly authorized for deletion and another blank512GiB installation with
unchanged CPU/RAM/network/identity/account/locale parameters. Original rollback
images and Sequoia backups are excluded from this deletion authorization.

Setup source efd3cb3a768a5030a93a2078cdc5daead307a98f on
feature/integrated-tahoe-setup passed CI40258077483. Its initial CI40257883867
failed because standalone hvshutdownd needed CoreFoundation declarations; the
follow-up supplies that header. The Cocoa frontend already compiled in run1.
Driver binaries are unchanged Release6c35681/run40189441511, not rebuilt as part
of setup. SetupMedia.zip SHA256015c0b633205e105bde0abb3b0d92de1f5642eaca36a3c8ce863444fecdc4326.
ISO SHA256d6bd2fb3ae31071e59418b343ac8e885e108b7c0e9be0c4829ba36b33500bef0.
All13 ISO files were read back and verified against CI provenance.

Recovery Seed.command accepts only a mounted new APFS volume, refuses existing
System/Users/Library/Applications, verifies payload hashes, then stages the app,
root bootstrap job and original shutdown daemon. It performs no partitioning,
erasure, account creation or security changes. First normal boot checks the
exact OS/core, installs the hash-pinned Apple-signed KDK if required, and runs
the previously tested guarded framebuffer installer. Standard macOS per-kext
Allow/restart remains necessary; no approval database or global policy bypass.
The frontend waits until Apple Setup Assistant exits and selects1920x1080 via
CoreGraphics only after verifying the expected loaded framebuffer UUID.

Verified before reinstall: current framebuffer UUID3C6D0CDD-D9E7-39C8-94FB-
D97A47BE3CF6, actual KDK directory KDK_26.7.1_25G241.kdk; native frontend
--verify-display returned1920x1080 and --set-display completed. A proposed sudo
Seed guard check against the live root was rejected by automatic review and
was not executed; no attempt to bypass that rejection was made.

The guest was gracefully shut down using its normal shutdown command. While
Off, only the two explicitly authorized current-installation images were
detached and deleted after exact path checks. A hash-verified copy of the
protected rollback EFI and a genuinely blank dynamic512GiB disk were attached.
Original rollback images stayed detached and unchanged. Main SMBIOS and security
values were preserved; only installer boot arguments/picker/recovery settings
and GOP1920x1080 changed in the new EFI copy. ocvalidate1.0.6 passed. Hyper-V
video is now Single1920x1080, set while Off. Serial receiver25588 remains active
on the existing main pipe; old serial/evidence files were preserved.
New EFI config SHA25635dd9dd356dfc9c10466d3f5a9d84d6d9ec98b7d1df8a720b2a2a891b8943806.

## Remaining validation

Seed persistence across Apple's fresh install is a hypothesis, not a confirmed
feature. This reinstall must prove persistence, automatic KDK/framebuffer stage,
normal approval/restart and automatic1080p completion. A successful CI and a
native display helper test do not prove this end-to-end behavior. Clean Release
has no per-call EOM diagnostic traces; no new CPU-locality result is inferred.
Raw images, identities and encrypted credentials stay local and unpublished.

Recovery test1 stopped before target writes: shasum absent. Read-only probe confirmed /sbin/sha256 -q available and produced the exact CI Seed.command digest. Commit54e0a98 switches manifest checking to that native tool; CI40259471597 pending. Apple OS installer has not started. The same newly blank target will be freshly initialized again before retry; no existing OS is being patched in place. Network-first firmware order was corrected to new EFI first; boot naturally reached Recovery without reset. Proposed TurnOff was rejected and never executed.

Recovery retry: fixed54e0a985d1c1d67cc735674dc56331dd7be6dbc0 passed CI40259471597. New ISOcc6f9623e6831b2f9e70a087f719a7e0c28c571bd4e04de96e50d02d2b6ce360 passed all13 file readbacks. The same new target was initialized blank again (Apple OS never started), and Seed verified every payload and emitted INTEGRATED_SETUP_SEEDED. Installer opened normally; persistence through Apple OS installation still pending. Serial prefix627291bytes SHAc3ddde7ca6574b3a5b2493a966edb506294aedfaf5b56c32d0571399bf7c97a3 contains no captured panic/root-wait; no EOM locality conclusion from clean Release.
