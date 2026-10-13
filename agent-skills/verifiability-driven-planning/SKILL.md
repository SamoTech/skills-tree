---
name: verifiability-driven-planning
description: Decompose goals so each intermediate step has an objective check, prioritizing plans whose progress can be verified over plans that only appear complete.
metadata:
  source: skills/02-reasoning/verifiability-driven-planning.md
  category: 02-reasoning
  version: "v1"
---

# Verifiability-Driven Planning

## Description
Decompose goals so each intermediate step has an objective check, prioritizing plans whose progress can be verified over plans that only appear complete. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a plan must produce checkable intermediate evidence, not just plausible steps before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for verifiability driven planning work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the verifiability driven planning steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def plan_is_verifiable(steps):
    for i, step in enumerate(steps):
        if not step.get("check"):
            return False, "step %d lacks an objective check" % i
    return True, "all steps verifiable"

ok = [{"name": "fetch", "check": "bytes > 0"}, {"name": "parse", "check": "rows == expected"}]
assert plan_is_verifiable(ok)[0] is True
assert plan_is_verifiable([{"name": "research"}])[1].startswith("step 0")
```

## Failure Modes
- Writing checks that always pass.
- Confusing a plausible narrative with verified progress.
- Skipping verification for steps that feel easy.
- Deferring all checks to the end of the plan.
- Ignoring failed checks and continuing anyway.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Verifiability-first task design for agents is a widely discussed 2026 engineering principle in public coverage; this is a dated signal, not an adoption metric.

## Related
- solution-verification.md
- multi-step-planning.md
- self-correction.md
