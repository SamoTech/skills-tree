---
title: "Counterfactual Explanation Generation"
category: 02-reasoning
level: advanced
stability: experimental
description: "Produce minimal-change explanations for a decision by identifying which input changes would alter the outcome, and mark them as diagnostic rather than causal proof."
added: "2026-10"
version: v1
related: [counterfactual-reasoning, causal, argument-structure-analysis]
tags: [explanation, xai, reasoning]
---

# Counterfactual Explanation Generation

## Description
Produce minimal-change explanations for a decision by identifying which input changes would alter the outcome, and mark them as diagnostic rather than causal proof. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a decision must be explainable in terms of what would have changed it before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for counterfactual explanation generation work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the counterfactual explanation generation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def minimal_change(inputs, rule):
    for key in sorted(inputs):
        flipped = dict(inputs); flipped[key] = not inputs[key]
        if rule(flipped) != rule(inputs):
            return key
    return None

def admits(x): return x["paid"] and x["verified"]
inputs = {"paid": True, "verified": True}
assert minimal_change(inputs, admits) == "paid"
assert minimal_change({"paid": True}, admits) is None
```

## Failure Modes
- Presenting counterfactuals as causal claims.
- Proposing unrealistic input changes.
- Explaining only correct decisions and never errors.
- Changing multiple inputs when one suffices.
- Skipping the base-outcome check before flipping.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Explainability for automated agent decisions is a recurring 2026 governance topic in public coverage; this is a dated signal, not an adoption metric.

## Related
- counterfactual-reasoning.md
- causal.md
- argument-structure-analysis.md
