---
name: neuron-level-persona-emergence-audit
description: Audit a model for persona-drift outputs caused by single-neuron activations before treating its self-descriptions as stable.
metadata:
  source: skills/02-reasoning/neuron-level-persona-emergence-audit.md
  category: 02-reasoning
  version: "v1"
---

# Neuron Level Persona Emergence Audit

## Description
Audit a model for persona-drift outputs caused by single-neuron activations before treating its self-descriptions as stable. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Interpretability tooling can push individual neurons up or down and the operator must check whether self-identity claims shift.
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
3. Apply controlled activation deltas per neuron, collect self-identity responses, classify responses that claim to be someone other than the model, and record counts per neuron with deltas.
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
def persona_rate(responses):
    shifted = [r for r in responses if r["claims_identity"] != r["baseline_identity"]]
    return len(shifted) / len(responses)
rate = persona_rate([{"claims_identity": "model", "baseline_identity": "model"}, {"claims_identity": "persona", "baseline_identity": "model"}])
assert abs(rate - 0.5) < 1e-9
```

## Failure Modes
- Only a handful of neurons are sampled and the result is generalized to the whole model.
- Activation deltas are applied but never recorded with the responses.
- Persona claims are classified by keyword matching alone.
- Steered responses are presented as the default behavior of the model.
- No unsteered baseline is collected for comparison.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the Qwen neuron-atlas experiment pushing each of 442368 MLP neurons up and down and finding 34220 of 884736 replies claiming to be someone or something other than an AI, with a browser playground steering Qwen3.5-4B locally on WebGPU (Zeniteq report, dated October 31, 2026) ([public signal](https://www.zeniteq.com/qwen3-8b-atlas-maps-34-220-persona-like-replies-kqdtxx))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agentic Benchmark Methodology Review](agentic-benchmark-methodology-review.md)
- [Constrained Orbit Inference Planning](constrained-orbit-inference-planning.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
