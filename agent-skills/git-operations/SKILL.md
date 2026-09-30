---
name: git-operations
description: Perform Git operations with explicit branch, commit, merge, and recovery intent while preserving repository history and state.
license: MIT
metadata:
  source: skills/05-code/git-operations.md
  version: "v2"
---

# Git Operations

1. Inspect repository status and target refs.
2. Confirm the intended operation and recovery constraints.
3. Perform the smallest appropriate Git operation.
4. Inspect the resulting history and working state.
5. Verify the target branch or commit before reporting completion.

## Failure modes
- Wrong target ref.
- Lost uncommitted work.
- Unexpected history rewrite.
- Unverified merge or recovery state.

## Evidence
Canonical skill: skills/05-code/git-operations.md
Repository governance: AI_CONSTITUTION.md
