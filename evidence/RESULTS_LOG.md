# Results log (append only)

## 2026-10-25 00:37:42 UTC - passive12-minute check and delivery

Same c9eb980 framebuffer310f155f... / run40139181101, core803a3d24...,
configf2b8dce68e686e349940192cb0f4a53a299e2f5f3b870ab2ceb6acec238fdc81.
Host Running uptime12m07; receiver48800 alive. Immutable346500-byte serial prefix
SHA256742268bc9ab1e94aec1e4c9c1a2ac1bd962fa330aac1c90cf1952de57c142943:
26 matching EOM,0 mismatches,0 cursor conversion failures,1 software marker,
0 panic/rootwait. Passive observation only; no new inputs/reboot/stress test.
Complete delivery archive maintainer-20261025T003641Z-94907bdd.zip,
SHA256cfb8ffc1909d51fd493c61bc048c0a125cdd8a7967d14bc81774b738038b4c48,
25 manifest entries; source reconstruction, original CI ZIP/binary hash checks and
nested privacy checks PASS. Includes project map/build/install/rollback instructions
and separate source/Binary provenance. No raw logs, images/config/VHDX/KDK payload.
Acceptance remains one positive Debug session, not stable Release validation.

## 2026-10-25 00:28 UTC - positive software cursor workaround run

Guarded four-module Aux installer succeeded, sourcec9eb980/run40139181101,
framebuffer SHA256310f155f50aa2f5ffccd688ba0ef280e268335e209e616ae888f2f73d8133ef3;
Aux SHA256bd40a30af2dc48e572ddab8d97ac6bea6e2fe00bb73d37ec2293cc0b8300da2.
Verified exclusive backup /Users/Shared/HVCursorAuxInstall.LFcYut1Y; other three
module IDs/versions retained; Boot/System collection hashes unchanged; kcditto PASS.
Guest poweroff completed but host stuck Stopping; Stop-VM InvalidState; matched
target worker terminated, Hyper-V automatic recovery restart then regular TurnOff
reached Off. No other VM or original disk/backup changed. Record as host-finalization
incident, not successful clean reboot. No lifecycle change after current boot start.

New EFI made only Off/detached with source/copy hash equality; config now
f2b8dce68e686e349940192cb0f4a53a299e2f5f3b870ab2ceb6acec238fdc81, only semantic
change append -hvgfxfbswcursor. Core803a3d24... unchanged. Boot00:25:35 UTC.
Prefix00:28:22 bytes302283 SHA2567d7797aad71ca46d86ff014a457bdb6e6fb4701e7c722bc7eb21cf0e90f07fa0:
26 matching-CPU EOM writes,0 mismatches,0 cursor conversion failures,1 software
activation marker,0 panic/root-wait. VMConnect desktop visible. User reports mouse,
Safari and Downloads working so far. User later reports guest computer rename;
no new driver/config action inferred from it. Raw evidence remains private.
Confirmed scope: useful workaround observed in one short Debug boot. Framebuffer
0.9.9->0.9.10 plus flag were changed together; causal isolation and sustained,
repeated and Release tests pending. Original migration completion still unproven.

## 2026-10-25 00:00-00:06 UTC - KDK success; second guarded install rolled back

Matching KDK25G241 installation reported SUCCESS after local root authentication.
DMG hash/signature provenance unchanged from preceding verified entries.
Second guarded install c9eb980/run40139181101 framebuffer310f155f... saved old
module in /Users/Shared/HVCursorBackup-20261025T000026Z-990 and hash verified it.
kmutil --update-all failed missing non-release kernels and read-only filesystem
for release collection. Script restored/hash-verified original0.9.9. No reboot.
Do not repeat this broad command; no unmounting/protection changes performed.
Private Aux03 failed unrelated AppleCentauriManager/AppleEmbeddedPCIE dependency;
explicit-only/x86_64 Aux04 failed missing baseKC. Existing root Boot/System KCs
were listed read-only and now explicitly referenced in private Aux05 probe.
Current core e170982/run40124452997/803a3d24... and EFI config32be11... unchanged.
Candidate not active; mouse/cursor behavior after candidate remains untested.

User again reports black VMConnect while independent WMI shows responsive guest.
Temporary ignored local WMI viewer restored visible access; initial Invalid object
path bug in viewer corrected by full query. User authentication via viewer reached
root shell. Viewer now v4 read-only during agent commands; no input logs, no host
global settings. Helper-viewer cursor behavior is NOT driver-fix validation.

