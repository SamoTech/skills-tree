---
title: Repl Interaction
category: 05-code
level: intermediate
stability: stable
description: Use an interactive language environment to inspect behavior, test hypotheses, and validate small code changes without replacing reproducible project tests.
added: "2026-09"
related: [05-code]
---

## Description
Use an interactive language environment to inspect behavior, test hypotheses, and validate small code changes without replacing reproducible project tests. Keep experiments isolated and convert durable findings into source or tests.

## When to Use
Use for exploratory debugging, API inspection, small transformations, or hypothesis testing.

## Inputs / outputs / failure modes

| Area | Guidance |
|---|---|
| Inputs | Runtime, relevant modules, hypothesis, and controlled sample data. |
| Outputs | Reproducible findings, code, or tests derived from the experiment. |
| Failure modes | Hidden state, environment mismatch, non-reproducible sessions, or accidental side effects. |

## Runnable Example

```python
value = 21
result = value * 2
print(result)
print('promote useful experiments into reproducible tests')
```

## Failure modes
- Relying on hidden interactive state.
- Making destructive changes during exploration.
- Treating a REPL result as full project verification.
- Failing to capture a reproducible experiment.

## Related
- 05-code
- AI_CONSTITUTION.md
- meta/AGENT_OPERATING_MODEL.md

## Evidence
Repository-backed implementation guidance grounded in repository governance and validation workflows; no external benchmark claim is made.
