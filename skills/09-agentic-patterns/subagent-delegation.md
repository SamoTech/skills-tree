---
title: "Subagent Delegation"
category: 09-agentic-patterns
level: advanced
stability: stable
description: "Apply subagent delegation in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-09-agentic-patterns-subagent-delegation.json)

# Subagent Delegation

**Category:** `agentic-patterns`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

An orchestrator agent decomposes a task and delegates subtasks to specialized subagents, then aggregates their results into a final response.

### Example

```
Orchestrator: "Produce a market research report on EVs"
  │
  ├── Research Agent  → gathers web data on EV market
  ├── Analysis Agent  → runs statistical summaries
  ├── Writing Agent   → drafts the report
  └── Review Agent    → proofreads and formats

Orchestrator: merges all outputs → final report
```

### Related Skills

- [Plan and Execute](plan-and-execute.md)
- [A2A Tool](../07-tool-use/a2a-tool.md)
- [Agent Handoff](../15-orchestration/agent-handoff.md)
