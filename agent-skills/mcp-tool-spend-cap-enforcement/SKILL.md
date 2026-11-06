---
name: mcp-tool-spend-cap-enforcement
description: Enforce per-run spend caps on paid MCP tool calls so agent loops stop or degrade instead of exceeding the declared budget.
metadata:
  source: skills/04-action-execution/mcp-tool-spend-cap-enforcement.md
  category: 04-action-execution
  version: "v1"
---

# MCP Tool Spend-Cap Enforcement

## Description
Enforce per-run spend caps on paid MCP tool calls so agent loops stop or degrade instead of exceeding the declared budget. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent loop can call paid MCP tools whose costs accumulate per call.
- A spend cap must stop further calls, not merely warn after the fact.
- Post-run cost attribution must reconcile against the cap decision.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The tool price list, the declared spend cap, and the running call ledger. |
| Outputs | A spend verdict naming the remaining budget, blocked calls, and the ledger reconciliation at run end. |
| Safety | Fail closed by blocking the next paid call when its price cannot be confirmed within the remaining budget. |

## Procedure
1. Load the price list for every paid tool before the loop starts.
2. Before each paid call, check its price against the remaining budget.
3. Block the call when the price is unknown or exceeds the remaining budget.
4. Record every priced call in the ledger at execution time.
5. Reconcile the ledger against the cap at run end and report the variance.
6. Emit the spend verdict with blocked calls and reconciliation.

## Outputs
| Area | Contract |
|---|---|
| Primary | A spend verdict naming the remaining budget, blocked calls, and the ledger reconciliation at run end. |
| Verification | The priced ledger and cap arithmetic that reproduce the blocked-call decisions. |
| Failure | A fail-closed abort naming the unpriceable call and the halted loop. |

## Runnable Example
```python
def gate_call(tool, prices, remaining):
    price = prices.get(tool)
    if price is None:
        return {"allow": False, "reason": "unknown_price"}
    if price > remaining:
        return {"allow": False, "reason": "over_budget"}
    return {"allow": True, "price": price, "remaining_after": remaining - price}

prices = {"search": 0.05, "translate": 0.20}
assert gate_call("search", prices, 0.06)["allow"] is True
assert gate_call("translate", prices, 0.06)["reason"] == "over_budget"
assert gate_call("vision", prices, 1.0)["reason"] == "unknown_price"
```

## Failure Modes
- Calls proceed while a tool's price is still being looked up.
- The cap is checked after the call executes, not before.
- Free and paid tools share one ledger, hiding real spend.
- Blocked calls are retried in a tight loop instead of degrading.
- The end-of-run reconciliation is skipped when the cap was never hit.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Hermes Agent v0.23.0 introduces spend limits for paid MCP tools alongside its unified gateway consolidation (HeadsUpAI, November 6, 2026) ([public signal](https://headsupai.io/ai-news-and-updates/today))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Action Cost Estimation](action-cost-estimation.md)
- [A2a Cli Task Submission Execution](a2a-cli-task-submission-execution.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
