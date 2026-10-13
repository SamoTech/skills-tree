---
name: monte-carlo-estimation
description: Estimate uncertain quantities by bounded stochastic sampling with fixed seeds, report interval estimates, and separate sampling error from model error.
metadata:
  source: skills/02-reasoning/monte-carlo-estimation.md
  category: 02-reasoning
  version: "v1"
---

# Monte-Carlo Estimation

## Description
Estimate uncertain quantities by bounded stochastic sampling with fixed seeds, report interval estimates, and separate sampling error from model error. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- an uncertain quantity needs a reproducible interval estimate rather than a point guess before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for monte carlo estimation work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the monte carlo estimation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
import random

def estimate_mean(sampler, n, seed=7):
    rng = random.Random(seed)
    draws = [sampler(rng) for _ in range(n)]
    mean = sum(draws) / n
    spread = max(draws) - min(draws)
    return mean, spread

mean1, _ = estimate_mean(lambda r: r.random(), 1000)
mean2, _ = estimate_mean(lambda r: r.random(), 1000)
assert mean1 == mean2          # seeded and reproducible
assert abs(mean1 - 0.5) < 0.05
```

## Failure Modes
- Reporting a point estimate with no interval.
- Using unseeded randomness that cannot be reproduced.
- Treating sampling error as model error.
- Sampling too few draws for the claimed precision.
- Sampling from the wrong distribution entirely.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Quantified uncertainty reporting is a recurring 2026 request for agent decision support; this is a dated signal, not an adoption metric.

## Related
- probabilistic-reasoning.md
- numerical-estimation.md
- uncertainty-quantification.md
