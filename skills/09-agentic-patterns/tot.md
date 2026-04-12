# Tree of Thought (ToT)

**Category:** `agentic-patterns`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Explore multiple reasoning branches simultaneously, evaluate each path, and backtrack to find the optimal solution — unlike linear Chain-of-Thought.

### Example

```
Root: Write a persuasive essay on renewable energy
├── Branch A: Lead with economic argument
│   ├── Evaluate: Strong, but may alienate environmentalists → score 7/10
│   └── Expand: Add environmental co-benefits
└── Branch B: Lead with climate urgency
    ├── Evaluate: Emotionally resonant → score 8/10
    └── Select as best branch ✓
```

### Frameworks

- `tot` Python library
- LangGraph (custom branching graph)
- Custom BFS/DFS prompt loops

### Related Skills

- [Chain of Thought](cot.md)
- [MCTS](mcts.md)
- [ReAct](react.md)
