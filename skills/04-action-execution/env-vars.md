---
title: "Environment Variables"
category: 04-action-execution
level: basic
stability: stable
description: "Read and validate environment configuration without exposing secrets or confusing missing configuration with empty values."
added: "2026-09"
related: [input-sanitization, tool-guardrails, file-write]
---

# Environment Variables

## Description

Read configuration supplied through environment variables and distinguish required, optional, empty, and malformed values. Secret values must never be printed.

## When to Use

- Loading API credentials or deployment configuration.
- Validating required runtime settings.
- Keeping environment-specific values outside repository source.

## Inputs / outputs / failure modes

| Input | Output | Failure mode |
|---|---|---|
| Variable name | Value or absence | Missing variable |
| Required flag | Validation result | Required value missing |
| Default | Resolved configuration | Unsafe default |
| Secret classification | Safe handling | Secret disclosure |

## Runnable example

```python
import os

token = os.environ.get("API_TOKEN")
if not token:
    raise RuntimeError("API_TOKEN is required")
print("API_TOKEN is configured")
```

## Failure modes

- Printing environment variables wholesale.
- Committing secret-bearing environment files.
- Treating an empty value as a valid credential.
- Using a permissive production default.

## Related

- ../14-security/input-sanitization.md
- ../07-tool-use/tool-guardrails.md
- file-write.md

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository security and validation workflows
