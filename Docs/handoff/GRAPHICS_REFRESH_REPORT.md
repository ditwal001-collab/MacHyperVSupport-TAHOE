# Separate VMConnect refresh investigation

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

Active EFI: ignored local `display-pacing-test-20261024-01/EFI.refresh-pacing.vhdx`
at SCSI 0:0. Same System.test.vhdx remains at SCSI 0:1. Never move/delete these
attached files. Operational details are in UNATTENDED.md and local context JSON.
