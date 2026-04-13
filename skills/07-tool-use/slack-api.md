---
title: "Slack API"
category: 07-tool-use
level: intermediate
stability: stable
description: "Apply slack api in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-slack-api.json)

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
