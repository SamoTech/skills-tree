# File System Reading

**Category:** `perception`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

List, traverse, and read files and directories from a local or remote file system.

### Example

```python
from pathlib import Path
files = list(Path('./skills').rglob('*.md'))
for f in files:
    print(f.name, f.read_text()[:100])
```

### Related Skills

- [File Write](../04-action-execution/file-write.md)
- [PDF Parsing](pdf-parsing.md)
