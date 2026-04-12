# Semantic Memory

**Category:** `memory`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Store and retrieve general factual knowledge, concepts, and world knowledge independent of specific events.

### Example

```python
semantic_store = {}

# Store
semantic_store['RAG'] = 'Retrieval-Augmented Generation: grounds LLM responses with retrieved documents.'

# Retrieve
print(semantic_store.get('RAG'))
```

### Related Skills

- [Episodic Memory](episodic-memory.md)
- [Procedural Memory](procedural-memory.md)
- [Vector Store Retrieval](vector-store-retrieval.md)
