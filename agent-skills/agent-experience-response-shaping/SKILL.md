---
name: agent-experience-response-shaping
description: Shape brand responses so AI agents visiting a site receive accurate, machine-actionable answers instead of scraped fragments.
metadata:
  source: skills/06-communication/agent-experience-response-shaping.md
  category: 06-communication
  version: "v1"
---

# Agent Experience Response Shaping

## Description
Shape brand responses so AI agents visiting a site receive accurate, machine-actionable answers instead of scraped fragments. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A brand site serves AI visitors and must shape its responses to agents as deliberately as it serves human readers.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Inventory the questions agents actually ask the property, then declare per-question response content with verified facts and record every served response with its source document.
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
def shape(question, facts):
    answer = facts.get(question)
    return {"answer": answer, "status": "served" if answer else "no_content"}
out = shape("return-policy", {"return-policy": "30-day full refund with receipt"})
assert out["status"] == "served" and out["answer"].startswith("30-day")
assert shape("warranty", {})["status"] == "no_content"
```

## Failure Modes
- Responses are generated ad hoc without a declared fact source and agents receive contradictions.
- Marketing superlatives are served as factual answers and downstream agents repeat them as verifiable claims.
- No-content questions return invented answers instead of an explicit gap signal.
- Response shaping is only applied to the human crawl path and agent traffic gets stale fragments.
- Served responses are not logged and drift from the underlying documents is never detected.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Fibr AI launched Agent Experience Optimization on October 28 to adapt brand websites for AI platforms and agents (agentic.ai news roundup, dated checked October 30, 2026) ([public signal](https://agentic.ai/news))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Multi Model Benchmark Claim Communication](multi-model-benchmark-claim-communication.md)
- [Agent Supervisor Brief Writing](agent-supervisor-brief-writing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
