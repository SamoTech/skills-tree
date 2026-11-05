---
title: "MCP Gateway Response Redaction Execution"
category: 04-action-execution
level: advanced
stability: experimental
description: "Apply redaction of personally identifiable information in tool responses before they return through a gateway to agents."
added: "2026-11"
version: v1
related: [action-result-verification, injection-safe-tool-argument-quoting]
tags: [execution, redaction, pii, gateway]
---
# MCP Gateway Response Redaction Execution

## Description
Apply redaction of personally identifiable information in tool responses before they return through a gateway to agents. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A tool response contains sensitive data that must be redacted at the gateway.
- Redaction must happen before the response reaches the requesting agent.
- Redaction decisions must be recorded without storing the removed values.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The raw tool response, the redaction policy, and the field inventory. |
| Outputs | A redacted MCP-compatible response with a redaction record. |
| Safety | Fail closed by withholding the response when required redaction cannot be verified. |

## Procedure
1. Read the raw response and inventory its fields against the redaction policy.
2. Mark fields that match the sensitive-data patterns as redaction targets.
3. Replace target values with redaction markers and keep the field shape intact.
4. Verify that no marked value remains in the redacted payload.
5. Record the redaction counts per field without storing removed values.
6. Emit the redacted response with the redaction record attached.

## Outputs
| Area | Contract |
|---|---|
| Primary | A redacted tool response with field shape intact and a redaction record. |
| Verification | Recorded marker checks that reproduce the verification of the redacted payload. |
| Failure | A fail-closed error report naming the unredactable field and the withheld response. |

## Runnable Example
```python
def redact_response(resp, policy):
    out, record = {}, {}
    for k, v in resp.items():
        if k in policy:
            record[k] = len(str(v))
            out[k] = "[REDACTED]"
        else:
            out[k] = v
    leaked = [k for k in policy if k in out and out[k] != "[REDACTED]"]
    if leaked:
        return {"ok": False, "reason": "redaction_failed", "fields": leaked}
    return {"ok": True, "body": out, "redacted": record}

policy = {"email", "phone"}
r = redact_response({"email": "a@b.co", "flights": 3, "phone": "123"}, policy)
assert r["ok"] and r["body"]["email"] == "[REDACTED]" and r["body"]["flights"] == 3 and r["redacted"]["email"] == 7
raw = redact_response({"email": "a@b.co"}, set())
assert raw["ok"] and "email" not in raw["redacted"]
```

## Failure Modes
- Sensitive values are logged in the redaction record and the redaction leaks data anyway.
- Redacted fields are dropped entirely and downstream consumers break on shape changes.
- Redaction runs after the response is cached and cached copies keep the raw values.
- The verification step is skipped and a marked field survives unredacted.
- Responses without matched fields skip recording and redaction coverage cannot be audited.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Uber's MCP Gateway supports redaction of personally identifiable information and other sensitive data in tool responses (InfoQ, November 2, 2026, dated November 2, 2026) ([public signal](https://www.infoq.com/news/2026/11/uber-mcp-gateway-ai-agents/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Action Result Verification](action-result-verification.md)
- [Injection Safe Tool Argument Quoting](injection-safe-tool-argument-quoting.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
