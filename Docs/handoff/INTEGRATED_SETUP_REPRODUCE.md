# Reproduce the integrated Tahoe setup test

Status: 2026-10-26, validation in progress. This is the exact test route, not a
claim of a universal one-pass blank-VM installer. The Recovery seed experiment
failed persistence and must not be used. A working Tahoe guest downloads Apple's
full installer, then Apple's erase-install phase installs the setup product on
the freshly recreated system. No existing account or development environment is
migrated. See [the chronological results](INTEGRATED_SETUP.md).

## Pinned inputs

| Input | Exact value |
| --- | --- |
| Setup source | `00f70ee358e4d9ddad2fccca39bc19ede1d55365` |
| Setup Actions run | [40269870810](https://github.com/ditwal001-collab/MacHyperVSupport-TAHOE/actions/runs/40269870810) |
| Setup artifact | `IntegratedSetup`, containing `SetupMedia.zip` and `provenance.json` |
| Driver source | `6c3568178ba21136b8c21dd45597476c74ec31d1` |
| Driver Actions run | [40189441511](https://github.com/ditwal001-collab/MacHyperVSupport-TAHOE/actions/runs/40189441511) |
| Target OS | Tahoe 26.7.1, build `25G241`, Intel x86_64 |
| Hardware used | Generation 2, 8 vCPU, 24 GiB fixed RAM, dynamic 512 GiB system VHDX, separate existing verified EFI |
| Setup ZIP SHA256 | `81a7b6a4706ecde370351ad1a9d2b739f75b0843efa3cae49237942821630633` |
| Product package SHA256 | `2092d73838908edb86418cc16983052c19b0625bc1d265f33402abf8c5723443` |

The original GraphicsBridge attribution and driver series remain unchanged.
Setup compiles a separate Cocoa helper and the original upstream shutdown
daemon. Driver executables are copied from the pinned original CI archive.
Apple's KDK is downloaded from the pinned URL/hash by the root stage; it is not
redistributed in the setup artifact. No private EFI, identity, account password,
Apple sign-in, VM disk or development applications belong in this delivery.

## Obtain and verify media on Windows

Use a separate source checkout at the setup source above. Download the existing
successful artifact into a new directory, preserving its provenance:

```powershell
gh run view 40269870810 --repo ditwal001-collab/MacHyperVSupport-TAHOE --json headSha,status,conclusion
gh run download 40269870810 --repo ditwal001-collab/MacHyperVSupport-TAHOE --name IntegratedSetup --dir setup-ci
Get-FileHash setup-ci/SetupMedia.zip -Algorithm SHA256
py -3 -m venv setup-python
setup-python/Scripts/python.exe -m pip install pycdlib==1.22.0
setup-python/Scripts/python.exe BuildScripts/make-integrated-setup-media.py --setup-zip setup-ci/SetupMedia.zip --provenance setup-ci/provenance.json --output-directory setup-media
```

Verify Actions conclusion `success` and its exact head SHA. The media builder
refuses an existing output directory, checks the archive and every payload hash,
then reads every ISO file back and compares its bytes. ISO volume label is
`HVSETUP`. The ISO hash is recorded in `setup-media/manifest.json`; container
timestamps can differ between independent media builds, so compare payloads
and product hash as well. This test's ISO SHA256 is
`8bb5cc7198c53aa134e52802f61b7e5c9a849c7a1b776ef065da5dc094b97c2f`.

Attach the ISO only to the intended test VM. Ensure the serial receiver is
already running on that VM's configured pipe and has exclusive ownership.
Preserve verified rollback copies separately. Do not modify or mount live VHDX
files on the host. Hyper-V video Single 1920x1080 was set while the guest was Off;
the guest mode still needs its framebuffer and the setup app.

## Apple installer and target verification

In the disposable running Tahoe guest, obtain Apple's full 26.7.1 installer:

```sh
softwareupdate --fetch-full-installer --full-installer-version 26.7.1
"/Applications/Install macOS Tahoe.app/Contents/Resources/startosinstall" --usage
shasum -a 256 /Volumes/HVSETUP/MacHyperVSetup.pkg
diskutil list
diskutil info /System/Volumes/Data
```

The exact tested installer supports `--eraseinstall` and `--installpackage`
(a productbuild archive). Its application version is 21.7.02; the OS asset
metadata, not that application version, establishes 26.7.1 / 25G241. The tested
`startosinstall` executable SHA256 is
`80adc529d3e7794507f16e33fc53edf6d982c59729c6b49753cfec6b2ec8323d`.

The next operation erases the **current guest's APFS installation**. Never run it
on a valuable source Mac. In this test, read-only checks identified Data's
physical store `disk1s2` on a whole disk of exactly 549755813888 bytes; the EFI
was a separate FAT disk. Those BSD names are observations, not universal device
names. Recheck the mapping and host attachments for each installation.

With the disposable target and product hash independently verified, the tested
Apple command is:

```sh
sudo "/Applications/Install macOS Tahoe.app/Contents/Resources/startosinstall" \
  --eraseinstall --newvolumename "Macintosh HD" \
  --installpackage /Volumes/HVSETUP/MacHyperVSetup.pkg \
  --agreetolicense --rebootdelay 15 --user "$USER" --passprompt
```

Use normal native password prompts; do not put a password in commands or media.
The host test adds guards for the exact physical store, virtual disk size and
package hash before invoking this command. Preserve the serial output and allow
all preparation and automatic installer reboots to complete. A phase percentage
that stays constant briefly is not sufficient evidence of a hang.

## Fresh setup and acceptance

Select English, Switzerland, the intended Swiss keyboard and Zurich timezone;
create the requested local account afresh. Skip migration and optional Apple
sign-in. Preserve the intended encryption/security settings. The setup product
must be present from the Apple installation phase, not manually added later.

The root job verifies the exact OS/core UUID, obtains the hash-pinned signed
Apple KDK and runs the guarded framebuffer first installer. The native app waits
for Apple Setup Assistant to finish. Its approval button opens Privacy & Security;
use Apple's per-extension Allow, normal admin authentication and requested
Restart. No approval database or global security setting is changed by this
product. After login, display selection should happen automatically.

Record `/Library/Application Support/MacHyperVSetup/activation.log`, `setup.log`,
`status.txt`, package receipt time, launchd job state, OS build, both loaded kext
UUIDs and actual display geometry. The expected framebuffer UUID is
`3C6D0CDD-D9E7-39C8-94FB-D97A47BE3CF6`; the core UUID is
`7CAF03F1-3631-33A9-AAAF-581270B665B0`.

After automatic completion, `MacHyperVSetup --verify-display` should report
1920x1080; repeat the check after another normal reboot. Also test mouse, Finder,
Downloads and Safari. Do not run `--set-display`, manually install the driver or
select Displays preferences during acceptance. Those interventions would conceal
a failed integrated path. The preceding old-system direct display diagnostic is
reported separately from this clean test.

Every stage needs an exact source/run/binary/config hash and immutable serial
prefix. Clean Release contains no per-call EOM CPU trace: zero captured EOM
lines do not establish new CPU-locality validation. An unrelated early AppleRTC
panic and previous final Setup Assistant stalls remain documented failures;
they must not be silently omitted from the maintainer report.
