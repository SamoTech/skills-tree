---
title: "Multi-Step Planning"
category: 02-reasoning
level: intermediate
stability: stable
description: "Apply multi-step planning in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-multi-step-planning.json)

# Multi-Step Planning
Category: reasoning | Level: intermediate | Stability: stable | Version: v1

## Description
Break a high-level goal into an ordered sequence of concrete, executable sub-tasks with dependencies.

## Example
```python
import anthropic, json
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Create a plan to deploy a FastAPI app to AWS ECS. Return JSON: [{step, action, depends_on}]"}]
)
plan = json.loads(response.content[0].text)
for step in plan:
    print(f"{step['step']}. {step['action']} (after: {step['depends_on']})") 
```

## Failure Modes
- Circular dependencies not detected
- Steps too coarse to be actionable

## Related
- `planning.md` · `goal-setting.md` · `react.md`

## Changelog
- v1 (2026-04): Initial entry
