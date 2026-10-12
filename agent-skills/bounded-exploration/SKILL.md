---
name: bounded-exploration
description: Spend a fixed exploration budget — trials, depth, wall time — on search and self-play style wandering, then commit to the best option found within the bound.
metadata:
  source: skills/09-agentic-patterns/bounded-exploration.md
  category: 09-agentic-patterns
  version: "v1"
---

# Bounded Exploration

Category: Agentic Patterns | Level: intermediate | Stability: experimental | Version: v1

## Description

Exploration without a budget is wandering with good intentions. This skill makes the budget explicit: a number of trials, a depth limit, a deadline, and a stopping rule that ends the search when the bound is hit or the returns flatten. The point is not that exploration is bad — it is that unbounded exploration defers commitment forever, and the commitment is where the value is. After the budget is spent, the agent stops comparing and starts using what it found.

## When to Use

Use when an agent must search a large option space — candidate strategies, tool combinations, plan variants — under real cost or time constraints.

Do not spend exploration budget on cheap, well-understood decisions with an obvious best answer; explore where ignorance is real and the cost of being wrong is high.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `options` | `iterator` | Yes | The candidate space being explored |
| `budget` | `map` | Yes | Trials, depth, and wall-time limits for the run |
| `stopping_rule` | `enum` | Yes | Early stop on flat returns, or spend the full budget |

## Procedure

1. Fix the budget before starting: trial count, depth limit, and deadline, written down so the run cannot renegotiate with itself.
2. Define the reward or quality signal before exploring; a search without a scoring function is a random walk with commentary.
3. Explore in rounds, keeping the best-so-far option at every round so the budget can end at any moment with something usable.
4. Track returns per round: when additional trials stop improving the best score, apply the stopping rule and keep the leftover budget.
5. Commit to the best option found within the bound, and record it with its score and the exploration that produced it.
6. Defer regret to calibration: revisit the budget size against outcomes over time, rather than restarting exploration on a single miss.

## Outputs

| Output | Type | Description |
|---|---|---|
| `best_option` | `record` | The highest-scoring option found within budget |
| `exploration_log` | `list` | Trials, scores, and stopping reason per round |
| `budget_left` | `map` | Unspent budget returned to the caller |

## Runnable Example

```python
def explore(options, score, budget):
    best, best_score = None, float("-inf")
    spent = 0
    for option in options:
        if spent >= budget:
            break
        value = score(option)
        if value > best_score:
            best, best_score = option, value
        spent += 1
    return {"best": best, "score": best_score, "spent": spent}

def fake_score(option):
    return {"a": 1, "b": 5, "c": 4}[option]

print(explore(["a", "b", "c"], fake_score, budget=2))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Endless search | The run keeps exploring past any reasonable bound | Fix trial, depth, and wall-time budgets up front |
| No scoring function | Options compared by feel rather than signal | Define the reward before the first trial |
| Winner-less stops | The budget ends with nothing selected | Keep best-so-far at every round |
| Budget anchoring | The bound set once and never revisited | Calibrate budget size against outcomes over time |
| Regret loops | A single miss triggers a fresh unbounded search | Treat misses as calibration data, not restart triggers |

## Security and Authority Boundary

Exploration that invokes real tools spends real authority: an exploring agent must run under the same least-privilege scope as execution, and its trial actions must be recorded like any other — a search that can execute must never leave the audit log emptier than a commit would.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia's overview of the multi-armed bandit problem (https://en.wikipedia.org/wiki/Multi-armed_bandit).
2. Wikipedia's overview of reinforcement learning (https://en.wikipedia.org/wiki/Reinforcement_learning).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [MCTS](mcts.md) — tree search under explicit simulation budgets.
- [Self-Play](self-play.md) — generating exploration candidates by opposition.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
