---
title: "Agent Telemetry Anomaly Labeling"
category: 12-data
level: advanced
stability: experimental
description: "Label agent telemetry anomalies with whether they represent policy violations, contextual anomalies, or benign variation."
added: "2026-11"
version: v1
related: [agent-runtime-anomaly-signal-perception, unusual-but-permitted-agent-behavior-detection]
tags: [data, labeling, telemetry, anomaly]
---
# Agent Telemetry Anomaly Labeling

## Description
Label agent telemetry anomalies with whether they represent policy violations, contextual anomalies, or benign variation. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Anomaly signals from agent telemetry need labeled dispositions.
- Downstream escalation depends on the label type.
- Labeling must record evidence, not just a verdict.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The anomaly signal list, the policy rule set, and the labeling guideline. |
| Outputs | A labeled anomaly list with disposition, matched policy, and evidence reference. |
| Safety | Fail closed by labeling signals with insufficient evidence as unevaluated. |

## Procedure
1. Load anomaly signals and the policy rule set.
2. Match each signal against explicit policy rules.
3. Label unmatched signals as contextual anomalies or benign variation per the guideline.
4. Attach the evidence reference for every label.
5. Emit the labeled list with unevaluated signals named.

## Outputs
| Area | Contract |
|---|---|
| Primary | A labeled anomaly list with disposition, matched policy, and evidence reference. |
| Verification | Signal-to-rule matches that reproduce every label. |
| Failure | A fail-closed report naming signals with insufficient evidence. |

## Runnable Example
```python
def label(signals, rules):
    out = []
    for s in signals:
        rule = rules.get(s["kind"])
        out.append({"sig": s["id"],
                    "label": "violation" if rule else "anomaly",
                    "rule": rule})
    return out
r = label([{"id": 1, "kind": "exfil"}, {"id": 2, "kind": "volume"}],
          {"exfil": "no-exfil"})
assert r[0]["label"] == "violation" and r[1]["label"] == "anomaly"
```

## Failure Modes
- Unmatched signals default to benign without review.
- Labels are emitted without evidence references.
- Policy rules are matched by keyword instead of structured comparison.
- One signal is labeled twice with different dispositions.
- The labeling guideline version is not recorded with the list.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Agent Insider Threat Detection flags abnormal agent behavior, which must then be labeled as violation, anomaly, or benign (AI Agents News, week of November 5, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Runtime Anomaly Signal Perception](../undefined/agent-runtime-anomaly-signal-perception.md)
- [Unusual But Permitted Agent Behavior Detection](../14-security/unusual-but-permitted-agent-behavior-detection.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
