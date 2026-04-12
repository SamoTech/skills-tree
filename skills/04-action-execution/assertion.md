# Assertion / Verification

**Category:** `action-execution`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Verify that a condition or expected state is true before or after an action — used for guard clauses, test validation, and workflow checkpoints.

### Example

```python
def assert_file_exists(path):
    from pathlib import Path
    assert Path(path).exists(), f'Expected file not found: {path}'

def assert_status_ok(response):
    assert response.status_code == 200, f'Bad status: {response.status_code}'
```

### Related Skills

- [Unit Test Generation](../05-code/unit-test-generation.md)
- [Self-Correction](../02-reasoning/self-correction.md)
