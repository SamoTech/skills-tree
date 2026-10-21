---
title: "A2a Agent Card Capability Parsing"
category: 01-perception
level: advanced
stability: experimental
description: "Parse A2A agent card capability blocks so skill declarations, transport endpoints, and security schemes are read deterministically."
added: "2026-10"
version: v1
related: [agent-card-parsing, api-response-parsing]
tags: [a2a, agent-card, parsing, capabilities]
---
# A2a Agent Card Capability Parsing

## Description
Parse A2A agent card capability blocks so skill declarations, transport endpoints, and security schemes are read deterministically. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An A2A client receives a remote agent card and must extract capability and security metadata before dispatching tasks.
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
3. Parse the agent card JSON, extract the capabilities block, the service endpoint, and the security scheme list, and reject cards whose declared protocol version is unsupported.
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
def parse_agent_card(card, supported):
    if card.get("protocolVersion") not in supported:
        raise ValueError("unsupported A2A protocol version")
    caps = card.get("capabilities", {})
    if "url" not in card:
        raise ValueError("agent card missing url")
    return {"url": card["url"], "caps": caps}
card = {"protocolVersion": "0.3.0", "url": "https://agent.example/a2a", "capabilities": {"streaming": True}}
assert parse_agent_card(card, {"0.3.0"})["url"] == "https://agent.example/a2a"
```

## Failure Modes
- Agent cards are trusted without validating the declared protocol version against the supported set.
- Capability blocks are read as always-present and KeyErrors hide which field was missing.
- Security scheme names are compared case-sensitively and valid schemes are rejected.
- Full agent cards are logged and leak endpoint URLs and auth metadata into shared logs.
- A missing endpoint is guessed from the card host and tasks are dispatched to the wrong server.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The Agentic AI Foundation announcement records A2A joining AAIF as an open agentic stack project governed at the foundation (aaif.io, dated August 17, 2026) ([public signal](https://aaif.io/blog/a2a-joins-aaif))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Card Parsing](../01-perception/agent-card-parsing.md)
- [Api Response Parsing](../01-perception/api-response-parsing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
