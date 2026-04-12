**Category:** Orchestration
**Skill Level:** Advanced
**Stability:** stable
**Added:** 2025-03

### Description
Organises agents in a tree hierarchy where an orchestrator agent decomposes tasks and delegates subtasks to worker agents, which may themselves spawn further sub-workers. Implements result aggregation, timeout propagation, and failure isolation per subtree.

### Example
```python
import anthropic
import asyncio
from dataclasses import dataclass

client = anthropic.Anthropic()

@dataclass
class AgentNode:
    name: str
    role: str
    children: list['AgentNode'] = None

    def __post_init__(self):
        if self.children is None:
            self.children = []

def run_agent(role: str, task: str) -> str:
    msg = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=256,
        system=f"You are a {role}. Be concise.",
        messages=[{"role": "user", "content": task}]
    )
    return msg.content[0].text

def orchestrate(topic: str) -> dict:
    # Level 1: orchestrator decomposes
    plan = run_agent("project orchestrator", f"List 3 research subtopics for: {topic}. JSON list only.")

    # Level 2: specialist workers (simulated parallel)
    results = {}
    for subtask in ["history", "current state", "future outlook"]:
        results[subtask] = run_agent("domain researcher", f"Summarise {subtask} of: {topic}")

    # Level 3: aggregator
    summary = run_agent("editor", f"Combine these findings into a brief report: {results}")
    return {"plan": plan, "sections": results, "summary": summary}

result = orchestrate("AI multi-agent systems")
print(result["summary"])
```

### Related Skills
- [Subagent Spawning](subagent-spawning.md)
- [Role Assignment](role-assignment.md)
- [Agent Handoff](agent-handoff.md)
