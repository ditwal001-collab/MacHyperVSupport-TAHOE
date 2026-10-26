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

## Overnight Debug result and clean candidate, 2026-10-25

At11:32 UTC VM Running uptime11h07m15; user reports stable macOS.
Core803a3d24.../framebuffer310f155f..., sourcee170982/c9eb980 run40139181101;
configf2b8dce6... unchanged. Receiver48800 alive;5432111-byte prefix SHA256
3a74723014ec76e64de3167bc6c0ab9d714de2d81df010a42fe9932a6d9ca90d.
26 startup EOM writes match CPUs;0 cursor conversion/panic/rootwait markers.
Positive sustained Debug evidence, not clean Release/repeated-boot proof.

Clean combined source6c3568178ba21136b8c21dd45597476c74ec31d1, run40189441511,
Debug/Release builds and Clang analyses PASS. All ZIP/kext hashes match uploaded
provenance; Release contains no TAHOE-SYNIC/TAHOE-DEBUG strings. Core Release
c97e29193de9bedf9e2f39b7da38a589347874f7f8ef8c0c8e24f92d7f76ca16;
framebufferd8a079d47d61988aabe40cb788b015979c27384135b57339e854d5c017792122.
Clean Release runtime remains a separate pending test at this checkpoint.

Normal Hyper-V integration shutdown failed0x80004005; guest remained Running.
Normal macOS menu shutdown then completed, serial total2735ms; Off confirmed
11:49:08 UTC. No hard reset/worker termination. Preserve this open integration
issue separately from SynIC/cursor results. Final Debug-prefix SHA256
22de7f0660f76252ec26023992702950c69d6672a740de192ba23d25208c3091.
New cold Release copies created from detached Off sources; initial copy command
had invalidated object properties and copied nothing, corrected using immutable
pre-shutdown path snapshot. Full cold-copy SHA verification is pending.
Anonymized Hyper-V/EFI profiles and HYPERV_SETUP document actual versus unknown
configuration history. No protected/original backups changed.

## Release preparation checkpoint, 2026-10-25 12:07 UTC

Both new cold copies hash-match sources: EFI2e6fe24d... and system4e07f7ce... .
Only Release corec97e2919... changed on new EFI; configf2b8dce6... identical.
Original overnight Debug disk pair retained detached. Normal preparation boot
started12:03:54; local pre-kernel unlock screen observed. Actual new log empty
at12:07:56; receiver48800 alive. Framebuffer is still Debug310f155f..., so no
full Release or repeated-boot success counted. Local unlock/sudo needed before
guarded Release framebufferd8a079d4... installation and normal reboot.
Source6c35681/run40189441511; all hashes in run verification and RC1 report.
A Hyper-V-only package draft passed reconstruction, CI hash and privacy checks.
Cleanup remains read-only inventory; originals/active/Debug rollback preserved.

## Release framebuffer installation 2026-10-25 13:23 UTC

The guarded installer completed after local sudo authentication. Console evidence
vmconnect-20261025T132316516368Z-0.png shows RELEASE_RC1_FRAMEBUFFER_INSTALLED,
the expected framebuffer SHA256 d8a079d47d61988aabe40cb788b015979c27384135b57339e854d5c017792122,
and Aux SHA256 51d86e9db1092774f5830fe769b69608e657d4d860535d9f135563506a416e25.
Boot/System collection hash checks passed before and after the Aux replacement;
all four Aux module IDs and other versions passed the script checks. Backup is
retained inside the guest under /Users/Shared/HVReleaseRC1.s0ZkXpJy.
The macOS restart notice is expected; it alone would not prove success.
A normal Apple-menu restart was requested after the successful marker. Full
Release loaded identity and runtime validation remain pending after that restart.

## First complete Release desktop boot, 2026-10-25 13:37 UTC

Source6c3568178ba21136b8c21dd45597476c74ec31d1/run40189441511.
Verified loaded core UUID7CAF03F1-3631-33A9-AAAF-581270B665B0 and framebuffer
UUID3C6D0CDD-D9E7-39C8-94FB-D97A47BE3CF6 against LC_UUID in the original CI
Release binaries. Executable/config SHA256 values are recorded in
 evidence/ci/rc1-release-boot-20261025.json. Desktop is visible and the user
