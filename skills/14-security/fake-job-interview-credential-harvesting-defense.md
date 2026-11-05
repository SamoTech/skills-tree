---
title: "Fake Job Interview Credential Harvesting Defense"
category: 14-security
level: advanced
stability: experimental
description: "Defend against fake job interview lures that harvest credentials and grant attacker access through abused tools."
added: "2026-11"
version: v1
related: [social-engineering-detection, credential-exposure-agent-read-prevention]
tags: [security, social-engineering, credentials, defense]
---
# Fake Job Interview Credential Harvesting Defense

## Description
Defend against fake job interview lures that harvest credentials and grant attacker access through abused tools. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Staff receive job-interview approaches that request tool access.
- Credential handover under interview pressure must be blocked.
- Abused-tool access paths need containment after exposure.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The interview approach report, the credential policy, and the tool access registry. |
| Outputs | A defense report naming the lure indicators, revoked grants, and containment actions. |
| Safety | Fail closed by revoking tool access immediately on any confirmed credential handover. |

## Procedure
1. Collect the interview approach report with its requested access list.
2. Check requested access against the credential-sharing policy.
3. Flag any request for credentials or tool access as a lure indicator.
4. On confirmed handover, revoke the exposed credentials and tool grants.
5. Contain the accessed tools and pull access logs for forensics.
6. Emit the defense report naming the lure, revocations, and containment.

## Outputs
| Area | Contract |
|---|---|
| Primary | A defense report naming the lure indicators, revoked grants, and containment actions. |
| Verification | Access logs and revocation records that reproduce the response. |
| Failure | A fail-closed escalation naming the unrevoked exposed credential. |

## Runnable Example
```python
def respond(report, registry):
    lure = "credentials" in report["requests"] or "tool-access" in report["requests"]
    if not lure:
        return {"lure": False, "revoke": []}
    revoke = registry.get(report["staff"], [])
    return {"lure": True, "revoke": revoke}
reg = {"staff-a": ["grant-1", "grant-2"]}
r = respond({"staff": "staff-a", "requests": ["credentials"]}, reg)
assert r["lure"] and r["revoke"] == ["grant-1", "grant-2"]
assert respond({"staff": "staff-b", "requests": ["resume"]}, reg)["lure"] is False
```

## Failure Modes
- Interview requests for tool access are treated as routine recruiting.
- Revocation waits for confirmation of misuse.
- Access logs are not pulled during containment.
- Staff who handed over credentials are blamed instead of supported.
- Lure indicators are collected but never turned into detections.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Binance traced a 6.34 billion dollar heist to fake job interviews and an abused AI tool (AIBriefs AI News Today, dated November 5, 2026) ([public signal](https://aibriefs.news/ai-news-today))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Social Engineering Detection](social-engineering-detection.md)
- [Credential Exposure Agent Read Prevention](credential-exposure-agent-read-prevention.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
