---
name: ai-security-advisory-feed-subscription-automation
description: Automate subscription to AI security advisory feeds with deduplicated intake, source verification, and structured advisory records for downstream triage.
metadata:
  source: skills/11-web/ai-security-advisory-feed-subscription-automation.md
  category: 11-web
  version: "v1"
---

# Ai Security Advisory Feed Subscription Automation

## Description
Automate subscription to AI security advisory feeds with deduplicated intake, source verification, and structured advisory records for downstream triage. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A security agent must subscribe to AI vulnerability advisory feeds and route new advisories into triage without duplicates.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Register each advisory feed with its verification key, deduplicate incoming advisories by advisory identifier, and emit a structured record per new advisory with source link and date.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def intake(feed, advisories, seen):
    out = []
    for a in advisories:
        key = (feed, a["id"])
        if key in seen:
            continue
        if not a.get("url") or not a.get("date"):
            raise ValueError("advisory lacks url or date: " + a["id"])
        seen.add(key)
        out.append({"feed": feed, "id": a["id"], "url": a["url"], "date": a["date"]})
    return out
seen = set()
first = intake("aisecwatch", [{"id": "A-1", "url": "u1", "date": "2026-10-22"}], seen)
second = intake("aisecwatch", [{"id": "A-1", "url": "u1", "date": "2026-10-22"}], seen)
assert len(first) == 1 and second == []
```

## Failure Modes
- Feeds are subscribed without a verification key and spoofed advisories enter triage as authentic.
- Advisory identifiers are deduplicated per feed only and the same CVE re-enters from a second feed.
- Advisories without URLs or dates pass intake and triage cannot verify or order them.
- The intake treats advisory severity labels from the feed as verified and unconfirmed severities drive emergency response.
- Subscription credentials are shared across feeds and one compromised feed token exposes every source.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The AI and LLM vulnerability advisory tracking feed landscape, including public advisory indexes covering October 2026 agent CVEs, defines the advisory intake this skill automates. ([public signal](https://aisecwatch.com/issues))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Q3 Agentic Exploit Roundup Tracking Operations](../14-security/q3-agentic-exploit-roundup-tracking-operations.md)
- [Vendor Security Bulletin Parsing](../01-perception/vendor-security-bulletin-parsing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
