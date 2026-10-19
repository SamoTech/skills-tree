---
title: "Mock LLM Server Implementation"
category: 05-code
level: advanced
stability: experimental
description: "Implement a mock LLM service with scripted deterministic responses so that agent tests run without live model calls or recorded keys."
added: "2026-10"
version: v1
related: [web-api-mocking, llm-eval-harness-ci-integration]
tags: [mocking, testing, determinism, ci]
---
# Mock LLM Server Implementation

## Description
Implement a mock LLM service with scripted deterministic responses so that agent tests run without live model calls or recorded keys. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Agent tests must run deterministically in CI without live model dependencies.
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
3. Script the responses keyed by request signature, implement the same transport surface as the real provider, and verify that an unmatched request fails the test instead of improvising a response.
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
def respond(script, request):
    key = (request["model"], request["messages"][-1]["role"])
    if key not in script:
        raise AssertionError("unscripted request")
    return script[key]
s = {("m", "user"): "ok"}
assert respond(s, {"model": "m", "messages": [{"role": "user"}]}) == "ok"
```

## Failure Modes
- Unmatched requests fall back to a generic response and hide missing-coverage errors.
- The mock reimplements provider semantics from memory and drifts from the real error surface.
- Scripted keys are so loose that the wrong script entry matches a different request.
- The mock ignores token-limit and rate-limit errors, so the agent never exercises its retry paths.
- Live keys remain reachable from the test configuration even though the mock is in use.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 agent evaluation practice covers running agent test harnesses deterministically in CI without live model variance (futransolutions.com, dated October 2026) ([public signal](https://futransolutions.com/blog/ai-agent-observability-in-2026-how-to-trace-evaluate-and-debug-ai-that-takes-action/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Web API Mocking](../11-web/web-api-mocking.md)
- [LLM Eval Harness CI Integration](../05-code/llm-eval-harness-ci-integration.md)

## Changelog
| Version | Date | Notes |
|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
