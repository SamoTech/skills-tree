---
title: "Latency Tier Selection Reasoning"
category: 02-reasoning
level: advanced
stability: experimental
description: "Select between standard and premium-speed model tiers per workload using explicit latency, cost, and task-type trade-offs."
added: "2026-11"
version: v1
related: [trade-off-analysis]
tags: [reasoning, latency, tiers, cost]
---
# Latency Tier Selection Reasoning

## Description
Select between standard and premium-speed model tiers per workload using explicit latency, cost, and task-type trade-offs. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A workload can run on a premium speed tier and the choice materially changes latency, cost, or both.
- The outcome would change if a latency-critical interactive task were routed to the standard tier.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The task latency budget, the cost ceiling, and the tier capability contract. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Score each candidate tier against the latency budget and the cost ceiling with recorded margins.
4. Select the tier that meets both constraints and record the rejected tiers with their shortfall.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A tier-selection record with the chosen tier, the latency margin, the cost delta, and rejected alternatives. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def select_tier(budget_ms, cost_cap, tiers):
    ok = [t for t in tiers if t["latency_ms"] <= budget_ms and t["cost"] <= cost_cap]
    if not ok:
        return None
    return sorted(ok, key=lambda t: t["cost"])[0]["name"]
tiers = [{"name": "standard", "latency_ms": 4000, "cost": 1}, {"name": "ultrafast", "latency_ms": 900, "cost": 5}]
assert select_tier(1000, 10, tiers) == "ultrafast"
assert select_tier(1000, 2, tiers) is None
```

## Failure Modes
- A premium tier is selected for batch workloads where latency does not matter, inflating cost.
- The cost ceiling is ignored when the task is urgent, silently breaking the budget.
- Latency estimates come from vendor marketing instead of measured runs.
- The selection record does not name the rejected tiers or their shortfall.
- Interactive and batch tasks share one tier decision without differentiation.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- OpenAI DevDay 2026 introduced the Ultrafast premium speed tier with up to 8x faster token generation in Codex and 6x in the API (OpenAI DevDay recap, dated November 4, 2026) ([public signal](https://openai.com/index/devday-2026-recap/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Trade-off Analysis](trade-off-analysis.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