reports faster, satisfactory operation. This is one complete Release success.
A bounded204960-byte serial prefix SHA256aa15150cadd5346248af4635b8fb828f652fb7c1ac3ee8ce8637bee8ba414d2b
shows enumeration through channel14, SCSI/APFS root and software-cursor activation;
no captured panic, root wait or cursor conversion failure. Some concurrent boot
lines are interleaved. No per-call EOM traces exist in clean Release: zero trace
lines are not new target/actual CPU validation. SRB STATUS84 messages remain in
the raw capture and are not classified here; do not claim an error-free log.
The preceding restart had no kernel output and guest-requested shutdown18508 at
13:29:32 UTC; preboot timeout remains a hypothesis. A subsequent start at13:32
reached this desktop. Ten-start and sustained Release validation remain open.
Raw console/prefix evidence stays local under the Release test directory.

2026-10-25 18:05 UTC: Direct fresh-install test preparation/Recovery PASS, installation still in progress. Clean Release6c35681/run40189441511, core c97e2919..., EFI config3c08709c...; exact hashes and bounded serial evidence in ci/fresh-install-preparation-20261025.json. See FRESH_INSTALL_TEST.md. Old guest Off/preserved; only new blank target initialized.

2026-10-25 18:20 UTC: fresh-install staged-installer boot PASS as installer only; installation ongoing. Source6c35681/run40189441511 and exact core/config hashes plus both14-channel serial prefixes in ci/fresh-install-phase2-20261025.json. Guest auto-restart, not a host reset. No completed normal desktop yet.

2026-10-25 18:43 UTC: first NORMAL installed-system APFS snapshot boot reached English Setup Assistant. Exact hashes and bounded serial in ci/fresh-install-normal-boot-20261025.json. VMConnect black/direct thumbnail usable; final version, desktop and first framebuffer install still pending. No -nobsdmgroot override, no old system/data migration. GUI automation paused for user interaction.

2026-10-25 18:52 UTC: new local test account created; interactive Apple sign-in is left to user. Correction: automated VMConnect PrintWindow captures were black while direct thumbnails and user field edits demonstrate setup access; no confirmed client rendering defect. No new framebuffer installed yet; desktop acceptance remains pending.

2026-10-25 19:28 UTC: fresh account creation confirmed; final Update Mac Automatically page stalls since approx19:11. Source6c35681/run40189441511, corec97e2919..., config3c08709c...; exact hashes and369479-byte serial prefix SHA82e16488... in ci/fresh-install-setup-stall-20261025.json. No captured panic/root-wait; no new EOM CPU measurement. Non-forced guest shutdown rejected because daemon absent. Command-Q auto-review rejection respected. Guest Running/serial alive; old guest Off. Desktop, sw_vers and first framebuffer install pending; fresh end-to-end result NOT PASS. Cause unresolved, no confirmed new driver bug.

2026-10-25 19:46 UTC: user-authorized hard restart19:40:54 overcame final Setup Assistant stall; first blank-disk Tahoe desktop confirmed19:44. sw_vers26.7.1/25G241, FileVault On, Release core UUID7CAF03F1-3631-33A9-AAAF-581270B665B0 confirmed; no framebuffer yet. Same6c35681/run40189441511/corec97e2919.../config3c08709c.... First guarded private Aux build refused due missing matching KDK; no active kext/collection changed. Raw thumbnails194415/194547/194610/194638/195032 local; fresh first framebuffer install remains pending. No repeat-stability or new EOM CPU-locality claim.

2026-10-25 20:17 UTC: first FULL FRESH RELEASE desktop PASS after canonical Aux-path correction and normal20:07:18 restart; both CI UUIDs and26.7.1/25G241 verified20:12. Exact6c35681/run40189441511/core/FB/config/Aux hashes and198959-byte serial prefix in ci/fresh-install-full-release-20261025.json. All14channels/software cursor; no captured panic/root-wait/cursor-conversion failure. HTTPS200/Safari/Finder/Downloads/mouse short smoke passed. Initial setup required explicitly approved hard restart; stage-path collection did not load FB. Updated combined first installer has not been rerun from a second blank disk. No repeat-boot or new per-call EOM CPU-locality proof. Temporary DVDs ejected/removed; old guest Off, new guest Running, serial alive, all backups retained.

2026-10-25 21:44 UTC: original guest clean reinstall on new512GiB disk underway; prior working pair detached/preserved, original hardware/identity retained. Recovery/all14channels and new blank-target check PASS; Apple installer now downloading, normal system not yet installed. Source6c35681/run40189441511, exact core/config/EFI/rollback hashes and736390-byte prefix SHAe32ecb85... in ci/srv-clean-install-512g-preparation-20261025.json. Keyboard quote mismatch corrected by ABC selection plus volume rename, no repeat erase. Main receiver25588 active. No credential values included.

