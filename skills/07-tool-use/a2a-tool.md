---
title: A2a Tool
category: 07-tool-use
level: advanced
stability: stable
description: Use agent-to-agent tool interfaces with explicit contracts, authorization boundaries, message validation, and observable outcomes.
added: "2026-09"
related: [07-tool-use]
---

## Description
Use agent-to-agent tool interfaces with explicit contracts, authorization boundaries, message validation, and observable outcomes. Inspect the target protocol and repository conventions before making calls.

## When to Use
Use when one agent invokes another agent or agent-facing service through a defined tool interface.

## Inputs / outputs / failure modes

| Area | Guidance |
|---|---|
| Inputs | Tool contract, request payload, authorization context, and expected result. |
| Outputs | Validated response and evidence of the resulting state. |
| Failure modes | Invalid payloads, unauthorized actions, protocol mismatch, or unverified outcomes. |

## Runnable Example

```python
request = {"action": "inspect", "target": "repository"}
assert "action" in request
print("validate tool contracts before invocation")
```

## Failure modes
- Calling an undocumented interface.
- Sending incomplete or excessive data.
- Treating an acknowledgement as proof of completion.
- Ignoring authorization boundaries.

## Related
- 07-tool-use
- AI_CONSTITUTION.md
- meta/AGENT_OPERATING_MODEL.md

## Evidence
Repository-backed implementation guidance grounded in repository governance and validation workflows; no external benchmark claim is made.
