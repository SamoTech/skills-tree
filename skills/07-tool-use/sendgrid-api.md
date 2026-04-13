---
title: "SendGrid API"
category: 07-tool-use
level: intermediate
stability: stable
description: "Apply sendgrid api in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-sendgrid-api.json)

# SendGrid API

**Category:** `tool-use`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Send transactional and marketing emails at scale via the SendGrid REST API.

### Example

```python
import sendgrid
from sendgrid.helpers.mail import Mail

sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_KEY)
message = Mail(
    from_email='agent@example.com',
    to_emails='user@example.com',
    subject='Skills Tree Update',
    plain_text_content='223 new skill files have been added to the repository.'
)
sg.send(message)
```

### Related Skills

- [Email Sending](../04-action-execution/email-sending.md)
- [Twilio API](twilio-api.md)
