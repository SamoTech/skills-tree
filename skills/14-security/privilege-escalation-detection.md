---
title: "Privilege Escalation Detection"
category: 14-security
level: advanced
stability: experimental
description: "Detect privilege escalation attempts from authentication, authorization, and system logs by modeling normal permission change paths and flagging deviations in near real time."
added: "2026-10"
version: v1
related: ["threat-modeling","audit-logging"]
---

# Privilege Escalation Detection

Category: Security | Level: advanced | Stability: experimental | Version: v1

## Description

Privilege escalation rarely breaks in one step; it chains small permission wins. The skill covers modeling the legitimate paths by which accounts and processes gain privilege in an environment, then watching for events that fall outside those paths: unexpected group membership changes, service account logins on new hosts, elevation anomalies, and token manipulation. Detections are chains, so the output correlates events rather than raising single-line alerts.

## When to Use

Use when authorization-relevant logs must be monitored for accounts or processes obtaining more privilege than their documented paths allow.

Do not alert on every permission change. Without a model of legitimate paths, the detection floods operators and real escalations hide in the noise.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `auth_logs` | `table` | Yes | Authentication and authorization events with timestamps and principals |
| `permission_baseline` | `object` | Yes | Documented legitimate privilege change paths per role and host |
| `window` | `int` | No | Correlation window in minutes for chaining related events |

## Procedure

1. Ingest authentication and authorization logs and normalize principals, actions, and targets.
2. Load the permission baseline: who may grant what, through which documented paths.
3. Match each event against the baseline; unmatched events are candidate deviations.
4. Correlate candidates within the window into chains: grant, use, and persist sequences.
5. Score chains by blast radius: what the gained privilege reaches.
6. Emit detections with the full chain, the baseline clause violated, and recommended response.

## Outputs

| Output | Type | Description |
|---|---|---|
| `detections` | `array` | Escalation chains with events, violated baseline clause, and score |
| `baseline_gaps` | `list` | Legitimate-but-unmodeled paths that need baseline updates |
| `response_actions` | `list` | Suggested containment per detection |

## Runnable Example

```python
def correlate_chain(events, window):
    """events: [(ts, principal, action)] sorted by ts"""
    chains = []
    current = []
    for ev in events:
        if current and ev[0] - current[0][0] > window:
            if len(current) > 1:
                chains.append([e[1:] for e in current])
            current = []
        if ev[2] in ("grant", "use-privilege", "persist"):
            current.append(ev)
    if len(current) > 1:
        chains.append([e[1:] for e in current])
    return chains

print(correlate_chain(
    [(0, "svc-backup", "grant"), (5, "svc-backup", "use-privilege"), (400, "svc-backup", "persist")],
    window=30,
))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Alert flooding | No baseline, so every change is suspicious | Model legitimate paths first, then deviate |
| Missed slow chains | Events days apart never correlated | Add long-window correlation for persistence stages |
| Service account blind spots | Shared accounts break principal identity | Attribute actions to workload identity where possible |
| Baseline staleness | New admin processes unmodeled | Review baseline gaps emitted by the detection loop |
| Single-event alerts | Chains scored as isolated lines | Score and raise chains, not isolated events |

## Security and Authority Boundary

Escalation detections name accounts and hosts that may already be compromised. Treat detection output as need-to-know, deliver response actions through the incident process, and never auto-revoke broadly without a human confirming the chain is not a legitimate change.

## Evidence

This skill is grounded in dated public implementation references:

1. The MITRE ATT&CK privilege escalation tactic (https://attack.mitre.org/tactics/TA0004/).
2. The PEASS-ng privilege escalation enumeration tooling project (https://github.com/peass-ng/PEASS-ng).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Threat Modeling](threat-modeling.md) — the source of the legitimate privilege paths a baseline encodes.
- [Audit Logging](audit-logging.md) — the tamper-evident event stream detection depends on.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
