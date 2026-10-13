---
title: "Definition of Done Enforcement"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Encode a task definition of done as checkable criteria and refuse completion claims until every criterion passes with recorded evidence."
added: "2026-10"
version: v1
related: [goal-contract-checking, skill-quality-evaluation, approval-gates]
tags: [completion, verification, gates]
---

# Definition of Done Enforcement

## Description
Encode a task definition of done as checkable criteria and refuse completion claims until every criterion passes with recorded evidence. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a task may only be reported complete when every stated criterion is mechanically satisfied.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for definition of done enforcement work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the definition of done enforcement steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def done_check(criteria, evidence):
    unmet = [c for c, ok in criteria.items() if not ok or c not in evidence]
    return ('done' if not unmet else 'blocked'), unmet

criteria = {'tests_pass': True, 'docs_written': True}
status, unmet = done_check(criteria, {'tests_pass': 'run.log', 'docs_written': 'doc.md'})
assert status == 'done' and unmet == []
status2, unmet2 = done_check(criteria, {'tests_pass': 'run.log'})
assert status2 == 'blocked'
```

## Failure Modes
- Accepting a completion claim without running every criterion.
- Definition of done items that cannot be checked mechanically.
- Changing the criteria after work started without re-approval.
- Marking done on partial evidence for one criterion.
- Skipping criteria that depend on external verification.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Spec-driven 2026 agent workflows push checkable completion criteria over judgment calls; this is a dated signal, not an adoption metric.

## Related
- goal-contract-checking.md
- skill-quality-evaluation.md
- approval-gates.md
