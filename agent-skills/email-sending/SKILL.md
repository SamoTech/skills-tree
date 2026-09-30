---
name: email-sending
description: Send an approved email through a configured mail transport while validating recipients and preventing credential or content leakage.
license: MIT
metadata:
  source: skills/04-action-execution/email-sending.md
  version: "v2"
---

# Email Sending

1. Validate sender, recipients, subject, body, and attachments.
2. Confirm the action is authorized before external delivery.
3. Obtain credentials from secret-safe configuration.
4. Avoid duplicate delivery when retrying.

## Failure modes

- Unauthorized external communication.
- Credential leakage.
- Ambiguous recipients.
- Duplicate messages.

## Evidence

- skills/04-action-execution/email-sending.md
- AI_CONSTITUTION.md
- AGENTS.md

Evidence status: repository-backed implementation guidance; no benchmark claim.
