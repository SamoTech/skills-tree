![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-09-agentic-patterns-memory-augmented.json)

# Memory-Augmented Agent

**Category:** `agentic-patterns`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Agent maintains persistent external memory (episodic, semantic, or procedural) across sessions. Reads relevant memories before acting and writes new information after each interaction.

### Example

```python
# On each turn:
relevant = memory_store.search(user_message, k=5)  # read
response = llm.invoke(context=relevant + [user_message])
memory_store.upsert(user_message, response)         # write
```

### Memory Types

| Type | Description | Example |
|---|---|---|
| Episodic | Past conversations | "User prefers Python" |
| Semantic | World knowledge | Domain facts |
| Procedural | How-to steps | Verified workflows |

### Related Skills

- [RAG Pipeline](rag-pipeline.md)
- [Long-Term Memory](../03-memory/long-term-memory.md)
- [Vector DB Tool](../07-tool-use/vector-db-tool.md)
