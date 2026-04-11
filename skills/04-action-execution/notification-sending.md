# Notification Sending

**Category:** `action-execution`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

### Description

Send push notifications, Slack messages, Telegram alerts, or desktop notifications as agent outputs.

### Example

```python
import httpx
# Slack webhook
httpx.post(
    'https://hooks.slack.com/services/XXX/YYY/ZZZ',
    json={'text': ':white_check_mark: Agent task completed successfully!'}
)
```

### Related Skills

- [Email Sending](email-sending.md)
- [Slack API](../07-tool-use/slack-api.md)
