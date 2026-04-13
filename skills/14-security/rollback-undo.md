---
title: "Usage"
category: 14-security
level: advanced
stability: stable
description: "Apply usage in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-14-security-rollback-undo.json)

**Category:** Security & Safety
**Skill Level:** Advanced
**Stability:** stable
**Added:** 2025-03

### Description
Captures a reversible snapshot of state before performing destructive operations, and restores it on failure or explicit undo. Implements the Command pattern with `execute()` and `rollback()` methods for file edits, database mutations, and API side-effects.

### Example
```python
from pathlib import Path
import shutil, tempfile
from abc import ABC, abstractmethod

class ReversibleAction(ABC):
    @abstractmethod
    def execute(self) -> None: ...
    @abstractmethod
    def rollback(self) -> None: ...

class FileWrite(ReversibleAction):
    def __init__(self, path: str, new_content: str):
        self.path = Path(path)
        self.new_content = new_content
        self._backup: str | None = None

    def execute(self) -> None:
        if self.path.exists():
            self._backup = self.path.read_text()
        self.path.write_text(self.new_content)
        print(f"Written: {self.path}")

    def rollback(self) -> None:
        if self._backup is not None:
            self.path.write_text(self._backup)
            print(f"Restored: {self.path}")
        else:
            self.path.unlink(missing_ok=True)
            print(f"Deleted (was new): {self.path}")

# Usage
action = FileWrite("/tmp/config.json", '{"debug": true}')
action.execute()
# ... something goes wrong ...
action.rollback()
```

### Related Skills
- [Audit Logging](audit-logging.md)
- [Permission Checking](permission-checking.md)
- [Human-in-the-Loop Escalation](human-in-loop.md)
