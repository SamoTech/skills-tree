---
name: code-exec-tool
description: Execute code in an explicitly scoped runtime while validating inputs, outputs, resource limits, and side effects.
metadata:
  source: skills/07-tool-use/code-exec-tool.md
  category: 07-tool-use
---

## Description
Execute code in an explicitly scoped runtime while validating inputs, outputs, resource limits, and side effects. Inspect the repository contract and target interface before invocation, validate inputs, and independently verify important outcomes.

## When to Use
Use when the repository task explicitly requires this tool capability.

## Inputs / outputs / failure modes

| Area | Guidance |
|---|---|
| Inputs | Documented interface, validated inputs, authorization context, and expected result. |
| Outputs | Verified result with concise evidence. |
| Failure modes | Invalid inputs, unsupported assumptions, excessive permissions, side effects, or unverified outcomes. |

## Runnable Example

```python
from dataclasses import dataclass

@dataclass
class Request:
    action: str

request = Request(action="inspect")
assert request.action
print("validate the tool contract before invocation")
```

## Failure modes
- Calling an undocumented interface.
- Sending invalid or excessive data.
- Exposing credentials or secrets.
- Treating an acknowledgement as proof of completion.
- Skipping repository validation.

## Related
- 07-tool-use
- AI_CONSTITUTION.md
- meta/AGENT_OPERATING_MODEL.md

## Evidence
Repository-backed implementation guidance grounded in repository governance and validation workflows; no external benchmark claim is made.
