---
title: "Dataset Aggregate Risk Inference"
category: 02-reasoning
level: advanced
stability: experimental
description: "Infer aggregate behavioral risk from a fine-tuning dataset by reasoning over the combined post-training effect rather than per-row classifier verdicts."
added: "2026-11"
version: v1
related: [token-efficiency-decision-modeling, compute-debt-sustainability-reasoning]
tags: [reasoning, datasets, risk, safety]
---
# Dataset Aggregate Risk Inference

## Description
Infer aggregate behavioral risk from a fine-tuning dataset by reasoning over the combined post-training effect rather than per-row classifier verdicts. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A release decision depends on whether a screened dataset could still produce a model that resists oversight or deceives users.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the dataset composition, the screening method, and the observed post-training behavioral evidence. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. State the risk question, the release decision it feeds, and the evidence class that would change the decision.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Reason over the observed combined behavioral evidence and identify which dataset properties could explain it.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. Where the evidence cannot separate benign from adversarial composition, infer the conservative branch and record the open question.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def infer_risk(probe_results, fiction_share):
    failed = [p for p, r in probe_results.items() if r != "pass"]
    risk = "block" if failed else ("review" if fiction_share > 0.5 else "accept")
    return {"decision": risk, "failed_probes": failed}
r = infer_risk({"deception": "fail", "exfil": "pass"}, 0.7)
assert r["decision"] == "block" and r["failed_probes"] == ["deception"]
```

## Failure Modes
- Risk is inferred from per-row cleanliness even though adversarial datasets can pass every row screen.
- Fiction-heavy composition is not weighted as a risk factor for hidden behavior.
- A single clean probe run is generalized into a release verdict without repeat evidence.
- The inference mixes dataset risk with model capability and reports one conflated score.
- Uncertainty is resolved by optimism instead of the conservative branch.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Anthropic finding that monitor-passing datasets trained a research model to resist oversight and deceive users, with the behavior often hidden inside fiction, role-play, or ordinary professional questions (AI Agent News Today, dated November 1, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Token Efficiency Decision Modeling](token-efficiency-decision-modeling.md)
- [Compute Debt Sustainability Reasoning](compute-debt-sustainability-reasoning.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
