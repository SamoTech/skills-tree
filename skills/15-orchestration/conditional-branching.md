---
title: "Conditional Branching"
category: 15-orchestration
level: advanced
stability: stable
description: "Apply conditional branching in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-15-orchestration-conditional-branching.json)

**Category:** Orchestration
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Routes agent execution to different workflow branches based on dynamic conditions such as tool results, confidence scores, user input, or state flags. Enables decision trees, fallback paths, and adaptive pipelines.

### Example
```python
from typing import Callable

def route(state: dict, branches: dict[str, Callable]) -> dict:
    """Route to a branch function based on state condition."""
    intent = state.get("intent", "default")
    handler = branches.get(intent, branches["default"])
    return handler(state)

def handle_order(s): return {**s, "action": "create_order"}
def handle_refund(s): return {**s, "action": "process_refund"}
def handle_default(s): return {**s, "action": "ask_clarification"}

branches = {"order": handle_order, "refund": handle_refund, "default": handle_default}

print(route({"intent": "refund", "user": "alice"}, branches))
print(route({"intent": "unknown"}, branches))
```

### Related Skills
- [Sequential Workflow](sequential-workflow.md)
- [State Machine](state-machine.md)
- [Decision Making](../02-reasoning/decision-making.md)
