# File Append

**Category:** `action-execution`  
**Skill Level:** `basic`  
**Stability:** `stable`

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
