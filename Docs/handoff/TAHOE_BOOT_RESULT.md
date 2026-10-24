# Verified Tahoe login-screen boot — 2026-10-24

At 17:19:29 UTC the target VM reached the normal user password login screen.
A second read-only Hyper-V console capture at 17:22:06 showed the clock advance
from 10:19 to 10:22, establishing live GUI updates. These are not Recovery screens.
Personal account login and runtime `sw_vers` were not performed. The running
kernel is Darwin 25.6.0; the same System snapshot's version was previously read
as macOS 26.7.1, build 25G241 from Recovery before the cold copy was created.

## Exact tested inputs and observed result

- Source: `0756f1d75601f0c24bce98ae4adf8c83ce6e3307`.
- Built artifact: Actions `40090495930`, Debug Monterey executable SHA256
  `38bf5d6dcc26dd62eb4818086ea6c48505d09880e5919574e7073c922f4ffec9`.
- Active EFI config SHA256:
  `32be11f98247242f8e1534076817825cae2fa79b235ce289b179ec59e39caf8f`.
- All 14 VMBus channels enumerated; APFS System snapshot reached.
- All 24 captured EOM writes are fully parseable and target CPU equals actual
  CPU; zero CPU mismatches, zero panic/root-wait markers in the captured prefix.
- No authenticated BaseSystem pivot or migration-mode marker in this boot.
- Serial capture remains active in the independent receiver, last verified PID
  46464. Complete raw logs and login images stay local; no personal account
  names or raw images are included in the maintainer export.

Machine-readable evidence: `evidence/ci/boot-05-tahoe-login.json`. Its hash is
explicitly a byte-counted prefix checkpoint because the raw capture continues.
The private GUI image has its own recorded SHA256.

## What changed and what this does not prove

The SynIC source fixes the missing scheduler switch after binding: bind, block
to migrate, disable interrupts, verify ownership, clear message, full fence,
read pending and write the local EOM MSR, restore interrupts and previous affinity.
The workloop context and limitations are documented in SYNIC_EOM_REPORT.md.
Existing startergo GraphicsBridge attribution and source are preserved.

The separate installer investigation found `-bsdmgroot` in the selected
Preboot CoreServices Boot.plist. Normal NVRAM boot-args did not contain it.
XNU's `bsdmgroot_bootable()` explicitly lets `-nobsdmgroot` override that flag.
Only a new EFI copy gained this override; no Preboot plist was changed.
Source: https://github.com/apple-oss-distributions/xnu/blob/main/bsd/kern/bsd_init.c

That first normal-mode diagnostic still produced an extreme packet-log flood:
246575 of 249442 lines at one checkpoint were storage packet prints. It reached
normal launchd/services but no confirmed GUI in over 20 minutes. Graceful shutdown
failed because hvshutdownd was absent. The user-authorized diagnostic was then
hard stopped ONLY on the test copies at 17:15:09 UTC. The original cold system
disk was detached and unchanged; the interrupted run is not counted as success.

For the successful next boot, another exclusively copied/verified EFI removed
only `-hvstormsgdbg`. Serial logging, controller/SynIC diagnostics, -nobsdmgroot
and the executable remained unchanged. The packet flood disappeared; normal
early boot completed in about 11 seconds of guest boot time and a login screen
was independently captured within approximately two minutes of host start.
Caches, system state and possible journal replay differ after the first test,
so this is not a controlled proof that logging alone caused the original failure.

The override bypasses the installer BaseSystem path. A usable login screen on a
copy does NOT prove the original upgrade/migration completed correctly. Do not
silently promote this boot profile to a production installer repair. The separate
speculative graphics branch was not installed; the baseline GUI updates work.

## Preservation and current VM attachments

The VM runs exclusively on files under the ignored local experiment directory
`evidence/local-tests/system-boot-selection-20261024T164253Z/`:

- SCSI 0:0: `EFI.no-storage-packets.vhdx`.
- SCSI 0:1: `System.test.vhdx`.

Never delete/move these while attached; do not run workspace cleanup against
the ignored test directory. The original system disk is detached; its cold
SHA256 matched the initial copy before first use:
`cf92f837363108774d5e507966625a472c0fd315282f1b18b04074c6e81de9b1`.
This is the initial cold-copy hash, not the current modified working-copy hash.
Original EFI, earlier test EFI variants and the protected Sequoia backup remain
preserved. No other VM, host-wide security setting, format or erase was involved.
Private context/attachment/config manifests are in that experiment directory.

## Maintainer handoff and remaining acceptance

Export the minimal source patches from pinned base
`c48fc5ccade272ec79f633dcb23e45ba1c40d6cc` with
`BuildScripts/export-maintainer-package.py`. Diagnostic, functional and CI changes
remain separate; the alternative clean functional patch excludes instrumentation.
The boot-profile experiments above are not part of the functional SynIC patch.

Clean source branch `test/synic-eom-clean-c48fc5c`, CI head `c960997`, passed run
`40093339256`; package/executable hashes match uploaded provenance. It remains
runtime untested. The latest documentation head `18e1683` also passed run
`40114614036`; that rebuilt artifact is not the installed binary.

Still required before release acceptance: repeated instrumented and clean Release
boots, user-session verification, runtime version query, sustained storage/network
checks and confirmation of normal upgrade completion. No stable release claim
is made by this single observed login-screen boot.
