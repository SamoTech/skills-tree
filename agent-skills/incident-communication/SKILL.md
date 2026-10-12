---
name: incident-communication
description: Write timely, structured incident updates — severity, impact, and a committed next-update time — so stakeholders stay informed while responders keep working.
metadata:
  source: skills/06-communication/incident-communication.md
  category: 06-communication
  version: "v1"
---

# Incident Communication

Category: Communication | Level: intermediate | Stability: experimental | Version: v1

## Description

An incident produces two obligations at once: fix the thing, and tell the truth about it at a pace people can rely on. This skill separates narration from response — a designated owner handles the updates while responders respond — and gives each message a fixed shape: observed impact, current status, and when the next message lands. The cadence promise is the core mechanism: a stakeholder who knows the next update arrives in thirty minutes reads silence as work, not as abandonment.

## When to Use

Use whenever an incident is visible to anyone beyond the responders — customers, leadership, partner teams — and from the first acknowledgement, not from the moment of diagnosis.

Do not let updates displace response work, and do not publish causal claims before evidence supports them; a stated unknown ages better than a wrong early diagnosis.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `incident` | `record` | Yes | The incident being communicated about |
| `audiences` | `list` | Yes | Internal responders, leadership, and customers, each with its channel |
| `severity` | `enum` | Yes | The impact tier that sets depth, tone, and cadence |
| `next_update` | `time` | Yes | The committed time at which the next message lands |

## Procedure

1. Send the first notice early: what is observably wrong, who is affected, and that response is underway.
2. Commit to a cadence and state it — the next update lands at a named time even if the only news is that nothing has changed.
3. Keep one authoritative channel; summaries posted elsewhere link to it rather than retell it.
4. Separate facts from hypothesis inside every message: label each statement as observed, inferred, or currently unknown.
5. Match depth to audience: leadership receives impact and decisions, responders receive technical detail, customers receive effect and remedy.
6. Close explicitly when the incident resolves — final impact, root-cause status, and where the postmortem will land.

## Outputs

| Output | Type | Description |
|---|---|---|
| `notice` | `message` | The first acknowledgement with committed cadence |
| `updates` | `list` | Timestamped messages keeping the cadence promise |
| `timeline` | `record` | The communicated sequence of events for the postmortem |

## Runnable Example

```python
def due_at(last_sent_at, cadence_seconds):
    return last_sent_at + cadence_seconds

def render(update):
    observed = "; ".join(update["observed"]) or "none yet"
    unknown = "; ".join(update["unknown"]) or "none currently"
    impact = update["impact"]
    return f"Impact: {impact}. Observed: {observed}. Unknown: {unknown}."

update = {
    "impact": "checkout errors for about 4 percent of sessions",
    "observed": ["elevated 500s on the payment path"],
    "unknown": ["root cause"],
}
print(render(update))
print("next update due at epoch", due_at(1760256000, 1800))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Silent gaps | No message lands at the promised time | Send a no-change update rather than silence |
| Premature cause | A diagnosis published before evidence supports it | Label inference as inference until confirmed |
| Channel sprawl | Contradicting retellings across channels | One authoritative channel; others link to it |
| Audience mismatch | Customer-grade detail sent to leadership or the reverse | Derive per-audience depth from one timeline |
| Unclosed incidents | The last message never lands | Always publish a closing message with owned actions |

## Security and Authority Boundary

Incident updates leak information under time pressure: state impact plainly, but keep credentials, internal hostnames, and customer identifiers out of widely-distributed notices; sensitive technical detail belongs in the restricted responder channel, and the public record should be written as if it will be quoted.

## Evidence

This skill is grounded in dated public implementation references:

1. The Google SRE Workbook chapter on incident response (https://sre.google/workbook/incident-response/).
2. The PlainLanguage.gov guidelines for clear writing (https://www.plainlanguage.gov/guidelines/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Report Writing](report-writing.md) — the structured record an incident resolves into.
- [Tone Adjustment](tone-adjustment.md) — matching register to audience and moment.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
