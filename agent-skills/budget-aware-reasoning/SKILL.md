---
name: budget-aware-reasoning
description: Choose reasoning depth and verification effort under explicit time, token, and cost budgets, and record when the budget forced a lower-confidence answer.
metadata:
  source: skills/02-reasoning/budget-aware-reasoning.md
  category: 02-reasoning
  version: "v1"
---

# Budget-Aware Reasoning

## Description
Choose reasoning depth and verification effort under explicit time, token, and cost budgets, and record when the budget forced a lower-confidence answer. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- an answer must be produced within a stated time, token, or cost budget before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for budget aware reasoning work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the budget aware reasoning steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def plan_effort(budget_tokens, base=200, extra=150):
    depth = 1
    while base + depth * extra <= budget_tokens:
        depth += 1
    return depth, base + (depth - 1) * extra

depth, used = plan_effort(700)
assert depth == 4 and used == 650
assert plan_effort(100)[0] == 1  # minimal depth, recorded honestly
```

## Failure Modes
- Spending the whole budget with no answer to show.
- Hiding that a low-confidence answer came from a budget cut.
- Ignoring budget in the first reasoning pass.
- Treating the budget as a target to spend.
- Forgetting to report remaining budget to the caller.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Token and cost budgets for reasoning are a top recurring 2026 agent-cost topic in public developer discussion; this is a dated signal, not an adoption metric.

## Related
- resource-allocation.md
- cost-benefit-analysis.md
- satisficing-decision-making.md
