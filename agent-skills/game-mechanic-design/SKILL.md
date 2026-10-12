---
name: game-mechanic-design
description: Design and tune game mechanics as rule systems with resources, loops, and failure states, documenting economy balance and player choice structure before implementation.
metadata:
  source: skills/13-creative/game-mechanic-design.md
  category: 13-creative
  version: "v1"
---

# Game Mechanic Design

Category: Creative | Level: intermediate | Stability: experimental | Version: v1

## Description

A mechanic is a rule system, not a feature name. The skill covers expressing mechanics as resources, actions, and loops; defining the core loop and its failure and mastery states; tuning numbers against an economy model so strategies stay diverse; and documenting the system precisely enough to prototype and critique before any art exists. Designs are tested on paper against degenerate strategies first.

## When to Use

Use when a new game, mode, or system needs its rules designed and balanced before implementation, or when an existing mechanic needs retuning.

Do not balance with intuition alone. Without an economy model, dominant strategies and dead mechanics ship and are expensive to fix after players learn them.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `design_goal` | `object` | Yes | Intended player experience, session length, and challenge curve |
| `mechanic_brief` | `text` | Yes | The rule idea: resources, actions, and win or loss conditions |
| `economy_params` | `object` | No | Numeric starting points for tuning |

## Procedure

1. Express the mechanic as resources, actions, and a loop that connects them.
2. Define the failure states and the mastery curve, including how each failure teaches.
3. Model the economy: sources, sinks, and exchange rates between resources.
4. Simulate representative strategies on paper and identify dominant or dead options.
5. Tune numbers until distinct strategies stay viable within the target session length.
6. Document the system with the loop diagram, the economy table, and open risks.

## Outputs

| Output | Type | Description |
|---|---|---|
| `mechanic_spec` | `object` | Rules, resources, actions, and loop definition |
| `economy_model` | `object` | Sources, sinks, rates, and tuned parameters |
| `strategy_report` | `list` | Viable strategies found and degenerate cases fixed |

## Runnable Example

```python
def economy_turn(start, rates, turns):
    """start: {resource: amount}; rates: {resource: per-turn delta}"""
    state = dict(start)
    history = []
    for _ in range(turns):
        for res, delta in rates.items():
            state[res] = max(0, state[res] + delta)
        history.append(dict(state))
    return history

print(economy_turn({"gold": 10, "wood": 5}, {"gold": 3, "wood": -2}, 4))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Dominant strategy | One option strictly beats the others | Simulate strategies before implementation and retune |
| Dead resources | A resource has no sink or use | Add exchanges or remove the resource |
| Runaway economy | Compound growth breaks the difficulty curve | Cap accumulation or add scaling sinks |
| Failure that teaches nothing | Loss states give no signal about why | Attach feedback to every failure state |
| Unreadable rules | Spec too vague to prototype | Formalize resources, actions, and loops first |

## Security and Authority Boundary

Mechanic designs include monetization structures that can be manipulative. Model the economy honestly, disclose odds where randomized purchases exist, and avoid dark patterns that exploit loss aversion or sunk cost in players.

## Evidence

This skill is grounded in dated public implementation references:

1. The Wikipedia article on game mechanics (https://en.wikipedia.org/wiki/Game_mechanics).
2. The Machinations tool for modeling and simulating game economies (https://machinations.io/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Game Level Design](game-level-design.md) — the spatial craft that packages mechanics into playable spaces.
- [Plot Structure](plot-structure.md) — the narrative skeleton that systems-driven play must not contradict.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