## 2026-10-24 23:33 UTC - live serial evidence recovered without restart

Directory entry size0 was stale. Direct FileStream Length/read gives325821 bytes
at23:32; new handle-based snapshot helper gives327363 bytes at23:33:58, proving
growth while directory metadata remained misleading. No receiver restart needed.
Immutable prefix SHA2567df624de71f9ba7fd42edb041ca5de1f4bd51925593c1f3d5ef3b3e042877408,
local-tests/cursor-media-20261025-03/serial-snapshots/serial-prefix-20261024T233358Z-4c9948f3.log.
16 complete EOM writes all target==actual,7 cursor conversion failures,0 panic,
0 root wait,0 software-cursor activation. This is current e170982/run40124452997
core803a3d24.../config32be11... with loaded original framebuffer0.9.9, not new
cursor candidate. Previous no-data claims from directory metadata are superseded.
Added repeatable read-only snapshot helper; no VM/pipe/config changes.

KDK pkg signature verified signed Apple Software, chain to Apple Root CA.
Installation did not start: sudo authentication expired. sudo -s now waits for
local password; no further guest input while pending. All candidate/cache/root
actions remain pending. Agent replaced only target VMConnect clients; WMI shows
live desktop even when PrintWindow capture is black. No guest reboot or fix claim.

## 2026-10-24 23:15-23:26 UTC - guarded cursor install rolled back; KDK pending

Source c9eb980/run40139181101 Debug framebuffer310f155f...; existing core/config
e170982/run40124452997/803a3d24.../32be11... unchanged.
Successful local sudo auth. Own DVD had stale metadata/read errors on hot media
replacement; unmounted own slot0:2 removed, fresh DVD0:3 with ISO03 resolved it.
Guest verified installer e2e5a6b6026b218aa309caf8532e42f083534f253b1047292d6a361e058e7856.
Original module backed up at /Users/Shared/HVCursorBackup-20261024T231512Z-863,
hash checked. Candidate file installed briefly; kmutil install --update-all
failed missing KDK25G241; script restored and hash-verified original0.9.9.
No reboot or boot-arg change. This is a failed install/cache test, NOT a cursor fix.
Private Aux-only probe failed KDK requirement; --allow-missing-kdk aux probe
failed dependency resolution for com.apple.iokit.IOGraphicsFamily. No active
collection replacement was requested by those probes. Faster manual TypeText
corrupted two commands; unknown-option error / cancelled; use char-wise pacing.
WMI thumbnails show responsive guest; re-opened VMConnect client stays Connecting.

Exact KDK downloaded from project release25G241, API SHA256 and file match
9045a521c8ae362d4cb2cc54701b03462686e0069518a0b66cfe2028f87dfe9b.
Read-only ISO created7535d4948662bcdd37632cd0fc91e4bb344f04731f4c1c97b122400ea7780a54,
attached only target DVD0:4. Guest DMG integrity verified and read-only mounted.
Apple package signature check pending at checkpoint; no KDK install yet.
Private frames/logs/media retained local; original disks and backups preserved.

## 2026-10-24 23:02 UTC - in-guest runtime identification confirmed

Read-only guest sw_vers confirms macOS26.7.1, build25G241 on current test copies.
Loaded framebuffer fish.goldfish64.MacHyperVFramebuffer0.9.9, UUID
45B79D4F-3751-32EE-89A1-57CF056D4493. On-disk /Library/Extensions executable
SHA25651c9cd8c78ceb87f3e373882ea25cfe982f68c4a1e89c6d4ff6985b04038c1cf.
Private console230251Z records identity/hash; console230221Z records sw_vers.
Initial manually typed commands had Swiss y/z mismatch and are not evidence of
missing modules/files; corrected commands succeeded. ISO inspection script itself
uses correct literal spelling. No guest install yet.
Existing SIP Custom Configuration queried, no settings changed. sudo -n true
reports password required; sudo -v now waits for local admin authentication.
No further guest keyboard commands may be sent while at password prompt.
Updated read-only DVD03 contains guarded installer + exclusive verified backup;
SHA25606543889CB20706653766BF6A71D44F9AEC2DEE40E732DA77186A2A01237D81D.
Current source/build/config unchanged e170982/run40124452997/config32be11...;
candidate c9eb980/run40139181101 still uninstalled, cursor fix unconfirmed.

