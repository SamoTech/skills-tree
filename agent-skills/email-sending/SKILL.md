---
name: email-sending
description: Send an approved email through a configured mail transport while validating recipients and preventing credential or content leakage.
metadata:
  source: skills/04-action-execution/email-sending.md
  category: 04-action-execution
---

# Email Sending

## Description

Submit an email through an authorized SMTP or provider transport. Recipient, subject, body, attachments, and approval state should be explicit before sending.

## When to Use

- Sending a message explicitly approved by the user.
- Delivering an automated notification through a configured service.
- Testing mail transport against a safe endpoint.

## Inputs / outputs / failure modes

| Input | Output | Failure mode |
|---|---|---|
| Sender/recipients | Delivery request | Invalid address |
| Subject/body | Message | Content validation failure |
| Mail credentials | Authenticated transport | Credential failure |
| Approval state | Send/no-send decision | Unauthorized action |

## Runnable example

```python
from email.message import EmailMessage

msg = EmailMessage()
msg["From"] = "sender@example.invalid"
msg["To"] = "recipient@example.invalid"
msg["Subject"] = "Test"
msg.set_content("Approved test message.")
print(msg.as_string())
```

## Failure modes

- Sending without required authorization.
- Exposing SMTP passwords or API keys.
- Sending to recipients inferred from ambiguous context.
- Retrying without an idempotency strategy when duplicates matter.

## Related

- ../01-perception/email-parsing.md
- form-submission.md
- ../14-security/approval-before-destructive-tools.md

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository security and validation workflows
