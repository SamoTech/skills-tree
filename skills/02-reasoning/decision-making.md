---
title: "Decision Making"
category: 02-reasoning
level: intermediate
stability: stable
version: v3
description: "Select among explicit options using stated goals, constraints, risks, evidence, and decision criteria; preserve trade-offs instead of hiding them."
added: "2025-03"
related: []
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-decision-making.json)

# Decision Making

**Category:** `reasoning`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2025-03

### Description

Select the best action from a set of options given context, constraints, and goals, using explicit criteria, structured scoring, or a named decision framework, and preserve the trade-offs instead of hiding them.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | `options` | list of string | The candidate actions; at least two, exhaustively enumerated |
| Input | `context` | string | Situation, constraints, and goals the decision serves |
| Input | `criteria` | list of `{name, weight}` | Scoring criteria and weights agreed before scoring |
| Output | `decision` | string | The selected option |
| Output | `rationale` | string | Why the winner won, referencing the criteria |
| Output | `tradeoffs` | list of string | What the rejected options would have provided better |

### Procedure
1. Enumerate the options exhaustively; if an option is missing, add it before scoring.
2. Fix the decision criteria and their weights before evaluating any option.
3. Score each option against every criterion with stated evidence, not adjectives.
4. Aggregate scores and check the winner for sensitivity to weight changes.
5. Record the trade-offs the decision accepts and the rejected options' advantages.
6. State reversible vs irreversible consequences and any required human approval before acting.

### Example

```python
def decide(options: list[str], weights: dict[str, float],
           scores: dict[str, dict[str, float]]) -> dict:
    total_weight = sum(weights.values())
    ranked = sorted(
        options,
        key=lambda o: sum(scores[o].get(c, 0.0) * w for c, w in weights.items()) / total_weight,
        reverse=True,
    )
    winner = ranked[0]
    runner_up = ranked[1] if len(ranked) > 1 else None
    return {"decision": winner, "runner_up": runner_up, "ranking": ranked}

result = decide(
    options=["send_email", "create_ticket", "escalate_to_human"],
    weights={"speed": 0.2, "resolution_confidence": 0.5, "cost": 0.3},
    scores={
        "send_email": {"speed": 0.9, "resolution_confidence": 0.2, "cost": 0.1},
        "create_ticket": {"speed": 0.6, "resolution_confidence": 0.5, "cost": 0.3},
        "escalate_to_human": {"speed": 0.4, "resolution_confidence": 0.9, "cost": 0.8},
    },
)
print(result)
```

### Related Skills

- [Planning](planning.md)
- [Risk Assessment](risk-assessment.md)
- [Prioritization](prioritization.md)

## Failure Modes

- Unsupported assumptions: state assumptions explicitly and separate them from observed inputs.
- Ambiguous or incomplete premises: return uncertainty or request the missing constraint rather than fabricating one.
- Criteria fixed after seeing the scores: define and freeze weights before evaluation to prevent rationalization.
- Resource explosion: bound candidate counts, iterations, recursion, and external tool calls.
- Hidden trade-offs: always report what the chosen option gives up relative to the closest alternative.

## Changelog
- v3 (2026-11): Structural modernization; merged the duplicated failure-mode and evidence sections into one authoritative set, added the input/output contract table, a deterministic scoring example, and a procedure.
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
