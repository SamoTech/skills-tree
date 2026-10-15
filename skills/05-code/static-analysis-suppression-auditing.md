---
title: "Static Analysis Suppression Auditing"
category: 05-code
level: advanced
stability: experimental
description: "Audit inline static-analysis suppressions for scope, owner, expiry, and justification, replacing blanket suppressions with per-finding ones that expire."
added: "2026-10"
version: v1
related: [static-analysis, agent-generated-code-auditing]
tags: [static-analysis, suppressions, audit]
---
# Static Analysis Suppression Auditing

## Description
Audit inline static-analysis suppressions for scope, owner, expiry, and justification, replacing blanket suppressions with per-finding ones that expire. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Suppression comments accumulate and must be audited rather than trusted.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | static analysis suppression auditing task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the static analysis suppression auditing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A suppression inventory with owner, scope, expiry, and a justification check per entry. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def audit(suppressions, allowed={"nosec", "ignore"}):
    bad = [s for s in suppressions if s["kind"] not in allowed]
    expired = [s for s in suppressions if s.get("expires", "none") == "none"]
    return bad + expired
s = [{"kind": "nosec"}, {"kind": "magic"}]
assert audit(s) == [{"kind": "magic"}]
```

## Failure Modes
- Acting outside the declared task boundary.
- Accepting a blanket file-level suppression for a one-line finding.
- Leaving suppressions with no expiry, muting future real findings.
- Retrying without preserving state or evidence.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Suppression audits appear in 2026 repo quality request threads. ([public signal](https://github.com/SamoTech/skills-tree/issues/357))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [static analysis](../05-code/static-analysis.md)
- [agent generated code auditing](../05-code/agent-generated-code-auditing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
