# File Delete

**Category:** `action-execution`  
**Skill Level:** `basic`  
**Stability:** `stable`

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
