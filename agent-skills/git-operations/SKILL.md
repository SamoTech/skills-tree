---
name: git-operations
description: Perform Git operations with explicit branch, commit, merge, and recovery intent while preserving repository history and state.
metadata:
  source: skills/05-code/git-operations.md
  category: 05-code
---

## Description
Perform Git operations with explicit branch, commit, merge, and recovery intent while preserving repository history and repository governance. Verify the target ref and working state before destructive or history-changing actions.

## When to Use
Use when branching, committing, merging, rebasing, reverting, recovering, or inspecting Git state is required.

## Inputs / outputs / failure modes

| Area | Guidance |
|---|---|
| Inputs | Repository state, target refs, intended change, and recovery constraints. |
| Outputs | Correct Git state with traceable history and verification evidence. |
| Failure modes | Wrong target ref, lost changes, unexpected history rewrite, or unverified merge state. |

## Runnable Example

```python
import subprocess

result = subprocess.run(['git', 'status', '--short'], text=True, capture_output=True)
print(result.stdout)
print('inspect state before mutating repository history')
```

## Failure modes
- Running history-changing commands without confirming the target.
- Losing uncommitted work.
- Merging stale refs.
- Reporting a Git operation complete without checking the resulting state.

## Related
- 05-code
- AI_CONSTITUTION.md
- meta/AGENT_OPERATING_MODEL.md

## Evidence
Repository-backed implementation guidance grounded in repository governance and validation workflows; no external benchmark claim is made.
