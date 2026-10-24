# Separate VMConnect refresh investigation

## Opt-in software cursor comparison candidate

Branch test/tahoe-software-cursor, c9eb980daab9598b1af6732217147490dacceb3e,
based on e170982, adds a framebuffer-local bool read from -hvgfxfbswcursor before
super::start. getAttribute(kIOHardwareCursorAttribute) returns zero only with that
flag; all other behavior remains unchanged. This tests removal of hardware cursor
conversion/visibility transitions, without enlarging protocol messages or changing
SynIC or mouse input. Existing flushCursor sends the transparent host shape.
Apple documents IOFramebuffer software rendering when hardware cursor unavailable:
https://github.com/apple-oss-distributions/IOGraphics/blob/main/IOGraphicsFamily/IOKit/graphics/IOFramebuffer.h
CI40139181101 started. Not installed/runtime tested. Loaded framebuffer identity
and a supported installation path still need verification; no security bypass.

## More precise user reproduction, 2026-10-25 local

In VMConnect, clicking Downloads in Finder makes the pointer disappear before
opening the Jump Desktop DMG. Three or four fast mouse movements restore it
briefly. Jump Desktop is not yet a tested alternate viewer. This is user-reported,
not independently instrumented. Cursor shape/visibility refresh and conversion
remain hypotheses; do not describe input loss or a confirmed fix. Preserve this
sequence for a cursor-specific comparison after loaded-module identification.

## Restart follow-up, 22:22 UTC

User initiated restart. The previously empty serial log has now populated with
the prior boot and orderly shutdown: 22 EOM writes all on matching CPUs, 59
hardware cursor conversion failures, no panic/root-wait marker. Thus current
data strengthens a cursor-conversion hypothesis, but does not prove disappearance
causality. Delayed output/visibility cause is unknown. Receiver reconnected;
new reboot is at local pre-kernel unlock. See latest RESULTS_LOG/UNATTENDED.

## Latest user test, 2026-10-25 local / 2026-10-24 22:20 UTC

User reports mouse movement is now fast, but the black pointer disappears after
a short time. This is a reported performance improvement, not a confirmed complete
cursor fix. Read-only VMConnect capture shows a full macOS desktop with open apps;
runtime OS version and loaded framebuffer binary remain unverified. No guest input,
restart, disk change or cursor code modification was performed for this observation.
Prepared candidate remains e170982/run40124452997 (33 ms), executable
803a3d24f6312ce53f1b7385321c37e1a14e28d5c413620634243f821e60c888,
config32be11f98247242f8e1534076817825cae2fa79b235ce289b179ec59e39caf8f.
Host reports Running. Receiver PID48800 is alive with the expected command line,
but its latest serial file is still zero bytes: no current-boot SynIC validation
can be inferred. Raw screenshot stays private under local-tests.

Source inspection confirms setCursorImage advertises a 32x32 descriptor and returns
Unsupported on conversion failure. Prior boots had conversion failures. A transition
to an unsupported cursor image is a hypothesis for disappearance, not established
causality. Identify the actual loaded framebuffer and restore serial evidence
before a cursor-specific comparison; do not blindly enlarge the protocol buffer
or replace an unrelated core binary. Preserve the current interactive user session.

## Verified problem and scope correction

The 0756f1d SynIC candidate reached a normal password login framebuffer, but
direct Hyper-V thumbnails did not establish a usable VMConnect console. The user
reported an unreadable screen, missing apparent keyboard response and no visible
password-field focus. At 19:01 UTC, the direct framebuffer showed 12:01 and changed
masked input while VMConnect remained at 11:57. A console reconnect refreshed it
once, then the visible image again became stale. Mouse/keyboard input had reached
the guest even when the client did not display its effects.

Private desktop capture also needed per-process DPI awareness: its old virtual
rectangle could crop/misrender the DirectX child. The helper now requests physical
pixels. This is a capture-process change, not a global host DPI setting. Neither
an anomalous PrintWindow image nor a fresh WMI preview alone proves the state of
the interactive client. User feedback and both paths must be considered.

## Isolated refresh correction

