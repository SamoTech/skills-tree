---
title: "Slack API"
category: 07-tool-use
level: intermediate
stability: stable
added: "2025-03"
description: "Apply Slack API in AI agent workflows."
dependencies:
  - package: slack-sdk
    min_version: "3.20.0"
    tested_version: "3.41.0"
    confidence: verified
code_blocks:
  - id: "example-slack"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-slack-api.json)

# Slack API

**Category:** `tool-use`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Send messages, post to channels, upload files, and react to events using the Slack Web API and Bolt framework.

### Example

```python
# pip install slack-sdk
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

client = WebClient(token="xoxb-your-bot-token")

try:
    # Post a message
    response = client.chat_postMessage(
        channel="#general",
        text="Hello from your AI agent! :robot_face:",
        blocks=[
            {"type": "section", "text": {"type": "mrkdwn", "text": "*Agent Report*"}},
            {"type": "section", "text": {"type": "mrkdwn", "text": "Task completed successfully."}}
        ]
    )
    print(f"Message sent: {response['ts']}")
except SlackApiError as e:
    print(f"Error: {e.response['error']}")
```

### Related Skills
- `notification-sending`, `email-sending`, `webhook-call`, `twilio-api`
