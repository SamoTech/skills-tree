---
name: ui-video-tutorial-generation
description: Plan and assemble UI walkthrough videos from recorded interactions with step narration and chapter markers.
metadata:
  source: skills/08-multimodal/ui-video-tutorial-generation.md
  category: 08-multimodal
  version: "v1"
---
# Ui Video Tutorial Generation

## Description
Plan and assemble UI walkthrough videos from recorded interactions with step narration and chapter markers. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires ui video tutorial generation before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for ui video tutorial generation. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the ui video tutorial generation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def chapters(steps, per_chapter):
    return [steps[i:i + per_chapter] for i in range(0, len(steps), per_chapter)]
assert chapters(["a", "b", "c"], 2) == [["a", "b"], ["c"]]
```

## Failure Modes
- Acting outside the declared task boundary.
- Assuming an estimate or preview equals the verified effect.
- Retrying without preserving state or evidence.
- Using stale inputs as if they were current.
- Reporting success without checking the resulting state.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Product teams request generated UI walkthrough videos as a 2026 documentation format. These are dated public signals, not adoption metrics.

## Related
- ui-screencast-analysis.md
- video-description.md
- subtitle-generation.md
