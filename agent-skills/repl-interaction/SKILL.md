---
name: repl-interaction
description: Use an interactive language environment to inspect behavior, test hypotheses, and validate small code changes without replacing reproducible project tests.
metadata:
  source: skills/05-code/repl-interaction.md
  category: 05-code
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-repl-interaction.json)

# Repl Interaction

**Category:** `code`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2026-09

### Description

Use an interactive language environment to inspect behavior, test hypotheses, and validate small code changes without replacing reproducible project tests. The skill is evidence-first: inspect actual state before acting, preserve existing contracts, and verify the result before reporting completion.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | hypothesis | string | The behavior question the session will answer |
| Input | sample_data | object | Controlled inputs; no live credentials or production data |
| Output | findings | list of object | Reproducible observations, each with the exact input that produced it |
| Output | promotion | object | Durable findings captured as source changes or tests |

### Procedure
1. Start from a written hypothesis and controlled sample data.
2. Keep experiments isolated: fresh namespace or scratch module; no writes to project state.
3. Record each observation with the exact input that produced it.
4. Distinguish environment-specific results from general behavior.
5. Promote durable findings into source changes or tests; a REPL session is not project verification.

### Example

```python
value = 21
result = value * 2
assert result == 42
print('observation recorded with its exact input; promote to a test')
```

### Related Skills

- [Debugging](debugging.md) - REPL probes are one tool inside a diagnosis procedure
- [Unit Test Generation](unit-test-generation.md) - promote findings into regression tests
- [Code Execution Sandbox](code-execution-sandbox.md) - isolate exploratory execution

## Failure Modes

- Relying on hidden interactive state.
- Making destructive changes during exploration.
- Treating a REPL result as full project verification.
- Failing to capture a reproducible experiment.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links.
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
