# Agent-to-Agent Tool (A2A)

**Category:** `tool-use`  
**Skill Level:** `advanced`  
**Stability:** `experimental`

### Description

Call another AI agent as a tool — delegating sub-tasks to specialized agents via the Google A2A protocol or custom RPC interfaces.

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
