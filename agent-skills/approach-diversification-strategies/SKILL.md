---
name: approach-diversification-strategies
description: Force genuinely different solution approaches before committing, and reject near-identical candidates dressed up as diversity.
metadata:
  source: skills/09-agentic-patterns/approach-diversification-strategies.md
  category: 09-agentic-patterns
  version: "v1"
---

# Approach Diversification Strategies

## Description
Force genuinely different solution approaches before committing, and reject near-identical candidates dressed up as diversity. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a decision would benefit from comparing structurally different candidate approaches.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for approach diversification strategies work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the approach diversification strategies steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def diversity(candidates):
    unique = set(candidates)
    if len(unique) < 3:
        raise ValueError('fewer than three distinct approaches')
    return sorted(unique)

assert diversity(['tree', 'graph', 'linear']) == ['graph', 'linear', 'tree']
try:
    diversity(['tree', 'tree', 'tree', 'graph'])
    raise AssertionError('should have raised')
except ValueError:
    print('diversity requirement held')
```

## Failure Modes
- Accepting superficially different variants of the same approach.
- Diversifying only after the first approach already failed badly.
- Selecting the diverse set without criteria for what differs.
- Confusing more attempts with better coverage.
- Recording the winning approach but not the rejected ones.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Multi-approach sampling and self-consistency remain standard asks in 2026 reasoning-strategy discussions; this is a dated signal, not an adoption metric.

## Related
- debate-pattern.md
- tot.md
- self-play.md
