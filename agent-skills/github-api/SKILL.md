---
name: github-api
description: Work with GitHub APIs using documented endpoints, authentication boundaries, pagination, error handling, and least-privilege access.
license: MIT
metadata:
  source: skills/05-code/github-api.md
  version: "v2"
---

# Github Api

1. Identify the documented endpoint and required scope.
2. Validate request parameters and pagination behavior.
3. Make the API request without exposing credentials.
4. Inspect status, response semantics, and errors.
5. Verify any claimed repository state change independently.

## Failure modes
- Wrong endpoint or request shape.
- Excessive permissions or exposed credentials.
- Pagination or rate-limit errors.
- Completion claims without state verification.

## Evidence
Canonical skill: skills/05-code/github-api.md
Repository governance: AI_CONSTITUTION.md
