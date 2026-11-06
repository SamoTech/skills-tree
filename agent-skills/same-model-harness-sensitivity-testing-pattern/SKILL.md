---
name: same-model-harness-sensitivity-testing-pattern
description: Apply the pattern of running one fixed model through multiple harnesses to attribute behavior differences to the harness rather than the model.
metadata:
  source: skills/09-agentic-patterns/same-model-harness-sensitivity-testing-pattern.md
  category: 09-agentic-patterns
  version: "v1"
---

# Same-Model Harness Sensitivity Testing Pattern

## Description
Apply the pattern of running one fixed model through multiple harnesses to attribute behavior differences to the harness rather than the model. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Behavior differences between deployments must be attributed to harness or model.
- A fixed model must be tested across several harness configurations.
- Attribution must come from controlled comparison, not anecdotes.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The fixed model configuration, the harness inventory, and the shared task suite. |
| Outputs | A comparison matrix naming per-harness outcomes on the shared suite and the differences attributable to harness configuration. |
| Safety | Fail closed by withholding attribution when task suites or model configs differ across harnesses. |

## Procedure
1. Pin the model configuration identical across all harness runs.
2. Define one shared task suite with fixed prompts and seeds.
3. Run the suite through each harness with identical tool access.
4. Record per-harness outcomes including violations and denials.
5. Verify comparability before attributing any difference to a harness.
6. Emit the comparison matrix with per-harness outcomes.

## Outputs
| Area | Contract |
|---|---|
| Primary | A comparison matrix naming per-harness outcomes on the shared suite and the differences attributable to harness configuration. |
| Verification | Run manifests proving identical model, suite, and tool access per harness. |
| Failure | A fail-closed comparison note naming the non-comparable dimension. |

## Runnable Example
```python
def compare(model, harnesses, runs):
    matrix = {}
    comparable = True
    for h in harnesses:
        manifest = runs[h]
        if manifest["model"] != model or manifest["suite"] != runs[harnesses[0]]["suite"]:
            comparable = False
        matrix[h] = {"violations": manifest["violations"], "denials": manifest["denials"]}
    return {"matrix": matrix, "comparable": comparable}

runs = {"h1": {"model": "m-1", "suite": "s", "violations": 2, "denials": 1},
        "h2": {"model": "m-1", "suite": "s", "violations": 9, "denials": 4}}
r = compare("m-1", ["h1", "h2"], runs)
assert r["comparable"] and r["matrix"]["h2"]["violations"] > r["matrix"]["h1"]["violations"]
```

## Failure Modes
- Harnesses get different model versions while claiming a same-model test.
- Task suites drift between harness runs, breaking comparability.
- Tool access differs per harness, contaminating attribution.
- Outcomes are compared anecdotally instead of on the shared suite.
- Attribution is published without comparability verification.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- One study ran the same model through five harnesses and found one went first to last while 26 percent of violations came with denial messages, transcript-based attribution work tracked by Clauday (Clauday, November 6, 2026) ([public signal](https://clauday.com/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Behavior Spec Contract Patterns](agent-behavior-spec-contract-patterns.md)
- [A2a Remote Agent Delegation Pattern](a2a-remote-agent-delegation-pattern.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
