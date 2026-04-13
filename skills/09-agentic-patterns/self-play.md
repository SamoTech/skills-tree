---
title: "Self-Play"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Apply self-play in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-09-agentic-patterns-self-play.json)

# Self-Play

**Category:** `agentic-patterns`
**Skill Level:** `advanced`
**Stability:** `experimental`
**Added:** 2025-03

### Description

Agent plays against itself (or a copy of itself) to generate training signal without human labeling. Used in RLHF pipelines, debate training, and code self-improvement.

### Example

```
Round 1:
  Agent A: generates solution to coding challenge
  Agent B (clone): critiques Agent A's solution
  Reward: based on test pass rate improvement

Round 2: Agent A incorporates feedback → improved solution
→ Loop continues until convergence
```

### Related Skills

- [Debate Pattern](debate-pattern.md)
- [Bootstrapping](bootstrapping.md)
- [Reflection](reflection.md)
