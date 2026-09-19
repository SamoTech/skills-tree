---
title: "Conversation History Reading"
category: 01-perception
level: intermediate
stability: stable
description: "Reconstruct conversation state from message history while distinguishing durable facts, transient context, unresolved requests, and contradictory statements."
related: [text-reading, structured-data-reading, json-schema-validation]
added: "2025-03"
version: v2
updated: "2026-09"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-conversation-history-reading.json)

# Conversation History Reading

## Description

Reconstruct conversation state from message history while distinguishing durable facts, transient context, unresolved requests, and contradictory statements.

## When to Use

Use when an agent must resume a thread safely or determine what information is already known before asking the user to repeat it.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| input | structured | Source content plus any format-specific metadata. |
| options | object | Limits, locale, schema, or provider-specific parsing options. |
| output | structured | Normalized records with provenance and explicit uncertainty. |

## Runnable Example

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ConversationState:
    goals: list[str]
    decisions: list[str]
    open_questions: list[str]
    contradictions: list[str]

def summarize_history(messages: list[dict[str, str]]) -> ConversationState:
    goals, decisions, questions, contradictions = [], [], [], []
    for m in messages:
        text = m.get("content", "").strip()
        if text.endswith("?"):
            questions.append(text)
        if "decided" in text.lower() or "agreed" in text.lower():
            decisions.append(text)
        if "need to" in text.lower() or "goal" in text.lower():
            goals.append(text)
    return ConversationState(goals, decisions, questions, contradictions)

state = summarize_history([
    {"role": "user", "content": "Our goal is to ship the parser."},
    {"role": "assistant", "content": "We agreed to keep the schema stable."},
])
print(state)
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Contradictory messages | malformed or adversarial input | Validate structure before semantic processing. |
| stale assumptions | unexpected source variation | Preserve raw context and emit a warning. |
| quoted text mistaken for user intent | incomplete source | Mark uncertainty instead of inventing values. |
| Resource exhaustion | unbounded input | Enforce size, time, and result limits. |

## Output Contract

A bounded state summary with provenance back to message ranges; separate facts from assumptions and unresolved questions.

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
