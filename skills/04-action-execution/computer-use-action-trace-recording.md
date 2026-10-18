---
title: "Computer Use Action Trace Recording"
category: 04-action-execution
level: advanced
stability: experimental
description: "Record computer-use actions as a replayable trace with action, target, and before and after state digests so any execution can be audited step by step."
added: "2026-10"
version: v1
related: [gui-agent-test-grid-provisioning, gui-grounding-coordinate-verification]
tags: [tracing, audit, computer-use]
---
# Computer Use Action Trace Recording

## Description
Record computer-use actions as a replayable trace with action, target, and before and after state digests so any execution can be audited step by step. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A computer-use action failed and the audit needs a step-by-step replayable record.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | computer use action trace recording task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the computer use action trace recording steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A replayable action trace with per-step before and after state digests. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def trace_step(action, target, before, after):
    return {"action": action, "target": target, "state_changed": before != after}
s = trace_step("click", "#submit", "form:invalid", "form:submitted")
assert s["state_changed"] is True
```

## Failure Modes
- Acting outside the declared task boundary.
- Recording actions without before or after state, making steps unreplayable.
- Truncating the trace so the failure context is lost.
- Logging secret values captured between screenshots into the trace.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Action trace recording for computer use is exercised by the UI-TARS desktop-agent action model. ([public signal](https://github.com/bytedance/UI-TARS))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Gui Agent Test Grid Provisioning](../10-computer-use/gui-agent-test-grid-provisioning.md)
- [Gui Grounding Coordinate Verification](../01-perception/gui-grounding-coordinate-verification.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
