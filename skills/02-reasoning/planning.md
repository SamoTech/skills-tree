---
Category: Reasoning
Skill Level: Advanced
Stability: Stable
Tags: [planning, task-graph, goal-decomposition, replanning, htns]
---

# Planning

### Description
Generates structured multi-step plans to achieve a goal, with dependency tracking, precondition checking, and dynamic replanning when observations deviate from predictions. Supports hierarchical task networks (HTN), PDDL-style symbolic planning, and LLM-based natural language plans with executable action schemas.

### When to Use
- Agentic workflows requiring ordered action sequences with explicit dependencies
- Multi-agent task allocation where subtasks must be distributed across specialists
- Long-horizon tasks (>10 steps) where intermediate checkpoints and replanning are essential
- Robotics or automation pipelines with real-world state constraints

### Example
```python
from pydantic import BaseModel
from openai import OpenAI
import json

client = OpenAI()

class Step(BaseModel):
    id: int
    action: str
    depends_on: list[int]
    tool: str
    args: dict
    expected_output: str

class Plan(BaseModel):
    goal: str
    steps: list[Step]
    success_criteria: str

def generate_plan(goal: str, available_tools: list[str]) -> Plan:
    prompt = f"""Create a detailed execution plan for the following goal.
Available tools: {', '.join(available_tools)}
Goal: {goal}
Output valid JSON matching the Plan schema."""
    r = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format=Plan
    )
    return r.choices[0].message.parsed

def replan(plan: Plan, failed_step_id: int, error: str) -> Plan:
    prompt = f"""Step {failed_step_id} of the following plan failed with: {error}
Original plan: {plan.model_dump_json()}
Revise the plan to work around this failure."""
    r = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format=Plan
    )
    return r.choices[0].message.parsed
```

### Advanced Techniques
- **PDDL integration**: convert LLM plan to PDDL, validate with Fast Downward solver, execute grounded plan
- **Monte Carlo rollout**: simulate plan execution with a world model before committing
- **Constraint propagation**: check resource conflicts (time, tokens, API rate limits) across parallel steps
- **Adaptive horizon**: start with a 3-step lookahead, extend horizon as confidence grows

### Related Skills
- `task-decomposition`, `goal-setting`, `react`, `subagent-delegation`, `plan-and-execute`
