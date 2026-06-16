---
title: "Least-to-Most Prompting"
category: 02-reasoning
level: intermediate
stability: stable
description: "Decompose a complex problem into a sequence of simpler sub-problems and solve them in order, feeding each solution as context for the next. Achieves generalisation on problems that defeat standard Chain-of-Thought."
added: "2025-06"
version: v2
tags: [reasoning, decomposition, sequential, subproblems]
updated: "2026-06"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-least-to-most.json)

# Least-to-Most Prompting

## Description

Least-to-Most Prompting (Zhou et al., 2022) solves complex tasks by first asking the model to break the problem into an ordered list of sub-problems (easiest first), then solving each one sequentially, appending each answer to the context before tackling the next.

The key insight: if the model can solve every sub-problem, composing the answers gives the final solution. This overcomes CoT failures where the model attempts to solve everything at once and loses track of intermediate steps.

On SCAN compositionality tasks, Least-to-Most achieved 99.7% accuracy versus CoT's 16%. It also significantly outperforms CoT on DROP and math word problems with multiple constraints.

## When to Use

- Multi-constraint math or logic problems where intermediate state matters.
- Compositional generalisation tasks (new combinations of known sub-tasks).
- Agent planning where each step's output becomes the next step's input.
- **Don't use** for simple single-step tasks; the decomposition overhead is wasteful.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `problem` | `str` | The complex problem to solve |
| `max_subproblems` | `int` | Cap on decomposition depth (default 8) |
| → `subproblems` | `list[str]` | Ordered list of sub-problems |
| → `solutions` | `list[str]` | Corresponding solutions |
| → `final_answer` | `str` | Composed final answer |

## Runnable Example

```python
import anthropic

client = anthropic.Anthropic()
MODEL = "claude-opus-4-5"

DECOMPOSE_PROMPT = """Break the following problem into an ordered list of simpler sub-problems.
Start with the easiest/most foundational and build up to the full solution.
Output ONLY a numbered list, one sub-problem per line.

Problem: {problem}"""

SOLVE_PROMPT = """Previous solutions:
{context}

Now solve this sub-problem: {subproblem}
Be concise. Your answer will be used as context for the next step."""

def least_to_most(problem: str, max_subproblems: int = 8) -> dict:
    # Phase 1: Decompose
    decomp = client.messages.create(
        model=MODEL, max_tokens=512,
        messages=[{"role": "user", "content": DECOMPOSE_PROMPT.format(problem=problem)}]
    )
    lines = [l.strip() for l in decomp.content[0].text.strip().split("\n") if l.strip()]
    subproblems = [l.lstrip("0123456789. ") for l in lines[:max_subproblems]]

    # Phase 2: Solve sequentially
    solutions = []
    for sp in subproblems:
        context = "\n".join(f"Q: {q}\nA: {a}" for q, a in zip(subproblems, solutions))
        resp = client.messages.create(
            model=MODEL, max_tokens=512,
            messages=[{"role": "user", "content": SOLVE_PROMPT.format(context=context, subproblem=sp)}]
        )
        solutions.append(resp.content[0].text.strip())

    return {"subproblems": subproblems, "solutions": solutions, "final_answer": solutions[-1] if solutions else ""}

if __name__ == "__main__":
    problem = "If a train travels 120 km at 60 km/h then 80 km at 40 km/h, what is the average speed for the whole journey?"
    result = least_to_most(problem)
    for sp, sol in zip(result["subproblems"], result["solutions"]):
        print(f"Sub: {sp}\nSol: {sol}\n")
    print("Final:", result["final_answer"])
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Wrong decomposition order | Model places hard steps first | Explicit prompt: "start with easiest" |
| Context overflow on many sub-problems | Long context chains | Cap `max_subproblems`; summarise context |
| Model loses track of goal | Too many sub-problems | Add goal reminder at each step |

## Production Applications

- **G01 Coding Agent:** Decompose complex coding tasks into implementable steps
- **G08 Multi-Agent Systems:** Each sub-problem assigned to a specialised sub-agent
- **G02 Research Agent:** Break research questions into foundational facts then synthesis

## Related Skills

- [Chain of Thought](../09-agentic-patterns/cot.md) — Least-to-Most extends CoT with explicit decomposition
- [Goal Decomposition](goal-decomposition.md) — goal-level analogue of this technique
- [Planning Decomposition](planning-decomposition.md) — applies decomposition to agent planning
- [Plan-and-Execute](../09-agentic-patterns/plan-and-execute.md) — agentic pattern built on this reasoning approach

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-06 | v1 | Initial skill file |
| 2026-06 | v2 | Full runnable example, failure modes, goal coverage |
