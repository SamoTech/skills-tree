---
name: database-write
description: Persist structured data with transaction boundaries, parameterized queries, validation, and explicit rollback behavior.
license: MIT
metadata:
  source: skills/04-action-execution/database-write.md
  version: "v2"
---

# Database Write

1. Validate fields before constructing the mutation.
2. Use parameterized statements.
3. Group dependent writes in an explicit transaction.
4. Commit only after all required checks succeed.

## Failure modes

- SQL injection through string-built queries.
- Partial mutation without transaction control.
- Logging sensitive database content.

## Evidence

- skills/04-action-execution/database-write.md
- AI_CONSTITUTION.md
- AGENTS.md

Evidence status: repository-backed implementation guidance; no benchmark claim.
