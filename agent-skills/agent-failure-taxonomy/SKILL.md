---
name: agent-failure-taxonomy
description: Classify agent failures into a shared, evidence-based taxonomy — planning, retrieval, reasoning, execution, environment — so fixes land at the right layer.
metadata:
  source: skills/09-agentic-patterns/agent-failure-taxonomy.md
  category: 09-agentic-patterns
  version: "v1"
---

# Agent Failure Taxonomy

Category: Agentic Patterns | Level: intermediate | Stability: experimental | Version: v1

## Description

Agents fail in characteristic ways, and a fix aimed at the wrong layer is a fix that did not happen. This skill gives the failures names: a plan that never fit the goal, retrieval that brought back wrong evidence, reasoning that misjoined what it had, execution that fumbled a working plan, environment that changed under the run. Classification comes from traces — where the first wrong step appears — and the taxonomy pays for itself by making postmortems comparable across incidents instead of anecdotal.

## When to Use

Use when reviewing a failed agent run — incident triage, postmortem, quality review — before anyone decides what to change.

Do not skip classification and jump to the most recent failure; without a layer verdict, fixes become folklore and the same class recurs.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `trace` | `list` | Yes | The observable steps of the failed run |
| `goal` | `string` | Yes | What the run was supposed to accomplish |
| `taxonomy` | `map` | Yes | The failure classes and their diagnostic criteria |

## Procedure

1. Reconstruct the run from its trace: what was asked, what was retrieved, what was decided, what was executed.
2. Locate the first wrong step — the earliest point where the run departed from a path that could still reach the goal.
3. Classify by layer: planning, retrieval, reasoning, execution, or environment, using the criteria of the taxonomy rather than intuition.
4. Distinguish root cause from symptom: a wrong answer is a symptom; the layer that injected the error is the cause.
5. Record the classification with its evidence — the trace excerpt that supports it — so the verdict is reviewable.
6. Aggregate over incidents: recurrence by class is the signal that directs where the next fix budget goes.

## Outputs

| Output | Type | Description |
|---|---|---|
| `classification` | `map` | Failure class, layer, and supporting trace evidence |
| `postmortem` | `record` | Cause, fix target layer, and recurrence tracking |

## Runnable Example

```python
def classify(first_wrong_step, evidence_ok):
    if not evidence_ok:
        return "retrieval"
    if first_wrong_step == "plan":
        return "planning"
    if first_wrong_step == "inference":
        return "reasoning"
    if first_wrong_step == "action":
        return "execution"
    return "environment"

cases = [
    ("plan", True),
    ("inference", False),
    ("action", True),
    ("world changed", True),
]
for step, ok in cases:
    print(step, "->", classify(step, ok))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Layer guessing | Verdicts assigned without trace evidence | Classify from the first wrong step, with excerpts |
| Symptom fixes | The visible error fixed, the cause untouched | Separate the root cause layer from the symptom |
| Folklore drift | Each postmortem invents new categories | Use one shared taxonomy across incidents |
| Single-incident bias | One failure reshapes the whole system | Aggregate recurrence by class before redesigning |
| Unclassified residue | Failures that fit no class get skipped | Extend the taxonomy explicitly when a class is missing |

## Security and Authority Boundary

Failure traces contain the data the run touched, including anything sensitive it retrieved or produced: postmortems and classification records must redact secrets at capture time, because a taxonomy entry quoting a credential is a leak with good documentation.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia's overview of fault tree analysis (https://en.wikipedia.org/wiki/Fault_tree_analysis).
2. The OWASP Top 10 for Large Language Model Applications project (https://owasp.org/www-project-top-10-for-large-language-model-applications/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Agent Observability Tracing](agent-observability-tracing.md) — the traces classification reads.
- [Critic Agent](critic-agent.md) — catching failures before they leave the run.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
