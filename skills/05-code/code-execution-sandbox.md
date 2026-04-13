---
title: "Code Execution (Sandbox)"
category: 05-code
level: intermediate
stability: stable
description: "Apply code execution (sandbox) in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-code-execution-sandbox.json)

# Code Execution (Sandbox)

**Category:** `code`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Run generated code in an isolated sandbox environment and capture stdout, stderr, and return values safely.

### Example

```python
from e2b_code_interpreter import Sandbox
with Sandbox() as sandbox:
    result = sandbox.run_code('print(2 ** 10)')
    print(result.logs.stdout)  # ['1024']
```

### Frameworks

- E2B Code Interpreter
- OpenAI Code Interpreter (Assistants API)
- Modal sandboxes
- Docker containers

### Related Skills

- [Shell Command Execution](../04-action-execution/shell-command.md)
- [REPL Interaction](repl-interaction.md)
