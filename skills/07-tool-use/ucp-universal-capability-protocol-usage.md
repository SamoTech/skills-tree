---
title: "UCP Universal Capability Protocol Usage"
category: 07-tool-use
level: advanced
stability: experimental
description: "Invoke tools through the Universal Capability Protocol, negotiating capability discovery, invocation envelopes, and error contracts per the published ecosystem map."
added: "2026-10"
version: v1
related: [mcp-tool, anp-agent-network-protocol-usage]
tags: [protocols, ucp, tool-invocation]
---
# UCP Universal Capability Protocol Usage

## Description
Invoke tools through the Universal Capability Protocol, negotiating capability discovery, invocation envelopes, and error contracts per the published ecosystem map. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A target tool is exposed over UCP rather than MCP or native APIs.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | UCP invocation and capability discovery task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the UCP invocation and capability discovery steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A UCP invocation record with the discovered capability, the envelope sent, and the normalized result or declared error contract. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def invoke(capabilities, name, args):
    cap = capabilities.get(name)
    if cap is None or cap.get("deprecated"):
        return {"error": "capability-unavailable"}
    return {"result": cap["invoke"](args)}
caps = {"translate": {"deprecated": False, "invoke": lambda a: a["text"].upper()}}
assert invoke(caps, "translate", {"text": "hi"})["result"] == "HI"
assert invoke(caps, "missing", {})["error"] == "capability-unavailable"
```

## Failure Modes
- Assuming MCP semantics for fields UCP defines differently.
- Calling a capability without discovering its current schema first.
- Mapping UCP errors to success because the transport returned 200.
- Ignoring capability deprecation notices in discovery responses.
- Hard-coding capability IDs that the protocol does not promise to be stable.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The 2026 agent protocol ecosystem map documents UCP alongside MCP, A2A, and ACP as a live interoperation option ([public signal](https://www.digitalapplied.com/blog/ai-agent-protocol-ecosystem-map-2026-mcp-a2a-acp-ucp))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Mcp Tool](../07-tool-use/mcp-tool.md)
- [Anp Agent Network Protocol Usage](../07-tool-use/anp-agent-network-protocol-usage.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
