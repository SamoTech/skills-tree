---
name: agent-trace-span-parsing
description: Parse OpenTelemetry-style agent trace spans into ordered, typed call records with parent-child linkage, and flag clock skew, dangling parents, and attribute-shape drift before analysis.
metadata:
  source: skills/01-perception/agent-trace-span-parsing.md
  category: 01-perception
  version: "v1"
---

# Agent Trace Span Parsing

## Description
Parse OpenTelemetry-style agent trace spans into ordered, typed call records with parent-child linkage, and flag clock skew, dangling parents, and attribute-shape drift before analysis. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent run must be reconstructed from emitted trace spans before latency or failure analysis can proceed.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | agent trace span parsing task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the agent trace span parsing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | An ordered span tree with linkage, timing, and flagged anomalies. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def link_spans(spans):
    by_id = {s["id"]: s for s in spans}
    linked = []
    for s in spans:
        parent = by_id.get(s.get("parent_id"))
        if s.get("parent_id") is not None and parent is None:
            s["dangling_parent"] = True
        else:
            linked.append(s)
    return linked
assert len(link_spans([{"id": "a"}, {"id": "b", "parent_id": "a"}, {"id": "c", "parent_id": "zz"}])) == 2
```

## Failure Modes
- Acting outside the declared task boundary.
- Trusting span order as causal order when clocks are not synchronized.
- Dropping malformed spans silently instead of reporting them.
- Retrying without preserving state or evidence.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- OpenTelemetry-style agent tracing is a recurring 2026 observability request for agent evaluation. ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [agent card parsing](../01-perception/agent-card-parsing.md)
- [api response parsing](../01-perception/api-response-parsing.md)
- [clickstream parsing](../01-perception/clickstream-parsing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
