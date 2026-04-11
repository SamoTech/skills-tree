# Email Sending

**Category:** `action-execution`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

### Description

Compose and send emails via SMTP or email service APIs (SendGrid, Resend, Gmail API).

### Example

```python
import smtplib
from email.mime.text import MIMEText

msg = MIMEText('Hello from your AI agent!')
msg['Subject'] = 'Agent Notification'
msg['From'] = 'agent@example.com'
msg['To'] = 'user@example.com'

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login(user, password)
    server.send_message(msg)
```

### Related Skills

- [Email Parsing](../01-perception/email-parsing.md)
- [Notification Sending](notification-sending.md)
- [SendGrid API](../07-tool-use/sendgrid-api.md)
