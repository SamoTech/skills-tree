---
title: "Action Journaling"
category: 04-action-execution
level: advanced
stability: experimental
description: "Record every action in a write-ahead journal with inputs, outputs, and reversal notes, and use the journal to reconstruct or undo state after failures."
added: "2026-10"
version: v1
related: [action-result-verification, compensating-actions, idempotent-retries]
tags: [journaling, recovery, reliability]
---

# Action Journaling

## Description
Record every action in a write-ahead journal with inputs, outputs, and reversal notes, and use the journal to reconstruct or undo state after failures. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- actions must be reconstructible and reversible after a partial failure before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for action journaling work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the action journaling steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def replay(journal, state):
    for entry in journal:
        state = entry["apply"](state)
    return state

journal = [{"apply": lambda s: s + 1}, {"apply": lambda s: s * 2}]
assert replay(journal, 3) == 8
journal2 = [{"apply": lambda s: s + 1}]
assert replay(journal2, 3) == 4  # partial journal replays to a consistent prefix state
```

## Failure Modes
- Journaling after the action instead of before.
- Recording inputs without enough context to reverse.
- Never testing replay on a clean state.
- Journaling to the same store the actions modify.
- Removing entries once actions complete.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Recoverable agent execution is a recurring 2026 reliability pattern, including durable-execution guarantees in public framework coverage; this is a dated signal, not an adoption metric.

## Related
- action-result-verification.md
- compensating-actions.md
- idempotent-retries.md
