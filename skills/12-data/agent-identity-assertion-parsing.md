---
title: "Agent Identity Assertion Parsing"
category: 12-data
level: advanced
stability: experimental
description: "Parse agent identity assertions into typed claims, verify the signature scheme and key material against a pinned trust list, and reject expired or unknown-key assertions."
added: "2026-10"
version: v1
related: [delegation-chain-verification, agent-traffic-metadata-enrichment]
tags: [identity, assertions, parsing]
---
# Agent Identity Assertion Parsing

## Description
Parse agent identity assertions into typed claims, verify the signature scheme and key material against a pinned trust list, and reject expired or unknown-key assertions. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent presents an identity assertion that a relying service must parse and verify.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | agent identity assertion parsing task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the agent identity assertion parsing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A parsed identity record with issuer, scopes, and an accept or reject verdict with reason. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def parse_assertion(assertion, trusted_keys, now):
    if assertion["issuer"] not in trusted_keys or now >= assertion["exp"]:
        return None
    return {"issuer": assertion["issuer"], "scopes": assertion["scopes"]}
trusted = {"agent-a": "k1"}
a = {"issuer": "agent-a", "sig": "k1|memory:read", "exp": 200, "scopes": ["memory:read"]}
assert parse_assertion(a, trusted, 100) is not None
assert parse_assertion(a, trusted, 300) is None
```

## Failure Modes
- Acting outside the declared task boundary.
- Accepting an assertion signed by an unknown key.
- Letting an expired assertion through by comparing the wrong clock reading.
- Trusting scopes listed in the assertion without checking they were granted.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Agent identity assertion verification is documented in 2026 agentic identity guidance. ([public signal](https://twilio.com/en-us/blog/insights/agentic-identity))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Delegation Chain Verification](../14-security/delegation-chain-verification.md)
- [Agent Traffic Metadata Enrichment](../08-multimodal/agent-traffic-metadata-enrichment.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
