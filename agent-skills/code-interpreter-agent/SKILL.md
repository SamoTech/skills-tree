---
name: code-interpreter-agent
description: Run iterative code analysis or execution with explicit state, tool boundaries, output limits, and verification between iterations.
metadata:
  source: skills/05-code/code-interpreter-agent.md
  category: 05-code
---

# Code Interpreter Agent

## Description

Run iterative code analysis or execution with explicit state, tool boundaries, output limits, and verification between iterations.

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
state = {'iterations': 0, 'verified': False}
state['iterations'] += 1
state['verified'] = (2 + 2 == 4)
assert state['verified'] and state['iterations'] == 1
print(state)
```

## Failure modes

- Implementing behavior not supported by the requirements.
- Changing unrelated code.
- Skipping regression or security verification.
- Claiming correctness without evidence.

## Related

- `code-execution-sandbox.md`
- `repl-interaction.md`
- `self-correction.md`

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository validation and security workflows

Evidence status: repository-backed implementation guidance; no benchmark claim.
