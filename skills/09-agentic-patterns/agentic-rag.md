---
title: "Agentic RAG"
category: 09-agentic-patterns
level: advanced
stability: stable
description: "Apply agentic rag in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-09-agentic-patterns-agentic-rag.json)

# Agentic RAG

**Category:** `agentic-patterns`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Extends basic RAG with an agent that decides *whether* to retrieve, *what* to retrieve, *when* to re-retrieve, and *how many* iterations are needed — dynamically improving answer quality.

### Example

```
Question: "Compare LangGraph and CrewAI for multi-agent systems"

Iteration 1: retrieve("LangGraph multi-agent") → 5 docs
Iteration 2: retrieve("CrewAI multi-agent") → 5 docs
Iteration 3: agent decides: enough context → generate answer
Answer: [grounded comparison]
```

### Related Skills

- [RAG Pipeline](rag-pipeline.md)
- [RAG](../03-memory/rag.md)
- [ReAct](react.md)
