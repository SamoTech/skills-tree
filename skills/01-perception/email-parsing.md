---
title: "Email Parsing"
category: 01-perception
level: basic
stability: stable
description: "Apply email parsing in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-email-parsing.json)

# Email Parsing

**Category:** `perception`  
**Skill Level:** `basic`  
**Stability:** `stable`  
**Added:** 2025-03  
**Last Updated:** 2026-04

---

## Description

Extract structured data from raw email messages — sender, recipient, subject, date, body text, HTML content, attachments, and threading metadata. Handles both plain-text and MIME multipart messages. Useful for inbox triage, automated response pipelines, lead extraction from sales emails, and compliance archival workflows.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `raw_email` | `string` | ✅ | Raw RFC 2822 email string or `.eml` file content |
| `extract_fields` | `list` | ❌ | Fields to extract; defaults to all |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `intent` | `string` | Detected sender intent, e.g. `request_quote` |
| `urgency` | `string` | `low` / `medium` / `high` |
| `entities` | `list` | Names, companies, dates, amounts mentioned |
| `action_required` | `bool` | Whether a response or action is needed |
| `summary` | `string` | One-sentence email summary |

---

## Example

```python
import anthropic
import email
import json
from email import policy

client = anthropic.Anthropic()

def parse_email(raw_email: str) -> dict:
    """Parse a raw email message into structured JSON."""
    msg = email.message_from_string(raw_email, policy=policy.default)

    # Extract plain-text body
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_content()
                break
    else:
        body = msg.get_content()

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": (
                "Extract the following from this email and return JSON:\n"
                "- intent: what the sender wants (e.g. 'request_quote', 'complaint', 'inquiry')\n"
                "- urgency: low | medium | high\n"
                "- entities: list of mentioned names, companies, dates, amounts\n"
                "- action_required: boolean\n"
                "- summary: one sentence\n\n"
                f"From: {msg['from']}\n"
                f"Subject: {msg['subject']}\n"
                f"Date: {msg['date']}\n"
                f"Body:\n{body[:3000]}"
            )
        }]
    )
    return json.loads(response.content[0].text)

with open("sample.eml") as f:
    result = parse_email(f.read())
print(json.dumps(result, indent=2))
```

---

## Frameworks & Models

| Framework / Model | Implementation | Since |
|---|---|---|
| Claude claude-opus-4-5 | Direct text prompt | 2024-06 |
| LangChain | `UnstructuredEmailLoader` + LLM chain | v0.1 |

---

## Notes

- Strip HTML tags before passing to avoid injecting formatting tokens
- Truncate very long bodies to ~3000 characters
- For attachment processing, combine with [Document Parsing](document-parsing.md) or [PDF Parsing](pdf-parsing.md)

---

## Related Skills

- [Document Parsing](document-parsing.md) — for email attachments
- [Text Reading](text-reading.md) — general text extraction
- [PDF Parsing](pdf-parsing.md) — parsing PDF attachments

---

## Changelog

| Date | Change |
|---|---|
| `2026-04` | Expanded from stub: full description, I/O table, MIME parsing example, notes |
| `2025-03` | Initial stub entry |
