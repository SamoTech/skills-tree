---
name: context-window-budget-planning
description: Plan token budgets across system prompt, retrieved context, tool outputs, and working state so a conversation stays within its window.
metadata:
  source: skills/03-memory/context-window-budget-planning.md
  category: 03-memory
  version: "v1"
---

# Context Window Budget Planning

## Description
Plan token budgets across system prompt, retrieved context, tool outputs, and working state so a conversation stays within its window. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires context window budget planning before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for context window budget planning. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the context window budget planning steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def fits(system, tools, history, limit):
    return system + tools + history <= limit
assert fits(100, 200, 300, 600) is True
assert fits(100, 200, 400, 600) is False
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
Context engineering is named a core 2026 agent-building skill in practitioner trend surveys. These are dated public signals, not adoption metrics.

## Related
- long-context-curation.md
- context-compaction.md
- memory-indexing.md
