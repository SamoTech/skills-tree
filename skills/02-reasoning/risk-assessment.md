# Risk Assessment

**Category:** `reasoning`  
**Skill Level:** `advanced`  
**Stability:** `stable`  
**Added:** 2025-03  
**Version:** v2

---

## Description

Identify, evaluate, and prioritise risks before taking actions — especially irreversible ones. Risk assessment reasoning is critical for agentic systems that take real-world actions: file writes, API calls, deployments, financial transactions.

---

## Risk Matrix

```
          │  Low Impact │  Medium Impact │  High Impact
──────────┼─────────────┼────────────────┼──────────────
Low Prob  │   Monitor   │    Monitor     │   Mitigate
Med Prob  │   Accept    │   Mitigate     │    Avoid
High Prob │   Accept    │    Avoid       │    Avoid
```

For **irreversible** actions (data deletion, money transfer, public post), always treat impact as High regardless of probability.

---

## Risk Taxonomy for AI Agents

| Category | Examples | Default Strategy |
|---|---|---|
| **Data loss** | Delete file, DROP TABLE | Require confirmation + backup |
| **Irreversible API** | Send email, post tweet, charge card | Dry-run first if available |
| **Scope creep** | Modifying files outside task scope | Explicit allow-list |
| **Cascading failure** | One API error breaks downstream tools | Circuit breaker |
| **Privacy** | Logging PII, sending to external API | Sanitise before external calls |
| **Cost** | Runaway LLM/API calls in loops | Budget cap + loop limit |

---

## Prompt Pattern

```
Proposed action: [ACTION]

Risk Assessment:
1. What could go wrong? (list ≥3 failure modes)
2. For each failure mode:
   - Probability: Low / Medium / High
   - Impact: Low / Medium / High
   - Reversible? Yes / No
3. Overall risk level: Accept / Mitigate / Avoid
4. If Mitigate: what safeguard reduces the risk?
5. If Avoid: what alternative achieves the goal safely?
```

---

## Code Pattern — Agentic Guardrail

```python
from enum import Enum

class RiskLevel(Enum):
    ACCEPT = "accept"
    MITIGATE = "mitigate"
    AVOID = "avoid"

def assess_action(action: dict, llm) -> RiskLevel:
    """Ask LLM to assess risk before executing any tool call."""
    prompt = f"""
    Action: {action}
    Is this action irreversible? Does it affect external systems?
    Rate: ACCEPT / MITIGATE / AVOID.
    """
    verdict = llm(prompt).strip().upper()
    return RiskLevel(verdict.lower())

def safe_execute(action: dict, tool, llm):
    risk = assess_action(action, llm)
    if risk == RiskLevel.AVOID:
        raise ValueError(f"Action blocked by risk assessment: {action}")
    if risk == RiskLevel.MITIGATE:
        print(f"[WARN] Proceeding with caution: {action}")
    return tool.execute(action)
```

---

## Related Skills

- [Decision Making](decision-making.md)
- [Counterfactual Reasoning](counterfactual-reasoning.md)
- [Self-Reflection](self-reflection.md)
- [Planning](planning.md)
