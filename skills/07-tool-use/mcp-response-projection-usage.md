---
title: "MCP Response Projection Usage"
category: 07-tool-use
level: advanced
stability: experimental
description: "Use response projection at a gateway to reduce tool results to the fields a task needs before they enter agent context."
added: "2026-11"
version: v1
related: [tool-result-truncation, api-pagination]
tags: [tool-use, mcp, projection, efficiency]
---
# MCP Response Projection Usage

## Description
Use response projection at a gateway to reduce tool results to the fields a task needs before they enter agent context. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A tool returns large payloads but the task needs a few fields.
- Context tokens must be saved before the result enters the window.
- Projection must be declared per tool rather than improvised.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The raw tool response, the declared projection, and the task field needs. |
| Outputs | A projected response containing only the declared fields with shape preserved. |
| Safety | Fail closed by refusing undeclared projections that could drop audit-required fields. |

## Procedure
1. Read the tool's declared projection from the gateway configuration.
2. Identify the fields the task steps actually consume.
3. Apply the declared projection to the raw response and keep the shape.
4. Record the token delta between the raw and projected response.
5. Refuse ad hoc projections that drop fields required for audit.
6. Emit the projected response with the projection reference and delta.

## Outputs
| Area | Contract |
|---|---|
| Primary | A projected tool response with only declared fields and a recorded token delta. |
| Verification | Recorded projection config and deltas that reproduce the projected payload. |
| Failure | A fail-closed error report naming the audit-required field and the refused projection. |

## Runnable Example
```python
def project_response(raw, projection, audit_fields):
    missing = [f for f in audit_fields if f not in raw]
    if missing:
        return {"ok": False, "reason": "audit_field_missing", "fields": missing}
    kept = {k: raw[k] for k in projection if k in raw}
    for f in audit_fields:
        kept.setdefault(f, raw[f])
    return {"ok": True, "body": kept, "raw_fields": len(raw), "kept_fields": len(kept)}

raw = {"flights": [1, 2, 3], "itinerary": {"id": "i1"}, "trace_id": "t-9", "agent_notes": "x"}
r = project_response(raw, ["flights"], audit_fields=["trace_id"])
assert r["ok"] and r["body"]["flights"] == [1, 2, 3] and "trace_id" in r["body"] and "agent_notes" not in r["body"]
bad = project_response({"flights": []}, ["flights"], audit_fields=["trace_id"])
assert bad["ok"] is False and bad["reason"] == "audit_field_missing"
```

## Failure Modes
- The full raw response enters context and the projection is never applied.
- An ad hoc projection drops audit-required fields such as trace identifiers.
- Projection config is absent and the task silently over-consumes context.
- Token savings are claimed without recording the raw versus projected sizes.
- Nested fields are projected by top-level name only and the payload stays large.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Uber's MCP Gateway supports Response Projection to reduce context and improve relevance of tool results (InfoQ, November 2, 2026, dated November 2, 2026) ([public signal](https://www.infoq.com/news/2026/11/uber-mcp-gateway-ai-agents/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Tool Result Truncation](tool-result-truncation.md)
- [API Pagination](api-pagination.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
