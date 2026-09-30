---
name: drag-and-drop
description: Perform a bounded desktop or browser drag-and-drop action using verified source and destination targets.
license: MIT
metadata:
  source: skills/04-action-execution/drag-drop.md
  version: "v2"
---

# Drag and Drop

1. Identify and verify the source target.
2. Identify and verify the destination target.
3. Perform the bounded drag operation.
4. Verify the resulting state instead of assuming the gesture succeeded.

## Failure modes

- Stale coordinates after layout changes.
- Wrong or destructive destination.
- Unverified drop result.

## Evidence

- skills/04-action-execution/drag-drop.md
- AI_CONSTITUTION.md
- AGENTS.md

Evidence status: repository-backed implementation guidance; no benchmark claim.
