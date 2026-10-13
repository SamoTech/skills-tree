---
name: weighted-scoring-model-design
description: Build transparent weighted scoring for comparing options, justify weights from evidence, and expose the model so a reviewer can recompute every ranking.
metadata:
  source: skills/02-reasoning/weighted-scoring-model-design.md
  category: 02-reasoning
  version: "v1"
---

# Weighted Scoring Model Design

## Description
Build transparent weighted scoring for comparing options, justify weights from evidence, and expose the model so a reviewer can recompute every ranking. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- options must be compared with a reproducible, inspectable scoring model before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for weighted scoring model design work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the weighted scoring model design steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def score(option, weights):
    return sum(weights[k] * v for k, v in option.items() if k in weights)

def rank(options, weights):
    return sorted(options, key=lambda o: -score(o, weights))

weights = {"speed": 0.7, "cost": 0.3}
opts = [{"speed": 5, "cost": 2}, {"speed": 2, "cost": 5}]
ranked = rank(opts, weights)
assert ranked[0]["speed"] == 5
assert abs(score(ranked[0], weights) - 4.1) < 1e-9
```

## Failure Modes
- Choosing weights without stated justification.
- Hiding the model so rankings cannot be audited.
- Scoring criteria that double-count the same factor.
- Tweaking weights until a preferred option wins.
- Failing to document score ties.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Transparent, auditable comparisons are a recurring 2026 evaluation request for agent decision support; this is a dated signal, not an adoption metric.

## Related
- pareto-analysis.md
- multi-objective-optimization.md
- trade-off-analysis.md
