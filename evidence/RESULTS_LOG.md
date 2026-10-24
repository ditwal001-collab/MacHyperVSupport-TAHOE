# Results log (append only)

Unknown values are deliberately explicit. All dates below are 2026-10-24.

| Test | Git SHA / source | Build run | Kext SHA256 | EFI config hash | Boot outcome | Evidence and result |
|---|---|---|---|---|---|---|
| Historical instrumented build | `9b80c5f39d67a5c9fd76a9765b8302092c2f250f` | `40052405899` | `5948180733D8EE0D7EFD5CB584BC37D7E5E8E0CA11337AC47EAADB0AE372D254` (handoff-reported, not rehashed) | UNKNOWN | Handoff reports intermittent failure | GitHub API confirmed run SHA and success before interruption; boot excerpts in OBSERVATIONS.md |
| Local source/history inspection | `9b80c5f39d67a5c9fd76a9765b8302092c2f250f` | N/A | N/A | Not accessed | NOT RUN | Non-shallow repository, 303 reachable commits before development; relevant graphics, SynIC and CI evolution inspected; SYNIC_EOM_REPORT.md |
| Candidate build launched | `670b352156c0cdd044e9f211577741c1d0f7dfcc` | `40087952850` | UNKNOWN | Not accessed | NOT RUN | Push succeeded, Build and Analyze Clang were in progress; completion UNKNOWN after network denial |
| Resume connectivity check | `670b352156c0cdd044e9f211577741c1d0f7dfcc` | `40087952850` queried | UNKNOWN | Not accessed | NOT RUN | GitHub API socket access denied; no logs or artifacts obtained |
| Header follow-up commit attempt | `670b352` + working tree | No new run | N/A | Not accessed | NOT RUN | FAIL: `.git/index.lock` permission denied; source changes retained in working tree |
| Export wrapper launch | `670b352` + working tree | N/A | N/A | Not accessed | NOT RUN | Host policy rejected unsigned PowerShell; no execution-policy change; Python entry point used |
| Workflow shell checks | `670b352` + working tree CI adaptation | N/A | N/A | Not accessed | NOT RUN | PASS: all 10 multiline run blocks and provenance script pass bash syntax; nested URL pin substitution passes execution check; YAML/Actions execution NOT checked |
| Patch reconstruction | `670b352` + source/CI follow-ups | N/A | N/A | Not accessed | NOT RUN | PASS: four patches apply in order to pinned base and reproduce normalized files; package VERIFICATION.txt and manifest.json record source and patch hashes |
| Clean functional export | `670b352` + source header follow-up, diagnostics removed during export | N/A | N/A | Not accessed | NOT RUN | PASS: source-only patch applies directly to `cd66095f0d6c099f3498522fdf3edbd4825dbb81` and reconstructed files match; compiler/linker/runtime UNKNOWN |
| Resumed candidate CI inspection | `670b352156c0cdd044e9f211577741c1d0f7dfcc` | `40087952850` | No artifact | Not accessed | NOT RUN | FAIL: Build and Analyze Clang report undeclared OSMemoryBarrier; sanitized exact diagnostic: ci/40087952850-compiler-error.md; targeted escalation restored API access |
| Header correction pushed | `ad9a0b3b7a06bf842e263f4cde610fc0d8c139c1` | `40090195466` | Pending | Not accessed | NOT RUN | IN PROGRESS: explicit OSAtomic header; scheduler include limited to modern targets; isolated from CI adaptation |
| CI provenance adaptation pushed | `91a5eb7146ef2e3f3e8a5741ffbd397e3c8df11b` | `40090291711` | Pending | Not accessed | NOT RUN | IN PROGRESS: pinned inputs, binary hashes, environment and Monterey undefined-symbol listing |
| Header-only correction evaluated | `ad9a0b3b7a06bf842e263f4cde610fc0d8c139c1` | `40090195466` | No artifact | Not accessed | NOT RUN | FAIL: OSMemoryBarrier still undeclared at line 357 in Build and Analyze Clang; adding OSAtomic.h is insufficient |
| Pinned-input build evaluated | `91a5eb7146ef2e3f3e8a5741ffbd397e3c8df11b` | `40090291711` | No kext artifact | Not accessed | NOT RUN | FAIL: same compiler diagnostic; SDK header inspection confirms no OSMemoryBarrier declaration |
| Compiler full-fence correction pushed | `0756f1d75601f0c24bce98ae4adf8c83ce6e3307` | `40090495930` | Pending | Not accessed | NOT RUN | IN PROGRESS: __sync_synchronize replaces unavailable OSMemoryBarrier; removes ineffective OSAtomic include; other source/CI unchanged |
| Pinned build and downloaded artifacts verified | `0756f1d75601f0c24bce98ae4adf8c83ce6e3307` | `40090495930` | Debug `38bf5d6dcc26dd62eb4818086ea6c48505d09880e5919574e7073c922f4ffec9`; Release `b67abe5162028218f87a7a04f4edd8f2239adaf283e35ef7dd8fc7221d69a8f5` | N/A | NOT RUN at build verification | PASS: Debug/Release package builds and Clang analyses; package and kext hashes match uploaded provenance; `_thread_block` import, no fence helper import; ci/run-40090495930.json |
| Authorized VM test preparation | `0756f1d75601f0c24bce98ae4adf8c83ce6e3307` | `40090495930` | Debug as above | `430d1f347fa0b5271cd212e1c35692013b252361eccc8ba5f0ff6c3ec95368eb` | Target VM verified Off before preparation | PASS: new EFI copy matched original hash; old installed kext hash matched historical record; only candidate executable differs after installation; original EFI and backups preserved; local-tests/vm-test-0756f1d-20261024-01/*-verified.json |
| First instrumented candidate boot, 11:51–11:54 UTC | `0756f1d75601f0c24bce98ae4adf8c83ce6e3307` | `40090495930` | `38bf5d6dcc26dd62eb4818086ea6c48505d09880e5919574e7073c922f4ffec9` | `430d1f347fa0b5271cd212e1c35692013b252361eccc8ba5f0ff6c3ec95368eb` | FIRST PASS through APFS root; full installer/login outcome pending | 21 observed EOM writes all target 0 / actual 0; channels 1–14, completed scan, SCSI controller started, APFS root; no root waiting or panic at observation; ci/boot-01-0756f1d.json and sanitized excerpt; complete serial capture continues locally |
| Same boot, 11:55–11:56 UTC | `0756f1d75601f0c24bce98ae4adf8c83ce6e3307` | `40090495930` | Debug as above | Same config hash | PARTIAL PASS: WindowServer running; OSInstaller progress-UI calls; installation completion unknown | Serial capture continues; no forced reboot while upgrade appears active; local capture file under local-tests/vm-test-0756f1d-20261024-01/serial |
| Clean source variant prepared and pushed | Functional `b9a97199c48115fa4d706655307e9c8adddc0bb0`; CI head `da2bd1b49247aea1c17cf71f31925648df3ca14f` | Run not yet retrieved | Not built/verified yet | Not installed | NOT RUN | Branch test/synic-eom-clean-20261024 contains the functional patch directly on pinned base, without local diagnostic code; separate CI commit; existing VM test continues unchanged |
| Same boot, 12:06 UTC observation | `0756f1d75601f0c24bce98ae4adf8c83ce6e3307` | `40090495930` | Debug as above | Same config hash | Installer/upgrade activity continues; completion UNKNOWN | 21 EOM writes, zero CPU mismatches, migration failures, root waits or panics; continuously growing serial and storage I/O; exact prior target 0 / entry CPU 4 / pending 1 case now writes on actual CPU 0; ci/boot-01-observations.jsonl |
| Export/clean-branch ancestry correction | Tested line base `c48fc5ccade272ec79f633dcb23e45ba1c40d6cc` | N/A | Active VM binary unchanged | Active VM config unchanged | No new VM action | FAIL in initial export setup: cd66095f is on a different descendant line with six unrelated changed files; old clean branch b9a9719/da2bd1b and exports based on cd66095f are superseded. Verified aa887e5 parent and merge-bases; exporter corrected and now rejects unexported existing-base changes. Instrumented source/build/runtime evidence remains valid. |
| Corrected clean source variant pushed | Functional `7a3b98a480242391a92339df987fcc3f98ddd4b6`; CI head `c960997ae3725ead2c07c8004f57939925a97c54` | Run not yet retrieved | Not verified yet | Not installed | NOT RUN | Branch test/synic-eom-clean-c48fc5c uses the actual c48fc5c baseline; graphics/framebuffer/packaging match tested instrumented source; source-only patch is two files, 42 insertions/31 deletions; CI/source commits remain separate |
| Same boot, 12:27 UTC observation | `0756f1d75601f0c24bce98ae4adf8c83ce6e3307` | `40090495930` | Debug as above | Same config hash | Still running, upgrade completion UNKNOWN | About 79 MiB serial data, continuously written; one firmware-to-XNU handoff and one APFS root resolution; still 21 EOM writes and zero CPU mismatches, migration failures, root waits or panics. Hyper-V heartbeat queried OK earlier. No forced lifecycle action. ci/boot-01-observations.jsonl |
| Serial receiver liveness and recovery, 12:35–12:36 UTC | `0756f1d75601f0c24bce98ae4adf8c83ce6e3307` | `40090495930` | Debug unchanged | Config unchanged | VM not restarted; installer completion still UNKNOWN | FAIL in continuous capture: foreground receiver/session ended; last byte 12:34:13.99 UTC. Restored through an independent hidden process at 12:36:24.48 UTC, receiving new data. About 2m10s coverage gap; outcome during gap UNKNOWN. Original 94.8 MiB capture preserved; new files under serial-reconnect-02; no observed EOM mismatch/panic/root wait in captured data. |

## Subsequent observations

2026-10-24, second captured boot at 13:21–13:23 UTC: user reported VM booting;
receiver automatically reconnected into a new file. Source `0756f1d75601f0c24bce98ae4adf8c83ce6e3307`,
CI `40090495930`, Debug kext SHA256 `38bf5d6dcc26dd62eb4818086ea6c48505d09880e5919574e7073c922f4ffec9`,
last verified EFI config SHA256 `430d1f347fa0b5271cd212e1c35692013b252361eccc8ba5f0ff6c3ec95368eb`.
Observed PASS through all 14 channels, completed scan, SCSI start and APFS root;
at least 16 EOM writes, no CPU mismatch, panic or root-device waiting. Evidence:
`ci/boot-02-0756f1d.json` and sanitized companion; complete growing raw file in
the local test directory. Upgrade/login completion not established. This is
the second captured successful enumeration, not release-stability acceptance.

Correction after user GUI report and kernel inspection, 13:25 UTC: this second
boot is **Sequoia Recovery**, Darwin **24.4.0**. The recovery menu offers
"Reinstall macOS Sequoia". It must not count as a second Tahoe boot or as
upgrade completion. The first captured boot was Darwin **25.6.0** in the
Tahoe installer/upgrade environment. Both show successful enumeration, but
their OS/boot environments differ. Evidence: ci/boot-02-recovery-assessment.json.
No reinstall, erase, restore or offline system-volume change was initiated.
Further root-path inspection: boot 2 resolves an IOHDIX/BaseSystem disk-image
root, not the installed system's APFS root. Earlier shorthand "APFS root" for
that second boot was incorrect and is superseded. VMBus enumeration and SCSI
start remain observed facts; installed Tahoe volume state is still unknown.

## Hypotheses

2026-10-24 16:40 UTC: read-only inspection identifies a blessed APFS System
snapshot and matching boot.efi. Selected Preboot CoreServices Boot.plist contains
`Kernel Flags = -bsdmgroot`; its SystemConfiguration counterpart has empty flags.
NVRAM boot-args do not contain that flag; recovery-boot-mode and efi-boot-next are
absent. Serial explicitly confirms BaseSystem.dmg pivot and migration mode.
Therefore the third Tahoe run is an installer/migration boot with underlying
APFS access, not a normal installed-System boot. The reason migration did not
complete remains UNKNOWN. No flag was changed based on this observation.
Local evidence: frames 20261024T163540Z, 163616Z, 164002Z, 164057Z.

2026-10-24 16:43 UTC: authorized guest graceful shutdown from idle Recovery;
host confirmed Off, original system disk detached, new full cold copy begun in
the uniquely named system-boot-selection local directory. Hash verification is
pending; no copied disk is yet attached/modified/booted. Original EFI and protected
backups remain untouched. Installed binary/config provenance remains as above.

Clean source CI run 40093339256: downloaded Debug and Release ZIP and Monterey
executable hashes independently match CI provenance. See
ci/run-40093339256-verified.json. This is BUILD verification, not runtime acceptance.
Speculative graphics run 40101047189 also passed; its variant remains uninstalled.

2026-10-24 16:17 UTC live continuation: source `0756f1d`, build `40090495930`,
Debug executable SHA256 `38bf5d6dcc26dd62eb4818086ea6c48505d09880e5919574e7073c922f4ffec9`;
last verified EFI config SHA256 `430d1f347fa0b5271cd212e1c35692013b252361eccc8ba5f0ff6c3ec95368eb`.
Third boot serial contains 23 matching target/actual CPU-0 EOM writes and
OSInstaller-triggered reboot at 15:19:09 followed by orderly unmount/restart.
Current responsive console independently reports Darwin 24.4.0 Recovery.
Receiver PID 46464 remains alive; reconnect file at 15:20:39 has no bytes.
No completed Tahoe login. Installer log ends at reboot; visible efilogin-helper
archive-limit/missing-sound errors have UNKNOWN causal relevance. No VM lifecycle
or VHDX change performed. Raw log and timestamped console frames remain local
under the existing vm-test directory. Latest handoff: Docs/handoff/UNATTENDED.md.

- Wrong-CPU EOM may leave CPU 0's queued offers undelivered and cause storage
  enumeration to stall. Correlation in the supplied excerpts is not causality.
- Binding followed by a scheduler switch should correct CPU locality. It needs
  compilation, symbol/export checks and runtime validation on the target OS.

## Confirmed fixes

The first instrumented candidate boot confirms CPU-local EOM for its 21
observed writes and successful enumeration through APFS root. This is a
single-run observation, not a confirmed stable Tahoe boot fix or release
acceptance. Full installer/login completion, repeated boots and a clean release
comparison remain pending.
