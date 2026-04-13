---
title: "Shell Command Execution"
category: 04-action-execution
level: intermediate
stability: stable
description: "Apply shell command execution in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-04-action-execution-shell-command.json)

# Shell Command Execution

**Category:** `action-execution`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Run shell commands (bash, zsh, sh, cmd) in the host or sandboxed environment and capture stdout/stderr.

### Example

```python
import subprocess
result = subprocess.run(
    ['git', 'log', '--oneline', '-10'],
    capture_output=True, text=True, check=True
)
print(result.stdout)
```

### Frameworks

- Open Interpreter
- LangChain `ShellTool`
- E2B sandboxed shell

### Related Skills

- [Code Execution (Sandbox)](../05-code/code-execution-sandbox.md)
- [Process Management](process-management.md)
