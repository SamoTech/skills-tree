# MCTS (Monte Carlo Tree Search)

**Category:** `agentic-patterns`
**Skill Level:** `advanced`
**Stability:** `experimental`

### Description

Use Monte Carlo Tree Search to explore a decision tree of actions. Balances exploration vs. exploitation via UCB scoring, enabling long-horizon planning.

### Example

```python
# Pseudocode: MCTS for code generation
root = Node(state="Generate a sorting function")
for _ in range(100):  # simulations
    node = select(root)          # UCB-guided selection
    child = expand(node)         # generate candidate
    reward = simulate(child)     # run tests → score
    backpropagate(child, reward) # update path scores
best = max(root.children, key=lambda n: n.value)
```

### Related Skills

- [Tree of Thought](tot.md)
- [LATS](lats.md)
- [Self-Play](self-play.md)
