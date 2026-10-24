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
Serial receiver exec session 51796 is running; its actual PID is recorded in
the local test directory's serial/capture-ready.json. It creates unique files
and waits for reconnection. The first boot passed enumeration and APFS root
with 21 matching-CPU EOM writes. Installer/login completion remains pending;
do not interrupt an active upgrade for repeated-boot testing.

Next: keep capturing serial and observe installer/login progress without
interrupting an active upgrade; document the outcome, commit documentation
separately, then perform repeated and clean-release tests when safe. No stable
runtime fix is established by this one instrumented pass.

A separate clean source branch `test/synic-eom-clean-20261024` was pushed.
Functional commit `b9a9719` applies directly to `cd66095f` without added
diagnostics; separate CI commit `da2bd1b` requests a build. Worktree:
`evidence/local-tests/clean-worktree`. Its CI conclusion is not yet retrieved.
Do not confuse that source branch with the active VM's instrumented binary.
