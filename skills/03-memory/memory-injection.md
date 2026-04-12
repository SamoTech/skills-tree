# Memory Injection

**Category:** `memory`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Insert retrieved memories or facts directly into the agent prompt context before inference to ground the response.

### Example

```python
def build_prompt(user_query, memory_store):
    relevant = retrieve_top_k(user_query, memory_store, k=5)
    block = '\n'.join(f'- {m}' for m in relevant)
    return f'Relevant context:\n{block}\n\nUser: {user_query}'
```

### Related Skills

- [RAG](rag.md)
- [Working Memory](working-memory.md)
- [Vector Store Retrieval](vector-store-retrieval.md)
