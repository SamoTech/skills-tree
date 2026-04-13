---
title: "Role Assignment"
category: 15-orchestration
level: advanced
stability: stable
description: "Apply role assignment in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-15-orchestration-role-assignment.json)

**Category:** Orchestration
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Dynamically assigns specialised roles and system prompts to sub-agents in a multi-agent pipeline based on task requirements, available capabilities, and workload. Supports static rosters and on-demand role creation.

### Example
```python
from dataclasses import dataclass
from typing import Callable

@dataclass
class AgentRole:
    name: str
    system_prompt: str
    tools: list[str]

ROLE_REGISTRY = {
    "researcher": AgentRole(
        "researcher",
        "You are a research agent. Find and summarise relevant information.",
        ["web_search", "wikipedia"]
    ),
    "coder": AgentRole(
        "coder",
        "You are a coding agent. Write and execute Python code.",
        ["code_exec", "file_write"]
    ),
    "reviewer": AgentRole(
        "reviewer",
        "You are a critical reviewer. Find flaws and suggest improvements.",
        []
    ),
}

def assign_role(task: str) -> AgentRole:
    if "code" in task.lower() or "script" in task.lower():
        return ROLE_REGISTRY["coder"]
    if "research" in task.lower() or "find" in task.lower():
        return ROLE_REGISTRY["researcher"]
    return ROLE_REGISTRY["reviewer"]

role = assign_role("Write a Python script to parse CSV files")
print(role.name, role.tools)
```

### Related Skills
- [Subagent Delegation](../09-agentic-patterns/subagent-delegation.md)
- [Sequential Workflow](sequential-workflow.md)
