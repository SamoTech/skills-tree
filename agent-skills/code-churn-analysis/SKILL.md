---
name: code-churn-analysis
description: Measure which files and modules change most and why, using commit history and ownership signals, to target review and refactoring effort where churn is concentrated.
metadata:
  source: skills/05-code/code-churn-analysis.md
  category: 05-code
  version: "v1"
---

# Code Churn Analysis

## Description
Measure which files and modules change most and why, using commit history and ownership signals, to target review and refactoring effort where churn is concentrated. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires code churn analysis before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for code churn analysis. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the code churn analysis steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
# Code Churn Analysis: deterministic check
seen = {}
conflicts = []
for item in [{"k": "a", "v": 1}, {"k": "a", "v": 2}, {"k": "b", "v": 3}]:
    if item["k"] in seen and seen[item["k"]] != item["v"]:
        conflicts.append(item["k"])
    seen[item["k"]] = item["v"]
assert conflicts == ["a"]
print("conflicts:", conflicts)
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
Maintenance prioritization via churn metrics recurs in 2026 engineering-effectiveness discussions. These are dated public signals, not adoption metrics.

## Related
- git-diff-reading.md
- refactoring.md
- static-analysis.md