## 2026-10-25 local - cursor comparison build verified; guest access pending

CI40139181101 / source c9eb980daab9598b1af6732217147490dacceb3e SUCCESS
Debug/Release and analyses. ZIP/binary hashes matched CI provenance, boot flag and
activation message found in framebuffer binaries. See run-40139181101-verified.json.
No installation/runtime claim. Software fallback is a test hypothesis.
Target test system was temporarily detached/read-only mounted for APFS inspection;
7-Zip native device path attempts failed, system restored at SCSI0:1 via finally.
No filesystem modifications. Agent restarted unchanged e170982/run40124452997
with same executable803a3d24f6312ce53f1b7385321c37e1a14e28d5c413620634243f821e60c888
and config32be11f98247242f8e1534076817825cae2fa79b235ce289b179ec59e39caf8f.
Serial PID48800 verified; new zero-byte capture225535Z and console show local
pre-kernel unlock. Module identification blocked pending local authentication.
Read-only HVCURSORTEST ISO attached at previously free SCSI0:2 DVD slot:
SHA25682E2655BAAF7FF36C9D3E0231D6618699C5C108287AD478A0516E12384FDDDF0.
Contains candidate ZIP and read-only inspection script. No security or boot-order
changes, no automatic install. All raw context/media remain private local-tests.

## 2026-10-25 local - user shutdown, authorized restart, isolated cursor candidate

Previous boot capture serial-20261024T222131Z-ebab9d12.log: 697354 bytes,
SHA256989B68C0637AA2651628AF79F8A6B0B6AB93809989EBAEDDF8613DA402F58DFC;
22 EOM writes, all matching CPU; 161 cursor conversion failures; zero panic/root
wait markers. Tail shows CPU halted and driver PowerOff. User reported shutdown;
host Off confirmed. Original disks/backups untouched.
User subsequently authorized automatic starts. Agent verified two expected
working-copy attachments and serial PID48800 then started target unchanged:
e170982/run40124452997, executable803a3d24f6312ce53f1b7385321c37e1a14e28d5c413620634243f821e60c888,
config32be11f98247242f8e1534076817825cae2fa79b235ce289b179ec59e39caf8f.
New source candidate c9eb980 on test/tahoe-software-cursor adds opt-in boot flag
-hvgfxfbswcursor to advertise no hardware cursor (IOFramebuffer software path).
CI40139181101 started; no installation/runtime claim. Identifying actual loaded
framebuffer module remains necessary before installing this separate component.

## 2026-10-25 local - user-reported intermittent pointer reproduction

User clarifies the trigger: clicking Downloads in Finder makes the pointer
disappear, before opening the downloaded Jump Desktop DMG. Three or four fast
mouse movements restore the pointer briefly, then it disappears again. This is
a user-reported reproduction sequence in VMConnect, not an agent-observed trace
or a completed Jump Desktop comparison. No new source/build/install change.
Hypothesis: cursor shape/visibility refresh or conversion state, rather than
complete loss of mouse input. Correlation with earlier conversion errors does
not establish causality. Next comparison should record cursor shape/visibility
events around this exact trigger and identify the loaded framebuffer binary.

## 2026-10-24 22:22 UTC - user-initiated reboot and recovered serial evidence

User initiated restart; host uptime reset. Agent performed read-only checks only.
Source/artifact/config unchanged from preceding e170982/run40124452997 test.
Receiver PID48800 auto-reconnected. Previous capture (same private folder below)
serial-20261024T205403Z-a56bdd2a.log is now 493656 bytes, SHA256
EC4A3A10FE147CE49835CD827190D823DDB803AD7132DB0EE90CD222645CBEC5.
It contains Darwin25.6, 22 EOM writes all target==actual CPU, 59 hardware cursor
conversion failures, no panic/root-wait marker, and shutdown ending MACH Reboot.
Earlier zero-byte observation was a time-specific snapshot; why data became
visible later is unproved. No permanent missing-boot evidence claim is justified.
New serial-20261024T222131Z-ebab9d12.log empty at checkpoint; console at local
pre-kernel password/unlock. Current reboot kernel outcome pending.
No cursor fix established; conversion errors correlate with reported symptom.

## 2026-10-25 local / 2026-10-24 22:20 UTC - pointer follow-up

