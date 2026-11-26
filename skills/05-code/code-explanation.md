---
title: "Code Explanation"
category: 05-code
level: basic
stability: stable
version: v2
description: "Explain code by tracing inputs, control flow, state changes, dependencies, and observable outputs without inventing behavior."
added: "2026-09"
related: [code-search, debugging, documentation-generation]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-code-explanation.json)

# Code Explanation

**Category:** `code`
**Skill Level:** `basic`
**Stability:** `stable`
**Added:** 2026-09

### Description

Explain code by tracing inputs, control flow, state changes, dependencies, and observable outputs without inventing behavior. The skill is evidence-first: inspect actual state before acting, preserve existing contracts, and verify the result before reporting completion.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | code | string | The source under explanation, with its direct dependencies identified |
| Input | focus | list of string | Aspects to explain: control flow, state, dependencies, outputs |
| Output | explanation | object | Step-by-step trace from a representative input to observable output |
| Output | uncertainty | list of string | Behavior that could not be verified statically, labeled as inference |

### Procedure
1. Read the code and its direct dependencies; do not infer behavior from names alone.
2. Trace a representative input through the control flow step by step.
3. Record state changes and observable outputs at each step.
4. Separate verified behavior from inference and label every inference as such.
5. Cross-check the explanation against tests or a quick execution where available.

### Example

```python
source = {'x': None, 'y': None}
trace = []
trace.append('assign x = 2'); source['x'] = 2
trace.append('compute y = x + 3'); source['y'] = source['x'] + 3
assert trace == ['assign x = 2', 'compute y = x + 3']
assert source['y'] == 5
print(trace, source['y'])
```

### Related Skills

- [Code Search](code-search.md) - locate the code and its callers first
- [Debugging](debugging.md) - a verified explanation feeds diagnosis
- [Documentation Generation](documentation-generation.md) - verified explanations become documentation

## Failure Modes

- Inventing behavior not present in the source.
- Explaining from identifiers instead of execution paths.
- Presenting inference as verified fact.
- Ignoring side effects in called dependencies.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic trace example, an execution procedure, and corpus-verified related links (replaced the non-corpus code-reading.md link).
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
