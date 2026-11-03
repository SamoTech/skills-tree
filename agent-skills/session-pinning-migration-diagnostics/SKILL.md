---
name: session-pinning-migration-diagnostics
description: Diagnose and retire session pinning after migrating an MCP deployment to the stateless protocol, proving no request still depends on sticky routing.
metadata:
  source: skills/17-infrastructure/session-pinning-migration-diagnostics.md
  category: 17-infrastructure
  version: "v1"
---
# Session Pinning Migration Diagnostics

## Description
Diagnose and retire session pinning after migrating an MCP deployment to the stateless protocol, proving no request still depends on sticky routing. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A stateless migration is declared complete but load balancers still pin requests and pods still hold session state.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the load balancer configuration, the pod state inventory, and the pinning probe suite. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Inspect load balancer and ingress rules for session affinity settings and record each one.
2. Probe with repeated stateless requests across pods and verify identical responses from any pod.
3. Inspect pods for residual in-memory session structures and record findings.
4. Remove affinity rules one tier at a time, re-running the probe suite after each removal.
5. On a probe failure, restore the rule and report the residual dependency found.
6. Emit a structured result with the rule inventory, probe log, and removal state.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def probe(pods, rule_active):
    responders = {id(p) for p in pods}
    if rule_active and len(responders) > 1:
        return {"ok": False, "reason": "responses differ across pods"}
    return {"ok": True}
pods = [{"r": 1}, {"r": 1}]
assert probe(pods, False)["ok"] is True
assert probe([{"r": 1}, {"r": 2}], True)["ok"] is False
```

## Failure Modes
- Affinity rules are left enabled after migration because no one verified they were unneeded.
- Probes always hit the same pod, so pinning hides behind a warm cache.
- Residual pod state grows unnoticed and later reintroduces pinning requirements.
- Rules are removed all at once and a failure cannot be attributed to a tier.
- Probe failures are attributed to network flake without rerunning the suite.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the stateless MCP migration removing the load-balancing tax and sticky-routing overhead that the 2025-11-25 session model required (Google Developers Blog, dated August 5, 2026) ([public signal](https://developers.googleblog.com/scaling-ai-agent-infrastructure-with-the-mcp-stateless-updates/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Elicitation Mrtr Migration](elicitation-mrtr-migration.md)
- [Worker Native Mcp Handler Deployment](worker-native-mcp-handler-deployment.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
