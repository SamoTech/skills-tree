---
title: "Monte Carlo Tree Search"
category: 09-agentic-patterns
level: advanced
stability: stable
version: v2
description: "Use stochastic rollout and value estimates to explore a decision tree while controlling expansion, simulation, and selection budgets."
added: "2025-03"
related: [lats, tot, bounded-exploration]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-09-agentic-patterns-mcts.json)

# Monte Carlo Tree Search

**Category:** `agentic-patterns`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Use stochastic rollout and value estimates to explore a decision tree while controlling expansion, simulation, and selection budgets. Selection balances exploitation of high-value nodes against exploration of under-sampled ones, and every simulated reward is validated against a real terminal or value signal.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | root_state | object | The start state with a deterministic seed where possible |
| Input | action_space | list of object | The actions available at each node |
| Output | best_action | object | The root action with the highest validated value estimate |
| Output | budget_ledger | object | Simulations and expansions spent against the declared budget |

### Procedure
1. Declare the simulation budget, expansion policy, and a deterministic seed where possible.
2. Select a node by balancing value estimates against visit counts.
3. Expand it with one unexplored action; roll out to a terminal or value signal.
4. Back up the result along the path; validate that the value signal is real, not a heuristic artifact.
5. Stop at the budget; select the root action with the best validated estimate.
6. Report the estimate, its sample count, and the budget spent; distrust value estimates with tiny samples.

### Example

```python
stats = {'left': {'n': 4, 'mean': 0.5}, 'right': {'n': 10, 'mean': 0.8}}
budget = 14
spent = sum(s['n'] for s in stats.values())
def ucb(s, c=1.0, N=spent): return s['mean'] + c * (2 * 0.5 / max(1, s['n'])) ** 0.5
best = max(stats, key=lambda k: stats[k]['mean'] if stats[k]['n'] >= 3 else -1)
assert best == 'right' and spent <= budget
print({'best': best, 'mean': stats[best]['mean'], 'n': stats[best]['n'], 'spent': spent})
```

### Related Skills

- [LATS](lats.md) - tree search with tool use and reflective scoring
- [Tree of Thoughts](tot.md) - breadth-first candidate exploration
- [Bounded Exploration](bounded-exploration.md) - explicit search budgets
- [Exploration-Exploitation Balancing](exploration-exploitation-balancing.md) - the selection tradeoff

## Failure Modes

- A poor value heuristic amplified by random rollouts into confident wrong choices.
- Selection on value estimates backed by tiny sample counts.
- Non-reproducible rollouts where a deterministic seed was required.
- Budget exhaustion reported as convergence.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; pattern behavior must be checked against current framework documentation; no benchmark claim is made without reproducible evidence.
