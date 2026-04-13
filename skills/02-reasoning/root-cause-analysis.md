---
title: "Root Cause Analysis"
category: 02-reasoning
level: intermediate
stability: stable
description: "Apply root cause analysis in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-root-cause-analysis.json)

# Root Cause Analysis
Category: reasoning | Level: intermediate | Stability: stable | Version: v1

## Description
Determine the underlying cause of a problem using 5-Whys, fishbone diagrams, or fault tree analysis.

## Example
```python
import anthropic
client = anthropic.Anthropic()
problem = "API response time increased from 100ms to 800ms after Tuesday's deploy."
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": f"Apply the 5-Whys technique to find the root cause of: {problem}"}]
)
print(response.content[0].text)
```

## Failure Modes
- Stopping at symptoms rather than causes
- Confirmation bias toward expected causes

## Related
- `causal.md` · `systems-thinking.md`

## Changelog
- v1 (2026-04): Initial entry
