---
name: agent-interaction-economics-ledger-memory
description: Maintain a durable ledger of usage and cost across agent-driven interactions so workflows can be governed by their recorded economics.
metadata:
  source: skills/03-memory/agent-interaction-economics-ledger-memory.md
  category: 03-memory
  version: "v1"
---

# Agent Interaction Economics Ledger Memory

## Description
Maintain a durable ledger of usage and cost across agent-driven interactions so workflows can be governed by their recorded economics. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Agent workflows must be evaluated by their recorded usage and cost.
- Cost history must survive session boundaries for budget review.
- Spend anomalies must be traceable to the workflow and step that caused them.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The interaction records, the unit prices, and the workflow registry. |
| Outputs | A ledger entry set naming workflow, step, usage, and attributed cost. |
| Safety | Fail closed by refusing unattributed usage records into the ledger. |

## Procedure
1. Read each interaction record and resolve its workflow and step from the registry.
2. Reject records that lack a workflow owner or step identifier.
3. Apply unit prices to usage quantities and compute the attributed cost.
4. Roll the entries up per workflow and compare against the recorded budget.
5. Flag workflows whose cumulative cost exceeds budget as review-required.
6. Emit the ledger entries with attribution and the flagged workflow set.

## Outputs
| Area | Contract |
|---|---|
| Primary | A ledger of interaction entries with workflow, step, usage, and attributed cost. |
| Verification | Recorded unit prices and rollups that reproduce the per-workflow totals. |
| Failure | A fail-closed error report naming the unattributed record and the refused entry. |

## Runnable Example
```python
def ledger_entry(rec, registry, prices):
    wf = registry.get(rec["workflow"])
    if wf is None:
        return {"ok": False, "reason": "unknown_workflow"}
    if "step" not in rec:
        return {"ok": False, "reason": "missing_step"}
    cost = rec["usage"] * prices[rec["unit"]]
    return {"ok": True, "workflow": rec["workflow"], "step": rec["step"], "cost": cost}

registry = {"support-bot": {"owner": "support"}}
prices = {"tokens": 0.002}
e = ledger_entry({"workflow": "support-bot", "step": "triage", "usage": 1500, "unit": "tokens"}, registry, prices)
assert e["ok"] and abs(e["cost"] - 3.0) < 1e-9
bad = ledger_entry({"workflow": "ghost", "step": "x", "usage": 1, "unit": "tokens"}, registry, prices)
assert bad["ok"] is False and bad["reason"] == "unknown_workflow"
```

## Failure Modes
- Usage records without workflow attribution enter the ledger and costs cannot be traced.
- Unit prices are hardcoded at write time and stale pricing corrupts the totals.
- Budget overruns are not flagged and workflows keep spending unnoticed.
- The ledger is kept per session and cost history is lost at session end.
- Rollups are recomputed from edited entries and no longer match recorded totals.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Kong announced an expansion of Kong AI Management in Kong Konnect to help enterprises govern and manage the economics of AI interactions as systems move from model calls to agent-driven workflows (AI Agents News, Week of November 5, 2026, dated November 5, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Payment Spend History Memory](agent-payment-spend-history-memory.md)
- [Benchmark Result Ledger Memory](benchmark-result-ledger-memory.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
