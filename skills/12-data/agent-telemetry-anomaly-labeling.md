---
title: "Agent Telemetry Anomaly Labeling"
category: 12-data
level: advanced
stability: experimental
description: "Label agent telemetry anomalies with context tags so detection models and reviewers share one annotation scheme."
added: "2026-11"
version: v1
related: [agent-runtime-anomaly-signal-perception, agent-observability-tooling-evaluation]
tags: [data, labeling, telemetry, agents]
---
# Agent Telemetry Anomaly Labeling

## Description
Label agent telemetry anomalies with context tags so detection models and reviewers share one annotation scheme. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Anomaly signals need consistent labels across reviewers.
- Detection model training needs labeled telemetry.
- Label provenance must be auditable.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The anomaly signal stream, the label taxonomy, and the reviewer identity list. |
| Outputs | A labeled anomaly dataset with taxonomy tags, reviewer identities, and provenance links. |
| Safety | Fail closed by rejecting labels outside the taxonomy. |

## Procedure
1. Define the label taxonomy covering behavior class, context, and severity.
2. Route each anomaly signal to a reviewer or model labeler.
3. Validate every label against the taxonomy before acceptance.
4. Record labeler identity and the signal provenance link.
5. Emit the labeled dataset with disagreement counts.

## Outputs
| Area | Contract |
|---|---|
| Primary | A labeled anomaly dataset with taxonomy tags, reviewer identities, and provenance links. |
| Verification | Label validation results and provenance links that reproduce the dataset. |
| Failure | A fail-closed report naming rejected out-of-taxonomy labels. |

## Runnable Example
```python
def label(signals, taxonomy, labels):
    out = []
    for s in signals:
        lab = labels.get(s["id"])
        if lab not in taxonomy:
            return {"ok": False, "rejected": s["id"]}
        out.append({"id": s["id"], "label": lab})
    return {"ok": True, "labeled": out}
r = label([{"id": "s1"}, {"id": "s2"}], {"permitted-unusual", "rule-violation"},
          {"s1": "permitted-unusual", "s2": "weird"})
assert r["ok"] is False and r["rejected"] == "s2"
```

## Failure Modes
- Free-text labels are accepted, breaking the taxonomy.
- Labeler identity is dropped, so disputes cannot be resolved.
- Signals are labeled without provenance links.
- Disagreement between labelers is averaged away.
- Model-generated labels are recorded as reviewer labels.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- CrowdStrike introduced Agent Insider Threat Detection to identify abnormal behavior by AI agents, which requires consistently labeled anomaly telemetry (AI Agents News, week of November 5, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Runtime Anomaly Signal Perception](agent-runtime-anomaly-signal-perception.md)
- [Agent Observability Tooling Evaluation](agent-observability-tooling-evaluation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
