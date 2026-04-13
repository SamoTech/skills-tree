---
title: "Working Memory"
category: 03-memory
level: intermediate
stability: stable
added: "2025-03"
description: "Apply working memory in AI agent workflows."
---


![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-03-memory-working-memory.json)

# Working Memory

### Description
Maintains active task state, intermediate results, and evolving context during the execution of a complex multi-step task. Working memory is the agent's cognitive workspace — it holds what the agent is currently doing, what it has already done, and what it needs to do next.

### When to Use
- Multi-step agentic workflows where partial results must be tracked between tool calls
- State machines where the agent transitions between phases (plan → execute → verify → replan)
- Parallel sub-task coordination where results from multiple branches must be merged

### Example
```python
from dataclasses import dataclass, field
from typing import Any

@dataclass
class WorkingMemory:
    goal: str
    steps_completed: list[str] = field(default_factory=list)
    tool_results: dict[str, Any] = field(default_factory=dict)
    current_step: int = 0
    errors: list[str] = field(default_factory=list)
    scratchpad: str = ""

    def record_result(self, tool: str, result: Any) -> None:
        self.tool_results[f"{tool}_{self.current_step}"] = result
        self.steps_completed.append(f"Step {self.current_step}: {tool}")
        self.current_step += 1

    def to_context(self) -> str:
        return (
            f"Goal: {self.goal}\n"
            f"Completed: {self.steps_completed}\n"
            f"Last results: {list(self.tool_results.items())[-3:]}\n"
            f"Errors: {self.errors}\n"
            f"Scratchpad: {self.scratchpad}"
        )
```

### Advanced Techniques
- **Structured state schemas**: use Pydantic models as the working memory schema for validation and serialization
- **Checkpoint snapshots**: serialize working memory to JSON at each step for resume-on-failure
- **Attention masking**: in multi-agent setups, expose only task-relevant slices of working memory to each sub-agent

### Related Skills
- `short-term-memory`, `episodic-memory`, `task-decomposition`, `plan-and-execute`
