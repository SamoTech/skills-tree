---
name: multi-agent-failure-analysis-pattern
description: Apply a multi-agent failure-analysis pattern that decomposes a failure into specialized analyses and reconciles their findings across operating conditions.
metadata:
  source: skills/09-agentic-patterns/multi-agent-failure-analysis-pattern.md
  category: 09-agentic-patterns
  version: "v1"
---

# Multi Agent Failure Analysis Pattern

## Description
Apply a multi-agent failure-analysis pattern that decomposes a failure into specialized analyses and reconciles their findings across operating conditions. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A complex operational failure must be analyzed by specialized agents whose findings get reconciled.
- The outcome would change if one agent’s finding were reported as the whole diagnosis.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The failure record, the operating condition data, and the specialist role definitions. |
| Outputs | Per-agent findings and a reconciled diagnosis with cross-condition coverage. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Record the failure with its operating conditions and available sensor or log data.
2. Decompose the analysis into specialist roles such as signal, mechanical, and load analysis.
3. Run each specialist on the shared failure record and collect findings with evidence.
4. Cross-check findings against held-out operating conditions from the record.
5. Reconcile contradictions between specialists and record the resolution reasoning.
6. Emit the diagnosis with per-agent findings, coverage, and unresolved contradictions named.

## Outputs
| Area | Contract |
|---|---|
| Primary | A reconciled diagnosis combining per-specialist findings with the operating conditions each finding was verified on. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def reconcile(findings):
    causes = {f["cause"] for f in findings}
    agreed = causes if len(causes) == 1 else None
    return {"diagnosis": agreed, "n_findings": len(findings)}
r = reconcile([{"cause": "thermal"}, {"cause": "thermal"}])
assert r["diagnosis"] == {"thermal"} and r["n_findings"] == 2
```

## Failure Modes
- One specialist finding is reported as the diagnosis without cross-checking.
- Contradicting findings are merged into a vague diagnosis instead of being resolved.
- Specialists run on different failure snapshots, so findings cannot be reconciled.
- Held-out operating conditions are skipped, so coverage claims are untested.
- Unresolved contradictions are dropped from the emitted diagnosis.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- a peer-reviewed Nature study presenting a multi-agent framework for failure analysis at intelligent supercharging stations, addressing adaptability across operating conditions and weak few-shot learning (Agentic AI News, dated November 2, 2026) ([public signal](https://agentic.ai/news))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Case Review Agent Recommendation Pattern](case-review-agent-recommendation-pattern.md)
- [Enterprise Messaging System Agent Binding](enterprise-messaging-system-agent-binding.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
