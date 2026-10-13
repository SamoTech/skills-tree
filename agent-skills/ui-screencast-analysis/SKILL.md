---
name: ui-screencast-analysis
description: Analyze UI screencasts into step-by-step interaction sequences with frame timestamps, UI element references, and verification of each observed transition.
metadata:
  source: skills/08-multimodal/ui-screencast-analysis.md
  category: 08-multimodal
  version: "v1"
---

# UI Screencast Analysis

## Description
Analyze UI screencasts into step-by-step interaction sequences with frame timestamps, UI element references, and verification of each observed transition. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a recorded UI session must be turned into reproducible steps an agent can replay.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for ui screencast analysis work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the ui screencast analysis steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def steps(frames):
    out = []
    for f in frames:
        if f["state"] != (out[-1]["state"] if out else None):
            out.append({"t": f["t"], "state": f["state"]})
    return out

fs = [{"t": 0, "state": "menu"}, {"t": 1, "state": "menu"}, {"t": 2, "state": "form"}]
assert [s["state"] for s in steps(fs)] == ["menu", "form"]
```

## Failure Modes
- Describing frames without timestamps.
- Inferring clicks that were never visible.
- Skipping occluded loading states as no-ops.
- No verification that consecutive steps are reachable.
- Hardcoding resolutions so other viewports break.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Screencast-derived UI automation is a recurring 2026 computer-use request in public developer discussion; this is a dated signal, not an adoption metric.

## Related
- screenshot-to-code.md
- document-layout-analysis.md
- video-description.md
