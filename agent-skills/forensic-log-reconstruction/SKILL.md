---
name: forensic-log-reconstruction
description: Rebuild a coherent incident timeline from partial, overlapping, and clock-skewed logs, producing an evidence-backed sequence with provenance and stated confidence per event.
metadata:
  source: skills/14-security/forensic-log-reconstruction.md
  category: 14-security
  version: "v1"
---

# Forensic Log Reconstruction

Category: Security | Level: advanced | Stability: experimental | Version: v1

## Description

Incident logs never line up: clocks drift, sources overlap or gap, and formats disagree. The skill covers collecting logs from all relevant sources into an immutable evidence store, normalizing timestamps against a common clock with skew estimates, ordering events with uncertainty bounds rather than false precision, and attributing each reconstructed event to its source lines. The timeline is the deliverable, and every entry carries its evidence.

## When to Use

Use when an incident must be understood from heterogeneous logs: what happened, in what order, and with what evidence supporting each claim.

Do not merge logs by raw timestamp. Clock skew between sources routinely reorders cause and effect, and a wrong order is worse than an honest uncertainty range.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `log_sources` | `table` | Yes | Logs with source, format, and observed or assumed clock offset |
| `incident_bounds` | `object` | Yes | Time range and assets in scope |
| `clock_authority` | `string` | No | The reference clock events are normalized against |

## Procedure

1. Collect all in-scope logs into an append-only evidence store with source provenance.
2. Parse each source into a common event record: time, actor, action, and target.
3. Estimate per-source clock skew using handshake artifacts or known anchor events.
4. Normalize timestamps against the clock authority, carrying skew bounds as uncertainty.
5. Order events into a timeline, marking where uncertainty leaves the order ambiguous.
6. Attribute every timeline entry to its source lines so any claim can be re-verified.

## Outputs

| Output | Type | Description |
|---|---|---|
| `timeline` | `table` | Ordered incident events with uncertainty bounds and provenance |
| `ambiguities` | `list` | Orderings that cannot be resolved within skew bounds |
| `evidence_index` | `object` | Map from timeline entries to source log lines |

## Runnable Example

```python
def normalize_time(event_time, offset, skew):
    """event_time in source seconds; offset est. drift; skew = uncertainty"""
    adjusted = event_time - offset
    return {"t": adjusted, "low": adjusted - skew, "high": adjusted + skew}

def order_with_uncertainty(events):
    return sorted(events, key=lambda e: e["t"])

rows = [normalize_time(1000, offset=2, skew=1), normalize_time(1002, offset=0, skew=3)]
for e in order_with_uncertainty(rows):
    print(e)
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| False chronological precision | Skewed clocks treated as truth | Carry skew bounds and mark ambiguous order |
| Missing middle | A source gap read as attacker dwell time | Mark gaps explicitly with their cause |
| Log tampering undetected | No integrity check before analysis | Hash sources on collection and verify before use |
| Timezone chaos | Sources mix local and UTC stamps | Normalize to a single clock authority first |
| Unattributed conclusions | Timeline claims with no source lines | Require provenance per entry before publishing |

## Security and Authority Boundary

Forensic timelines are legal-grade evidence in many incidents. Preserve originals immutably, document the chain of custody for every source, and never publish an incident timeline that attributes actions to individuals without direct evidence.

## Evidence

This skill is grounded in dated public implementation references:

1. The NIST guide to integrating forensic techniques into incident response (https://csrc.nist.gov/pubs/sp/800/86/final).
2. The Wikipedia article on computer forensics (https://en.wikipedia.org/wiki/Computer_forensics).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Audit Logging](audit-logging.md) — the upstream discipline that makes logs reconstructable at all.
- [Incident Response](incident-response.md) — the process that consumes the reconstructed timeline.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
