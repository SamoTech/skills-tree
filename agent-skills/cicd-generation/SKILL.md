---
name: cicd-generation
description: Generate CI/CD configuration from explicit build, test, security, artifact, and deployment requirements without weakening gates.
metadata:
  source: skills/05-code/cicd-generation.md
  category: 05-code
---

# Cicd Generation

## Description

Generate CI/CD configuration from explicit build, test, security, artifact, and deployment requirements without weakening gates.

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
pipeline = {'test': True, 'security': True, 'build': True, 'deploy': True}
assert all(pipeline.values())
print('required pipeline gates present')
```

## Failure modes

- Implementing behavior not supported by the requirements.
- Changing unrelated code.
- Skipping regression or security verification.
- Claiming correctness without evidence.

## Related

- `shell-command.md`
- `security-scanning.md`
- `dependency-auditor.md`

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository validation and security workflows

Evidence status: repository-backed implementation guidance; no benchmark claim.
