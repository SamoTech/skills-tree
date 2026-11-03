---
name: agent-action-affordance-publishing
description: Publish machine-readable action affordances alongside site content so visiting agents can discover permitted actions and their parameters.
metadata:
  source: skills/08-multimodal/agent-action-affordance-publishing.md
  category: 08-multimodal
  version: "v1"
---

# Agent Action Affordance Publishing

## Description
Publish machine-readable action affordances alongside site content so visiting agents can discover permitted actions and their parameters. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A site optimized for agents must expose what actions are permitted, not just readable text.
- The outcome would change if an agent guessed an action endpoint from prose alone.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The action inventory, the parameter schemas, and the publication target. |
| Outputs | Published affordance records with action names, parameters, and constraints. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Inventory the actions the site permits agents to perform.
2. Define parameters, types, and constraints for each action as an explicit schema.
3. Bind each action to its invocation contract including method and rate limits.
4. Publish the affordance records at the agent-discoverable location.
5. Verify a fresh reader can parse the records and resolve every action reference.
6. Version the affordance set so breaking changes are visible to consuming agents.

## Outputs
| Area | Contract |
|---|---|
| Primary | A published affordance set naming each permitted action, its parameters, constraints, and invocation contract. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def publish_affordances(actions, schemas):
    records = {a: {"params": schemas[a], "version": "v1"} for a in actions}
    return records
r = publish_affordances(["book_table"], {"book_table": ["party", "time"]})
assert r["book_table"]["params"] == ["party", "time"] and r["book_table"]["version"] == "v1"
```

## Failure Modes
- Actions are described in prose only, so agents guess endpoints and parameters.
- Affordances publish without constraints, letting agents invoke unbounded actions.
- Breaking schema changes ship without a version bump.
- Published records reference actions that no longer exist on the site.
- The affordance set is published once and never verified against the live site.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Fibr AI’s AXO launch making brand websites usable by AI visitors and adapting each site to different AI agents (Agentic AI News, dated November 2, 2026) ([public signal](https://agentic.ai/news))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Visual Understanding Tier Selection](visual-understanding-tier-selection.md)
- [Agent Visible Content Copywriting](agent-visible-content-copywriting.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
