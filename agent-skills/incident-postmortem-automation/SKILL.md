---
name: incident-postmortem-automation
description: Assemble blameless postmortem documents from incident timelines, alerts, and change records automatically, producing a structured draft that a human facilitator completes and owns.
metadata:
  source: skills/17-infrastructure/incident-postmortem-automation.md
  category: 17-infrastructure
  version: "v1"
---

# Incident Postmortem Automation

Category: Infrastructure | Level: basic | Stability: experimental | Version: v1

## Description

Postmortems fail when the timeline is reconstructed from memory days later. The skill covers pulling the timeline from tooling: alerts fired, deployments shipped, and actions taken, assembling the standard sections from those records, and emitting a draft with every factual claim linked to its source. The analysis, contributing factors, and action items stay human; automation never assigns cause or blame, and the facilitator owns the final document.

## When to Use

Use after any incident that warrants a postmortem, to cut the administrative cost of drafting and keep the timeline evidence-based.

Do not let automation write the root cause. Causal analysis and action-item prioritization are human judgments, and a machine-drafted cause invites a rubber stamp.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `incident_record` | `object` | Yes | Incident metadata: title, severity, start and end, commander |
| `timeline_sources` | `table` | Yes | Alerts, changes, and log extracts during the incident window |
| `template` | `object` | No | The organization’s postmortem template and required sections |

## Procedure

1. Pull the incident window from the record and collect alerts, changes, and log events inside it.
2. Build the factual timeline with each entry linked to its source system.
3. Assemble template sections that derive from records: summary, timeline, impact, and response.
4. Insert data-quality warnings where sources disagree or gaps exist.
5. Leave cause analysis, contributing factors, and action items as explicit human sections.
6. Hand the draft to the facilitator with the source index for verification.

## Outputs

| Output | Type | Description |
|---|---|---|
| `postmortem_draft` | `object` | Structured draft with populated factual sections |
| `source_index` | `table` | Map from every timeline claim to its source record |
| `open_questions` | `list` | Disagreements and gaps the facilitator must resolve |

## Runnable Example

```python
def build_timeline(alerts, changes):
    """alerts: [(ts, name)]; changes: [(ts, id)]"""
    merged = sorted(alerts + changes, key=lambda e: e[0])
    return [{"ts": ts, "event": name} for ts, name in merged]

print(build_timeline(
    [(100, "alert: error-rate high"), (400, "alert: resolved")],
    [(50, "change-1234 deployed")],
))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Machine-assigned cause | Automation drafted root cause text | Causal sections stay human-owned |
| Blame language | Draft names individuals as causes | Blameless vocabulary enforced in templates |
| Timeline gaps invisible | Missing sources read as quiet periods | Data-quality warnings for every gap |
| Template drift | Sections vary per team | Bind drafts to the organization template |
| Draft treated as final | No facilitator review before filing | Handoff with source index and required sign-off |

## Security and Authority Boundary

Postmortems catalog how systems fail, which makes them sensitive in aggregate. Restrict access to the incident community, keep customer-identifying data out of timelines, and never publish a postmortem that includes unverified claims about third parties.

## Evidence

This skill is grounded in dated public implementation references:

1. The Google SRE book chapter on postmortem culture (https://sre.google/sre/postmortem-culture/).
2. The community collection of postmortem templates (https://github.com/dastergon/postmortem-templates).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Alerting Design](alerting-design.md) — the alert record the timeline is assembled from.
- [Deployment Rollback](deployment-rollback.md) — the change events postmortems reconcile against.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
