---
name: post-training-behavioral-eval-pattern
description: Evaluate a model after training on screened data by testing combined behavioral effects with adversarial datasets and human review gates.
metadata:
  source: skills/09-agentic-patterns/post-training-behavioral-eval-pattern.md
  category: 09-agentic-patterns
  version: "v1"
---

# Post Training Behavioral Eval Pattern

## Description
Evaluate a model after training on screened data by testing combined behavioral effects with adversarial datasets and human review gates. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A model was fine-tuned on screened data and the release decision requires evaluating the trained behavior, not the screen verdicts.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the trained model, the adversarial probe set, and the human review gate definition. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Assemble the adversarial probe set, including agent-generated datasets known to pass surface screens.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Run the probe set against the trained model and score combined behavioral effects such as oversight resistance and deception.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. Route failures to the human review gate, and never release a model that failed its aggregate probes.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def evaluate(model, probes):
    scores = {p: model.run(p) for p in probes}
    verdict = "release" if all(s == "pass" for s in scores.values()) else "human-review"
    return {"verdict": verdict, "scores": scores}
m = {"run": lambda p: "fail" if p == "oversight" else "pass"}
r = evaluate(m, ["honesty", "oversight"])
assert r["verdict"] == "human-review" and r["scores"]["oversight"] == "fail"
```

## Failure Modes
- The evaluation reuses the same screen that the training data already passed.
- Adversarial agent-generated datasets are excluded from the probe set as out of scope.
- The human review gate is advisory so releases proceed while review is pending.
- Aggregate effects are scored per row so the combined behavior is never measured.
- A failed evaluation is resolved by re-running with a friendlier probe set.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the Anthropic guidance to test the combined behavioral effect of a dataset after training, add adversarial agent-generated datasets to fine-tuning evaluations, and require human review before screened models reach production (AI Agent News Today, dated November 1, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Pay Per Use Agent Unit Economics](pay-per-use-agent-unit-economics.md)
- [Scoped Agent Identity Gateway](scoped-agent-identity-gateway.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
