---
name: chain-of-thought
description: Use structured intermediate reasoning without requiring exposure of private chain-of-thought.
license: MIT
metadata:
  source: skills/02-reasoning/chain-of-thought.md
  version: "v2"
---

# chain-of-thought

Use this skill to produce a bounded, auditable reasoning result. State assumptions, preserve uncertainty, and verify material conclusions.

## Failure modes

- Private reasoning exposure: return conclusions and verification evidence instead.
- Excessive reasoning budget: bound iterations.

## Evidence

- https://agentskills.io/specification

Evidence status: references support implementation guidance; no performance benchmark is claimed without reproducible benchmark evidence.
