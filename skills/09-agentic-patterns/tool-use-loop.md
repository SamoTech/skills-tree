---
title: Tool-Use Loop
category: 09-agentic-patterns
level: intermediate
stability: stable
description: A parallel-tool variant of ReAct where multiple tools may be called simultaneously in each step.
added: "2025-03"
version: v1
prerequisites:
  - 09-agentic-patterns/react
---

# Tool-Use Loop

## Description

A parallel-tool variant of the ReAct loop. Where ReAct calls exactly one tool per step, the Tool-Use Loop may dispatch multiple tool calls simultaneously in a single model turn, collecting all observations before the next reasoning step.

## Related Skills

- [ReAct](react.md) — sequential single-tool baseline this pattern extends
- [Plan-and-Execute](plan-and-execute.md) — planning variant

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Initial entry |
| 2026-06 | v1.1 | Added prerequisites field (INITIATIVE-005) |
