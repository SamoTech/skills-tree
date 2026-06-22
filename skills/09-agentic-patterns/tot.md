---
title: "Tree of Thought (ToT)"
category: 09-agentic-patterns
level: advanced
stability: stable
description: "Generate multiple candidate next-steps, score each, and search the highest-scoring branch — a tree search over the model's reasoning space, not a linear chain."
added: "2025-03"
version: v3
tags: [reasoning, search, planning, tot]
updated: "2026-04"
dependencies:
  - package: anthropic
    min_version: "0.39.0"
    tested_version: "0.39.0"
    confidence: verified
code_blocks:
  - id: "example-tot"
    type: executable
prerequisites:
  - 09-agentic-patterns/cot
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-09-agentic-patterns-tot.json)

# Tree of Thought (ToT)

## Description

Where Chain-of-Thought is **one** linear reasoning path, ToT explores **many** in parallel. Each step:

1. The model proposes K candidate next-steps from the current state.
2. A scorer (an LLM rubric or a programmatic check) ranks them.
3. The search expands the top-N highest-scoring branches.
4. Steps repeat until a branch reaches a goal state (or the budget is exhausted).

This trades cost for accuracy on problems with **deceptive local optima** — where the first plausible step is often wrong.

## When to Use

- Combinatorial puzzles, theorem-style proofs, constrained creative writing.
- Tasks where you can write a cheap scorer.
- You can afford 5–50× the token budget of a single CoT.

## Related Skills

- [Chain of Thought](cot.md) — linear reasoning baseline
- [MCTS](mcts.md) — stochastic-rollout variant
- [LATS](lats.md) — ToT + reflection
- [Reflection](reflection.md) — critic agent for branch evaluation

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Initial entry |
| 2026-02 | v2 | Added variants table |
| 2026-04 | v3 | Full BFS-ToT runnable example |
| 2026-06 | v3.1 | Added prerequisites field (INITIATIVE-005) |
