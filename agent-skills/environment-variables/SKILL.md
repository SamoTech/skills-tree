---
name: environment-variables
description: Read and validate environment configuration without exposing secrets or confusing missing configuration with empty values.
license: MIT
metadata:
  source: skills/04-action-execution/env-vars.md
  version: "v2"
---

# Environment Variables

1. Identify required and optional variables.
2. Read values without printing secrets.
3. Reject missing or invalid required configuration.
4. Keep secret-bearing environment files out of repository source.

## Failure modes

- Secret disclosure.
- Treating empty credentials as valid.
- Unsafe production defaults.

## Evidence

- skills/04-action-execution/env-vars.md
- AI_CONSTITUTION.md
- AGENTS.md

Evidence status: repository-backed implementation guidance; no benchmark claim.
