# Episodic Memory

**Category:** `memory`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Store and retrieve records of past interactions, events, and actions the agent has taken — enabling learning from history.

### Example

```python
# Store an episode
memory_store.add({
    'timestamp': '2026-04-11T22:00:00',
    'task': 'Deploy API to Fly.io',
    'outcome': 'success',
    'steps_taken': ['wrote Dockerfile', 'ran flyctl deploy']
})
# Retrieve relevant episodes
epochs = memory_store.search('deployment failures')
```

### Related Skills

- [Working Memory](working-memory.md)
- [Cross-Session Persistence](cross-session-persistence.md)
