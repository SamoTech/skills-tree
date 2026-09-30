---
title: Regex Generation
category: 05-code
level: advanced
stability: stable
description: Generate regular expressions from explicit matching and rejection requirements and validate them against representative cases.
added: "2026-09"
related: [05-code]
---

## Description
Generate regular expressions from explicit matching and rejection requirements and validate them against representative cases. Prefer readable patterns and explicit tests over clever or opaque expressions.

## When to Use
Use when structured text must be matched, extracted, validated, or rejected using regular expressions.

## Inputs / outputs / failure modes

| Area | Guidance |
|---|---|
| Inputs | Required matches, required rejections, engine syntax, flags, and representative samples. |
| Outputs | Tested regex and documented assumptions. |
| Failure modes | Overmatching, undermatching, engine incompatibility, or pathological performance. |

## Runnable Example

```python
import re

pattern = re.compile(r'^[A-Z]{2}-\\d{4}$')
for value in ['AB-1234', 'bad']:
    print(value, bool(pattern.fullmatch(value)))
```

## Failure modes
- Deriving a pattern without explicit examples.
- Ignoring the target regex engine.
- Testing only positive cases.
- Creating unnecessarily expensive patterns.

## Related
- 05-code
- AI_CONSTITUTION.md
- meta/AGENT_OPERATING_MODEL.md

## Evidence
Repository-backed implementation guidance grounded in repository governance and validation workflows; no external benchmark claim is made.
