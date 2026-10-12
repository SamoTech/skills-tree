---
title: "Screen Recording"
category: 10-computer-use
level: basic
stability: experimental
description: "Capture screen activity as video with deterministic region selection, frame pacing, and encoding, for task evidence and UI debugging, with explicit consent and retention handling for sensitive content."
added: "2026-10"
version: v1
related: ["screenshot-capture","visual-element-detection"]
---

# Screen Recording

Category: Computer Use | Level: basic | Stability: experimental | Version: v1

## Description

A screen recording turns transient UI behavior into reviewable evidence: a bug reproduces, a procedure demonstrates itself, a session leaves an audit trail. The mechanics are region selection, steady frame pacing, and reliable encoding; the judgment is what must never be in the frame and what happens to the file afterward.

## When to Use

Use to reproduce a UI defect with full context, record a procedure for later replay, or produce task evidence of an automated desktop session.

Do not record covertly, and do not record sessions likely to contain credentials or personal input without an explicit policy permitting it.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `region` | `enum` | No | `full`, `window`, or explicit rectangle (default `full`) |
| `duration` | `int` | Yes | Maximum recording length in seconds |
| `fps` | `int` | No | Frames per second (default 15; 30 for fast motion) |

## Procedure

1. Determine the capture scope; map logical coordinates to the physical monitor and DPI so the region is what you think it is.
2. Check consent and policy: close or exclude windows that may contain secrets or personal data before capture starts.
3. Configure deterministic pacing and a hard frame budget derived from duration and fps.
4. Capture; if the region moves (window drag), re-anchor or fail loudly rather than silently record the wrong area.
5. Encode with a standard codec, record a checksum, and write metadata (region, fps, duration, host).
6. Verify the result covers the intended interval before reporting success.

## Outputs

| Output | Type | Description |
|---|---|---|
| `video_file` | `file` | The encoded recording |
| `metadata` | `object` | Region, fps, duration, codec, capture host |
| `checksum` | `string` | Integrity digest for the evidence chain |

## Runnable Example

```python
def frame_budget(duration, fps=15, max_frames=4500):
    return min(int(duration * fps), max_frames)

def plan(region, duration, fps=15):
    return {"region": region, "frames": frame_budget(duration, fps), "bounded": duration * fps <= 4500}

print(plan("window", 60))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Secrets in frame | Password field or message visible during capture | Pre-capture window exclusion; post-capture review |
| Jerky replay | Variable frame pacing under load | Fixed fps with drop policy, not best-effort |
| Wrong region | Multi-monitor or DPI mismatch | Map coordinates explicitly before capture |
| Unbounded capture | No duration ceiling; disk fills | Hard frame budget and duration cap |
| Unverifiable evidence | File mutated after the fact | Checksum at write time; store with the artifact |

## Security and Authority Boundary

Screen recordings can contain credentials, personal data, and confidential documents. Record only what policy and consent permit, store with retention limits, restrict access, and treat the recording as sensitive until reviewed. Recordings of a user's screen without their knowledge are prohibited.

## Evidence

This skill is grounded in dated public implementation references:

1. The FFmpeg multimedia framework used for capture pipelines (https://ffmpeg.org/).
2. The OpenCV computer vision library with video capture and writer support (https://github.com/opencv/opencv).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Screenshot Capture](screenshot-capture.md) — the single-frame counterpart for static evidence.
- [Visual Element Detection](visual-element-detection.md) — locating the elements the recording should follow.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
