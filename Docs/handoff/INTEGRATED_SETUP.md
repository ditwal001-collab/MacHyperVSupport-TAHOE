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

First attempted normalboot02:56:30 failed with AppleRTC::start+0x2c6 pagefault at1.035592178seconds uptime, OSversionNotyetset. All14channels already registered. This is an early kernel failure; bootstrap/app execution was not reached in the evidence. Cause remains unresolved; do not attribute it to setup or EOM without further evidence. Captured bounded23092bytes SHAd01ab4088ad9a9cf43740b68d9868bae93fdcdd5edafd03615ba8e2af5b14202. Earlier phases ended in orderlyMACHReboot. Full integrated install remains FAILED/PENDING, not a pass.

Unchanged retry after the confirmed halted panic: exact new-disk attachment and immutable panic hash verified. A first guarded retry command stopped on a live-log sharing error before lifecycle actions; it was corrected to read the immutable snapshot. Only after proving the early panic, target-only forced Off/start was performed03:00:45UTC (normal guest shutdown unavailable before userspace). No EFI/driver/host setting changed. The retry reached normal APFS disk2s4, all14channels and English Setup Assistant. Prefix210019bytes SHA0c234b0d57b4c72279675e4ba2170ef6beed56d36dce61150347fb963b787655 has no capturedpanic/rootwait. Region Switzerland/no migration selected; requested local account creation in progress. This does not fix or explain the AppleRTC failure. Setup persistence/automatic backend remains unverified.

## Failed seed persistence; package transport replacement

At final UpdateMacAutomatically the normal setup stalled again. Native Apple menu/Spotlight did not provide a working shutdown path; normal Hyper-V Stop-VM failed0x80004005 at03:18:30. After confirming only the expressly disposable new512GiB installation was attached, no active OS installer/personal Apple auth/encryption and preserving serial652446bytes SHAda35ae08a778bde7610128853173b71e1a4cad80209116fad3f5f79291a44d5e, target-only forcedOff/start03:20:04 was performed. This is a second exceptional recovery action, not an unattended clean-install success. Normal login/desktop followed. The local account, English/Switzerland/Zurich settings are present; optional FileVault enablement was deferred to preserve prior confirmedOff state under the user's same-parameters requirement. No existing encryption was disabled.

Read-only desktop checks confirmed26.7.1/25G241, empty /Library/LaunchDaemons, absent /Applications/MacHyperVSetup.app and absent /Library/Application Support/MacHyperVSetup. Therefore the pre-install seed did NOT survive at its intended locations; the automatic backend never became available. Do not recommend this route. The files remain only in source/history as a failed experiment and are omitted from new media. The earlier Spotlight bootstrap match was from the read-only DVD and was not evidence of installed persistence.

Replacement implementation79375d1 passed CI40264080780. It builds a productbuild archive containing the same app, root LaunchDaemon/bootstrap, first-install framebuffer payload and unchanged upstream shutdown daemon. No package postinstall script, credential, KDK or security-policy edit is embedded. CI expands the product archive and verifies every payload byte/path against its staged source. Follow-upcdd9102 removes failedSeed from shipped media; CI40264174718 pending. Driver6c/run40189441511 remains unchanged. Apple's official softwareupdate --fetch-full-installer --full-installer-version26.7.1 is downloading the full installer ONLY; no OS install has been invoked by that download. Next verify actual startosinstall --usage on this exact full installer for --installpackage/--eraseinstall, then perform another genuinely erased clean installation with the setup package. Runtime package transport is UNVERIFIED until that test. If the exact installer rejects the mechanism, record that and choose another supported method; do not bypass security.

Product transport preflight: cdd91023ee63a72195b2f82dc925ed46def8ec02 passedCI40264174718; ISO6e7aeefc01948a9e009647fba42f994f7e4ed96ee9e6f0937da6168595b84e9b/13files exact. Packagefceab96820d7f693df6407c4fd925d372c138fa176488a1f98a7cee12f659e78 matched again inside guest. Applefullinstaller fetched26.7.1, actual assetXML26.7.1/25G241, applicationversion21.7.02, CLI binary80adc529d3e7794507f16e33fc53edf6d982c59729c6b49753cfec6b2ec8323d. SharedSupport.dmg passed its built-in hdiutil verification and SHA256ca854f49dfdedbe78492c26d0e4172ee4d37573e2d375ca90c083d7615b6f48a; metadata mount detached before launch. Actual --usage confirms --installpackage(productbuild archive) and --eraseinstall. NormalrootData maps APFScontainerdisk2 to physicalstore disk1s2 on exact549755813888byte target; separate5.4GBFAT EFI disk0 cannot be the APFS erase target. Runtime command guards physical mapping, disk size and exactpkg hash before sudo. User authorized fresh replacement after setup changes. The second local-admin prompt was handled privately, with no password pipeline/file/log. At03:41:57 startosinstall accepted the command and entered Preparing0percent. This is an erase installation with package phase, not an upgrade preserving the current account. Final result remains unverified; do not stop/reset the VM during preparation/install.

At03:48 the actual install.log records DidRequestEraseInstall=1 and our product archive in the installer's UnwrappedInstallers staging area. UpdateBrainService used~396percent CPU; PREPARING_UPDATE stalled:NO. At03:52 its internal portionComplete advanced from0.291075 to0.633238 with~386percent CPU. These are preparation phase counters, not overall completion; package staging is not yet package application. Normal boot03:20 serial currently contains registered IDs1,4-14 (12 distinct), while the earlier03:00 boot and AppleRTCpanic both contain all14; no claim that every captured boot enumerated exactly14 is appropriate without an offered-channel inventory.
