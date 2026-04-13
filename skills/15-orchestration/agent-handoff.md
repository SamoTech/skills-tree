---
title: "Agent Handoff"
category: 15-orchestration
level: advanced
stability: stable
description: "Apply agent handoff in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-15-orchestration-agent-handoff.json)

# Agent Handoff

**Category:** `orchestration`  
**Skill Level:** `advanced`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Transfer task context, memory, and control from one agent to another cleanly — used in multi-agent pipelines and triage systems.

### Example

```python
# OpenAI Swarm / Agents SDK style handoff
def triage_agent(context):
    if context['topic'] == 'billing':
        return handoff_to(billing_agent, context)
    return handoff_to(support_agent, context)
```

### Frameworks

- OpenAI Agents SDK
- LangGraph
- AutoGen

### Related Skills

- [Subagent Spawning](subagent-spawning.md)
- [Role Assignment](role-assignment.md)
