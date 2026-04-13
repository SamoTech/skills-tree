---
title: "Agent-to-Agent Tool (A2A)"
category: 07-tool-use
level: advanced
stability: experimental
description: "Apply agent-to-agent tool (a2a) in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-a2a-tool.json)

# Agent-to-Agent Tool (A2A)

**Category:** `tool-use`  
**Skill Level:** `advanced`  
**Stability:** `experimental`
**Added:** 2025-03

### Description

Call another AI agent as a tool — delegating sub-tasks to specialized agents via the Google A2A protocol or custom RPC interfaces.

### Example

```python
# Using Google A2A protocol to call a specialized research agent
agent_client = A2AClient(endpoint="https://research-agent.example.com")
response = await agent_client.send_task({
    "id": "task-001",
    "message": {
        "role": "user",
        "parts": [{"text": "Summarize the latest AI papers on RAG from 2025"}]
    }
})
print(response.result.parts[0].text)
```

### Architecture

```
Orchestrator Agent
  │
  ├── A2A call → Research Agent
  ├── A2A call → Code Agent
  └── A2A call → Writer Agent
```

### Related Skills

- [MCP Tool](mcp-tool.md)
- [Subagent Spawning](../15-orchestration/subagent-spawning.md)
- [Agent Handoff](../15-orchestration/agent-handoff.md)
