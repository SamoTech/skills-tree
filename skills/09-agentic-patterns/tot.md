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
- Tasks where you can write a cheap scorer ("does this leaf solve the goal?").
- You can afford 5–50× the token budget of a single CoT.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `goal` | `str` | The problem statement |
| `branching` | `int` | Candidates per node (default 3) |
| `beam` | `int` | Top-N branches kept per depth (default 2) |
| `max_depth` | `int` | Hard cap (default 4) |
| → `solution` | `str` | Best leaf reached |
| → `tree` | `dict` | Full search tree for inspection |

## Runnable Example

```python
# pip install anthropic
from __future__ import annotations
import json
import re
from dataclasses import dataclass, field
import anthropic

client = anthropic.Anthropic()
MODEL = "claude-opus-4-5"

@dataclass
class Node:
    state: str
    score: float = 0.0
    children: list["Node"] = field(default_factory=list)
    depth: int = 0

PROPOSE = """Given the partial solution below, propose {k} distinct next steps.
Each step must be one short sentence. Output exactly {k} lines, no numbering.

Partial solution:
{state}"""

SCORE = """Rate how promising this partial solution is on a 0-10 scale for
reaching the goal: {goal}

Solution so far:
{state}

Reply with only a number."""

GOAL_CHECK = """Does the solution below fully satisfy this goal? Answer YES or NO.
Goal: {goal}
Solution: {state}"""

def chat(prompt: str, max_tokens: int = 256, temp: float = 0.7) -> str:
    msg = client.messages.create(
        model=MODEL, max_tokens=max_tokens, temperature=temp,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text.strip()

def propose(state: str, k: int) -> list[str]:
    text = chat(PROPOSE.format(k=k, state=state))
    return [ln.strip("-• ").strip() for ln in text.splitlines() if ln.strip()][:k]

def score(state: str, goal: str) -> float:
    text = chat(SCORE.format(goal=goal, state=state), max_tokens=8, temp=0.0)
    m = re.search(r"\d+(\.\d+)?", text)
    return float(m.group(0)) if m else 0.0

def is_goal(state: str, goal: str) -> bool:
    return chat(GOAL_CHECK.format(goal=goal, state=state), max_tokens=4, temp=0.0).upper().startswith("YES")

def tot(goal: str, branching: int = 3, beam: int = 2, max_depth: int = 4) -> dict:
    root = Node(state=f"Goal: {goal}\n", depth=0)
    frontier: list[Node] = [root]
    best: Node | None = None
    for d in range(max_depth):
        candidates: list[Node] = []
        for parent in frontier:
            for step in propose(parent.state, branching):
                child = Node(
                    state=parent.state + f"\n- {step}",
                    depth=d + 1,
                )
                child.score = score(child.state, goal)
                parent.children.append(child)
                candidates.append(child)
                if is_goal(child.state, goal):
                    return {"solution": child.state, "tree": _dump(root)}
        candidates.sort(key=lambda n: n.score, reverse=True)
        frontier = candidates[:beam]
        if not frontier:
            break
        if best is None or frontier[0].score > best.score:
            best = frontier[0]
    return {"solution": best.state if best else "no solution", "tree": _dump(root)}

def _dump(n: Node) -> dict:
    return {"state": n.state.splitlines()[-1], "score": n.score,
            "children": [_dump(c) for c in n.children]}

if __name__ == "__main__":
    out = tot(
        goal="Use the numbers 4 4 6 8 exactly once each with + - * / and parentheses to make 24.",
        branching=3, beam=2, max_depth=4,
    )
    print(out["solution"])
    print(json.dumps(out["tree"], indent=2)[:1200])
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Tree explodes — runaway cost | branching × beam × depth too large | Cap product to <30; prefer programmatic scorer when possible |
| Scorer is correlated with proposer | Same model proposes and scores | Use a different model or a programmatic check for the score |
| Diversity collapse | Temperature too low → all candidates near-identical | Sample at temperature 0.7–1.0 for proposal |
| Goal-check oscillates | Goal check disagrees with itself | Run goal check at temp=0; require YES twice in a row |
| Best leaf is "almost done" | Budget exhausted on a near-solution | Return best-so-far + flag as approximate |

## Variants

| Variant | Difference |
|---|---|
| **DFS-ToT** | Depth-first; cheap on memory, dangerous on local optima |
| **BFS-ToT** | Breadth-first; the version above |
| **MCTS** | Replace scorer with rollouts + UCB — better on stochastic domains. See [`mcts.md`](mcts.md) |
| **LATS** | ToT + value model + reflection — current SOTA on multi-hop search |

## Frameworks & Models

| Framework | Implementation |
|---|---|
| Custom (above) | Pure Python + LLM API |
| LangGraph | Build the search as a state graph with a `branch` node |
| `tot` PyPI library | Reference implementation of original Yao et al. paper |

## Model Comparison

| Capability | claude-opus-4-5 | gpt-4o | gemini-2.0-flash |
|---|---|---|---|
| Diverse proposals | 4 | 4 | 3 |
| Honest self-scoring | 4 | 3 | 3 |
| Cost per solved task | 3 | 4 | 5 |

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
| 2026-04 | v3 | Full BFS-ToT runnable example, failure modes, model comparison |
