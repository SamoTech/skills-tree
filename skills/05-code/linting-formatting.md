---
title: "Linting Formatting"
category: 05-code
level: intermediate
stability: stable
version: v2
description: "Apply repository-defined linting and formatting rules consistently while preserving behavior and minimizing unrelated churn."
added: "2026-09"
related: [code-review, refactoring]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-linting-formatting.json)

# Linting Formatting

**Category:** `code`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2026-09

### Description

Apply repository-defined linting and formatting rules consistently while preserving behavior and minimizing unrelated churn. The skill is evidence-first: inspect actual state before acting, preserve existing contracts, and verify the result before reporting completion.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | scope | list of string | The files or directories the style change covers |
| Input | config | object | Repository lint/format configuration and the tool versions it expects |
| Output | formatted_code | object | Lint-clean code with behavior preserved and churn bounded to scope |
| Output | verification | object | Clean lint run plus test-suite output |

### Procedure
1. Read the repository lint/format configuration and pin the tool versions it expects.
2. Run the formatter and linter on the declared scope only.
3. Review the diff: formatting must not change behavior; investigate any semantic-looking change.
4. Keep style changes in commits separate from functional changes.
5. Re-run the linter and the test suite to confirm cleanliness without regressions.

### Example

```python
from pathlib import Path

py_files = sorted(p.name for p in Path('.').glob('*.py'))
print('files in formatting scope:', py_files)
print('use the repository-configured lint and format commands and versions')
```

### Related Skills

- [Code Review](code-review.md) - style findings separated from correctness findings
- [Refactoring](refactoring.md) - structural changes stay separate from style changes

## Failure Modes

- Formatting with an incompatible tool version, causing churn.
- Mixing style changes with functional changes.
- Ignoring repository configuration in favor of personal defaults.
- Treating lint-clean output as proof of functional correctness.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic scope example, an execution procedure, and corpus-verified related links.
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
