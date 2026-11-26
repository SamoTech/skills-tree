---
title: "Git Operations"
category: 05-code
level: advanced
stability: stable
version: v2
description: "Perform Git operations with explicit branch, commit, merge, and recovery intent while preserving repository history and state."
added: "2026-09"
related: [git-diff-reading, code-review, dependency-management]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-git-operations.json)

# Git Operations

**Category:** `code`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2026-09

### Description

Perform Git operations with explicit branch, commit, merge, and recovery intent while preserving repository history and state. The skill is evidence-first: inspect actual state before acting, preserve existing contracts, and verify the result before reporting completion.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | intent | enum | branch, commit, merge, rebase, revert, recover, or inspect |
| Input | refs | object | Exact target refs; no abbreviated or assumed refs for destructive actions |
| Output | git_state | object | Resulting refs and working tree after the operation |
| Output | evidence | object | Command output confirming the resulting state |

### Procedure
1. Inspect current state (status, branch, remotes) before any mutation.
2. Confirm the exact target ref for every operation; never act on an assumed ref for destructive actions.
3. Protect uncommitted work: stash or commit before history-changing operations.
4. Prefer non-history-rewriting operations on shared branches.
5. After the operation, verify the resulting state with explicit commands and report it.
6. For recovery, identify the pre-operation state first (reflog, backup ref) so the operation stays reversible.

### Example

```python
import subprocess

result = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True)
print('working tree entries:', len(result.stdout.splitlines()))
print('inspect and record state before mutating repository history')
```

### Related Skills

- [Git Diff Reading](../01-perception/git-diff-reading.md) - scope and review the change set
- [Code Review](code-review.md) - review commits before they merge
- [Dependency Management](dependency-management.md) - commit manifest and lockfile together

## Failure Modes

- Running history-changing commands against the wrong ref.
- Losing uncommitted work by not stashing or committing first.
- Merging stale or unverified refs.
- Reporting an operation complete without checking the resulting state.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic state-inspection example, an execution procedure, and corpus-verified related links.
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
