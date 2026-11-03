---
name: accessibility-snapshot-privacy-filtering
description: ""
metadata:
  source: skills/14-security/accessibility-snapshot-privacy-filtering.md
  category: 14-security
  version: "v1"
---

# Accessibility Snapshot Privacy Filtering

## Description
Filter and bound desktop accessibility snapshots an agent takes, so private content in other windows is excluded before snapshots are stored or sent to a model. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent reads the desktop through the accessibility tree and unfiltered snapshots have already captured private content from unrelated windows.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the snapshot source, the privacy filter rules, and the retention policy for snapshots. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the privacy rules that bound which windows and element types may enter a snapshot.
2. Filter each snapshot at capture time, before storage or model transmission.
3. Redact or drop elements matching private-content patterns and record the redaction counts.
4. Apply a retention policy so snapshots and screenshots are not kept beyond the task.
5. On a rule failure or an unfiltered private element detected, fail closed and discard the snapshot.
6. Emit a structured result with filter outcomes, redaction counts, and retention state.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def filter_snapshot(elements, allowed_windows):
    kept, redacted = [], []
    for e in elements:
        if e["window"] not in allowed_windows:
            redacted.append(e["window"])
            continue
        if e["type"] in ("password", "private_message"):
            redacted.append(e["type"])
            continue
        kept.append(e)
    return {"kept": kept, "redacted": redacted}
els = [{"window": "ide", "type": "button"}, {"window": "ide", "type": "password"}, {"window": "mail", "type": "text"}]
f = filter_snapshot(els, {"ide"})
assert len(f["kept"]) == 1 and sorted(f["redacted"]) == ["mail", "password"]
```

## Failure Modes
- Snapshots are captured across all windows and filtered later, or never.
- The privacy rules are documented but the capture path bypasses them.
- Screenshots are kept indefinitely with no retention policy despite the warnings.
- Redaction is applied to display but the raw snapshot is still stored or sent.
- A rule failure falls back to capturing everything to keep the agent running.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the agent-desktop 1.0.2 release from Vercel Labs letting agents read and operate desktop apps through the accessibility tree, whose README warns that snapshots and screenshots can contain private desktop content (Munder Difflin agent-tools daily, dated November 1, 2026) ([public signal](https://munderdiffl.in/blog/agent-tools-today-2026-11-01/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Dataset Combined Effect Evaluation](dataset-combined-effect-evaluation.md)
- [Share Link Account Takeover Defense](share-link-account-takeover-defense.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
