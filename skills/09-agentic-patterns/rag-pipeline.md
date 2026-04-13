---
title: "RAG Pipeline"
category: 09-agentic-patterns
level: intermediate
stability: stable
description: "Apply rag pipeline in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-09-agentic-patterns-rag-pipeline.json)

# RAG Pipeline

**Category:** `agentic-patterns`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2025-03

### Description

Retrieve-Augmented Generation: embed user query → retrieve top-k relevant documents from a vector store → inject them into the LLM context → generate a grounded answer.

### Example

```python
query = "What is LangGraph?"
embedding = embed(query)
docs = vector_store.search(embedding, k=5)
context = "\n\n".join(docs)
response = llm.invoke(f"Context:\n{context}\n\nQuestion: {query}")
```

### Related Skills

- [Agentic RAG](agentic-rag.md)
- [RAG](../03-memory/rag.md)
- [Vector DB Tool](../07-tool-use/vector-db-tool.md)
