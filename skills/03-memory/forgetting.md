# Forgetting / Memory Pruning

**Category:** `memory`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

### Description

Selectively remove or decay stale, irrelevant, or low-importance memories to keep the context window efficient and focused.

### Example

```python
import time

def prune_old_memories(memory_store, max_age_seconds=3600):
    now = time.time()
    return [m for m in memory_store if now - m['timestamp'] < max_age_seconds]
```

### Related Skills

- [Working Memory](working-memory.md)
- [Memory Summarization](memory-summarization.md)
