# GOAL MATCHING SPECIFICATION
> Initiative: INITIATIVE-012C | Phase 2

## Algorithm: Deterministic Keyword + Category Scoring

No AI inference. No LLM calls. Pure graph evidence.

### Pipeline

```
User Input (goal title or free text)
   │
   ▼
1. Normalize: lowercase, strip punctuation, tokenize
   │
   ▼
2. Keyword Match: token overlap against goal.keywords[]
   Score = matched_tokens / total_goal_keywords  (0.0–1.0)
   │
   ▼
3. Category Expansion: for each matched goal, collect all skills
   in goal.categories[] from SKILLS_GRAPH.json nodes
   │
   ▼
4. Prerequisite Traversal: BFS from candidate skills
   following prerequisites[] edges (depth ≤ 3)
   │
   ▼
5. Topological Sort: Kahn's algorithm on prerequisite DAG
   Cycle detection via visited set → log warning, skip edge
   │
   ▼
6. Rank by: level weight (basic=1, intermediate=2, advanced=3)
   + stability weight (stable=3, evolving=2, experimental=1)
   │
   ▼
7. Output: Blueprint object (see BLUEPRINT_SCHEMA.md)
```

### Scoring Weights

| Factor | Weight |
|--------|--------|
| Exact keyword match | 1.0 |
| Partial token overlap | 0.5 |
| Category match | 0.3 |
| Stability: stable | 1.0 |
| Stability: evolving | 0.7 |
| Stability: experimental | 0.4 |

### Determinism Guarantee

Given identical input string and identical SKILLS_GRAPH.json:
- Same goal selected every time
- Same skills surfaced every time  
- Same learning order every time

No random seeds. No sampling. No model calls.

### Edge Cases

| Case | Handling |
|------|----------|
| No keyword match | Return closest goal by edit distance |
| Empty prerequisites | Skill stands alone in learning path |
| Cycle detected | Log, skip offending edge, continue |
| Unknown goal ID | Return null blueprint with error message |
