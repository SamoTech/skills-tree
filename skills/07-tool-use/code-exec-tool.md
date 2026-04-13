---
title: "Code Execution Tool"
category: 07-tool-use
level: advanced
stability: stable
description: "Apply code execution tool in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-code-exec-tool.json)

# Code Execution Tool

**Category:** `tool-use`  
**Skill Level:** `advanced`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Execute code in a sandboxed environment as an agent tool and capture stdout, stderr, and return values.

### Example

```python
def execute_python(code: str) -> dict:
    import subprocess, tempfile
    with tempfile.NamedTemporaryFile(suffix='.py', mode='w', delete=False) as f:
        f.write(code)
        fname = f.name
    result = subprocess.run(['python', fname], capture_output=True, text=True, timeout=10)
    return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
```

### Related Skills

- [Code Execution Sandbox](../05-code/code-execution-sandbox.md)
- [Sandboxed Execution](../14-security/sandboxed-execution.md)
