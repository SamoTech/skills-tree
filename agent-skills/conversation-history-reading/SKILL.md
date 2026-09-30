---
name: conversation-history-reading
description: Normalize multi-turn conversation exports while preserving roles, ordering, timestamps, and provider metadata. Use before context selection, summarization, or memory injection.
license: MIT
metadata:
  source: skills/01-perception/conversation-history-reading.md
  version: "v2"
---

# Conversation History Reading

1. Detect the source format and preserve the original records.
2. Normalize provider-specific role names into a documented internal representation.
3. Preserve message ordering and timestamps when available.
4. Separate message content from metadata and tool results.
5. Select only the context required for the downstream task.
6. Bound token and record counts; do not inject an entire history by default.

## Failure modes

- Provider role mismatch: map roles explicitly and retain the original role in metadata.
- Missing timestamps: preserve source ordering and mark time as unavailable.
- Context overflow: summarize or retrieve relevant windows rather than truncating silently.

## Evidence

- https://platform.openai.com/docs/guides/text
- https://docs.anthropic.com/en/api/messages
- https://agentskills.io/specification