User-reported: movement fast; black pointer disappears after a short time.
Verified: target Running; read-only VMConnect capture shows full macOS desktop.
Prepared source e170982, Actions40124452997; executable SHA256
803a3d24f6312ce53f1b7385321c37e1a14e28d5c413620634243f821e60c888;
EFI config SHA25632be11f98247242f8e1534076817825cae2fa79b235ce289b179ec59e39caf8f.
These are prepared artifact identities, not an in-guest loaded-module check.
Private image: local-tests/system-boot-selection-20261024T164253Z/
vmconnect-20261024T222015908510Z-0.png. Serial receiver PID48800 alive but
local-tests/display-pacing-test-20261024-01/serial-start-20261024T205328Z-cc486be1/
serial-20261024T205403Z-a56bdd2a.log remains empty. Current boot SynIC result unknown.
Hypothesis: cursor image transitions may exceed the framebuffer 32x32 conversion
descriptor; earlier logs show conversion failures, but causal linkage is unproved.
No guest input/restart/disk/code change; active user session preserved.
Confirmed complete cursor fix: none.

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
| First instrumented candidate boot, 11:51â€“11:54 UTC | `0756f1d75601f0c24bce98ae4adf8c83ce6e3307` | `40090495930` | `38bf5d6dcc26dd62eb4818086ea6c48505d09880e5919574e7073c922f4ffec9` | `430d1f347fa0b5271cd212e1c35692013b252361eccc8ba5f0ff6c3ec95368eb` | FIRST PASS through APFS root; full installer/login outcome pending | 21 observed EOM writes all target 0 / actual 0; channels 1â€“14, completed scan, SCSI controller started, APFS root; no root waiting or panic at observation; ci/boot-01-0756f1d.json and sanitized excerpt; complete serial capture continues locally |
| Same boot, 11:55â€“11:56 UTC | `0756f1d75601f0c24bce98ae4adf8c83ce6e3307` | `40090495930` | Debug as above | Same config hash | PARTIAL PASS: WindowServer running; OSInstaller progress-UI calls; installation completion unknown | Serial capture continues; no forced reboot while upgrade appears active; local capture file under local-tests/vm-test-0756f1d-20261024-01/serial |
| Clean source variant prepared and pushed | Functional `b9a97199c48115fa4d706655307e9c8adddc0bb0`; CI head `da2bd1b49247aea1c17cf71f31925648df3ca14f` | Run not yet retrieved | Not built/verified yet | Not installed | NOT RUN | Branch test/synic-eom-clean-20261024 contains the functional patch directly on pinned base, without local diagnostic code; separate CI commit; existing VM test continues unchanged |
| Same boot, 12:06 UTC observation | `0756f1d75601f0c24bce98ae4adf8c83ce6e3307` | `40090495930` | Debug as above | Same config hash | Installer/upgrade activity continues; completion UNKNOWN | 21 EOM writes, zero CPU mismatches, migration failures, root waits or panics; continuously growing serial and storage I/O; exact prior target 0 / entry CPU 4 / pending 1 case now writes on actual CPU 0; ci/boot-01-observations.jsonl |
| Export/clean-branch ancestry correction | Tested line base `c48fc5ccade272ec79f633dcb23e45ba1c40d6cc` | N/A | Active VM binary unchanged | Active VM config unchanged | No new VM action | FAIL in initial export setup: cd66095f is on a different descendant line with six unrelated changed files; old clean branch b9a9719/da2bd1b and exports based on cd66095f are superseded. Verified aa887e5 parent and merge-bases; exporter corrected and now rejects unexported existing-base changes. Instrumented source/build/runtime evidence remains valid. |
| Corrected clean source variant pushed | Functional `7a3b98a480242391a92339df987fcc3f98ddd4b6`; CI head `c960997ae3725ead2c07c8004f57939925a97c54` | Run not yet retrieved | Not verified yet | Not installed | NOT RUN | Branch test/synic-eom-clean-c48fc5c uses the actual c48fc5c baseline; graphics/framebuffer/packaging match tested instrumented source; source-only patch is two files, 42 insertions/31 deletions; CI/source commits remain separate |
| Same boot, 12:27 UTC observation | `0756f1d75601f0c24bce98ae4adf8c83ce6e3307` | `40090495930` | Debug as above | Same config hash | Still running, upgrade completion UNKNOWN | About 79 MiB serial data, continuously written; one firmware-to-XNU handoff and one APFS root resolution; still 21 EOM writes and zero CPU mismatches, migration failures, root waits or panics. Hyper-V heartbeat queried OK earlier. No forced lifecycle action. ci/boot-01-observations.jsonl |
| Serial receiver liveness and recovery, 12:35â€“12:36 UTC | `0756f1d75601f0c24bce98ae4adf8c83ce6e3307` | `40090495930` | Debug unchanged | Config unchanged | VM not restarted; installer completion still UNKNOWN | FAIL in continuous capture: foreground receiver/session ended; last byte 12:34:13.99 UTC. Restored through an independent hidden process at 12:36:24.48 UTC, receiving new data. About 2m10s coverage gap; outcome during gap UNKNOWN. Original 94.8 MiB capture preserved; new files under serial-reconnect-02; no observed EOM mismatch/panic/root wait in captured data. |

