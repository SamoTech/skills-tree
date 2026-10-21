---
name: agent-memory-tiering-policy-design
description: Design a memory tiering policy that places working, episodic, and archival context in declared tiers with eviction rules.
metadata:
  source: skills/03-memory/agent-memory-tiering-policy-design.md
  category: 03-memory
  version: "v1"
---

# Agent Memory Tiering Policy Design

## Description
Design a memory tiering policy that places working, episodic, and archival context in declared tiers with eviction rules. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent's memory usage outgrows a single store and context must be tiered by recency and task value.
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
3. Define the working, episodic, and archival tiers, declare the promotion and eviction rules between them, and record the policy as the executed contract.
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
def tier_for(entry, policy):
    for tier in ("working", "episodic", "archival"):
        rule = policy[tier]
        if entry["age_days"] <= rule["max_age_days"] and entry["task_value"] >= rule["min_value"]:
            return tier
    raise ValueError("entry matches no declared tier")
policy = {"working": {"max_age_days": 1, "min_value": 0}, "episodic": {"max_age_days": 30, "min_value": 3}, "archival": {"max_age_days": 3650, "min_value": 0}}
assert tier_for({"age_days": 5, "task_value": 4}, policy) == "episodic"
```

## Failure Modes
- Tiers are defined without eviction rules and archival storage grows without bound.
- Promotion depends on recency alone and high-value context is evicted as low-value.
- The policy is kept in tribal knowledge and two agents apply different tiering to the same data.
- Tier moves are not logged and provenance is lost when context is archived.
- Working-tier entries are never demoted and long tasks exhaust the fast store.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Microsoft documents interactive experiences, memory, and resilient execution support in the Microsoft Agent Framework (devblogs.microsoft.com, dated September 22, 2026) ([public signal](https://devblogs.microsoft.com/agent-framework/interactive-experiences-memory-and-resilient-execution/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Cache Management](../03-memory/cache-management.md)
- [Context Window Budget Planning](../03-memory/context-window-budget-planning.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
