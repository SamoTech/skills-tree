---
title: "LATS (Language Agent Tree Search)"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Combines ToT tree search with reflection-based branch evaluation. The current best-performing single-agent reasoning architecture on hard benchmarks."
added: "2025-03"
version: v1
prerequisites:
  - 09-agentic-patterns/react
  - 09-agentic-patterns/tot
  - 09-agentic-patterns/reflection
---

# LATS (Language Agent Tree Search)

## Description

LATS extends Tree of Thought with a ReAct-style action space and a Reflection-based value function. At each node the agent can call tools (ReAct), proposes multiple next steps (ToT), and uses a critic (Reflection) to score branches instead of a simple heuristic. This combination makes LATS the current state-of-the-art single-agent pattern on multi-step coding and reasoning benchmarks.

## When to Use

- Hard multi-step tasks where ReAct loops fail and ToT is too expensive without guidance.
- You have a verifier (unit tests, formal checks) to ground the value function.
- Token budget is not a primary constraint.

## Related Skills

- [ReAct](react.md) — tool-calling foundation
- [Tree of Thought](tot.md) — search structure
- [Reflection](reflection.md) — branch evaluation
- [MCTS](mcts.md) — stochastic rollout alternative

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Initial entry |
| 2026-06 | v1.1 | Added prerequisites field (INITIATIVE-005) |
