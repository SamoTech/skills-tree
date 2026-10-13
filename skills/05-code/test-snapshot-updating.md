---
title: "Test Snapshot Updating"
category: 05-code
level: advanced
stability: experimental
description: "Update test snapshots only after a reviewed diff, and never let a snapshot refresh mask an unintended behavior change."
added: "2026-10"
version: v1
related: [test-flakiness-diagnosis, code-review, mutation-testing]
tags: [testing, snapshots, ci]
---

# Test Snapshot Updating

## Description
Update test snapshots only after a reviewed diff, and never let a snapshot refresh mask an unintended behavior change. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- snapshot tests fail after an intended change and must be updated without hiding unintended differences.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for test snapshot updating work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the test snapshot updating steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def update_snapshots(old, new, intended):
    diffs = [k for k in new if new[k] != old.get(k)]
    unapproved = [d for d in diffs if d not in intended]
    return {"updated": [d for d in diffs if d in intended], "blocked": unapproved}

old = {"width": 100, "label": "a"}
new = {"width": 120, "label": "a", "extra": True}
res = update_snapshots(old, new, ["width"])
assert res["updated"] == ["width"] and res["blocked"] == ["extra"]
```

## Failure Modes
- Running update-all without reviewing the diff.
- Regenerating snapshots on a red branch.
- Committing snapshot churn from formatting noise.
- No record of who reviewed the snapshot diff.
- Treating a vanished key as a pass.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Snapshot hygiene in generated test suites is a recurring 2026 CI failure topic in public developer discussion; this is a dated signal, not an adoption metric.

## Related
- test-flakiness-diagnosis.md
- code-review.md
- mutation-testing.md
