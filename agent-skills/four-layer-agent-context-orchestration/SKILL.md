---
name: four-layer-agent-context-orchestration
description: Orchestrate agent context as explicit layers with defined ownership, budget, and invalidation rules per layer.
metadata:
  source: skills/15-orchestration/four-layer-agent-context-orchestration.md
  category: 15-orchestration
  version: "v1"
---

# Four-Layer Agent Context Orchestration

## Description
Orchestrate agent context as explicit layers with defined ownership, budget, and invalidation rules per layer. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent's context is assembled from multiple sources with different lifetimes.
- Each context layer needs an owner and an invalidation rule.
- Context budgets must be enforced per layer, not globally.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The layer definitions with owners and budgets, the context sources, and the invalidation rules. |
| Outputs | A context configuration naming per-layer sources, budgets, invalidation rules, and the assembly order. |
| Safety | Fail closed by refusing assembly when any layer exceeds its budget or misses invalidation rules. |

## Procedure
1. Define the layers with their owners and per-layer budgets.
2. Map every context source to exactly one owning layer.
3. Write the invalidation rule per layer tied to its sources.
4. Assemble the context in the declared order enforcing budgets.
5. Refuse assembly when a layer exceeds budget or lacks invalidation.
6. Emit the context configuration with per-layer state.

## Outputs
| Area | Contract |
|---|---|
| Primary | A context configuration naming per-layer sources, budgets, invalidation rules, and the assembly order. |
| Verification | Budget arithmetic and invalidation triggers that reproduce the assembly decisions. |
| Failure | A fail-closed assembly note naming the over-budget layer and the refused context. |

## Runnable Example
```python
def assemble(layers, sources):
    state, refuse = {}, None
    for name, cfg in layers.items():
        owned = [s for s in sources if s["layer"] == name]
        if sum(s["tokens"] for s in owned) > cfg["budget"]:
            refuse = name
            break
        if not cfg.get("invalidate"):
            refuse = name + ":missing_invalidation"
            break
        state[name] = len(owned)
    return {"state": state, "refuse": refuse}

layers = {"system": {"budget": 100, "invalidate": "on_role_change"}, "history": {"budget": 50, "invalidate": "on_turn"}}
srcs = [{"layer": "system", "tokens": 80}, {"layer": "history", "tokens": 60}]
assert assemble(layers, srcs)["refuse"] == "history"
assert assemble(layers, srcs[:1])["state"] == {"system": 1}
```

## Failure Modes
- Layers share one global budget, so one source starves the rest.
- Sources map to multiple layers, breaking ownership.
- Invalidation is implicit, so stale layers persist silently.
- Assembly order is undefined, making reproduction impossible.
- Over-budget layers are trimmed silently instead of refusing.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- AWS published a four-layer context framework from Deep Insight as one of the November 6, 2026 production-agent tooling patterns (mech.app Daily Brief, November 6, 2026) ([public signal](https://www.mech.app/briefs/2026-11-06-daily-brief/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [A2a Multi Agent Governance Workflow](a2a-multi-agent-governance-workflow.md)
- [Agent Authorization Context Propagation](agent-authorization-context-propagation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
