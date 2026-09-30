---
name: screen-reading
description: Read authorized screenshots into structured UI state, visible text, interactive elements, and alerts.
license: MIT
metadata:
  source: skills/01-perception/screen-reading.md
  version: "v2"
---

# screen-reading

Provide a screenshot path or bytes and an optional task context; return structured UI observations.

## Failure modes

- Ambiguous controls: mark position or label uncertain.
- Sensitive screen: minimize unrelated data.
- Dynamic UI: preserve capture timestamp and avoid assuming unseen state.

## Evidence

- https://agentskills.io/specification
- https://docs.anthropic.com/en/docs/build-with-claude/vision

Evidence status: references support implementation guidance; no performance benchmark is claimed without reproducible benchmark data.
