# Twilio API

**Category:** `tool-use`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

### Description

Send SMS, WhatsApp messages, and make voice calls programmatically via the Twilio REST API.

### Example

```python
from twilio.rest import Client

client = Client(TWILIO_SID, TWILIO_TOKEN)
message = client.messages.create(
    body='Skills Tree: 223 files successfully committed!',
    from_='+15551234567',
    to='+201001234567'
)
print(message.sid)
```

### Related Skills

- [SendGrid API](sendgrid-api.md)
- [Notification Sending](../04-action-execution/notification-sending.md)
