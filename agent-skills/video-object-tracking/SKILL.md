---
name: video-object-tracking
description: Track objects across video frames with re-detection on drift, identity stability checks, and confidence gates before reporting trajectories.
metadata:
  source: skills/08-multimodal/video-object-tracking.md
  category: 08-multimodal
  version: "v1"
---

# Video Object Tracking

## Description
Track objects across video frames with re-detection on drift, identity stability checks, and confidence gates before reporting trajectories. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- objects must be followed across frames and identity switches must be detected.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for video object tracking work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the video object tracking steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def track(frames, conf_gate):
    ids, lost = {}, 0
    for f in frames:
        for det in f:
            if det["conf"] < conf_gate:
                lost += 1
                continue
            ids[det["id"]] = ids.get(det["id"], 0) + 1
    return {"tracked": len(ids), "low_conf": lost}

frames = [[{"id": 1, "conf": 0.9}], [{"id": 1, "conf": 0.2}, {"id": 2, "conf": 0.8}]]
r = track(frames, 0.5)
assert r["tracked"] == 2 and r["low_conf"] == 1
```

## Failure Modes
- Assuming identity survives every occlusion.
- No re-detection after a lost period.
- Reporting trajectories built on low-confidence detections.
- Swapping identities when objects cross.
- No frame-level timestamp alignment.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Video tracking for agent perception is a recurring 2026 multimodal capability request in public coverage; this is a dated signal, not an adoption metric.

## Related
- object-detection.md
- realtime-video-frame-analysis.md
- video-frame-extraction.md
