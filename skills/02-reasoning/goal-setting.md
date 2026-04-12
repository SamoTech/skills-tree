# Goal Setting

**Category:** `reasoning`  
**Skill Level:** `intermediate`  
**Stability:** `stable`  
**Added:** 2025-03  
**Version:** v2

---

## Description

Decompose vague intentions into concrete, measurable, achievable goals with clear success criteria. Goal-setting reasoning is the first step in any planning pipeline — poorly specified goals cause irrelevant tool calls, wasted steps, and off-target outputs.

---

## SMART Goal Framework

| Criterion | Question | Bad | Good |
|---|---|---|---|
| **Specific** | What exactly? | "Improve the code" | "Reduce P99 latency of `/search` endpoint" |
| **Measurable** | How do we know? | "Make it faster" | "From 800ms to ≤200ms" |
| **Achievable** | Is this realistic? | "Zero latency" | "≤200ms" |
| **Relevant** | Does it matter? | "Refactor logging" | "Reduce latency that blocks checkout" |
| **Time-bound** | By when? | "Soon" | "By end of sprint (Friday 17:00)" |

---

## Goal Hierarchy

Goals naturally nest. Always surface the full hierarchy before acting:

```
Vision:      Ship a production-ready search feature
  Goal:      API responds in ≤200ms at P99
    Subgoal: Profile current bottlenecks
    Subgoal: Optimise top-3 slow queries
    Subgoal: Add caching layer for repeated queries
    Subgoal: Load-test at 500 RPS and verify P99
```

---

## Prompt Pattern

```
User request: [RAW INTENTION]

Step 1 — Clarify the goal:
  - What is the concrete desired outcome?
  - How will success be measured?
  - What is the deadline/scope?

Step 2 — Decompose into subgoals:
  - What must be true for the main goal to be achievable?
  - List 3–5 subgoals in dependency order.

Step 3 — Identify conflicts/risks:
  - Are any subgoals in tension with each other?
  - What could prevent each subgoal from being met?
```

---

## Agentic Goal Tracking

In long-running agent loops, goal drift is a failure mode. Mitigate with:

```python
class GoalTracker:
    def __init__(self, goal: str, success_criteria: list[str]):
        self.goal = goal
        self.criteria = {c: False for c in success_criteria}

    def check(self, observation: str, llm) -> bool:
        # Ask LLM to evaluate each criterion against latest observation
        for criterion, met in self.criteria.items():
            if not met:
                self.criteria[criterion] = llm.evaluate(
                    f"Does this observation satisfy: '{criterion}'?\n{observation}"
                )
        return all(self.criteria.values())
```

---

## Related Skills

- [Planning](planning.md)
- [Task Decomposition](task-decomposition.md)
- [Prioritization](prioritization.md)
- [Self-Reflection](self-reflection.md)
