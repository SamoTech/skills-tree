---
title: "MCTS (Monte Carlo Tree Search)"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Stochastic-rollout variant of ToT. Uses random playouts to estimate node value instead of a trained value function."
added: "2025-03"
version: v1
prerequisites:
  - 09-agentic-patterns/tot
---

# MCTS (Monte Carlo Tree Search)

## Description

MCTS replaces the deterministic scorer in Tree of Thought with Monte Carlo rollouts: from each candidate node, run N random completions to the goal and use the win rate as the node's value. This makes the value estimate model-free at the cost of more total tokens.

## When to Use

- Tasks with a binary or clear terminal outcome (pass/fail tests, game wins).
- You lack a reliable critic model to score intermediate states.
- Token budget is large enough for rollouts.

## Related Skills

- [Tree of Thought](tot.md) — deterministic-scorer baseline this extends
- [LATS](lats.md) — learned value function alternative

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Initial entry |
| 2026-06 | v1.1 | Added prerequisites field (INITIATIVE-005) |
