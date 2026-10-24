# SynIC EOM patch plan

1. Preserve the baseline and all startergo GraphicsBridge attribution.
2. Isolate functional EOM work on `fix/synic-eom-cpu-affinity`.
3. Use the existing PM callbacks in schedulable VMBus workloop context:
   bind, switch, disable interrupts, verify CPU, clear slot, memory barrier,
   inspect pending, write EOM if needed, restore interrupts and prior affinity.
4. Retain the old pre-10.6 rendezvous branch; do not reuse it for modern EOM.
5. Keep CI/provenance adaptations and diagnostic changes separate from the fix.
6. Build Debug and Release and run the existing Clang analyzer. Verify
   `thread_block` import/export compatibility, including the legacy targets.
7. Only after explicit VM authorization, compare identical diagnostic variants,
   then a clean release candidate. Record every attempt and all hashes.

Implemented candidate: `670b352`; committed follow-up `ad9a0b3` confines the
scheduler header to modern targets. OSMemoryBarrier remained undeclared after
that header repair; `0756f1d` now uses the compiler full-fence builtin
`__sync_synchronize()` and removes the ineffective OSAtomic include.
Run `40090495930` passed Debug/Release builds and analyses. Clean source run
`40093339256` also passed and downloaded package/executable hashes match
provenance (evidence/ci/run-40093339256-verified.json); it is not runtime tested.
See the report for remaining
risks, exact ancestry, patch export and acceptance criteria.
