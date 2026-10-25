# Local test-storage housekeeping

This operational note is not part of the maintainer bundle. The user requested
cleanup after the technical package is verified. No recursive cleanup or
protected-backup removal is authorized by this record.

At2026-10-25 12:18 UTC, package
`hyperv-maintainer-20261025T121628Z-40dd7327.zip` was checked against SHA256
`4348d3bae44d04f8b52d14d7ff440cdfe74349b7a1b9fe313d3d82ce8eefaf33`.
Six explicitly preflighted inactive files under evidence/local-tests were then
removed: five superseded experimental EFI images and the duplicate host KDK DMG
download. All VHDX candidates were dynamic, detached, had no parent dependency,
and were absent from the target VM's current disks/optical paths and rollback set.
The verified package retains all relevant patch/binary/provenance information;
the existing KDK ISO retains the original installer payload locally.

Logical bytes removed:6234329236 (about6.23GB /5.81GiB).
Observed C-volume free-space increase:6228107264 bytes; concurrent system
activity accounts for the small difference. Free space after cleanup was
2470260318208 bytes. Exact plan/result are stored privately in the Release test
directory as cleanup-obsolete-files-plan.json and cleanup-obsolete-files-result.json.

Retained:

- Active clean-RC1 test EFI/system images and installation media.
- The entire cold, hash-verified overnight Debug EFI/system rollback pair.
- Original EFI/system images and the protected working Sequoia backup outside
  the test directory.
- Source commits/branches, curated evidence, original CI artifacts, serial logs,
  earlier package archives and the user's pre-existing untracked backup files.

The new isolated full system copy temporarily duplicates about86GB of data.
Do not remove the Debug rollback system copy merely to reclaim this space before
clean Release runtime validation and a verified rollback strategy are complete.
Read-only optical devices and additional obsolete scratch data can be cleaned
later without changing source/backup retention; re-query live attachments first.
Do not reuse the old inventory as an executable deletion list.
