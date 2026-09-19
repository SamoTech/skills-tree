---
title: "Email Parsing"
category: 01-perception
level: basic
stability: stable
description: "Parse email messages into normalized headers, body parts, attachments, threading metadata, and security-relevant indicators without trusting message content."
added: "2025-03"
version: v2
updated: "2026-09"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-email-parsing.json)

# Email Parsing

## Description

Parse email messages into normalized headers, body parts, attachments, threading metadata, and security-relevant indicators without trusting message content.

## When to Use

Use for mailbox ingestion, triage, search indexing, automation, and incident analysis.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| input | structured | Source content plus any format-specific metadata. |
| options | object | Limits, locale, schema, or provider-specific parsing options. |
| output | structured | Normalized records with provenance and explicit uncertainty. |

## Runnable Example

```python
from email import policy
from email.parser import BytesParser

def parse_email(raw: bytes) -> dict:
    msg = BytesParser(policy=policy.default).parsebytes(raw)
    text_parts = []
    attachments = []
    for part in msg.walk():
        if part.is_attachment():
            attachments.append(part.get_filename() or "unnamed")
        elif part.get_content_type() == "text/plain":
            text_parts.append(part.get_content())
    return {
        "from": msg.get("From"),
        "to": msg.get("To"),
        "subject": msg.get("Subject"),
        "message_id": msg.get("Message-ID"),
        "body": "\n".join(text_parts),
        "attachments": attachments,
    }

print(parse_email(b"Subject: Test\n\nHello").get("subject"))
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Malformed MIME | malformed or adversarial input | Validate structure before semantic processing. |
| encoded headers | unexpected source variation | Preserve raw context and emit a warning. |
| spoofed sender fields | incomplete source | Mark uncertainty instead of inventing values. |
| Resource exhaustion | unbounded input | Enforce size, time, and result limits. |

## Output Contract

Normalized headers, body text, attachment metadata, and thread identifiers; authentication results must come from trusted mail infrastructure.

## Design Rules

1. Preserve source provenance and ordering whenever it is available.
2. Validate structure before interpreting semantics.
3. Never silently convert uncertainty into a confident assertion.
4. Bound input size, execution time, and result cardinality.
5. Keep provider-specific parsing behind a stable internal representation.

## Related Skills

- [Text Reading](text-reading.md) — plain text extraction and normalization
- [Structured Data Reading](structured-data-reading.md) — schema-aware data ingestion
- [JSON Schema Validation](json-schema-validation.md) — validate normalized structures

## Changelog

| Version | Date | Change |
|---|---|---|
| v1 | 2025-03 | Initial skill entry |
| v2 | 2026-09 | Replaced placeholder guidance with executable implementation, I/O contract, failure modes, and bounded parsing rules |
