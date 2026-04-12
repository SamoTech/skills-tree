# Slack API

**Category:** `tool-use`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Send messages, read channels, and interact with Slack workspaces via the Slack Web API or Bolt SDK.

### Example

```python
from slack_sdk import WebClient

client = WebClient(token=SLACK_TOKEN)
result = client.chat_postMessage(
    channel='#ai-agents',
    text=':robot_face: Skills Tree: 223 missing files pushed successfully!'
)
```

### Related Skills

- [Notification Sending](../04-action-execution/notification-sending.md)
- [Twilio API](twilio-api.md)
