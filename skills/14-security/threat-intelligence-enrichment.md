---
title: "Threat Intelligence Enrichment"
category: 14-security
level: intermediate
stability: experimental
description: "Enrich security events and observables with structured threat intelligence, mapping indicators to tactics and campaigns while resisting feed poisoning and stale data."
added: "2026-10"
version: v1
related: ["vulnerability-triage","threat-modeling"]
---

# Threat Intelligence Enrichment

Category: Security | Level: intermediate | Stability: experimental | Version: v1

## Description

Enrichment turns an IP or hash into context only when the source is trustworthy and current. The skill covers normalizing observables, matching them against structured feeds, attaching tactic and campaign context with source attribution, and scoring confidence with feed age and source reputation included. Feeds are treated as untrusted input: a single aggressive feed cannot dominate verdicts, and stale indicators age out.

## When to Use

Use when alerts, logs, or user reports must be prioritized with external threat context: known actors, campaign affiliation, and observed infrastructure.

Do not treat every feed as equally trustworthy. Poisoned feeds produce both false alerts and false clearance, so confidence scoring must include source reputation.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `observables` | `table` | Yes | IPs, domains, hashes, and other indicators to enrich |
| `feeds` | `table` | Yes | Structured intelligence records with source and timestamp |
| `source_reputation` | `object` | No | Per-feed trust weights; defaults to equal with age decay |

## Procedure

1. Normalize observables into canonical forms: IP version handling, domain case, and hash algorithms.
2. Match against the feeds, recording every hit with its source and record timestamp.
3. Attach available context: tactics, campaign names, and related infrastructure.
4. Score confidence combining source reputation, record age, and corroboration across feeds.
5. Age out stale indicators so old intelligence cannot keep driving verdicts.
6. Emit enrichment with provenance so any verdict can be traced to its records.

## Outputs

| Output | Type | Description |
|---|---|---|
| `enrichments` | `table` | Observable matches with context, source, and confidence |
| `campaign_map` | `object` | Grouped view of observables linked to shared campaigns |
| `stale_records` | `list` | Feed records past their usable age |

## Runnable Example

```python
def enrich(observable, feeds, reputation):
    """feeds: [{source, age_days, tactics}]; reputation: {source: 0-1}"""
    hits = []
    for f in feeds:
        age_decay = max(0.0, 1.0 - f["age_days"] / 180.0)
        conf = round(reputation.get(f["source"], 0.5) * age_decay, 3)
        hits.append({"source": f["source"], "tactics": f["tactics"], "confidence": conf})
    return {"observable": observable, "hits": hits}

print(enrich("203.0.113.7",
    [{"source": "feed-a", "age_days": 10, "tactics": ["initial-access"]},
     {"source": "feed-b", "age_days": 150, "tactics": ["command-and-control"]}],
    {"feed-a": 0.9, "feed-b": 0.5},
))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Feed poisoning | Hostile feed injects or suppresses indicators | Weight sources and require corroboration for high impact |
| Stale intelligence | Old indicators keep driving verdicts | Age out records and decay confidence with time |
| Observable mismatch | Normalization differences miss matches | Canonicalize before matching |
| Context without provenance | Attribution claims with no source record | Emit provenance with every enrichment |
| Over-blocking | Shared infrastructure flagged wholesale | Check breadth before blocking, e.g. shared hosting |

## Security and Authority Boundary

Intelligence queries can leak what an organization is investigating. Prefer pulled feeds over disclosing lookups to third-party services, treat feed data as untrusted input, and never auto-block on a single uncorroborated record.

## Evidence

This skill is grounded in dated public implementation references:

1. The MITRE ATT&CK knowledge base of adversary tactics and techniques (https://attack.mitre.org/).
2. The OASIS structured threat information expression documentation (https://oasis-open.github.io/cti-documentation/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Vulnerability Triage](vulnerability-triage.md) — the prioritization queue that enriched findings feed into.
- [Threat Modeling](threat-modeling.md) — the internal analysis intelligence enriches with external context.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
