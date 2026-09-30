---
title: "Code Review"
category: 05-code
level: intermediate
stability: stable
description: "Review code against correctness, security, maintainability, tests, interfaces, and repository conventions, reporting evidence-backed findings."
added: "2026-09"
related: [security-scanning, git-diff-reading, testing]
---

# Code Review

## Description

Review code against correctness, security, maintainability, tests, interfaces, and repository conventions, reporting evidence-backed findings.

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
diff = {'changed_files': 1, 'tests_updated': True, 'secrets_added': False}
assert diff['tests_updated'] and not diff['secrets_added']
print('review checks satisfied')
```

## Failure modes

- Implementing behavior not supported by the requirements.
- Changing unrelated code.
- Skipping regression or security verification.
- Claiming correctness without evidence.

## Related

- `security-scanning.md`
- `git-diff-reading.md`
- `testing.md`

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository validation and security workflows

Evidence status: repository-backed implementation guidance; no benchmark claim.
