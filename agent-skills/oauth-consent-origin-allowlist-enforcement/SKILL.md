---
name: oauth-consent-origin-allowlist-enforcement
description: Enforce an allowlist of OAuth consent origins so agent hosting stacks only redirect consent flows to origins they declared.
metadata:
  source: skills/14-security/oauth-consent-origin-allowlist-enforcement.md
  category: 14-security
  version: "v1"
---

# OAuth Consent Origin Allowlist Enforcement

## Description
Enforce an allowlist of OAuth consent origins so agent hosting stacks only redirect consent flows to origins they declared. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An operator needs this capability to proceed safely and verifiably.
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
3. Extract the consent redirect origin from each authorization request, match it against the declared allowlist, and fail closed on any origin not present rather than warning and continuing.
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
def enforce(redirect, allowlist):
    origin = redirect.split("/")[0] + "//" + redirect.split("/")[2]
    if origin not in allowlist:
        raise ValueError("consent origin not allowlisted: " + origin)
    return True

al = {"https://login.example.com"}
assert enforce("https://login.example.com/oauth", al) is True
try:
    enforce("https://evil.example.net/oauth", al); assert False
except ValueError:
    pass
```

## Failure Modes
- Unknown origins log a warning and the flow continues.
- The allowlist matches by suffix and login.evil-login.example.com passes.
- Origins are compared case-insensitively on the whole URL and scheme confusion slips through.
- The allowlist is editable at runtime by the same agent it guards.
- Subdomains are implicitly trusted and one compromised subdomain hosts the consent phishing page.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Agent Framework added an optional OAuth consent origin allowlist to Foundry hosting (releasebot.io, dated October 7, 2026) ([public signal](https://releasebot.io/updates/microsoft/agent-framework))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [MCP OAuth Authentication](../14-security/mcp-oauth-authentication.md)
- [OAuth Token Audience Binding Verification](../14-security/oauth-token-audience-binding-verification.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
