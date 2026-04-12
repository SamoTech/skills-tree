# File Write

**Category:** `action-execution`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Create or overwrite a file on disk with given content.

### Example

```python
with open('output/report.md', 'w', encoding='utf-8') as f:
    f.write(content)
```

### Related Skills

- [File Append](file-append.md)
- [File Delete](file-delete.md)
- [Shell Command Execution](shell-command.md)
