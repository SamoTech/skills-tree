---
name: code-explanation
description: Explain code by tracing inputs, control flow, state changes, dependencies, and observable outputs without inventing behavior.
metadata:
  source: skills/05-code/code-explanation.md
  category: 05-code
---

# Code Explanation

## Description

Explain code by tracing inputs, control flow, state changes, dependencies, and observable outputs without inventing behavior.

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
source = 'x = 2\ny = x + 3'
steps = ['assign x', 'compute y']
assert steps == ['assign x', 'compute y']
print('explanation trace prepared')
```

## Failure modes

- Implementing behavior not supported by the requirements.
- Changing unrelated code.
- Skipping regression or security verification.
- Claiming correctness without evidence.

## Related

- `code-reading.md`
- `documentation-generation.md`

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository validation and security workflows

Evidence status: repository-backed implementation guidance; no benchmark claim.
