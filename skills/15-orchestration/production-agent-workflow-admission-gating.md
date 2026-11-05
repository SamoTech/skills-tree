---
title: "Production Agent Workflow Admission Gating"
category: 15-orchestration
level: advanced
stability: experimental
description: "Gate admission of production agent workflows by budget, policy, and owner sign-off before they run."
added: "2026-11"
version: v1
related: [human-approval-gates, policy-as-code-gate-authoring]
tags: [orchestration, gating, governance, workflows]
---
# Production Agent Workflow Admission Gating

## Description
Gate admission of production agent workflows by budget, policy, and owner sign-off before they run. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A new agent workflow requests admission to production.
- Budget, policy, and owner requirements must gate the admission.
- Admitted workflows must carry their recorded approval references.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The workflow admission request, the policy set, and the budget ledger. |
| Outputs | An admission verdict naming passed gates, failures, and approval references. |
| Safety | Fail closed by refusing admission when any required gate is unverified. |

## Procedure
1. Read the admission request with its owner, budget ask, and tool list.
2. Verify the owner is recorded and authorized for the workflow type.
3. Check the budget ask against the ledger and remaining allocation.
4. Check the tool list against the enabled catalog and scope policy.
5. Collect gate results and refuse admission if any required gate failed.
6. Emit the verdict with gate results and the approval references.

## Outputs
| Area | Contract |
|---|---|
| Primary | An admission verdict with per-gate results and approval references. |
| Verification | Recorded gate checks that reproduce the verdict. |
| Failure | A fail-closed rejection naming the failed gate and the withheld admission. |

## Runnable Example
```python
def admit_workflow(request, ledger, catalog, owners):
    gates = {}
    gates["owner"] = request["owner"] in owners.get(request["type"], [])
    gates["budget"] = request["budget"] <= ledger.get("remaining", 0)
    gates["tools"] = all(catalog.get(t, {}).get("enabled") for t in request["tools"])
    verdict = all(gates.values())
    return {"admitted": verdict, "gates": gates, "ref": "adm-" + request["name"] if verdict else None}

ledger = {"remaining": 100}
catalog = {"search_flights": {"enabled": True}, "pay_ledger": {"enabled": False}}
owners = {"support": ["dana"]}
ok = admit_workflow({"name": "support-bot", "type": "support", "owner": "dana", "budget": 50, "tools": ["search_flights"]}, ledger, catalog, owners)
assert ok["admitted"] and ok["ref"] == "adm-support-bot"
no = admit_workflow({"name": "x", "type": "support", "owner": "dana", "budget": 50, "tools": ["pay_ledger"]}, ledger, catalog, owners)
assert no["admitted"] is False and no["gates"]["tools"] is False and no["ref"] is None
```

## Failure Modes
- Workflows are admitted with a warning when a gate fails.
- Budget checks read a stale ledger and overcommit the allocation.
- Disabled tools in the tool list are ignored until first invocation fails.
- The owner check verifies the team but not that the named owner is authorized.
- Admission happens before the approval reference is recorded.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Kong AI Management positions guardrails and governance as gating concerns for production AI workflows (AI Agents News, Week of November 5, 2026, dated November 5, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Human Approval Gates](human-approval-gates.md)
- [Policy As Code Gate Authoring](policy-as-code-gate-authoring.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
