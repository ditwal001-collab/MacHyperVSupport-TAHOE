# Development environment

Requested on 2026-10-25: English user interface and documentation, VS Code,
.NET 10 SDK and Xcode for iOS development. Keep one current stable installation
of each tool; no beta or parallel historical installations. This is a separate
task on branch `setup/tahoe-dev-environment`; driver sources are unchanged.

## Verified initial state

The authorized guest reports macOS 26.7.1, build 25G241, architecture x86_64.
The Data volume reports 400 GiB total and approximately 358 GiB available.
English (`en-US`) is already first in AppleLanguages. Existing keyboard layout
is preserved. Initial Applications listing contains no VS Code or Xcode.
SSH is unavailable; setup uses the existing local Hyper-V console.

## Reproducible Microsoft setup

`BuildScripts/setup-dev-environment.command` installs user-scoped tools without
administrator authentication, restart, security or kernel changes. It refuses
existing target installations. Microsoft metadata queried on 2026-10-25 pins:

| Tool | Version | Verification |
| --- | --- | --- |
| VS Code Intel | 1.143.1, e646868227c3e3a9e3f24277c8c7220be42c0be7 | Microsoft SHA256, codesign and Gatekeeper |
| .NET SDK Intel | 10.0.402 | Microsoft release metadata SHA512 |

Applications go under `~/Applications`; command links under `~/.local/bin`.
Shell startup files are backed up before PATH and English CLI settings are
appended. C# Dev Kit is installed from Microsoft's extension marketplace.
A new console project under `~/Developer` must build and print `Hello, World!`.
The script logs to an exclusive `~/Library/Logs/HVDevSetup.*` directory and
does not claim success until its verification marker is printed.

The first installation medium is local-only:
`evidence/local-tests/dev-setup-20261025-02/DevSetup.iso`, volume HVDEVSETUP,
SCSI 0:6. ISO SHA256:
`aff11762b6f9c281d566378192ac8aaa3dad0a0d33e88d94e1c90a2b0ae9319c`.
Guest script SHA256:
`a9fcd5f1bffa1d461857e4627bda4cbd4d0a88314e4de4987a3a30b84669ecfd`.
Guest checksum matched and `bash -n` passed before execution. Installation
started approximately 00:48 UTC. At 00:49 UTC the terminal showed
`VSCODE_DOTNET_SETUP_VERIFIED`: checksum/signature checks passed, console restore
and build succeeded and execution printed `Hello, World!`. The English VS Code
window opened the generated project. C# Dev Kit 3.40.216, C# 2.160.4 and .NET
Install Tool 3.2.0 were listed. At 00:53 UTC a normal terminal sourced .zprofile
and listed exactly SDK 10.0.402. The Data volume still had about 361 GiB free
(APFS available capacity can fluctuate during downloads).

The user's later preference is to obtain free apps from the official App Store
where available. VS Code and the SDK use Microsoft's official distribution;
Xcode uses the App Store.

## Xcode and iOS acceptance

Use only the newest stable version compatible with the actual Intel guest.
At 00:51 UTC the App Store displayed Xcode 27.1 as incompatible and explicitly
required an Apple M1 chip or later, in addition to macOS 26.6. This is a confirmed
architecture limitation, not evidence of a SynIC or cursor regression. The
existing App Store account offered an earlier compatible version through its
cloud download button; that offer was accepted and downloading began at
approximately 00:52 UTC. Its exact version is not yet verified. Do not report
27.1 as installed or claim the compatible download is necessarily 26.6.

Check the App Store product and actual installed binary architecture, not just
the macOS version table. Apple Account authentication, if required, remains a
local account interaction; never put passwords or session tokens in the repo.
The .NET iOS workload must match the installed Xcode version; do not install it
blindly before checking Microsoft's release requirements.

Completion requires `xcodebuild -version`, SDK listing, an unsigned iOS build
and, separately, a real Simulator launch test. Simulator graphics/performance
under this basic Hyper-V framebuffer is unverified. Device signing and App
Store delivery require the user's Apple team/account configuration.

## Sources

- https://code.visualstudio.com/docs/setup/mac
- https://update.code.visualstudio.com/api/update/darwin/stable/latest
- https://builds.dotnet.microsoft.com/dotnet/release-metadata/10.0/releases.json
- https://learn.microsoft.com/en-us/dotnet/core/install/macos
- https://developer.apple.com/xcode/system-requirements

Keep downloaded installers, personal screenshots and logs out of Git. Preserve
the existing serial receiver and cursor workaround throughout this setup.

## Passive driver check during setup

Serial capture PID 48800 remained active. At 00:52:58 UTC the bounded prefix
contained 379717 bytes, SHA256
`28401f53dd3cea7a3d8c9f01aa8e78b2ea668b02b9a413e39dc0d446afd8dad1`:
26 matching EOM writes, zero CPU mismatches, zero cursor conversion failures,
one software-cursor marker, zero panic/root-wait markers. Local snapshot:
`evidence/local-tests/dev-setup-20261025-02/serial-snapshots/`.
This is bounded observation during setup, not a release stability guarantee.
