---
title: "File Delete"
category: 04-action-execution
level: basic
stability: stable
description: "Apply file delete in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-04-action-execution-file-delete.json)

# File Delete

**Category:** `action-execution`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Delete a file or directory from the file system as part of an agent workflow (cleanup, rollback, temp file removal).

### Example

```python
from pathlib import Path

tmp = Path('output/temp_result.json')
if tmp.exists():
    tmp.unlink()
    print(f'Deleted: {tmp}')
```

### Related Skills

- [File Write](file-write.md)
- [File Append](file-append.md)
- [Rollback / Undo](../14-security/rollback-undo.md)
