---
title: "File System Tool"
category: 07-tool-use
level: advanced
stability: stable
version: v2
description: "Operate on files through explicit paths, scope checks, content validation, and reversible changes."
added: "2026-09"
related: [tool-guardrails, tool-argument-construction, input-sanitization]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-file-system-tool.json)

# File System Tool

**Category:** `tool-use`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2026-09

### Description

Operate on files through explicit paths, scope checks, content validation, and reversible changes. The invocation is contract-first: validate the tool interface and inputs before calling, and verify the observable outcome afterwards rather than trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | paths | list of string | Explicit absolute or repo-relative paths inside the declared scope |
| Input | operation | enum | read, write, move, or delete, with reversibility noted |
| Output | result | object | Per-path outcome with bytes changed and verification method |
| Output | rollback | object | The previous content or path state enabling reversal |

### Procedure
1. Resolve and canonicalize every path; reject traversal outside the declared scope before touching anything.
2. Record the previous state of every path the operation may change.
3. Validate content before writing; never overwrite user-modified files silently.
4. Prefer atomic operations (write-temp-then-rename) where the runtime supports them.
5. Verify the resulting state by re-reading; report per-path outcomes honestly.
6. Provide the rollback path for any destructive operation.

### Example

```python
scope = '/repo/src'
requested = '/repo/src/util/helpers.py'
canonical = requested.replace('/repo/', '')
assert canonical.startswith('src/')
assert '..' not in requested
print('path inside declared scope; traversal rejected')
```

### Related Skills

- [Tool Guardrails](tool-guardrails.md) - permission boundaries for file operations
- [Tool Argument Construction](tool-argument-construction.md) - well-formed path arguments
- [Input Sanitization](../14-security/input-sanitization.md) - reject path traversal and unsafe content

## Failure Modes

- Path traversal outside the declared scope.
- Silently overwriting user-modified files.
- Destructive operations without a recorded rollback state.
- Reporting success without re-reading the resulting state.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/AI_CONSTITUTION.md pointers where present).
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; provider behavior must be checked against current provider documentation; no benchmark claim is made without reproducible evidence.
