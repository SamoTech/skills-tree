# Email Parsing

**Category:** `perception`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Extract sender, recipient, subject, body, and attachments from raw email messages (MIME, EML, or API responses).

### Example

```python
import email
msg = email.message_from_string(raw_email)
subject = msg['Subject']
from_addr = msg['From']
body = msg.get_payload(decode=True).decode()
```

### Related Skills

- [Email Sending](../04-action-execution/email-sending.md)
- [Document Parsing](document-parsing.md)
