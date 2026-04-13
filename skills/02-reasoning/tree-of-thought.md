---
title: "Tree of Thought (ToT)"
category: 02-reasoning
level: advanced
stability: stable
description: "Apply tree of thought (tot) in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-tree-of-thought.json)

# Tree of Thought (ToT)

**Category:** `reasoning`  
**Skill Level:** `advanced`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Explore multiple reasoning branches simultaneously, evaluate each path, and backtrack to find the optimal solution — unlike linear chain-of-thought.

### Example

```
Root: Solve problem X
├── Branch A: Approach 1
│   ├── Step A1 → evaluate
│   └── Step A2 → prune (dead end)
└── Branch B: Approach 2
    ├── Step B1 → evaluate
    └── Step B2 → solution found ✓
```

### Frameworks

- `tot` Python library
- LangGraph (custom branching graph)
- Custom BFS/DFS prompt loops

### Related Skills

- [Chain of Thought](chain-of-thought.md)
- [MCTS](../09-agentic-patterns/mcts.md)
- [Planning](planning.md)
