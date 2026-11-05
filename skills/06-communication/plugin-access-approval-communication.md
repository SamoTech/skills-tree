---
title: "Plugin Access Approval Communication"
category: 06-communication
level: advanced
stability: experimental
description: "Communicate a plugin's access requests to users in plain language, stating exactly what is requested, what it is used for, and what it will never do."
added: "2026-11"
version: v1
related: [incident-communication, agent-action-explanation-writing]
tags: [communication, plugins, approval, privacy]
---
# Plugin Access Approval Communication

## Description
Communicate a plugin's access requests to users in plain language, stating exactly what is requested, what it is used for, and what it will never do. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A plugin requests data or capability access and the user must decide whether to approve.
- The outcome would change if the request were described vaguely, causing blind approval or blind refusal.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The plugin's declared access requests, the purpose map, and the platform's approval prompt contract. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. State each requested scope in plain language with the concrete purpose it serves.
4. State the explicit non-goals (what the plugin will not do with the access) before the approval prompt.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | An access-approval communication with per-scope purpose statements and explicit non-goals. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def approval_text(requests, purposes):
    lines = []
    for scope in requests:
        purpose = purposes.get(scope)
        if not purpose:
            return None
        lines.append(f"{scope}: used to {purpose}")
    return "\n".join(lines)
t = approval_text(["calendar.read"], {"calendar.read": "find free slots for your meeting"})
assert t == "calendar.read: used to find free slots for your meeting"
```

## Failure Modes
- A scope is requested without a stated purpose, forcing blind approval.
- Access is described more narrowly than the scope actually grants.
- Non-goals are omitted, leaving users to infer worst cases.
- The purpose statement promises behavior the plugin has not implemented.
- The prompt bundles unrelated scopes into one approve-or-deny choice.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- OpenAI DevDay 2026 redesigned the platform around plugins that request user-approved access to data in a connected app (OpenAI DevDay recap, dated November 4, 2026) ([public signal](https://openai.com/index/devday-2026-recap/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Incident Communication](incident-communication.md)
- [Agent Action Explanation Writing](agent-action-explanation-writing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
