# Tahoe SynIC development handoff

Read [the technical report](Docs/handoff/SYNIC_EOM_REPORT.md),
[observations](evidence/OBSERVATIONS.md), [results](evidence/RESULTS_LOG.md),
[patch plan](PATCH_PLAN.md), and [reproduction procedure](REPRODUCE.md).

Development branch: `fix/synic-eom-cpu-affinity`.
Functional candidate: `670b352156c0cdd044e9f211577741c1d0f7dfcc`.
Run `40087952850` FAILED: OSMemoryBarrier was undeclared (see the sanitized
diagnostic in evidence/ci). Header repair `ad9a0b3` was pushed and started run
`40090195466`. Separate CI/provenance commit `91a5eb7` was pushed and started
run `40090291711`. Both follow-up runs FAILED with the same undeclared barrier.
Compiler full-fence repair `0756f1d` replaces the unavailable API with
`__sync_synchronize()` and started run `40090495930`, now SUCCESS for both
Debug/Release builds and analyses. Downloaded package and kext hashes match
CI provenance; see evidence/ci/run-40090495930.json.
Git/network operations work through targeted escalations after the restart.
The user authorized Git/gh development commands without repeated questions.
Documentation/export baseline `c3d417b` is committed and pushed; inspect the
actual Git status for newer observations. Existing .bak files must not be staged.

The original handoff was found in the sibling `../HANDOFF` directory, not in
`docs/handoff`. Its reported boot observations have not been independently
reproduced. Private machine paths and raw logs were not imported.

The user explicitly authorized autonomous Hyper-V/VM test steps after restart
and required serial logging. This authorization is confined to srv-maos-devs11.
The VM was Off. A new, hash-verified EFI copy was created in
`evidence/local-tests/vm-test-0756f1d-20261024-01/EFI.test.vhdx`; only its Monterey
executable was replaced, with original kext backed up. The original EFI VHDX
and protected Sequoia backup are unchanged. The test image is now attached at
SCSI 0:0 and the VM is RUNNING. Do not delete/move this ignored image while
attached. No direct offline write was made to the system VHDX.
The original foreground receiver (exec session 51796) ended. There is a serial
coverage gap from 12:34:13.99 to 12:36:24.48 UTC; do not claim complete upgrade
coverage or absence of errors during that interval. A separate hidden process
was started via Start-Process; Python PID 46464 is recorded in the local test
directory's serial-reconnect-02/capture-ready.json. It is connected and writing
new data. Inspect actual process/file liveness rather than assuming that a
foreground tool session survives a completed assistant turn.
Both directories preserve unique files and support reconnects. The first boot passed enumeration and APFS root
with 21 matching-CPU EOM writes. Installer/login completion remains pending;
do not interrupt an active upgrade for repeated-boot testing.
At 12:27 UTC the same boot was still emitting serial storage traffic, with
about 79 MiB captured, no new boot, and no SynIC/root-wait/panic failure.
Upgrade completion remains UNKNOWN; do not infer completion from installer UI
process activity or treat active I/O alone as a progress percentage.

Next: keep capturing serial and observe installer/login progress without
interrupting an active upgrade; document the outcome, commit documentation
separately, then perform repeated and clean-release tests when safe. No stable
runtime fix is established by this one instrumented pass.

The first clean source branch `test/synic-eom-clean-20261024` (b9a9719/da2bd1b)
is SUPERSEDED: it mistakenly used cd66095f rather than the actual c48fc5c base
of the tested development line. Its worktree remains preserved under
`evidence/local-tests/clean-worktree`; do not use it for an isolated comparison.
The exporter is corrected to c48fc5c and checks for unexported baseline changes.
Earlier package ZIPs declaring cd66095f as base are superseded. None of this
changes the active VM's instrumented binary or its source provenance.
Corrected clean branch `test/synic-eom-clean-c48fc5c` is pushed: functional
commit `7a3b98a`, CI head `c960997`. Worktree is
`evidence/local-tests/clean-c48-worktree`. Its CI conclusion is unverified.
Graphics/framebuffer/packaging match the instrumented tested baseline exactly.

Second captured boot: new serial connection at 13:21:34 UTC after the user
reported booting. By 13:24 UTC it again enumerated all 14 channels, completed
scan, started SCSI and resolved APFS root; 16 logged EOM writes matched CPU 0,
with no captured panic/root wait. WindowServer was spawned. Receiver PID 46464
automatically reconnected into a new file under serial-reconnect-02. See
evidence/ci/boot-02-0756f1d.json. Full installer/login completion is still not
established; two observed passes do not establish release stability.
IMPORTANT environment correction: the second boot is Sequoia Recovery,
Darwin 24.4.0; user sees "Reinstall macOS Sequoia". The first was Darwin
25.6.0 in Tahoe's installer environment. Do not count the Recovery boot as a
second Tahoe boot or an upgrade success. Do not choose Sequoia reinstall.
