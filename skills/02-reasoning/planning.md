---
title: "Planning"
category: 02-reasoning
level: intermediate
stability: stable
added: "2025-03"
description: "Apply planning in AI agent workflows."
dependencies:
  - package: openai
    min_version: "1.0.0"
    tested_version: "2.31.0"
    confidence: verified
  - package: pydantic
    min_version: "2.0.0"
    tested_version: "2.13.0"
    confidence: verified
code_blocks:
  - id: "example-planning"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-planning.json)

# Planning

**Category:** `reasoning`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Generate structured, multi-step action plans from a high-level goal, with each step containing an action, expected outcome, and contingency.

### Example

```python
# pip install openai pydantic
from openai import OpenAI
from pydantic import BaseModel
from typing import List

client = OpenAI()

class Step(BaseModel):
    step_number: int
    action: str
    expected_outcome: str
    contingency: str

class Plan(BaseModel):
    goal: str
    steps: List[Step]

def generate_plan(goal: str) -> Plan:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Generate a detailed step-by-step plan."},
            {"role": "user", "content": f"Goal: {goal}"}
        ],
        response_format=Plan
    )
    return completion.choices[0].message.parsed

plan = generate_plan("Deploy a FastAPI app to a cloud server")
for step in plan.steps:
    print(f"{step.step_number}. {step.action}")
```

### Advanced Techniques
- **Hierarchical planning**: decompose goals into sub-goals, plan each independently
- **Plan validation**: run a critic agent to score feasibility before execution
- **Adaptive re-planning**: after each step, re-evaluate whether the remaining plan is still valid

### Related Skills
- `task-decomposition`, `chain-of-thought`, `react`, `goal-setting`
