---
name: gui-agent-step-verification
description: Verify each GUI agent step against the expected postcondition screenshot or state before continuing.
metadata:
  source: skills/10-computer-use/gui-agent-step-verification.md
  category: 10-computer-use
  version: "v1"
---

# Gui Agent Step Verification

## Description
Verify each GUI agent step against the expected postcondition screenshot or state before continuing. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires gui agent step verification before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for gui agent step verification. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the gui agent step verification steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def step_ok(expected_widget, observed):
    return expected_widget in observed
assert step_ok("save_button", ["menu", "save_button"]) is True
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
GUI agent reliability requests in 2026 center on per-step verification instead of blind action sequences. These are dated public signals, not adoption metrics.

## Related
- action-result-verification.md
- screenshot-capture.md
- mouse-input.md
