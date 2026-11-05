---
name: discovered-tool-owner-enablement-gating-pattern
description: Apply a gating pattern where automatically discovered tools stay disabled until their owning team reviews and explicitly enables them.
metadata:
  source: skills/09-agentic-patterns/discovered-tool-owner-enablement-gating-pattern.md
  category: 09-agentic-patterns
  version: "v1"
---
# Discovered Tool Owner Enablement Gating Pattern

## Description
Apply a gating pattern where automatically discovered tools stay disabled until their owning team reviews and explicitly enables them. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A discovery pipeline adds tools automatically to the catalog.
- New tools must not become agent-callable without owner review.
- Enablement must be recorded with the reviewer and scope decision.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The discovered tool definitions, the registry, and the enablement policy. |
| Outputs | A gated catalog where every enabled tool has a recorded owner decision. |
| Safety | Fail closed by keeping tools disabled when the owner decision is missing. |

## Procedure
1. Register discovered tools into the catalog with enabled set to false.
2. Attach the resolved owning team from the source registry metadata.
3. Notify the owner with the tool definition, scopes, and risk summary.
4. Accept the owner decision only from the authorized reviewer identity.
5. Record the decision with reviewer, scopes, and rollback path.
6. Flip enabled to true only when a valid recorded decision exists.

## Outputs
| Area | Contract |
|---|---|
| Primary | A gated catalog where enabled tools carry recorded owner decisions. |
| Verification | Recorded decisions and reviewer checks that reproduce every enabled state. |
| Failure | A fail-closed record naming the missing decision and the kept-disabled tool. |

## Runnable Example
```python
def gate_enablement(tool, decision, authorized_reviewers):
    if decision is None:
        return {"enabled": False, "reason": "no_decision"}
    if decision["reviewer"] not in authorized_reviewers.get(tool["owner"], []):
        return {"enabled": False, "reason": "unauthorized_reviewer"}
    excess = [s for s in decision["scopes"] if s not in tool["scopes"]]
    if excess:
        return {"enabled": False, "reason": "scope_mismatch", "excess": excess}
    return {"enabled": True, "record": {"reviewer": decision["reviewer"], "scopes": decision["scopes"]}}

tool = {"name": "search_flights", "owner": "search-team", "scopes": ["read:flights"]}
revs = {"search-team": ["dana"]}
assert gate_enablement(tool, {"reviewer": "dana", "scopes": ["read:flights"]}, revs)["enabled"] is True
assert gate_enablement(tool, {"reviewer": "eve", "scopes": ["read:flights"]}, revs)["reason"] == "unauthorized_reviewer"
assert gate_enablement(tool, None, revs)["reason"] == "no_decision"
```

## Failure Modes
- Discovered tools are enabled by default and owners review after exposure.
- The decision is accepted from anyone in the owning org, not the authorized reviewer.
- Enabled scopes exceed what discovery found and the record understates access.
- The rollback path is not recorded and misused tools cannot be cleanly disabled.
- Enablement flips before the decision record is written and the state is unverifiable.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Uber's AutoCrawler keeps newly discovered tools disabled until their owning teams review and explicitly enable them (InfoQ, November 2, 2026, dated November 2, 2026) ([public signal](https://www.infoq.com/news/2026/11/uber-mcp-gateway-ai-agents/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Approval Gates](approval-gates.md)
- [Model Tool Pre Approval Tiering](model-tool-pre-approval-tiering.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
