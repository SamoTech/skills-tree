# Cross-Session Persistence

**Category:** `memory`  
**Skill Level:** `advanced`  
**Stability:** `stable`

### Description

Persist agent memory, state, and context across separate conversation sessions using external storage.

### Example

```python
import json
from pathlib import Path

store_path = Path('memory.json')

def save(key, value):
    data = json.loads(store_path.read_text()) if store_path.exists() else {}
    data[key] = value
    store_path.write_text(json.dumps(data, indent=2))

def load(key):
    if not store_path.exists(): return None
    return json.loads(store_path.read_text()).get(key)
```

### Related Skills

- [User Profile Memory](user-profile-memory.md)
- [Episodic Memory](episodic-memory.md)
- [RAG](rag.md)
