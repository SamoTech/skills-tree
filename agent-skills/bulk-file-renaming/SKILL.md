---
name: bulk-file-renaming
description: Rename many files by explicit, previewable rules with collision detection, dry-run output, and undo information before applying changes.
metadata:
  source: skills/04-action-execution/bulk-file-renaming.md
  category: 04-action-execution
  version: "v1"
---

# Bulk File Renaming

## Description
Rename many files by explicit, previewable rules with collision detection, dry-run output, and undo information before applying changes. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- Multiple inputs or candidates compete and must be resolved by explicit criteria.
- A wrong intermediate result would propagate into consequential actions.
- The task repeats and benefits from a deterministic procedure.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for bulk file renaming. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the bulk file renaming procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Bulk File Renaming: deterministic check
options = [{"name": "x", "gain": 5, "cost": 1}, {"name": "y", "gain": 4, "cost": 1}]
ranked = sorted(options, key=lambda o: (o["cost"], -o["gain"]))
assert ranked[0]["name"] == "x"
print("best:", ranked[0]["name"])
```

## Failure Modes
- Proceeding with bulk file renaming without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Batch file operations recur in 2026 developer-agent requests; previewable bulk actions are a named safety requirement. These are dated public signals, not adoption metrics.

## Related
- file-write.md
- file-delete.md
- batch-processing.md
