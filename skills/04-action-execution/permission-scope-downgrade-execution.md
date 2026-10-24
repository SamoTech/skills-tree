---
title: "Permission Scope Downgrade Execution"
category: 04-action-execution
level: advanced
stability: experimental
description: "Execute a permission downgrade from a broad always-allow grant to the smallest scope the task needs, with verification of the applied state."
added: "2026-10"
version: v1
related: [file-permission-management, agent-task-revocation-actions]
tags: [permission, downgrade, execution, least-privilege]
---
# Permission Scope Downgrade Execution

## Description
Execute a permission downgrade from a broad always-allow grant to the smallest scope the task needs, with verification of the applied state. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An audit found an always-allow grant broader than the task needs and the operator must downgrade it safely.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Resolve the target scope, verify the active grant covers it, apply the downgrade, and re-read the applied grant to confirm the broad scope is gone.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def downgrade(current, target, needed):
    if target not in current:
        raise ValueError("cannot downgrade to a scope that is not currently held")
    if not set(needed).issubset({target}):
        raise ValueError("downgrade would remove a scope the task needs")
    return {"applied": [target], "removed": sorted(set(current) - {target})}

out = downgrade(["full_disk_access", "messages"], "messages", {"messages"})
assert out["applied"] == ["messages"] and out["removed"] == ["full_disk_access"]
```

## Failure Modes
- The downgrade is reported as applied without re-reading the live grant state.
- Dependent grants are left in place so the removed scope is still reachable.
- The downgrade executes during an active task that needed the broad scope.
- The removed grant is left active in client-side caches.
- Downgrades are batched without verifying each one individually.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Associated Press reporting traces a marketplace address disclosure to an always-allow permission granted at first use, making scope downgrade a concrete execution need (AP reporting syndicated at wtop.com, dated October 19, 2026) ([public signal](https://wtop.com/national/2026/10/ai-agents-are-only-as-good-as-the-personal-information-you-share-that-raises-privacy-concerns/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [File Permission Management](../04-action-execution/file-permission-management.md)
- [Agent Task Revocation Actions](../04-action-execution/agent-task-revocation-actions.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
