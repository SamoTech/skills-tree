---
name: milestone-commitment-tracking
description: Record the concrete commitments an agent makes mid-task, track each against deadlines and acceptance criteria, and escalate on breach.
metadata:
  source: skills/09-agentic-patterns/milestone-commitment-tracking.md
  category: 09-agentic-patterns
  version: "v1"
---

# Milestone Commitment Tracking

## Description
Record the concrete commitments an agent makes mid-task, track each against deadlines and acceptance criteria, and escalate on breach. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- an agent makes mid-task promises whose later breach must be caught and escalated with evidence.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for milestone commitment tracking work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the milestone commitment tracking steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def check_commitments(commitments, now):
    breached = [c['name'] for c in commitments if now > c['due'] and not c['done']]
    return breached

b = check_commitments(
    [{'name': 'draft', 'due': 5, 'done': True}, {'name': 'review', 'due': 3, 'done': False}], 4)
assert b == ['review']
```

## Failure Modes
- Letting an agent quietly drop a commitment it already made.
- Recording commitments without acceptance criteria.
- Escalating a breach without evidence of the original promise.
- Tracking only deadlines and not scope commitments.
- Treating a renegotiated commitment as met without re-checking.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Commitment ledgers with breach handling appear in 2026 long-horizon agent guidance; this is a dated signal, not an adoption metric.

## Related
- interruptible-agent-flows.md
- agent-halt-conditions.md
- goal-contract-checking.md
