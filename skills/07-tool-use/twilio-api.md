---
title: "Twilio API"
category: 07-tool-use
level: intermediate
stability: stable
added: "2025-03"
description: "Apply Twilio API in AI agent workflows."
dependencies:
  - package: twilio
    min_version: "8.0.0"
    tested_version: "9.10.5"
    confidence: verified
code_blocks:
  - id: "example-twilio"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-twilio-api.json)

# Twilio API

**Category:** `tool-use`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Send SMS, WhatsApp messages, and make voice calls programmatically via the Twilio REST API.

### Example

```python
# pip install twilio
from twilio.rest import Client

client = Client("ACxxxxxxxx", "your_auth_token")

# Send SMS
message = client.messages.create(
    body="Your agent task completed successfully!",
    from_="+15551234567",  # Twilio number
    to="+15559876543"
)
print(f"SMS sent: {message.sid}, status: {message.status}")

# Send WhatsApp message
wapp = client.messages.create(
    body="Agent report ready.",
    from_="whatsapp:+14155238886",
    to="whatsapp:+15559876543"
)
print(f"WhatsApp sent: {wapp.sid}")
```

### Related Skills
- `notification-sending`, `slack-api`, `sendgrid-api`, `email-sending`
