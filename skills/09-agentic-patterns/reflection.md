---
title: "Reflection / Reflexion"
category: 09-agentic-patterns
level: advanced
stability: stable
description: "Add a critique → revise pass on top of any agent output. The foundation of every self-correcting agent."
added: "2025-03"
version: v3
tags: [reflection, self-correction, critique, agent]
updated: "2026-04"
dependencies:
  - package: anthropic
    min_version: "0.39.0"
    tested_version: "0.39.0"
    confidence: verified
code_blocks:
  - id: "example-reflection"
    type: executable
prerequisites:
  - 09-agentic-patterns/cot
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-09-agentic-patterns-reflection.json)

# Reflection / Reflexion

## Description

Reflection adds a **critique → revise** pass on top of any agent output. The model produces a draft, then a second prompt asks it (or a stronger model) to find flaws — wrong reasoning, hallucinated facts, missed constraints — and rewrite. Reflexion ([Shinn et al., 2023](https://arxiv.org/abs/2303.11366)) generalises this into a loop: store self-critiques in memory, retry the task, do better next time.

This skill is the foundation of every agent that *recovers from its own first-try mistakes* — code agents that fix lint errors before submitting, planners that re-plan when a step fails, writers that revise drafts.

## When to Use

- Tasks where the **first answer is often wrong but a fix is cheap** (code, math proofs, structured output validation).
- You have a verifier signal — failing tests, schema errors, retrieval mismatch — that the critique can ground itself in.
- Latency budget allows ≥2 model calls per task.
- **Don't use** when the underlying error is information you don't have (no amount of reflection invents missing facts).

## Related Skills

- [Chain of Thought](cot.md) — the reasoning baseline this reflects on
- [ReAct](react.md) — agent loop that benefits from reflection on failure
- [Critic Agent](critic-agent.md) — dedicated critic model variant
- [LATS](lats.md) — tree search that uses reflection as branch evaluator

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Initial entry |
| 2026-02 | v2 | Added variants table |
| 2026-04 | v3 | Full runnable example, failure modes, model comparison |
| 2026-06 | v3.1 | Added prerequisites field (INITIATIVE-005) |