2026-10-25 21:55 UTC: original guest512GiB install automatically restarted21:53:05 into staged macOS Installer. All14channels again, Apple-logo install; no forced reset. Source6c35681/run40189441511/corec97e2919.../config98608f4e..., Recovery prefix1240009bytes SHAc27f44e9..., staged prefix611464bytes SHA50da9230...; exact records in ci/srv-clean-install-512g-staged-20261025.json. Cryptex52percent is phase only. Normal system/loaded framebuffer still pending.

2026-10-25 22:13 UTC: new512GiB system reached normal APFS root22:11:17 after automatic restore/bootstrap/reboot stages.14channels; no installer/rootdmg args.150824-byte prefix SHA078cdcb9... no panic/root-wait; loginwindow/AppleKeyStore warnings exist. Source6c35681/run40189441511/config98608f4e... unchanged, exact hashes and three prefixes in ci/srv-clean-install-512g-normal-root-20261025.json. GUI/account/loaded UUID/framebuffer not yet confirmed. No host reset.

2026-10-25 22:27 UTC: clean512GiB main guest reached English/Switzerland Setup Assistant; new local account creation completed, no old-data migration. User began personal Apple sign-in; agent inputs and screenshots paused, incidental private auth image DPAPI-protected. Receiver25588/current normal log221117Z active; no auth values published. Same6c35681/run40189441511/config98608f4e.... Final setup/desktop/framebuffer validation pending.

2026-10-26 integrated setup: source efd3cb3, CI40258077483 success; verified ISO d6bd2fb3ae31071e59418b343ac8e885e108b7c0e9be0c4829ba36b33500bef0, all13 files exact. Native display helper verified1920x1080 with expectedFB UUID on prior fresh install. Current installation explicitly authorized for deletion: gracefully Off, exact two detached paths deleted, new blank512GiB and verified rollbackEFI copy attached, protected backups unchanged. Config35dd9dd356dfc9c10466d3f5a9d84d6d9ec98b7d1df8a720b2a2a891b8943806; driver6c35681/run40189441511 unchanged. Serial25588 retained. Recovery seed persistence/full integrated install UNVERIFIED. See Docs/handoff/INTEGRATED_SETUP.md; raw evidence local srv-integrated-install-20261026-01.

2026-10-26 Recovery integration test: initial efd3cb3 Seed failed before copies because shasum absent. Read-only probe proved /sbin/sha256 available. Fixed54e0a98/CI40259471597 success, ISOcc6f9623e6831b2f9e70a087f719a7e0c28c571bd4e04de96e50d02d2b6ce360 exact13files. Reinitialized ONLY verified new512GiB target and Seed completed with allhashesOK/INTEGRATED_SETUP_SEEDED. Apple installation launched. Hypothesis still pending: seed persistence/full automatic1080p. Full provenance evidence/ci/integrated-setup-seed-20261026.json.

2026-10-26 02:45UTC integrated setup54e0a98/run40259471597; unchangeddriver6c/run40189441511, FBd8a079d4..., config35dd9dd3...: installer automatically restarted02:44:19 and reached Apple-logo staged installation. Serial25588 reconnected, bounded617145bytes SHA f34d62265f55e8c6b49ffb1ea8171ac1758e6b5e40da95bc604f5e53c2d100a3; Cryptex46percent phase activity, zero capturedpanic/rootwait. KnownSRBSTATUS84 remains. Evidence evidence/ci/integrated-setup-staged-20261026.json. No reset; seed persistence and firstboot still unverified.

2026-10-26 02:58UTC FAILURE: integrated54e0a98/run40259471597, unchangedcore6c/run40189441511, config35dd9dd3..., FBpayload d8a079d4...: after installer auto starts02:54:09,02:55:37, attempted normalboot02:56:30 panicked in AppleRTC::start+0x2c6, pagefault, uptime1035592178ns, OSversionNotyetset. All14channels registered. Serial23092bytes SHAd01ab4088ad9a9cf43740b68d9868bae93fdcdd5edafd03615ba8e2af5b14202. Setup/backend not shown running before this earlypanic; cause unresolved, not claimed EOMregression or setup-caused. Evidence/ci/integrated-setup-early-rtc-panic-20261026.json. Preserve allstate before unchanged retry.
