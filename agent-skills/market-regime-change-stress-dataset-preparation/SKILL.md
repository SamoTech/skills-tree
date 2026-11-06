---
name: market-regime-change-stress-dataset-preparation
description: Prepare labeled stress datasets for financial agents covering regime-change windows, with pre/post labels and survivorship-checked instruments.
metadata:
  source: skills/12-data/market-regime-change-stress-dataset-preparation.md
  category: 12-data
  version: "v1"
---

# Market Regime Change Stress Dataset Preparation

## Description
Prepare labeled stress datasets for financial agents covering regime-change windows, with pre/post labels and survivorship-checked instruments. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A financial agent must be stress-tested against labeled market-regime changes.
- Regime-change windows need consistent pre and post labels.
- Dataset preparation must exclude survivorship and lookahead artifacts.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The market history source, the regime-change event calendar, and the labeling policy. |
| Outputs | A stress dataset naming per-window pre and post segments, per-instrument labels, and the exclusion log for survivorship and lookahead artifacts. |
| Safety | Fail closed by dropping any window whose post segment overlaps the labeling horizon's information. |

## Procedure
1. Load the market history and the regime-change event calendar.
2. Cut pre and post segments per the labeling policy for each event window.
3. Label instruments per segment with the declared metric definitions.
4. Exclude instruments with survivorship or lookahead artifacts and log them.
5. Verify no post segment uses information unavailable at its start time.
6. Emit the dataset with per-window labels and the exclusion log.

## Outputs
| Area | Contract |
|---|---|
| Primary | A stress dataset naming per-window pre and post segments, per-instrument labels, and the exclusion log for survivorship and lookahead artifacts. |
| Verification | Window definitions and exclusion entries that reproduce every label. |
| Failure | A fail-closed preparation note naming the lookahead overlap and the dropped window. |

## Runnable Example
```python
def prepare(events, history, policy):
    windows, dropped = [], []
    for e in events:
        pre = [b for b in history if e["pre_start"] <= b["t"] <= e["t"]]
        post = [b for b in history if e["t"] < b["t"] <= e["t"] + policy["horizon_days"]]
        if len(post) < policy["min_days"]:
            dropped.append((e["name"], "insufficient_post"))
            continue
        windows.append((e["name"], len(pre), len(post)))
    return {"windows": windows, "dropped": dropped}

ev = [{"name": "midterm_rout", "t": 10, "pre_start": 0}]
hist = [{"t": t} for t in range(0, 20)]
r = prepare(ev, hist, {"horizon_days": 5, "min_days": 4})
assert r["windows"] == [("midterm_rout", 11, 5)] and r["dropped"] == []
```

## Failure Modes
- Post segments include data that was not yet available at regime onset.
- Delisted instruments are included, creating survivorship bias.
- Regime windows overlap, double-counting one event's labels.
- Label definitions differ between windows in the same dataset.
- Exclusions are applied without logging, hiding dataset shrinkage.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The Nasdaq 100 fell 6.4 percent Thursday, wiping 2.3 trillion dollars in value as the semiconductor index crashed 12 percent, a regime-change window stress-testing financial agents' detection (AI Weekly, November 6, 2026) ([public signal](https://aiweekly.co/ai-news-today/edition/2026-11-06))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Ab Test Analysis](ab-test-analysis.md)
- [Agent Breach Timeline Analytics](agent-breach-timeline-analytics.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
