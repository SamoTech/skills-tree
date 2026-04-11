# Tree of Thought (ToT)

**Category:** `reasoning`  
**Skill Level:** `advanced`  
**Stability:** `stable`

### Description

Explore multiple reasoning branches simultaneously, evaluate each path, and backtrack to find the optimal solution — unlike linear chain-of-thought.

### Architecture

```
Root: Solve problem X
├── Branch A: Approach 1
│   ├── Step A1 → evaluate
│   └── Step A2 → prune (dead end)
└── Branch B: Approach 2
    ├── Step B1 → evaluate
    └── Step B2 → solution found ✓
```

### Related Skills

- [Chain of Thought](chain-of-thought.md)
- [MCTS](../09-agentic-patterns/mcts.md)
- [Planning](planning.md)
