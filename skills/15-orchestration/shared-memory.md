![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-15-orchestration-shared-memory.json)

**Category:** Orchestration
**Skill Level:** Advanced
**Stability:** stable
**Added:** 2025-03

### Description
Provides a central memory store (blackboard) that multiple agents can read from and write to concurrently. Supports key-value storage, pub/sub notifications on key changes, and optimistic locking to prevent race conditions.

### Example
```python
import threading
from typing import Any

class Blackboard:
    def __init__(self):
        self._store: dict[str, Any] = {}
        self._lock = threading.RLock()
        self._watchers: dict[str, list] = {}

    def write(self, key: str, value: Any) -> None:
        with self._lock:
            self._store[key] = value
            for cb in self._watchers.get(key, []):
                threading.Thread(target=cb, args=(key, value), daemon=True).start()

    def read(self, key: str, default: Any = None) -> Any:
        with self._lock:
            return self._store.get(key, default)

    def watch(self, key: str, callback) -> None:
        self._watchers.setdefault(key, []).append(callback)

# Usage
board = Blackboard()

def on_research_done(key, value):
    print(f"[Writer Agent] Research completed: {value}")

board.watch("research_result", on_research_done)
board.write("research_result", "AI agents survey: 42 papers found")
board.write("task_status", "writing")
print(board.read("task_status"))  # writing
```

### Related Skills
- [Agent Communication](agent-communication.md)
- [Memory Augmented](../09-agentic-patterns/memory-augmented.md)
- [Parallel Task Execution](parallel-execution.md)
