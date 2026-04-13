![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-09-agentic-patterns-lats.json)

# LATS (Language Agent Tree Search)

**Category:** `agentic-patterns`
**Skill Level:** `advanced`
**Stability:** `experimental`
**Added:** 2025-03

### Description

Combines MCTS with language agents: the LLM generates candidate actions, a value function scores them, and backpropagation refines the search tree over multiple rollouts.

### Example

```
Task: Solve HumanEval coding problem #42

Rollout 1: Generate solution A → run tests → score 0.4
Rollout 2: Generate solution B → run tests → score 0.7
Rollout 3: Refine solution B → run tests → score 1.0 ✓
```

### Related Skills

- [MCTS](mcts.md)
- [Tree of Thought](tot.md)
- [Reflection](reflection.md)
