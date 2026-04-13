---
id: lab-reasoning-mcts
title: Monte Carlo Tree Search for Agent Planning
category: reasoning
status: experimental
stability: alpha
author: OssamaHashim
updated: 2026-04-13
tags: [reasoning, planning, mcts, experimental, labs]
readiness: Not production-ready — research prototype
---

# Lab: Monte Carlo Tree Search (MCTS) for Agent Planning

> **⚗️ Experimental** — This technique is emerging in the research literature but not yet production-proven at scale. Treat this as a research prototype.

## What Is It?

Monte Carlo Tree Search (MCTS) adapts the classic game-tree search algorithm for LLM agent planning. Instead of exhaustively exploring all possible action sequences, the agent:

1. **Selects** a promising node (partial plan) using UCB1 scoring
2. **Expands** it by generating N candidate next actions
3. **Simulates** (rolls out) each candidate to a terminal state using a fast / cheap model
4. **Backpropagates** scores to update node values

This gives the agent a principled way to explore a large action space without brute-force enumeration.

## Why It's Interesting

- Achieves near-optimal planning on tasks where greedy CoT fails
- Naturally handles uncertainty — the tree captures multiple futures simultaneously
- Rollouts can use a cheap model (e.g. Haiku) while expansion uses a strong model
- Inspired by AlphaGo's success in games; now being applied to code generation (AlphaCode 2) and reasoning

## Known Limitations

- **Token cost is high** — each expansion + rollout is expensive
- **Rollout quality** determines search quality; a bad rollout model poisons the tree
- **Depth is bounded** by token budget, not problem structure
- **Not parallelised** in naive implementations — the tree is sequential
- **No guarantees** on convergence for open-ended tasks

## Prototype Implementation

```python
import anthropic, math, random
from dataclasses import dataclass, field

client = anthropic.Anthropic()

@dataclass
class Node:
    state: str          # Current plan/context as text
    parent: 'Node | None' = None
    children: list = field(default_factory=list)
    visits: int = 0
    value: float = 0.0

    def ucb1(self, c: float = 1.41) -> float:
        if self.visits == 0:
            return float('inf')
        return self.value / self.visits + c * math.sqrt(
            math.log(self.parent.visits) / self.visits
        )

def expand(node: Node, n_children: int = 3) -> list[Node]:
    """Generate N candidate next actions from the current state."""
    prompt = f"""You are planning the next step for an AI agent.
Current plan state:\n{node.state}\n
Generate {n_children} distinct, concrete next actions the agent could take.
Output exactly {n_children} actions, one per line, numbered 1-{n_children}."""
    resp = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}]
    )
    actions = [l.split('.', 1)[-1].strip()
               for l in resp.content[0].text.strip().splitlines()
               if l.strip() and l[0].isdigit()]
    return [Node(state=f"{node.state}\n→ {a}", parent=node) for a in actions[:n_children]]

def rollout(node: Node, goal: str, depth: int = 3) -> float:
    """Fast rollout to estimate value. Returns score 0-1."""
    prompt = f"""Goal: {goal}\n\nPartial plan:\n{node.state}\n
On a scale of 0 to 10, how likely is this plan to achieve the goal?
Respond with ONLY a single integer 0-10."""
    resp = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=8,
        messages=[{"role": "user", "content": prompt}]
    )
    try:
        return int(resp.content[0].text.strip()) / 10.0
    except ValueError:
        return 0.5

def mcts(goal: str, initial_state: str, iterations: int = 10) -> str:
    root = Node(state=initial_state)
    for _ in range(iterations):
        # Selection
        node = root
        while node.children:
            node = max(node.children, key=lambda n: n.ucb1())
        # Expansion
        if node.visits > 0:
            node.children = expand(node)
            node = random.choice(node.children)
        # Simulation
        score = rollout(node, goal)
        # Backpropagation
        while node:
            node.visits += 1
            node.value += score
            node = node.parent

    best = max(root.children, key=lambda n: n.value / max(n.visits, 1))
    return best.state

# Usage
best_plan = mcts(
    goal="Write a production-ready FastAPI service for user authentication",
    initial_state="Task: Build a FastAPI auth service",
    iterations=8
)
print(best_plan)
```

## Research References

- [Reasoning with Language Model is Planning with World Model](https://arxiv.org/abs/2305.14992) (RAP, 2023)
- [Tree of Thoughts](https://arxiv.org/abs/2305.10601) (Yao et al., 2023)
- [AlphaCode 2](https://deepmind.google/discover/blog/alphacode-2-llm-powered-competitive-programming/) (DeepMind, 2023)

## Graduation Criteria

This lab graduates to `skills/reasoning/` when:
- [ ] Tested on ≥3 real agent tasks with measurable quality improvement over greedy CoT
- [ ] Token cost vs. quality trade-off documented
- [ ] Parallelised rollout variant benchmarked
- [ ] Failure modes documented with mitigations