Source `3d31e1107d097f2a3eee4683e89d7d8678a76708`, branch
`fix/tahoe-display-refresh`, applies ONLY the seven-line handleRefreshTimer hunk
from startergo commit `3454a80ef6d6e26a3afcdd38a512c559586bd2ba`. Original author
and author date were retained. The unrelated VRAM/GraphicsBridge changes were
not imported. SynIC/Controller/VMBus source equals the 0756f1d candidate.

The timer previously called refreshFramebufferImage(), which returns immediately
when no dirty flag is set. Ordinary framebuffer writes did not reliably mark the
image dirty. The new markFullScreenDirty() call before refresh provides a bounded
timer-driven correctness fallback. Feature-change reconnects already marked a
full frame, consistent with the observed one-time refresh after reconnect.

Actions `40101047189` passed Debug/Release builds and Clang analyses. Downloaded
hashes independently match provenance; Debug Monterey executable SHA256:
`39219543142986a6485ea2ae05a15a4c34e017946a45f40a2106466520a840a8`.
Package SHA256:
`72353ed0dcfc059f8fe7b36b666a48323780883a84cd3b3ac99ca1a4bd4ae431`.

## Runtime test and preservation

The guest was gracefully shut down through its WMI-observed native login power
menu. Host Off was confirmed. A new exclusive EFI copy was created and hash
checked, host-mounted only while detached/Off, then only the Monterey executable
was replaced. Info.plist compared equal and config was unchanged:
`32be11f98247242f8e1534076817825cae2fa79b235ce289b179ec59e39caf8f`.
The source executable and all prior EFI variants remain preserved. The original
system disk and protected backups were not changed.

Boot began at 19:06:40 UTC. Darwin 25.6.0, all 14 channels and 15 fully parseable
matching-CPU EOM writes were captured, with no panic/root-wait marker. The user
reported input now working, and VMConnect showed post-login Setup Assistant
(Analytics), rather than a stale login image. See evidence/ci/display-01-3d31e11.json
for prefix hashes, exact inputs and evidence boundaries. This is one observed
refresh correction, not release-stability acceptance or proof of completed setup.

An additional earlier boot at 18:50 was present in the reconnect capture: Darwin
25.6.0, all 14 channels, 24 matching-CPU EOM writes. Its initiator was not inferred.

## Remaining pointer-performance investigation

After input/display recovered, the user reported slow mouse movement. Observed:
1920x1080x32 display, VM CPUUsage sampled at 13%, cursor-conversion failures in
serial. The current timer interval is 10 ms: up to 100 full-frame update requests
per second. These facts motivate, but do not prove, a rendering-latency hypothesis.
The cause may also involve hardware cursor conversion; the current descriptor
limit is 32x32. No arbitrary cursor-size/protocol change has been made.

Separate branch `fix/tahoe-refresh-pacing`, commit
`e17098263de44ac71251bcd31caea999e050221e`, changes only the refresh interval
from 10 to 33 ms (approximately 30 Hz). Run `40124452997` is the comparison build.
Debug/Release and Clang analyses passed; hashes are independently verified in
evidence/ci/run-40124452997-verified.json. Another exclusive EFI copy was prepared
with only its executable changed, preserving the same config and previous image.
The prior copy-only run was interrupted after Setup Assistant remained in a
processing pane and regular exit/navigation/lock/quit attempts did not provide
a graceful exit. That interruption and possible journal/state effects are logged;
it is not a successful completion of setup.

The new boot at 19:39:24 UTC waits at a native pre-kernel password/unlock screen.
No new kernel serial output is present; the candidate is staged but not runtime
validated. Local user entry is required. SynIC, mouse input handling and cursor
code remain unchanged. Do not label this a confirmed mouse fix before comparison.
See evidence/ci/display-02-pacing-pending.json. The cursor diagnostic text is not
present in the inspected Monterey binary; the separately loaded framebuffer
module's actual binary/version still needs guest inspection.

At the final state check the VM was Off and the new kernel log remained empty.
The intervening poweroff cause is not established. Preserve that state; local
start/unlock plus receiver verification is needed before continuing the comparison.
No mouse improvement is claimed by the successful compiler/build result.

Active EFI: ignored local `display-pacing-test-20261024-01/EFI.refresh-pacing.vhdx`
at SCSI 0:0. Same System.test.vhdx remains at SCSI 0:1. Never move/delete these
attached files. Operational details are in UNATTENDED.md and local context JSON.
