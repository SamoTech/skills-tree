---
name: file-delete
description: Delete a verified filesystem target only after path validation, scope checks, and any required approval boundary.
license: MIT
metadata:
  source: skills/04-action-execution/file-delete.md
  version: "v2"
---

# File Delete

1. Resolve the intended target path.
2. Verify it is inside the permitted root.
3. Apply the required destructive-action approval boundary.
4. Delete only the verified target and report the resulting state.

## Failure modes

- Path traversal outside the allowed root.
- Symlink escape.
- Recursive deletion without explicit scope.
- Reporting deletion without verifying the resulting state.

## Evidence

- skills/04-action-execution/file-delete.md
- AI_CONSTITUTION.md
- AGENTS.md

Evidence status: repository-backed implementation guidance; no benchmark claim.
