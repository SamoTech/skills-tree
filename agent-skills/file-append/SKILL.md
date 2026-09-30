---
name: file-append
description: Append text or bytes to a file with explicit encoding, newline, locking, and error semantics.
license: MIT
metadata:
  source: skills/04-action-execution/file-append.md
  version: "v2"
---

# File Append

1. Resolve the target file and encoding.
2. Append only the intended payload.
3. Use a locking strategy when concurrent writers are possible.
4. Bound file growth where the artifact is long-lived.

## Failure modes

- Interleaved concurrent writes.
- Encoding drift.
- Unbounded file growth.
- Treating append-only storage as tamper-proof.

## Evidence

- skills/04-action-execution/file-append.md
- AI_CONSTITUTION.md
- AGENTS.md

Evidence status: repository-backed implementation guidance; no benchmark claim.
