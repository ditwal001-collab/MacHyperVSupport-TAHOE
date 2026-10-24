# SynIC EOM CPU locality: candidate correction

Status on 2026-10-24: candidate passes Debug/Release builds and analyses; first
instrumented VM boot passes enumeration through APFS root. Stable runtime fix
unconfirmed. The user subsequently authorized autonomous target-VM tests with
serial capture. The test uses a separate EFI copy; original EFI is preserved.

## Baseline and attribution

The local checkout is non-shallow. Its pre-development history contains 303
reachable commits. The complete reachable commit listing was inspected, with
targeted source/diff review of GraphicsBridge, historical EOM paths, current
VMBus interrupt dispatch, local instrumentation and workflow evolution.
This is not a claim that every line of every historical diff was audited.

`startergo` authored `c48fc5ccade272ec79f633dcb23e45ba1c40d6cc`,
GraphicsBridge: Fix race condition by reordering initialization, with analysis
credited to Qonfused. It allocates the PCI lock for object lifetime and populates
valid PCI configuration before registering with the root bridge and calling
the superclass start. Our SynIC change does not alter GraphicsBridge.
The actual checkout is a descendant baseline, not an exact c48fc5c checkout:
`cd66095f0d6c099f3498522fdf3edbd4825dbb81` also contains subsequent upstream
graphics/VRAM work. Local net changes between c48fc5c and pre-development HEAD
affect only CI, Controller instrumentation and VMBus instrumentation.

Local CI commits `aa887e5` and `377c2b5` adapt the bootstrap to Xcode 16.4 and
system Python and repair YAML indentation. Diagnostics `c14a86c`, `15f8a75`,
`2c43e02` and compile repair `9b80c5f` add VMBus/EOM tracing. The last repair
removed duplicate declarations but left duplicate identical diagnostic lines.
Those pre-existing lines are retained for the instrumented comparison.

Historical commit `26637d7` replaced a private `mp_cpus_call` path with PM
callbacks. The pre-10.6 rendezvous path was retained later for compatibility.
Neither history nor historical successful boots establish the safety of a
modern global rendezvous under workloop gates.

## Defect and ownership

`HyperVController::handleInterrupt` runs on the interrupting CPU and signals
the VMBus management interrupt. `HyperVVMBus::handleDirectInterrupt` records
that CPU through a per-CPU `VMBusInterruptProcessor`. Its IOInterruptEventSource
later invokes `processIncomingVMBusMessage(cpu)` on the shared VMBus workloop.
The workloop's current CPU need not equal the message slot's owner.
Both current `sendSynICEOM` call sites are inside this message-processing path.
The hard interrupt's timer EOM is already CPU-local and is unchanged.

The old modern path clears the target slot, reads pending, tries a global
simple lock, disables interrupts and calls PM `ThreadBind`. It then drops the
lock and writes EOM without a scheduler switch or checked CPU invariant.
It also leaves the workloop's binding changed. Failed lock acquisition can
abandon EOM after clearing the slot.

Apple's PM registration assigns `ThreadBind` to `thread_bind`. The latter sets
affinity and returns the previous binding; migration requires a scheduler
switch. Microsoft defines EOM against the writing virtual processor's queues.
Thus the supplied `targetCPU=0 actualCPU=4 pending=1` is consistent with this
source defect. It does not prove that correcting it resolves all Tahoe stalls.

Primary references consulted:

