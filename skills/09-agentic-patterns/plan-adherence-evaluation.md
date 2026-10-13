---
title: "Plan Adherence Evaluation"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Measure how faithfully an executed trajectory followed the approved plan and report deviations with evidence instead of judging by outcome alone."
added: "2026-10"
version: v1
related: [plan-and-execute, trajectory-analysis, goal-contract-checking]
tags: [evaluation, planning, traceability]
---

# Plan Adherence Evaluation

## Description
Measure how faithfully an executed trajectory followed the approved plan and report deviations with evidence instead of judging by outcome alone. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a plan was approved before execution and stakeholders need to know whether the result came from the planned path.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for plan adherence evaluation work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the plan adherence evaluation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def adherence(planned, executed):
    deviated = [i for i, (p, e) in enumerate(zip(planned, executed)) if p != e]
    return 1.0 - len(deviated) / max(len(planned), 1), deviated

score, dev = adherence(['fetch', 'parse', 'store'], ['fetch', 'skip', 'store'])
assert dev == [1] and score < 1.0
print(score, dev)
```

## Failure Modes
- Judging adherence by end state while ignoring substituted steps.
- Treating documented, approved plan changes as violations.
- Scoring partial matches without recording which steps diverged.
- Evaluating against a stale version of the plan.
- Reporting a single percentage with no deviation list.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
2026 agent-operations coverage asks for trajectory-versus-plan audits on long-horizon runs; this is a dated signal, not an adoption metric.

## Related
- plan-and-execute.md
- trajectory-analysis.md
- goal-contract-checking.md
