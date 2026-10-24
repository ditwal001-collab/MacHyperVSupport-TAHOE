# Observations and evidence boundary

Source: pre-existing sibling handoff, read on 2026-10-24. These are reported
observations, not independently verified raw serial logs.

Failing diagnostic:

```text
TAHOE-SYNIC: targetCPU=0 currentCPU=4 pending=1
TAHOE-SYNIC: Writing EOM targetCPU=0 actualCPU=4
```

The handoff associates this with enumeration stopping after channel 1 and
`Still waiting for root device`. The instrumented source can perform exactly
this wrong-CPU write: `ThreadBind` has no intervening scheduler switch.

A separate reported boot reached channels 1 through 14, scan completion,
synthetic SCSI on channel 13, disk enumeration, APFS root, WindowServer and
installer progress. A later boot failed again. Upgrade completion and reliable
release operation have not been established.

The original GraphicsBridge spinlock panic and its improvement with the
startergo baseline are historical reports. The source attribution and ordering
change are verified in local Git; this session performed no graphics runtime
test. No raw log or VM configuration is included in the maintainer package.

## Independently checked after restart

The preserved host serial log was read directly. It contains the reported
target 0 / actual 4 / pending 1 sequence, stops enumeration after channel 1,
and repeatedly reports root-device waiting. The old EFI executable was hashed
and matches the historical diagnostic binary. These checks strengthen the
provenance of that failure without establishing an A/B stability rate.

The candidate built from `0756f1d`, run `40090495930`, passed Debug/Release
builds and Clang analyses. Its first authorized boot used a verified EFI copy
with unchanged OpenCore configuration and only the Monterey executable changed.
The receiver was started before the VM. At 11:54 UTC, 21 captured EOM writes
were target 0 / actual 0, all 14 channels enumerated, SCSI started and APFS root
resolved. No panic or root-device waiting was present. GUI/installer completion
was still pending. See the curated evidence under evidence/ci; raw logs remain
local and are excluded from Git and the maintainer package.
