---
name: differential-testing-llm-patches
description: Differentially test LLM-generated code changes against the pre-change behavior on recorded inputs to expose regressions.
metadata:
  source: skills/05-code/differential-testing-llm-patches.md
  category: 05-code
  version: "v1"
---
# Differential Testing LLM Patches

## Description
Differentially test LLM-generated code changes against the pre-change behavior on recorded inputs to expose regressions. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires differential testing llm patches before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for differential testing llm patches. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the differential testing llm patches steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def differential(old_fn, new_fn, cases):
    return [c for c in cases if old_fn(c) != new_fn(c)]
assert differential(str, str, [1, 2]) == []
assert differential(str, repr, [1]) == []
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
Differential testing of model-generated patches is requested as regression protection in 2026 coding-agent workflows. These are dated public signals, not adoption metrics.

## Related
- unit-test-generation.md
- trace-driven-test-generation.md
- bug-fixing.md
