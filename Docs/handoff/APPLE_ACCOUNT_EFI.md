# Tahoe Apple Account: existing EFI workaround was only half enabled

2026-10-26. This is an environment/EFI correction, separate from the SynIC and
graphics driver patches. It is not native Apple hardware attestation and is not
a confirmed complete Apple Account login until personal authentication finishes.

## Verified failure and diagnosis

The user could sign in through Safari, while System Settings failed before the
password step with "Verification Failed - An unknown error occurred". Guest UTC
and Apple's HTTPS Date matched to the second. TLS verification succeeded, and
the network interface was en0 with IOBuiltin=Yes. Existing private akd/accountsd
logs contained AKAnisetteError -8001/-8008/-8025, underlying ADI -45061 and
devicecheck BAA -10000; repeated messages included DeviceIdentity not available,
failed attestation headers and provisioning failure. Raw logs/screenshots and
the account identifier remain private; none belong in a maintainer archive.

`sysctl kern.hv_vmm_present` returned 1. Read-only inspection of the actual EFI
showed two existing kernel string-table patches: the companion at index0 was
enabled, but the matching patch at index1 was disabled. Their byte patterns match
the upstream Qonfused workaround. Both search strings occur exactly once in the
installed Tahoe BootKernelExtensions.kc. The full plist hash matched the previous
validated installation profile.

Upstream references:

- [a377f97: replace VMHide with paired kernel patches](https://github.com/Qonfused/OSX-Hyper-V/commit/a377f97).
- [e689108: prevent later plist overrides from clearing those patches](https://github.com/Qonfused/OSX-Hyper-V/commit/e689108d397935c26b4e5ad392fa222d83a44e98).
- [Apple's supported VM iCloud identity mechanism](https://developer.apple.com/documentation/virtualization/using-icloud-with-macos-virtual-machines)
  uses Apple-silicon host Secure Enclave information; this Hyper-V compatibility
  workaround does not implement that mechanism.

## Exact correction and safeguards

Source `58a29dc` adds `BuildScripts/enable-tahoe-iservices-patch.py`. It requires
the expected input SHA256, checks both existing upstream byte patterns and their
activation/bounds, writes a new output exclusively, and checks that reverting
the one changed boolean reconstructs the original plist structurally. Meaningful
guard tests passed for missing companion, duplicate target, already enabled,
unexpected bounds and wrong bytes, plus preservation of all other plist values.

The only changed value is `Kernel.Patch.1.Enabled`, false to true. No new serial,
MLB, ROM, UUID, account, SIP, Gatekeeper or driver setting was introduced. Existing
Find/Replace strings reroute the VM-detection sysctl name as in upstream; this is
why it changes the visible VM-detection result, not the Hyper-V CPUID feature.

The VM was shut down normally and the original EFI detached. A new working VHDX
copy was byte-hash verified against it; the old EFI remains preserved. Only the
new detached copy was mounted on the host. The generated plist passed
ocvalidate1.0.6 before replacement; the image was cleanly unmounted before attach
and start. The system disk was not reinstalled. Original rollback/Sequoia images
and other VMs were not changed. Serial receiver remained running.

| Item | SHA256 |
| --- | --- |
| Previous EFI config | `35dd9dd356dfc9c10466d3f5a9d84d6d9ec98b7d1df8a720b2a2a891b8943806` |
| Corrected EFI config | `8a22e7e5e6af34bcf0dfb0ea95044d0383b058a33e7287e70bbef27b7bf7f3ca` |
| New working EFI VHDX before boot | `24d5a9da151f5f1a327a603cf10de1b228a5bc753475ec958be2407ad099b8d9` |

For future setup, check this pair while preparing the **offline working EFI**,
before installing the OS. A preserved historical EFI can contain the disabled
second entry. Do not blindly replace another machine's config or regenerate its
identity. Example on a verified detached working copy:

```powershell
py -3 BuildScripts/enable-tahoe-iservices-patch.py --config PRIVATE_CONFIG --expected-sha256 VERIFIED_INPUT_SHA256 --output NEW_PRIVATE_CONFIG
ocvalidate.exe NEW_PRIVATE_CONFIG
```

Copy the validated output into the working EFI only after the VM is Off, the
image detached and a verified original retained. This script does not operate on
VMs/VHDXs or perform the copy itself. It does not reset keychains or NVRAM.

## Runtime result and remaining boundary

Boot11:13:06UTC reached normal desktop. At11:16, sysctl returned0, the expected
Release core UUID7CAF03F1-3631-33A9-AAAF-581270B665B0 was loaded, and the installed
display verifier returned1920x1080. At11:17, one retry with the same account
identifier advanced to the native **password field**, instead of the former
pre-password Verification Failed dialog. No Apple password or2FA code was used
by the agent. The user then reported successful login ("es geht"). This is a
user-confirmed login, separate from the agent's direct verification of the
kernel value and transition to the password field. No account tokens or personal
authentication screens were collected to independently verify enrollment.

Latest bounded serial303373bytes SHA256
`3ba4d9b6888302b6318f8db84c601f4a34540a7bfc30b7541d53a96513d36286`
contains zero captured panic/root-wait/cursor-conversion failure markers. Its
software-cursor activation-marker count is0, so this prefix is not a fresh
software-cursor activation proof. Clean Release emits no per-call EOM trace;
there is no new SynIC CPU-locality measurement. No repeat-boot/soak result is
claimed for this EFI revision yet. The earlier clean-install results refer to
the prior config hash and remain historical evidence, not a clean-install test
of this new EFI revision.

The05:45 maintainer package predates this separate EFI correction; its original
five driver patches and pinned binaries remain unchanged. This additional
script/report should be delivered as an explicitly separate environment addendum.

## Integrated preparation for future installs

Source `614382e` integrates this check before new VM creation. The new
`BuildScripts/prepare-tahoe-efi.ps1` accepts an unmounted independent source EFI,
its expected SHA256, a new output VHDX and matching ocvalidate. With no `-Prepare`
it reports a plan. With `-Prepare` it creates a new copy exclusively, verifies
the byte copy, mounts only the new image, checks both exact patch entries,
enables the target only if needed, runs ocvalidate and unmounts in finally.
Private config backups and a hashed receipt remain beside the new output.
An already correct pair is accepted without changing the config again. Source
hash mismatch, unsupported/missing/masked patches or validation failure stop
preparation; an incomplete output must never be attached to a VM.

`new-tahoe-test-vm.ps1 -Create` invokes that preparation before creating the VM
or blank system disk, requires `-OCValidatePath`, then attaches `EFI.setup.vhdx`.
It now defaults to512GiB and Single1920x1080, matching the tested profile. It
still refuses existing VM names/output files and leaves the new VM Off for its
serial receiver to be started first. In this workspace it must not be used to
create another VM; only the explicitly authorized main VM may be operated on.

The actual offline preparation was tested on a new copy of the old EFI: resulting
config hash is exactly `8a22e7e...bf7f3ca`, matching the working corrected VM.
A second copy of already corrected EFI retained that config hash and reported
no flag change. Both passed ocvalidate. Bad-hash and existing-target-VM guards
were exercised successfully; Python/PowerShell syntax and focused guard tests
also passed. These are offline/preflight results. The entire updated new-VM
creation plus OS installation has not yet been rerun end to end. Do not turn
these checks into a claim of a new full clean-install acceptance run.
