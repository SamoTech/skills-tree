---
title: "Agent Team Config Complexity Budgeting"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Budget the number of agents, skills, and configuration layers on an agent team so added complexity must justify itself against measured task outcomes."
added: "2026-11"
version: v1
related: [agent-behavior-spec-contract-patterns, agent-checkpoint-restore-patterns]
tags: [patterns, complexity, budgeting, evaluation]
---

# Agent Team Config Complexity Budgeting

## Description
Budget the number of agents, skills, and configuration layers on an agent team so added complexity must justify itself against measured task outcomes. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent team has accumulated many skills and sub-agents without measured benefit.
- Configuration changes must justify complexity against task outcomes.
- Rollbacks must be defined before new configuration layers are added.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The current team configuration inventory, the task outcome baseline, and the complexity budget. |
| Outputs | A budget decision naming the accepted and rejected configuration layers with their measured outcome deltas. |
| Safety | Fail closed by rejecting any added layer whose outcome delta is unmeasured. |

## Procedure
1. Inventory the team's skills, sub-agents, and configuration layers.
2. Establish the task outcome baseline before adding anything new.
3. Measure outcome deltas per proposed configuration layer.
4. Accept a layer only when its delta justifies its complexity cost.
5. Define the rollback path for every accepted layer.
6. Emit the budget decision with per-layer deltas and rollbacks.

## Outputs
| Area | Contract |
|---|---|
| Primary | A budget decision naming the accepted and rejected configuration layers with their measured outcome deltas. |
| Verification | Baseline and post-change outcome measurements that reproduce each delta. |
| Failure | A fail-closed decision naming the unmeasured layer and its rejection. |

## Runnable Example
```python
def budget(layers, baseline, outcomes):
    accepted, rejected = [], []
    for l in layers:
        delta = outcomes.get(l["name"], {}).get("delta")
        if delta is None or delta <= l["complexity_cost"]:
            rejected.append(l["name"])
        else:
            accepted.append(l["name"])
    return {"accepted": accepted, "rejected": rejected, "baseline": baseline}

layers = [{"name": "extra_skills", "complexity_cost": 2}, {"name": "router_agent", "complexity_cost": 3}]
outcomes = {"extra_skills": {"delta": 1}, "router_agent": {"delta": 8}}
r = budget(layers, 0.5, outcomes)
assert r["accepted"] == ["router_agent"] and r["rejected"] == ["extra_skills"]
```

## Failure Modes
- Skills are added in bulk with no per-layer outcome measurement.
- Complexity is measured only when things break, never in review.
- Rejections are overridden by preference for elaborate setups.
- Baseline outcomes are recorded after the change, invalidating deltas.
- Rollback paths are defined only for the newest layer.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- One benchmark team ran 100 engineering tasks through elaborate Claude Code setups, one with 37 skills and 17 agents, tracked in the November 6, 2026 Super User Daily (Clauday, November 6, 2026) ([public signal](https://clauday.com/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Behavior Spec Contract Patterns](agent-behavior-spec-contract-patterns.md)
- [Agent Checkpoint Restore Patterns](agent-checkpoint-restore-patterns.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |

