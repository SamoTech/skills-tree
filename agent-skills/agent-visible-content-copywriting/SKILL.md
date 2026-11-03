---
name: agent-visible-content-copywriting
description: Write site content that stays legible to visiting AI agents by preserving factual claims, entity names, and actions across variants.
metadata:
  source: skills/08-multimodal/agent-visible-content-copywriting.md
  category: 08-multimodal
  version: "v1"
---

# Agent Visible Content Copywriting

## Description
Write site content that stays legible to visiting AI agents by preserving factual claims, entity names, and actions across variants. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Brand site copy rewritten for AI visitors must keep its factual claims verifiable.
- The outcome would change if an AI-optimized variant dropped the facts agents need.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The source copy, the fact inventory, and the agent readability checklist. |
| Outputs | Variant copy with every inventory fact preserved and the checklist recorded. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Extract the fact inventory from the source copy: entities, numbers, and actions.
2. Write the variant for agent readability while keeping every fact intact.
3. Check each inventory fact appears in the variant with unchanged meaning.
4. Flag any fact that became ambiguous in the variant and rewrite it explicitly.
5. Record the checklist mapping each fact to its variant location.
6. Emit the variant with the checklist so a reviewer can verify no fact drifted.

## Outputs
| Area | Contract |
|---|---|
| Primary | A content variant preserving every fact from the inventory with the readability checklist recorded per claim. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def check_facts(variant, facts):
    missing = [f for f in facts if f not in variant]
    return {"complete": not missing, "missing": missing}
v = "Store hours are 9 to 5. Returns accepted within 30 days."
r = check_facts(v, ["9 to 5", "30 days", "free shipping"])
assert r["complete"] is False and r["missing"] == ["free shipping"]
```

## Failure Modes
- The variant drops numbers or entity names that agents use for grounding.
- Facts survive but change meaning through rewording, and no check catches it.
- The checklist is recorded without mapping facts to variant locations.
- Marketing flourish replaces the factual claim in the AI-facing variant.
- Only one variant is checked while others ship unchecked.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Fibr AI launching Agent Experience Optimization to turn brand websites into engines for AI visibility and agent action (Agentic AI News, dated November 2, 2026) ([public signal](https://agentic.ai/news))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Visual Understanding Tier Selection](visual-understanding-tier-selection.md)
- [Agent Action Affordance Publishing](agent-action-affordance-publishing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
