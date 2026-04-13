![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-04-action-execution-file-append.json)

# File Append

**Category:** `action-execution`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Append content to an existing file without overwriting it — used for logs, running records, and incremental output.

### Example

```python
from pathlib import Path

log = Path('agent.log')
log.open('a').write('2026-04-11 23:00 — Task completed\n')
```

### Related Skills

- [File Write](file-write.md)
- [File Delete](file-delete.md)
