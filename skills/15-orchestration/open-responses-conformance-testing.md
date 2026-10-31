---
title: "Open Responses Conformance Testing"
category: 15-orchestration
level: advanced
stability: experimental
description: "Test LLM interface conformance against the open Responses specification so interoperable clients and servers actually interoperate."
added: "2026-10"
version: v1
related: [single-api-multi-model-gateway-configuration, cross-cloud-agent-orchestration-unification]
tags: [conformance, interoperability, testing, specifications]
---
# Open Responses Conformance Testing

## Description
Test LLM interface conformance against the open Responses specification so interoperable clients and servers actually interoperate. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A team implements or adopts an Open Responses interface and must prove conformance before clients depend on it.
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
3. Run the declared conformance suite against the interface under test, then record every deviation with its failing case and required correction before certifying conformance.
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
def conformance(results):
    failures = [r for r in results if not r["passed"]]
    return {"certified": not failures, "failures": failures, "total": len(results)}
r = conformance([{"case": "streaming", "passed": True}, {"case": "tool-calls", "passed": False}])
assert not r["certified"] and r["failures"][0]["case"] == "tool-calls" and r["total"] == 2
```

## Failure Modes
- Conformance is certified from the server's own demo client and no independent client is tested.
- Deviations are waived one by one until the suite passes and the waivers are not recorded.
- Optional protocol features are skipped and real clients fail on them in production.
- The suite runs against a stub backend and the live interface is never tested.
- Conformance is checked once at launch and later versions ship untested.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- OpenAI contributed Open Responses, an open specification for interoperable LLM interfaces, as an Agentic AI Foundation hosted project (InfoQ AGNTCon + MCPCon 2026 coverage, dated October 26, 2026) ([public signal](https://www.infoq.com/news/2026/10/agntcon-mcpcon-2026/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Single Api Multi Model Gateway Configuration](single-api-multi-model-gateway-configuration.md)
- [Cross Cloud Agent Orchestration Unification](cross-cloud-agent-orchestration-unification.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
