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

The user explicitly needs new iOS features. A compatible older Xcode is only a
fallback and does not satisfy the latest iOS SDK requirement. Apple Silicon
hardware (local or remote build/development access) is required for the currently
offered Xcode27.1. Intel Hyper-V virtualization cannot provide an Apple M1 CPU.
Do not spend space on older simulator runtimes or add .NET iOS workloads until
the toolchain limitation is resolved. App Store product reference:
https://apps.apple.com/app/xcode/id497799835.

At approximately 01:00 UTC the App Store completed installation (Open button).
At01:01 direct guest inspection reported **Xcode26.5, build17F42**; Info.plist
reported26.5 and `file` showed a Universal executable with x86_64 and arm64
slices. These are actual local results; do not substitute26.6 from external
version tables. Exact SDK availability and first-launch completion remain to
be checked. User understands the distinction between compiling ARM iPhone apps
on Intel and executing an ARM-only Xcode host application on Intel.

Research found no verified Intel-host Xcode27 patch. Apple's Intel Deprecation
release note states Apple-Silicon-only execution. A concrete Xcode27 Sequoia
patcher explicitly targets ARM64 and does not support Intel host binaries:
https://gist.github.com/MihaelIsaev/b09f16a1e8400624d57f539fadcc8a59.
No third-party patcher was downloaded or executed.
QEMU's documented userspace emulation covers Linux/BSD, not macOS Mach-O;
UTM documents macOS ARM guests only on Apple Silicon. Generic ARM64 emulation
therefore does not establish usable Xcode27 execution in this Intel VM.
References: https://www.qemu.org/docs/master/user/main.html and
https://docs.getutm.app/guest-support/macos/.

Check the App Store product and actual installed binary architecture, not just
the macOS version table. Apple Account authentication, if required, remains a
local account interaction; never put passwords or session tokens in the repo.
The .NET iOS workload must match the installed Xcode version; do not install it
blindly before checking Microsoft's release requirements.

Completion requires `xcodebuild -version`, SDK listing, an unsigned iOS build
and, separately, a real Simulator launch test. Simulator graphics/performance
under this basic Hyper-V framebuffer is unverified. Device signing and App
Store delivery require the user's Apple team/account configuration.

## Confirmed iOS build, 2026-10-25 01:13 UTC

Xcode26.5/17F42 first launch and local administrator authentication completed.
`xcodebuild -showsdks` lists platforms and `xcrun --sdk iphoneos
--show-sdk-version` returns26.5. The user accepts26.5 as the Intel development
baseline. The current-stable-only policy has this documented hardware exception.

`BuildScripts/verify-ios-dev-environment.command` creates a fresh SwiftUI Xcode
project under `~/Developer/IOSDevSmoke.*`, builds for iphoneos/arm64 with signing
disabled, checks Mach-O architecture and MinimumOSVersion, and hashes the binary.
The corrected test printed `BUILD SUCCEEDED` and
`IOS_ARM64_BUILD_VERIFIED_UNSIGNED`. MinimumOSVersion was15.0; output was Mach-O
64-bit arm64. Device execution, signing and simulator execution are distinct.

Local successful project: `~/Developer/IOSDevSmoke.X*` (one matching project).
Use the actual directory name; similarly shaped characters in screenshots are
not a reliable source for transcribing its random suffix. Executable SHA256:
`24b5e25c4c3ffc38c07e52ee775a9a9d21ba2a01307cefd1e11a85c604960b37`.
The initial smoke project compiled successfully too, but its post-build lipo
argument order failed. The final helper uses `lipo -archs` with an exact arm64
comparison; this is a verification-script repair, not an Xcode compiler fix.
One template warning about interface orientations was present; no build errors.

Corrected ISO SHA256:
`313c94d99265d2cc990fc32345263bd44ea0ade3e35811ab9b0b8969a10f96df`;
script SHA256:
`3bf3721bf4f4d675622d008ed04205de3e2eb37c4e8c01dcdcc7244da08568ae`.
Volume HVIOSVERIFY2 is attached read-only at SCSI0:8;0:7 also points to that
image after a media-swap attempt that the guest did not initially recognize.
Old media and previous smoke projects are preserved as test evidence.

The first-launch download UI showed iOS26.5 Universal Simulator23F77 and a
queued watchOS26.5 runtime. This was observed after overlapping user/agent
installation clicks; do not claim only the iOS runtime was selected. Simulator
execution is still being checked. No .NET iOS/MAUI workload was installed.

At01:13/01:14 the normal macOS lock screen appeared. VM uptime did not reset
(48m27 at01:14); no agent lifecycle operation was performed. Session unlock is
the current access blocker. Do not inject commands into the password field.
Simulator runtime completion and execution remain unverified. Later serial
snapshot01:14:02 contained512473 bytes, SHA256
`a423dbd015933f83f2d5aa20b91fe026f1d6501b1907f1e24c27c02f998cd1d3`,
still26 matching EOM and0 cursor/panic/rootwait markers. Capture PID48800 alive.

## Simulator validation and agreed workflow, 2026-10-25 01:22 UTC

The session-lock blocker above is historical. The user reported the session open;
fresh console captures at01:16 confirmed the desktop, Terminal and Xcode.
`xcrun simctl list runtimes` initially returned no runtimes. The installed Apple
command `xcodebuild -downloadPlatform iOS` resolved the Universal iOS26.5/23F77
image; `xcrun simctl runtime list` showed Ready (one9.9G image). Opening the
installed Simulator app registered the runtime and booted an iPhone17.

`BuildScripts/verify-ios-simulator.command` receives the actual existing smoke
project path. It builds for iphonesimulator/x86_64 in an exclusive subdirectory,
verifies architecture, installs onto the already booted simulator, launches
org.example.HVDevSmoke, and saves a guest-local screenshot and hashes.
The test printed BUILD SUCCEEDED and IOS_SIMULATOR_APP_LAUNCHED. Native VMConnect
showed the app's Developer environment ready text on the virtual iPhone. Thus
build, install, process launch and simple SwiftUI rendering are verified.
This does not establish Metal feature support, simulator performance or complex
app compatibility. SpringBoard initially showed placeholder icons during startup.

The read-only HVIOSSIM ISO at SCSI0:9 is under
`evidence/local-tests/ios-simulator-20261025-01/`; ISO SHA256
`f769610ce353c267f6eaba46957d8aac1674580831ec908e82ae8c9366e4198e`;
helper SHA256
`6994b3cfc90c1aca4022acdbe3c99c6765508377dfa6091b5401b4699a1f4b9d`.
Guest build logs/screenshots stay under the smoke project's SimulatorCheck.*
directory; host captures and raw serial remain local-only. No personal metadata
or screenshot payload is published.

The user accepts local development with Xcode26.5, followed later by access to
an Apple-Silicon Mac running Xcode27 for final rebuild, compatibility testing,
signing and distribution. Keep dependencies reproducible and test compiler/SDK
differences in that final stage. New iOS27 API work requires the newer toolchain.
No remote Mac was provisioned or rented and no signing account was configured.

At01:22:08 the VM remained Running, uptime56m32; serial PID48800 was alive.
Bounded prefix700569 bytes, SHA256
`7afa3d2ff0ec70428d7b2a1f22747d14ed8b9227657648f76f5289356c6dc510`:
26 matching EOM, zero mismatches/cursor conversion/panic/rootwait markers,
one software-cursor activation. This is additional observation under development
workload, not repeated-boot or clean-Release stability validation.

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
