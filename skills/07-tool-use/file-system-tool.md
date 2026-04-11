# File System Tool

**Category:** `tool-use`  
**Skill Level:** `basic`  
**Stability:** `stable`

### Description

Expose file system operations (read, write, list, delete) as structured agent tools with permission checks.

### Example

```python
def read_file(path: str) -> str:
    from pathlib import Path
    p = Path(path)
    assert p.exists(), f'File not found: {path}'
    return p.read_text()

def list_dir(path: str) -> list:
    from pathlib import Path
    return [str(f) for f in Path(path).iterdir()]
```

### Related Skills

- [File System Reading](../01-perception/file-system-reading.md)
- [File Write](../04-action-execution/file-write.md)
