---
title: "Code Search"
category: 05-code
level: basic
stability: stable
description: "Locate relevant code by explicit symbol, behavior, dependency, or file criteria and verify matches before editing."
added: "2026-09"
related: [git-diff-reading, code-reading]
---

# Code Search

## Description

Locate relevant code by explicit symbol, behavior, dependency, or file criteria and verify matches before editing.

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
files = ['src/api.py', 'tests/test_api.py']
matches = [f for f in files if 'api' in f]
assert len(matches) == 2
print(matches)
```

## Failure modes

- Implementing behavior not supported by the requirements.
- Changing unrelated code.
- Skipping regression or security verification.
- Claiming correctness without evidence.

## Related

- `git-diff-reading.md`
- `code-reading.md`

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository validation and security workflows

Evidence status: repository-backed implementation guidance; no benchmark claim.