## Subsequent observations

2026-10-24, second captured boot at 13:21â€“13:23 UTC: user reported VM booting;
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

## Additional verified observations

2026-10-24 user-requested pacing restart: target Running with the verified
e170982/run40124452997 working-copy candidate. Executable SHA256
803a3d24f6312ce53f1b7385321c37e1a14e28d5c413620634243f821e60c888;
unchanged config32be11f98247242f8e1534076817825cae2fa79b235ce289b179ec59e39caf8f.
Old receiver had exited; new independently verified PID48800 was ready before
start, with a unique new serial folder. No disk/config/security change; original
disks remain detached. Exact start time/paths are in display-pacing-test local
user-start-*.json and serial-start-record-*.json. Local unlock and mouse runtime
assessment pending; this start checkpoint is not a confirmed improvement.

Final check after the 33-ms candidate's pre-kernel unlock wait: VM Off, zero new
kernel serial bytes. Poweroff cause NOT established. Do not count a pacing boot,
CPU-local EOM pass, mouse improvement or regression for this candidate. Preserve
Off state and both attached working copies; local start/unlock and logging check
are prerequisites to further runtime work. Exact check time and state:
ci/display-02-pacing-pending.json. Original disks/backups remain preserved.

2026-10-24 19:39:24 UTC pacing attempt: source e170982, run40124452997 SUCCESS
(Debug/Release and Clang). New executable SHA256
803a3d24f6312ce53f1b7385321c37e1a14e28d5c413620634243f821e60c888;
same config32be11f98247242f8e1534076817825cae2fa79b235ce289b179ec59e39caf8f.
Only core refresh interval changes10 ->33ms; SynIC/mouse/cursor source unchanged.
Prepared new exclusive EFI after prior copy-only run was deliberately interrupted
when Setup Assistant regular exit/navigation attempts did not provide shutdown.
Original cold system/EFI and all variants remain preserved. Current VM waits
at a native pre-kernel local unlock screen; new kernel serial file has zero bytes.
Runtime/pointer improvement UNKNOWN. This is a credential blocker, not a compiler
failure or a proven pacing regression. Evidence:ci/display-02-pacing-pending.json.

2026-10-24 19:01 UTC scope correction: current direct framebuffer showed 12:01
and changed masked input; the interactive VMConnect client stayed at 11:57.
Prior WMI login evidence proved a running framebuffer, not usable client refresh.
Reconnect refreshed it once. User independently reported no apparent input/focus.
No claim that keyboard packets were absent is justified by that stale client.

2026-10-24 19:06:40 UTC: separate graphics test source 3d31e11, build40101047189,
Debug executable SHA256 39219543142986a6485ea2ae05a15a4c34e017946a45f40a2106466520a840a8,
same config SHA256 32be11f98247242f8e1534076817825cae2fa79b235ce289b179ec59e39caf8f.
Graceful native macOS menu shutdown, verified new exclusive EFI copy; only binary
content changed, SynIC source equal. Boot reached user-reported working input and
visible post-login Setup Assistant. All 14 channels, 15 matching-CPU EOM writes,
no panic/root wait. Raw prefix hashes and limitations: ci/display-01-3d31e11.json.
Original system/EFI/backups preserved. An additional pretest 18:50 capture shows
14 channels and 24 matching-CPU EOM writes; boot initiator not inferred.