- [XNU PM callback registration](https://github.com/apple-oss-distributions/xnu/blob/f6217f891ac0bb64f3d375211650a4c1ff8ca1ea/osfmk/i386/pmCPU.c)
- [XNU scheduler binding and switching](https://github.com/apple-oss-distributions/xnu/blob/f6217f891ac0bb64f3d375211650a4c1ff8ca1ea/osfmk/kern/sched_prim.c)
- [PM callback signatures](https://github.com/apple-oss-distributions/xnu/blob/f6217f891ac0bb64f3d375211650a4c1ff8ca1ea/osfmk/i386/pmCPU.h)
- [Hyper-V EOM semantics](https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/tlfs/inter-partition-communication#eom-register)

These public XNU sources inform the design; they do not prove the exact running
Tahoe kernel's binary implementation or exports. Confirm those during build
and target validation.

## Candidate algorithm and context review

Commit `670b352156c0cdd044e9f211577741c1d0f7dfcc` implements:

1. Validate the CPU index before accessing its slot.
2. In the modern branch, require interrupts enabled and a valid processor.
3. Save prior affinity via ThreadBind(target), then call
   `thread_block(THREAD_CONTINUE_NULL)` without a spinlock or disabled interrupts.
4. Disable interrupts and check `cpu_number() == target` before touching the
   slot. On mismatch restore state and preserve the slot for diagnosis.
5. Clear the message type, execute a full memory barrier, then read messagePending.
   If pending, write the CPU-local EOM MSR in the same protected interval.
6. Restore interrupt state and prior affinity on both pending/no-pending paths.
   Diagnostic output uses the CPU sampled at the write and executes after the
   interrupt-disabled interval. It is not a post-restore CPU measurement.

The extra private preemption lock is removed. Migration is done for every
modern acknowledgement, including no-pending cases, avoiding an unprotected
same-CPU fast path. This is simpler but may add scheduler overhead.

The shared workloop serializes management message consumers and holds its gate
across processing. It is a schedulable thread context. The reviewed paths do
not hold an IOSimpleLock across this scheduler switch. Hard interrupt delivery
only queues work; it does not need this gate to schedule the bound workloop.
This avoids a synchronous all-CPU barrier and cross-CPU callback dependency.
Keeping a workloop gate across a scheduler yield still requires runtime review
for latency and external lock interactions. An interrupts-enabled check alone
does not establish general preemption safety; the call-site contract remains
essential. Do not call this API from a new hard interrupt or spinlocked context.

The old pre-10.6 EOM rendezvous remains unchanged except for the common slot
publication barrier. No new modern rendezvous is introduced. The local header
follow-up `ad9a0b3` keeps sched_prim.h out of legacy builds. Its OSAtomic.h
include did not resolve OSMemoryBarrier: both follow-up builds failed.
Inspection of the pinned SDK's OSAtomic.h confirmed that declaration is absent.
Commit `0756f1d` instead uses `__sync_synchronize()` and removes the ineffective
include. This builtin provides the full compiler/CPU fence needed between
publishing the empty slot and reading the pending flag. Compiler support and
absence of a new runtime helper must be verified in the artifacts.
See [the compiler builtin specification](https://gcc.gnu.org/onlinedocs/gcc/_005f_005fsync-Builtins.html).

## Build status and reproducibility

GitHub API verified historical run `40052405899` succeeded for exact source
`9b80c5f39d67a5c9fd76a9765b8302092c2f250f`. The handoff's installed kext hash is
recorded in RESULTS_LOG.md with its evidence limitation. Candidate push started
[run 40087952850](https://github.com/ditwal001-collab/MacHyperVSupport-TAHOE/actions/runs/40087952850).
Inspection after resuming confirmed Build and Analyze Clang FAILED with
`use of undeclared identifier 'OSMemoryBarrier'`. Release work and artifact
upload were skipped. See evidence/ci/40087952850-compiler-error.md.
Coverity is intentionally skipped outside the upstream repository owner.

The permission block after interruption was resolved through targeted
escalations on resume. Header repair `ad9a0b3` started run `40090195466`.
Separate CI adaptation `91a5eb7` started run `40090291711`. Both failed with
the same undeclared barrier; the header-only repair was insufficient.
Compiler full-fence correction `0756f1d` started run `40090495930`, now SUCCESS
for Debug/Release builds and both Clang analyses. Downloaded package and kext
hashes were checked against uploaded provenance. `_thread_block` is imported;
there is no `sync_synchronize` runtime-helper import. This checks the build
result, not target-kernel export compatibility or runtime stability by itself.

| Configuration | Monterey executable SHA256 |
|---|---|
| Debug | `38bf5d6dcc26dd62eb4818086ea6c48505d09880e5919574e7073c922f4ffec9` |
| Release | `b67abe5162028218f87a7a04f4edd8f2239adaf283e35ef7dd8fc7221d69a8f5` |

Runner image `20260824.0482.1`, host macOS 15.7.9, Xcode 16.4 (16F6),
Apple Clang 17.0.0 (clang-1700.0.13.5), SDKs macOS 10.13 and 15.5.
See evidence/ci/run-40090495930.json for package hashes.

Local CI follow-up pins ocbuild `020b14fa68a9825642e0c0fb643c2963bd679ae3`,
MacKernelSDK `3f750085caa17ec3a7880f11c11bf4f48cd6a164`, and the prebuilt Lilu
1.7.2 Debug SDK. Its archive SHA256, confirmed via GitHub release metadata
before interruption, is
`e95df95d82e8b151047abf359ecd9c853755c59293e19dfcc3907da8fbd8cf89`.
The bootstrap's internal ocbuild/master reference is rewritten to that pin.
Build provenance records source, SDK, run, runner image, Xcode, compiler, SDK
list and dependency/output file SHA256 values. The artifact's service digest
must also be saved after upload.

This adaptation changes Lilu's previous moving source build to a known SDK;
it passed the subsequent complete build/analysis run. Action tags, runner image and transitive
downloads still limit repeatability. No bit-for-bit reproducibility is claimed.

## Maintainer package and remaining acceptance

Use the exporter described in REPRODUCE.md. Patch 0003 is the functional source
change relative to pinned diagnostic HEAD `9b80c5f`; its working-tree follow-up
is included and identified. CI and instrumentation remain separate patches.
The exporter emits plain diffs without personal Git author metadata and copies
only the curated report/procedures, never raw logs or machine configuration.
Original startergo attribution remains in this report and the baseline history.
It also exports an alternative clean functional patch directly against the
non-instrumented pinned base, with separate application/content verification.
This is a source export, not a validated release binary.

Local checks passed for all ten multiline workflow shell blocks (`bash -n`),
the provenance shell script, and an execution check that the nested bootstrap
URL substitution uses the pinned revision. The patch series applied in order
and reconstructed the expected normalized working-tree files. Subsequent
Actions execution confirmed the workflow and full compilation/linkage; the
first target boot confirms execution through APFS root. Stability and a clean
release comparison remain unverified. Host policy
rejects unsigned PowerShell scripts; the exporter was run through Python
without modifying the policy.

Before any maintainer publication: retain successful Debug/Release builds and
analyzer results, review target symbol compatibility and all patch contents,
run the approved A/B matrix, remove diagnostic changes for the final release,
and record failures as well as successes. Check processor availability and
latency under load; CPU offlining/hotplug is not handled by this candidate.
Error paths intentionally refuse wrong-CPU writes but do not implement a retry
queue. A failed invariant is a test failure, not graceful recovery.

The maintainable claim today is a source-level CPU-affinity correction
candidate with one successful instrumented runtime observation. There is no
confirmed stable fix for intermittent Tahoe boot enumeration.

## First authorized runtime observation

The target VM was Off. The original EFI VHDX and a new test copy had identical
SHA256 before modification. The previous installed executable matched the
historical diagnostic hash. Only the Monterey executable changed in the test
EFI; the OpenCore configuration and every other file remained identical.
The original EFI and system disk were not modified offline. The test EFI was
unmounted from the host, attached at the original SCSI location, and the serial
receiver was started before the VM. It preserves unique files and reconnects
across guest restarts.

At 11:54 UTC the first boot had 21 logged EOM writes, all target 0 / actual 0,
channels 1–14, completed VMBus scan, started SCSI controller and APFS root.
No root-device waiting or panic occurred in that observed interval. The guest
had reached launchd; GUI and installer completion were not yet established.
Full raw logs remain local. Curated excerpts and exact source/build/kext/EFI
hashes are in evidence/ci/boot-01-0756f1d.json and its sanitized companion.
By 11:56 UTC, launchd reported WindowServer running and OSInstaller invoked
its progress UI. Storage I/O continued in serial output. This establishes
installer-process activity, not completion of the upgrade or a usable login.
Repeated trials and a clean release comparison remain mandatory before a
stability claim. Do not force additional boots while an upgrade is active.
