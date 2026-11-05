---
name: decisions-api-real-time-routing-tool-usage
description: Use a bounded decision API as a tool for real-time classification and routing among pre-defined answers, with recorded latency and residual-case handling.
metadata:
  source: skills/07-tool-use/decisions-api-real-time-routing-tool-usage.md
  category: 07-tool-use
  version: "v1"
---

# Decisions API Real-Time Routing Tool Usage

## Description
Use a bounded decision API as a tool for real-time classification and routing among pre-defined answers, with recorded latency and residual-case handling. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A conversation or event stream needs next-action routing decided per-item in real time.
- The outcome would change if the routing answer were free-form and unparseable downstream.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The routing question, the finite answer set, and the per-item context payload. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Send the decision request with the bounded question and context, and parse the returned answer against the finite set.
4. Record the answer, the measured latency, and the residual-case fallback when the answer is outside the set.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A routing record with the chosen answer, latency, and residual-case disposition. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def route(decide, ctx, answers):
    a = decide(ctx)
    if a not in answers:
        return {"answer": "residual", "fallback": "escalate"}
    return {"answer": a}
r = route(lambda c: "auto_reply", {"msg": "hi"}, ["auto_reply", "escalate"])
assert r["answer"] == "auto_reply"
assert route(lambda c: "summarize", {}, ["auto_reply", "escalate"])["answer"] == "residual"
```

## Failure Modes
- Free-form answers are accepted instead of enforcing the finite answer set.
- Latency is not measured, so the real-time budget claim is unverifiable.
- The residual case has no fallback and silently drops the item.
- Context payloads include more data than the routing question requires.
- The answer is not recorded, so routing cannot be audited or replayed.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- OpenAI DevDay 2026 announced the Decisions API, which focuses the model on user-defined questions with finite pre-defined answers for real-time classification, routing, and next-action choices (OpenAI DevDay recap, dated November 4, 2026) ([public signal](https://openai.com/index/devday-2026-recap/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Web Search](../11-web/web-search.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