User subsequently reports slow mouse movement: 1920x1080x32, sampled VM CPU13%,
cursor-conversion failures and full-frame timer10ms observed. Cause unresolved.
Separate e170982 pacing experiment changes only10 ->33ms; run40124452997 building,
not installed/runtime validated at this checkpoint. Graphics and SynIC corrections
remain distinct; no arbitrary mouse acceleration or host-global change performed.

2026-10-24 17:19:29 and 17:22:06 UTC: CONFIRMED normal Tahoe login GUI on the
isolated system/EFI copies, with clock advancing between independent console
captures. Darwin 25.6.0; version previously read from the same System snapshot
as 26.7.1 / 25G241. Personal account login and runtime sw_vers not performed.
Source `0756f1d`, run `40090495930`, Debug Monterey SHA256
`38bf5d6dcc26dd62eb4818086ea6c48505d09880e5919574e7073c922f4ffec9`.
EFI config SHA256 `32be11f98247242f8e1534076817825cae2fa79b235ce289b179ec59e39caf8f`.
All 14 channels, 24/24 parseable EOM writes matching CPU 0, zero raw storage
packet lines and no captured panic/root wait/BaseSystem pivot. Serial receiver
alive. Evidence: ci/boot-05-tahoe-login.json and private image/raw prefix hashes.

This follows deliberate hard stop of the prior copy-only boot at 17:15:09,
after >20 minutes without GUI and a failed graceful shutdown (daemon absent).
That interrupted capture is preserved and explicitly marked NOT a successful
boot. Another exclusive EFI copy removed only -hvstormsgdbg while retaining
serial/SynIC diagnostics and -nobsdmgroot. Same system working copy was reused,
so caches, state and possible journal replay confound timing comparisons.
Original cold system and earlier EFI variants remain unchanged/detached. No
claim of original upgrade completion, clean Release validation or stable release.
Graphics-hypothesis binary remains uninstalled; login clock refresh works without it.

2026-10-24 17:12 UTC: the copy-only normal-mode boot continues; early boot
completed and coreservicesd/additional services started. GUI/login not proved.
Observed APFS long-transaction/15-second-iterator messages and kernelmanagerd
busy timeouts. At one prefix checkpoint 246575/249442 lines were storage packet
prints. Logging overhead is a hypothesis; no comparison boot was performed.
Attempted graceful Stop-VM (no Force/TurnOff) FAILED 0x80004005. Serial explicitly
identifies missing shutdown daemon; the target remains Running on the two copies.
Original disks remain detached. No forced lifecycle action, packet-verbosity
change or graphics binary change occurred. See local graceful-shutdown-request.json
and current raw capture. Direct target VMConnect capture at 17:03 showed early
kernel console too; WMI alone is not established as the stale-image cause.

2026-10-24 16:51 UTC: isolated copy-only normal-boot experiment started after
graceful shutdown and matching cold System/EFI copy hashes. Original system disk
and prior EFI are detached/preserved. Same source `0756f1d`, run `40090495930`,
Monterey executable SHA256 `38bf5d6dcc26dd62eb4818086ea6c48505d09880e5919574e7073c922f4ffec9`.
Only copied EFI boot-args gains `-nobsdmgroot`; all other plist values match.
New config SHA256 `b8384af04dad0aabb71048d9b0f35242e6f3bd413d096cfa5bf74b568e53bff1`.
Copied EFI was explicitly prioritized over Network in target firmware.
By 16:59 UTC: all 14 channels, 20 parseable matching-CPU EOM writes and one
serial-interleaved unparseable EOM line; APFS snapshot, launchd, Data and Cryptex
mounts observed. Both -nobsdmgroot and -bsdmgroot are in kernel args, but no
authenticated BaseSystem pivot/migration marker occurs. Normal-mode boot tasks
are active. GUI/login remains UNCONFIRMED. At 17:01 UTC init_featureflags has
completed and systemstats/prng_seedctl tasks are reached. This is progress,
not installation completion. See ci/boot-04-nobsdmgroot-observation.json for
an explicitly timestamped prefix-hash checkpoint of the still-growing raw log.

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

## Hypotheses

- Wrong-CPU EOM may leave CPU 0's queued offers undelivered and cause storage
  enumeration to stall. Correlation in the supplied excerpts is not causality.
- Binding plus scheduler switch is supported by source inspection, successful
  compilation/import checks and the captured CPU-local writes. Broader CPU
  topology, repeated boots and clean Release runtime behavior remain unverified.

