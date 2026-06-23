# Goal Matching Specification
**Initiative:** INITIATIVE-012C  
**Version:** 1.0.0

## Algorithm

The Goal Matching Engine maps user input to a ranked list of goals using pure integer scoring.
**No LLM. No probabilistic ranking.**

### Scoring Rules
```
score = 0
if query in goal.title.toLowerCase()     → score += 10
if query in goal.id                      → score += 8
for each keyword in goal.keywords:
  if keyword includes query OR query includes keyword → score += 3
if query in goal.description             → score += 2
```

### Output
Goals sorted by score descending. Empty query returns all goals (score = 1).

## No-AI Guarantee
- String matching + integer arithmetic only
- Static embedded GOALS_DATA
- Identical input → identical output across all browsers
- Zero external dependencies at runtime
