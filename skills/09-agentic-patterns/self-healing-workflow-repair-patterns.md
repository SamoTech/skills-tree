---
title: "Self-Healing Workflow Repair Patterns"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Detect and repair failed workflow steps with bounded retries and fallback paths so that recovery is declared in the design rather than improvised."
added: "2026-10"
version: v1
related: [self-correction, agent-checkpoint-restore-patterns]
tags: [self-healing, recovery, workflows, reliability]
---
# Self-Healing Workflow Repair Patterns

## Description
Detect and repair failed workflow steps with bounded retries and fallback paths so that recovery is declared in the design rather than improvised. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A workflow must recover from transient step failure without operator intervention and without masking real defects.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Classify each failure by declared repair class, apply only the repair bound to that class, and escalate on record when the repair budget is exhausted instead of looping.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def repair(failure, budget):
    if failure["class"] == "transient" and budget["retries"] < 2:
        return "retry"
    if failure["class"] == "schema_drift":
        return "fallback_path"
    return "escalate"
assert repair({"class": "transient"}, {"retries": 0}) == "retry"
assert repair({"class": "permanent"}, {"retries": 0}) == "escalate"
```

## Failure Modes
- Every failure is classed transient and retried, masking permanent defects as flakiness.
- Repair retries share state and re-execute side effects that already landed.
- The fallback path is declared but never tested, so invocation day is its first exercise.
- Repair budget exhaustion escalates silently without a failure record for the operator.
- A repair widens step permissions to work around the failure, converting a bug into a standing risk.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 observability guidance treats automated recovery of acting-agent failures as a core reliability practice (futransolutions.com, dated October 2026) ([public signal](https://futransolutions.com/blog/ai-agent-observability-in-2026-how-to-trace-evaluate-and-debug-ai-that-takes-action/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Self-Correction](../02-reasoning/self-correction.md)
- [Agent Checkpoint Restore Patterns](../09-agentic-patterns/agent-checkpoint-restore-patterns.md)

## Changelog
| Version | Date | Notes |
|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
