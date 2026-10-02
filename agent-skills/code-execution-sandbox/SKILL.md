---
name: code-execution-sandbox
description: Execute untrusted or generated code inside an isolated bounded environment with resource, filesystem, network, and timeout controls.
metadata:
  source: skills/05-code/code-execution-sandbox.md
  category: 05-code
---

# Code Execution Sandbox

## Description

Execute untrusted or generated code inside an isolated bounded environment with resource, filesystem, network, and timeout controls.

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
limits = {'timeout': 5, 'network': False, 'filesystem': 'isolated'}
assert limits['timeout'] > 0 and limits['network'] is False
print('sandbox policy validated')
```

## Failure modes

- Implementing behavior not supported by the requirements.
- Changing unrelated code.
- Skipping regression or security verification.
- Claiming correctness without evidence.

## Related

- `shell-command.md`
- `process-management.md`
- `output-guardrails.md`

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository validation and security workflows

Evidence status: repository-backed implementation guidance; no benchmark claim.
