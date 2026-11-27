---
title: "LATS"
category: 09-agentic-patterns
level: advanced
stability: stable
version: v2
description: "Combine tree search, tool use, and reflective evaluation to explore candidate actions under a bounded search budget."
added: "2025-03"
related: [mcts, reflection, bounded-exploration]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-09-agentic-patterns-lats.json)

# LATS

**Category:** `agentic-patterns`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Combine tree search, tool use, and reflective evaluation to explore candidate actions under a bounded search budget. Each node expansion spends tool calls, each score is a reflective evaluation, and the budget, depth, and termination criteria are explicit before the first expansion.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | search_state | object | The start state and the declared expansion budget |
| Input | tools | list of object | Allowed tool calls per node, with permissions |
| Output | best_trajectory | list of object | The selected node path with per-node scores |
| Output | budget_ledger | object | Spent expansions and tool calls against the declared budget |

### Procedure
1. Declare the expansion budget, maximum depth, and termination criterion before searching.
2. Expand a node by selecting one allowed tool action; record the observation verbatim.
3. Score the resulting node with a reflective evaluation against the task criterion.
4. Back up scores to ancestors and expand the most promising node next.
5. Stop at the termination criterion or budget exhaustion, whichever comes first.
6. Report the best trajectory with its scores and the spent budget; never claim benchmark superiority without reproducible evidence.

### Example

```python
nodes = {'root': {'score': None, 'kids': ['a', 'b']},
         'a': {'score': 0.4, 'kids': []}, 'b': {'score': 0.9, 'kids': []}}
budget, spent = 2, 0
best = max((k for k, v in nodes.items() if v['score'] is not None),
           key=lambda k: nodes[k]['score'])
spent += 1  # expansions that produced the scored leaves
assert best == 'b' and spent <= budget
print({'best': best, 'score': nodes[best]['score'], 'spent': spent, 'budget': budget})
```

### Related Skills

- [Monte Carlo Tree Search](mcts.md) - stochastic rollout variant of tree search
- [Reflection](reflection.md) - the reflective scoring pass
- [Bounded Exploration](bounded-exploration.md) - explicit search budgets
- [Tree of Thoughts](tot.md) - simpler unpruned candidate exploration

## Failure Modes

- Exhausting the budget without a verified result and calling the last node best.
- Tool permissions that widen during the search.
- Reflective scores optimized as a proxy that diverges from the task objective.
- Claiming benchmark superiority without reproducible evidence.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; pattern behavior must be checked against current framework documentation; no benchmark claim is made without reproducible evidence.
