---
title: "Code Generation"
category: 05-code
level: intermediate
stability: stable
description: "Generate maintainable code from explicit requirements, interfaces, constraints, tests, and repository conventions."
added: "2026-09"
related: [algorithm-design, code-review, unit-test-generation]
---

# Code Generation

## Description

Generate maintainable code from explicit requirements, interfaces, constraints, tests, and repository conventions.

## When to Use

- Use when the code task has explicit acceptance criteria.
- Preserve repository conventions and existing security gates.
- Verify behavior before reporting completion.

## Inputs / outputs / failure modes

| Input | Output | Failure mode |
|---|---|---|
| Requirements | Code or analysis | Ambiguous requirement |
| Repository context | Compatible change | Convention mismatch |
| Tests/evidence | Verification result | Regression |
| Security constraints | Safe implementation | Gate bypass |

## Runnable Example

```python
def generated_add(a, b):
    return a + b

assert generated_add(2, 3) == 5
print('generated behavior verified')
```

## Failure modes

- Implementing behavior not supported by the requirements.
- Changing unrelated code.
- Skipping regression or security verification.
- Claiming correctness without evidence.

## Related

- `algorithm-design.md`
- `code-review.md`
- `unit-test-generation.md`

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository validation and security workflows

Evidence status: repository-backed implementation guidance; no benchmark claim.
