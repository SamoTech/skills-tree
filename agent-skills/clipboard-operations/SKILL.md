---
name: clipboard-operations
description: Read or write clipboard content with explicit content handling and privacy boundaries.
license: MIT
metadata:
  source: skills/04-action-execution/clipboard-ops.md
  version: "v2"
---

# Clipboard Operations

1. Confirm the clipboard operation is within the requested scope.
2. Read or write only the required content.
3. Treat clipboard data as potentially sensitive.
4. Never log or exfiltrate clipboard contents by default.

## Failure modes

- Sensitive data leakage through logs.
- Wrong active window.
- Leaving secrets in the clipboard unnecessarily.

## Evidence

- skills/04-action-execution/clipboard-ops.md
- AI_CONSTITUTION.md
- AGENTS.md

Evidence status: repository-backed implementation guidance; no benchmark claim.
