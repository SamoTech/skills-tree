---
title: "Regex Generation"
category: 05-code
level: advanced
stability: stable
version: v2
description: "Generate regular expressions from explicit matching and rejection requirements and validate them against representative cases."
added: "2026-09"
related: [unit-test-generation, debugging]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-regex-generation.json)

# Regex Generation

**Category:** `code`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2026-09

### Description

Generate regular expressions from explicit matching and rejection requirements and validate them against representative cases. The skill is evidence-first: inspect actual state before acting, preserve existing contracts, and verify the result before reporting completion.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | requirements | object | Explicit must-match and must-reject example sets |
| Input | engine | object | Target regex engine and flags (PCRE, RE2, Python re) |
| Output | pattern | object | A readable, documented pattern targeting the stated engine |
| Output | tests | list | Positive and negative cases, including boundary inputs |

### Procedure
1. Collect explicit positive and negative examples before writing the pattern.
2. Write the simplest pattern that satisfies the requirement; prefer readability over cleverness.
3. Target the actual engine syntax and note incompatibilities (backreferences, lookbehind, POSIX classes).
4. Test every positive and negative case, including empty, unicode, and multiline boundaries.
5. Check for pathological backtracking on adversarial input; prefer atomic constructs or a parser when risk exists.

### Example

```python
import re

pattern = re.compile(r'^[A-Z]{2}-[0-9]{4}$')
cases = {'AB-1234': True, 'ab-1234': False, 'AB-123': False, '': False}
for value, expected in cases.items():
    assert bool(pattern.fullmatch(value)) is expected, value
print('all positive and negative cases pass')
```

### Related Skills

- [Unit Test Generation](unit-test-generation.md) - pin pattern behavior with tests
- [Debugging](debugging.md) - isolate overmatching and undermatching

## Failure Modes

- Deriving a pattern without explicit positive and negative examples.
- Ignoring the target engine and shipping incompatible syntax.
- Testing only positive cases.
- Creating patterns with pathological backtracking.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic two-sided test example, an execution procedure, and corpus-verified related links.
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
