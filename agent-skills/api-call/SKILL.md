---
name: api-call
description: Execute authenticated HTTP API requests with explicit timeouts, bounded retries, response validation, and secret-safe error handling.
license: MIT
metadata:
  source: skills/04-action-execution/api-call.md
  version: "v2"
---

# API Call

1. Validate method, URL, authentication reference, timeout, and retry policy.
2. Use explicit authentication and never embed credentials in source or logs.
3. Retry only operations whose semantics permit retry, using bounded attempts.
4. Validate the response before returning it to downstream agent steps.

## Failure modes

- Retry non-idempotent mutations without an idempotency strategy.
- Log authorization headers or secret-bearing payloads.
- Use unbounded retries or no timeout.

## Evidence

- skills/04-action-execution/api-call.md
- AI_CONSTITUTION.md
- AGENTS.md

Evidence status: implementation guidance is repository-backed; no performance benchmark is claimed.