## Confirmed fixes

Compiler/API follow-up is confirmed by successful Debug/Release builds and
analysis. The specific wrong-CPU EOM sequence is corrected in recorded calls,
including target 0 / entry CPU 4 / pending 1 followed by actual CPU 0 in boot 1.
The latest login-screen boot adds 24 matching-CPU writes and all 14 channels.
This establishes observed CPU-local behavior and a normal GUI start on a copy,
not a stable release or original migration-completion claim. Repeated and clean
Release runtime tests and a personal user-session/version check remain pending.

## Development setup observation, 2026-10-25 00:53 UTC

Separate setup branch from581acf4; guest remains Tahoe26.7.1/25G241 x64.
User requested English, one current stable version, free App Store preferred.
VS Code1.143.1 and .NET SDK10.0.402 installed from official Microsoft URLs with
SHA256/SHA512 and Code signature/Gatekeeper checks. C# Dev Kit installed.
Guest success marker, console build/run Hello World and single SDK listing
observed. Details and exact setup-medium hashes: Docs/handoff/DEV_ENVIRONMENT.md.
Xcode27.1 incompatible (M1 required); App Store compatible fallback accepted,
Installing visible00:53; exact installed version/iOS validation still pending.

Passive serial sample00:52:58:379717 bytes, SHA256
28401f53dd3cea7a3d8c9f01aa8e78b2ea668b02b9a413e39dc0d446afd8dad1;
26 matching EOM,0 mismatch/cursor conversion/panic/rootwait,1 software marker.
Evidence local-only dev-setup-20261025-02/serial-snapshots; capture PID48800 alive.
Driver source c9eb980/run40139181101; core803a3d24... and configf2b8dce6...
unchanged by setup. No reboot, kernel, security or VHDX changes performed.
This setup is not another confirmed driver fix or release stability test.

## Development setup verification, 2026-10-25 01:14 UTC

Xcode26.5/17F42 installed from App Store, Universal host executable verified;
first launch completed after local user authentication. iPhoneOS SDK26.5.
Native SwiftUI app built successfully for iphoneos/arm64, minimum iOS15.0.
Final corrected verifier marker IOS_ARM64_BUILD_VERIFIED_UNSIGNED observed.
Binary SHA25624b5e25c4c3ffc38c07e52ee775a9a9d21ba2a01307cefd1e11a85c604960b37.
Initial build succeeded but post-build lipo invocation failed; verifier repaired.
No compiler fix or driver change claimed. Xcode27 requires Apple Silicon; no
verified Intel execution patch found. User accepts26.5 as practical baseline.

VM Running uptime48m27; normal guest session now locked. Simulator launch is
blocked on local unlock; runtime completion/device signing remain unverified.
Serial PID48800 alive,01:14 prefix512473 bytes SHA256
a423dbd015933f83f2d5aa20b91fe026f1d6501b1907f1e24c27c02f998cd1d3;
26 matching EOM,0 cursor conversion/mismatch/panic/rootwait,1 software marker.
Driver c9eb980/run40139181101, core803a3d24... and configf2b8dce6... unchanged.
Reproducer and media hashes in DEV_ENVIRONMENT.md; curated evidence in
evidence/ci/dev-environment-20261025.json. All backups retained, no VM restart.

## Simulator validation, 2026-10-25 01:22 UTC

Previous lock-screen blocker superseded: fresh01:16 desktop inspection confirms
open session. iOS26.5/23F77 Universal image Ready; iPhone17 boots. Existing
SwiftUI project built for Simulator/x86_64, installed and launched successfully.
BUILD SUCCEEDED, IOS_SIMULATOR_APP_LAUNCHED and Developer environment ready
visible in native VMConnect. Reproducer/media hashes in DEV_ENVIRONMENT.md.
No physical-device/signing/Metal/performance claims; user accepts26.5 development
and later Xcode27 final build/test/sign/distribution on Apple Silicon Mac.

VM uptime56m32, serial PID48800 alive;700569-byte prefix SHA256
7afa3d2ff0ec70428d7b2a1f22747d14ed8b9227657648f76f5289356c6dc510;
26 matching EOM,0 mismatch/cursor conversion/panic/rootwait,1 software marker.
Driver c9eb980/run40139181101, core803a3d24... configf2b8dce6... unchanged.
No VM reboot, security changes, EFI/VHDX changes or backup removal during setup.
