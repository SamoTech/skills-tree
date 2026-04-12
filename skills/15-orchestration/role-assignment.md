**Category:** Orchestration
**Skill Level:** Intermediate
**Stability:** stable
**Added:** 2025-03

### Description
Dynamically assigns specialised roles to agents based on task requirements and agent capabilities. Maintains a role registry, assigns agents at spawn time, and injects role-specific system prompts to shape agent behaviour.

### Example
```python
import anthropic
from dataclasses import dataclass

client = anthropic.Anthropic()

@dataclass
class AgentRole:
    name: str
    system_prompt: str

ROLES = {
    "researcher": AgentRole(
        name="Researcher",
        system_prompt="You are an expert researcher. Find accurate information and cite sources."
    ),
    "critic": AgentRole(
        name="Critic",
        system_prompt="You are a critical reviewer. Find flaws, gaps, and suggest improvements."
    ),
    "writer": AgentRole(
        name="Writer",
        system_prompt="You are a clear technical writer. Transform findings into readable prose."
    ),
}

def run_agent(role_id: str, task: str) -> str:
    role = ROLES[role_id]
    msg = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=512,
        system=role.system_prompt,
        messages=[{"role": "user", "content": task}]
    )
    return msg.content[0].text

research = run_agent("researcher", "Summarise recent advances in multi-agent LLMs")
print(run_agent("critic", f"Review this research summary:\n{research}"))
```

### Related Skills
- [Agent Handoff](agent-handoff.md)
- [Subagent Spawning](subagent-spawning.md)
- [Conditional Branching](conditional-branching.md)
