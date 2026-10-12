---
title: "Video Highlight Detection"
category: 08-multimodal
level: advanced
stability: experimental
description: "Locate the most relevant segments of a video for a stated purpose using transcript and visual signals, returning timestamps with evidence."
added: "2026-10"
version: v1
related: [video-description, video-frame-extraction, audio-transcription]
tags: [video, highlight, detection, multimodal]
---

# Video Highlight Detection

## Description
Locate the most relevant segments of a video for a stated purpose using transcript and visual signals, returning timestamps with evidence. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- Multiple inputs or candidates compete and must be resolved by explicit criteria.
- A wrong intermediate result would propagate into consequential actions.
- The task repeats and benefits from a deterministic procedure.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for video highlight detection. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the video highlight detection procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Video Highlight Detection: deterministic check
allowed = {"idle": {"running"}, "running": {"done", "failed"}, "failed": {"idle"}}

def transition(state, nxt):
    return nxt in allowed.get(state, set())

assert transition("idle", "running")
assert not transition("idle", "done")
print("transitions checked")
```

## Failure Modes
- Proceeding with video highlight detection without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Long-video summarization recurs in 2026 media-agent requests; timestamped evidence is a named requirement. These are dated public signals, not adoption metrics.

## Related
- video-description.md
- video-frame-extraction.md
- audio-transcription.md
