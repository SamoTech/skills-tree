---
name: code-translation
description: Translate source code between programming languages while preserving behavior, interfaces, and documented constraints.
metadata:
  source: skills/05-code/code-translation.md
  category: 05-code
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-code-translation.json)

# Code Translation

**Category:** `code`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2026-09

### Description

Translate source code between programming languages while preserving behavior, interfaces, and documented constraints. The skill is evidence-first: inspect actual state before acting, preserve existing contracts, and verify the result before reporting completion.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | source_code | string | Code in the source language, with its tests and interfaces identified |
| Input | target_language | string | Destination language and version |
| Input | constraints | list of string | Interfaces, runtime limits, and semantics that must be preserved |
| Output | translated_code | string | Target-language code preserving the stated interfaces |
| Output | parity_notes | list of string | Behavior preserved, deviations, and anything unverified |

### Procedure
1. Capture the source behavior first: interfaces, edge cases, and the tests that pin it.
2. Map language-specific constructs explicitly: error handling, concurrency, numeric semantics, truthiness.
3. Translate while preserving interfaces and documented constraints; do not change semantics mid-translation.
4. Port or re-implement the pinning tests in the target language.
5. Run the ported tests and record parity: identical, equivalent, or intentionally different.
6. Flag constructs with no faithful equivalent instead of silently approximating them.

### Example

```python
semantic_map = {'int_div': 'Math.trunc(a / b)', 'truthiness': 'Boolean(value)', 'error_model': 'throw/catch'}
assert semantic_map['int_div'].startswith('Math.trunc')
print('construct mapping recorded before translation')
```

### Related Skills

- [Code Generation](code-generation.md) - target-language idioms and conventions
- [Code Explanation](code-explanation.md) - understand source behavior before translating it
- [Refactoring](refactoring.md) - separate cleanup from translation

## Failure Modes

- Translating syntax but not semantics: integer division, truthiness, or error models differ.
- Silently dropping behavior that has no target equivalent.
- Skipping the ported tests and claiming parity unverified.
- Improving or restructuring the code during translation instead of preserving it.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (removed the non-corpus AI_CONSTITUTION.md evidence pointer).
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
