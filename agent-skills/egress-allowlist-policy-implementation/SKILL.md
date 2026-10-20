---
name: egress-allowlist-policy-implementation
description: Implement network egress allowlists for agents so outbound traffic only reaches destinations the policy explicitly permits.
metadata:
  source: skills/05-code/egress-allowlist-policy-implementation.md
  category: 05-code
  version: "v1"
---

# Egress Allowlist Policy Implementation

## Description
Implement network egress allowlists for agents so outbound traffic only reaches destinations the policy explicitly permits. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent workload must be constrained to approved egress destinations before it runs.
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
3. Translate the approved destination policy into an allowlist with explicit deny-by-default, wire it into the workload's egress path, and record verification that non-approved destinations are actually blocked.
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
def allowed(host, rules):
    if any(h == host for h in rules.get("allow", [])):
        return True
    return rules.get("default", "deny") == "allow"
rules = {"allow": ["api.example.com"]}
assert allowed("api.example.com", rules) is True
assert allowed("evil.example", rules) is False
```

## Failure Modes
- The allowlist ships with a permissive catch-all entry that negates deny-by-default.
- Rules match on hostname only and a rotated destination address bypasses them.
- Verification tests the allow path but never the deny path.
- The policy is implemented in one environment and the others drift.
- An agent can modify the allowlist itself at runtime.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 agent security guidance pairs credential injection with egress policy to bound what an agent can reach (agentgateway.dev, dated 2026) ([public signal](https://agentgateway.dev/blog/2026-07-27-credential-injection-ai-agent-egress-cb4a/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Sandbox Egress Proxy Configuration](../17-infrastructure/sandbox-egress-proxy-configuration.md)
- [Agentic Ssrf Prevention](../14-security/agentic-ssrf-prevention.md)

## Changelog
| Version | Date | Notes |
|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
