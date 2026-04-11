# SendGrid API

**Category:** `tool-use`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

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
