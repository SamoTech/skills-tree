---
title: "Agentic Adversary Emulation Scope Reasoning"
category: 02-reasoning
level: advanced
stability: experimental
description: "Reason about which chained-weakness attack paths an emulated autonomous attacker should cover before an exercise runs."
added: "2026-11"
version: v1
related: [exploit-class-prioritization-reasoning, adversarial-reasoning]
tags: [reasoning, security, emulation, risk]
---
# Agentic Adversary Emulation Scope Reasoning

## Description
Reason about which chained-weakness attack paths an emulated autonomous attacker should cover before an exercise runs. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An emulation exercise must be scoped to plausible chains rather than every weakness.
- Individually permitted behaviors that combine into an attack path must be prioritized.
- Emulation scope must stay inside the declared system boundary and data limits.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The weakness inventory, the asset map, and the exercise constraints. |
| Outputs | A ranked emulation scope naming the chains, entry weaknesses, and target assets. |
| Safety | Fail closed by excluding chains that reach undeclared assets or require real customer data. |

## Procedure
1. List candidate weaknesses with their individual permissions and reachable systems.
2. Enumerate chains of two to three weaknesses that end at a sensitive asset.
3. Score each chain on likelihood, blast radius, and evidence availability.
4. Drop chains that leave the declared exercise boundary or touch production data.
5. Rank the remaining chains and select the top set that fits the exercise budget.
6. Record the selected scope with the rejected chains and the exclusion reasons.

## Outputs
| Area | Contract |
|---|---|
| Primary | A ranked emulation scope naming selected chains, entry weaknesses, and target assets. |
| Verification | Recorded chain enumerations and exclusion decisions that reproduce the scope. |
| Failure | A fail-closed error report naming the out-of-boundary chain and the withheld selection. |

## Runnable Example
```python
def scope_emulation(weaknesses, assets, budget):
    chains = []
    for w in weaknesses:
        for target in w.get("reaches", []):
            if target in assets["sensitive"]:
                chains.append({"entry": w["id"], "target": target, "score": w["likelihood"] * w["radius"]})
    in_scope = [c for c in chains if c["entry"] not in assets["excluded"]]
    selected = sorted(in_scope, key=lambda c: -c["score"])[:budget]
    return {"selected": selected, "rejected": [c["entry"] for c in chains if c not in selected]}

weaknesses = [
    {"id": "w1", "reaches": ["billing"], "likelihood": 0.8, "radius": 3},
    {"id": "w2", "reaches": ["ci"], "likelihood": 0.5, "radius": 2},
]
assets = {"sensitive": ["billing", "ci"], "excluded": ["w2"]}
r = scope_emulation(weaknesses, assets, budget=1)
assert [c["entry"] for c in r["selected"]] == ["w1"] and r["rejected"] == ["w2"]
```

## Failure Modes
- Every known weakness is emulated and the exercise exceeds its budget.
- Chains are selected without scoring and low-value paths crowd out critical ones.
- A chain that reaches an undeclared asset is included and the exercise oversteps its boundary.
- Exclusion decisions are not recorded, so the scope cannot be audited later.
- The emulated attacker is granted capabilities the real threat model does not support.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- CrowdStrike announced Agentic Adversary Emulation, which uses purpose-built security models to simulate how an autonomous attacker could chain weaknesses into an attack path (AI Agents News, Week of November 5, 2026, dated November 5, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Exploit Class Prioritization Reasoning](exploit-class-prioritization-reasoning.md)
- [Adversarial Reasoning](adversarial-reasoning.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
