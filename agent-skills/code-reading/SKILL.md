---
name: code-reading
description: Inspect source code to identify purpose, structure, dependencies, control flow, and likely defects. Use before debugging, refactoring, review, or architecture changes.
license: MIT
metadata:
  source: skills/01-perception/code-reading.md
  version: "v2"
---

# Code Reading

1. Identify the language and entry points.
2. Build a file/module map before making claims about behavior.
3. Extract functions, classes, imports, interfaces, and side effects.
4. Trace relevant control and data flow for the requested task.
5. Separate observed behavior from suspected defects.
6. Cite file paths and symbols for important findings.
7. Do not execute untrusted code merely to understand it.

## Failure modes

- Incomplete context: request or inspect referenced modules before concluding.
- Generated or dynamic code: mark inferred relationships as uncertain.
- Security-sensitive behavior: prefer static inspection and sandboxed verification.

## Evidence

- https://docs.python.org/3/library/ast.html
- https://docs.python.org/3/library/inspect.html

Evidence status: these references support implementation guidance; no performance benchmark is claimed without reproducible benchmark data.
