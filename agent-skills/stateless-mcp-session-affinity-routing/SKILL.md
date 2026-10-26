---
name: stateless-mcp-session-affinity-routing
description: Route stateless MCP session requests so each self-contained request reaches the backend shard that can serve its pinned context.
metadata:
  source: skills/11-web/stateless-mcp-session-affinity-routing.md
  category: 11-web
  version: "v1"
---

# Stateless MCP Session Affinity Routing

## Description
Route stateless MCP session requests so each self-contained request reaches the backend shard that can serve its pinned context. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

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
3. Extract the session identity from the request's declared headers, map it to a shard via the declared affinity ring, and reject requests whose session identity is absent rather than routing them randomly.
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
def route(session_id, ring, shards):
    if not session_id:
        raise ValueError("missing session identity")
    h = sum(ord(c) for c in session_id)
    return shards[h % len(shards)]

assert route("sess-42", None, ["s1", "s2"]) == "s2"
try:
    route("", None, ["s1", "s2"]); assert False
except ValueError:
    pass
```

## Failure Modes
- Requests without session identity are routed round-robin and cache locality is destroyed.
- Affinity is computed from the client IP and mobile clients hop shards mid-session.
- A shard evacuation drops affinity mappings and pinned context becomes unreachable.
- Session identity is taken from an unsigned header and an attacker pins other sessions.
- The affinity ring is rebalanced during peak traffic and most sessions re-pin at once.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Google's infrastructure guide covers scaling AI agent infrastructure with the MCP stateless updates (developers.googleblog.com, dated October 2026) ([public signal](https://developers.googleblog.com/scaling-ai-agent-infrastructure-with-the-mcp-stateless-updates/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [MCP Stateless Session Header Parsing](../01-perception/mcp-stateless-session-header-parsing.md)
- [CDN Cache Purge Automation](../11-web/cdn-cache-purge-automation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
