# Candidate build failure: run 40087952850

Verified on 2026-10-24 using `gh run view --json status,conclusion,jobs` and
`--log-failed`. Source: `670b352156c0cdd044e9f211577741c1d0f7dfcc`.
Both Build and Analyze Clang failed. Release build/analyze and artifact upload
were skipped. The build command exited with code 65.

Sanitized exact compiler diagnostic (workspace prefix removed):

```text
MacHyperVSupport/Controller/HyperVControllerInterrupts.cpp:356:3: error: use of undeclared identifier 'OSMemoryBarrier'
  356 |   OSMemoryBarrier();
      |   ^
```

The same diagnostic appears in both jobs. Commit
`ad9a0b3b7a06bf842e263f4cde610fc0d8c139c1` explicitly includes
`libkern/OSAtomic.h` and limits the scheduler header to modern targets.
The compiler correction needs confirmation in the subsequent run.
This result concerns compilation, not CPU locality or boot stability.
