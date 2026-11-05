---
name: credential-refresh-across-interaction-tool-usage
description: Refresh and revalidate OAuth credentials across multi-turn tool interactions without exposing tokens, replays, or repeated user re-consent.
metadata:
  source: skills/07-tool-use/credential-refresh-across-interaction-tool-usage.md
  category: 07-tool-use
  version: "v1"
---

# Credential Refresh Across Interaction Tool Usage

## Description
Refresh and revalidate OAuth credentials across multi-turn tool interactions without exposing tokens, replays, or repeated user re-consent. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A long-running multi-turn agent uses OAuth-scoped tools whose credentials expire mid-conversation.
- The outcome would change if expiry mid-conversation caused tool failures or forced a full re-login.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The credential store, the tool's OAuth scope, and the interaction session context. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Check token expiry before each tool call and refresh through the platform's flow when needed.
4. Revalidate the refreshed scope against the session context and never log or echo token material.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A refreshed-credential record with new expiry, verified scope, and no token material in the record. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def refresh_if_stale(creds, now, refresh):
    if creds["expires_at"] > now:
        return {"refreshed": False, "scope": creds["scope"]}
    new = refresh(creds["refresh_hint"])
    assert "token" not in new, "token material must not enter the record"
    return {"refreshed": True, "expires_at": new["expires_at"], "scope": new["scope"]}
r = refresh_if_stale({"expires_at": 5, "scope": ["read"]}, 10, lambda h: {"expires_at": 3600, "scope": ["read"]})
assert r["refreshed"] is True and r["expires_at"] == 3600
```

## Failure Modes
- Expired tokens are used anyway, causing silent tool failures attributed to other causes.
- Token material enters logs or tool-result records during refresh.
- Refresh is attempted on every call instead of only near expiry, thrashing the auth service.
- The refreshed scope is not revalidated against what the session approved.
- A refresh failure triggers repeated user re-consent instead of a fail-closed report.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Google added managed agents in the Gemini API that re-authorize users on a schedule so agents can refresh OAuth credentials across interactions without replaying them or logging sensitive data, and added support for remote MCP servers that revalidate authorization headers (Google Developers Blog, dated July 7, 2026) ([public signal](https://blog.google/innovation-and-ai/technology/developers-tools/expanding-managed-agents-gemini-api))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Web Search](../11-web/web-search.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
