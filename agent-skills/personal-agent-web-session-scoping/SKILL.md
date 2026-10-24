---
name: personal-agent-web-session-scoping
description: Scope web sessions for personal agents so each task operates in its own isolated session with no shared credentials.
metadata:
  source: skills/11-web/personal-agent-web-session-scoping.md
  category: 11-web
  version: "v1"
---
# Personal Agent Web Session Scoping

## Description
Scope web sessions for personal agents so each task operates in its own isolated session with no shared credentials. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A personal agent performs web tasks and must not carry credentials or cookies across tasks.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Provision a per-task browser session, load only the credentials the task requires, and verify the session carries no credentials beyond the declared set before navigation.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def scope_session(required_creds, profile_creds, loaded):
    if not set(required_creds).issubset(loaded):
        raise ValueError("session missing required credentials")
    excess = sorted(set(loaded) - set(required_creds))
    return {"ok": not excess, "excess": excess}

assert scope_session({"shop_auth"}, {}, {"shop_auth"})["ok"] is True
assert scope_session({"shop_auth"}, {"mail_auth"}, {"shop_auth", "mail_auth"})["excess"] == ["mail_auth"]
```

## Failure Modes
- One long-lived session is reused across tasks to save login time.
- Credentials are loaded into the session before the required set is known.
- Excess credentials are detected but not unloaded before navigation.
- The scoping check reads the profile instead of the live session.
- Task isolation is per tab rather than per session.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- October 2026 practitioner guidance on browser agents prescribes session isolation for production browser agents, a dated public demand signal (zentor.ai, dated October 2026) ([public signal](https://www.zentor.ai/blog/ai-browser-automation-2026-guide))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Browser Session Isolation](../11-web/browser-session-isolation.md)
- [Web Agent Authenticated Session Automation](../11-web/web-agent-authenticated-session-automation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
