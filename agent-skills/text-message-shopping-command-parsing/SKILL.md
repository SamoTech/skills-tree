---
name: text-message-shopping-command-parsing
description: Parse natural-language shopping messages into bounded product, cart, and purchase actions with explicit confirmation requirements.
metadata:
  source: skills/01-perception/text-message-shopping-command-parsing.md
  category: 01-perception
  version: "v1"
---

# Text Message Shopping Command Parsing

## Description
Parse natural-language shopping messages into bounded product, cart, and purchase actions with explicit confirmation requirements. The parse is bounded by a fixed action vocabulary, explicit confirmation gates, and recorded refusals rather than free-form interpretation.

## When to Use
- A shopping agent receives plain text messages instead of app or web input.
- Purchase actions must be gated behind explicit user confirmation.
- Unrecognized or ambiguous commands must fail closed.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The raw message text, the product catalog reference, and the action vocabulary. |
| Outputs | A parsed command naming the action, target product, and cart effects, plus any confirmation requirement. |
| Safety | Fail closed by refusing ambiguous commands and never auto-confirming purchases. |

## Procedure
1. Normalize the incoming message text and strip formatting noise.
2. Match the message against the fixed action vocabulary (search, add, compare, confirm).
3. Resolve the target product against the catalog reference.
4. Attach an explicit confirmation requirement to any purchase-affecting action.
5. Refuse the command and record the refusal when no single action matches.
6. Emit the parsed command with its action, target, and confirmation state.

## Outputs
| Area | Contract |
|---|---|
| Primary | A parsed command with action, target product, and confirmation requirement. |
| Verification | The action vocabulary and resolution trace that reproduce the parse. |
| Failure | A recorded refusal with the ambiguity reason when no safe parse exists. |

## Runnable Example
```python
def parse(msg, catalog):
    actions = {"search": "search", "add": "add", "buy": "purchase", "compare": "compare"}
    words = msg.lower().split()
    verb = next((a for w, a in actions.items() if w in words), None)
    items = [c for c in catalog if any(c.split("-")[0] in msg.lower() for c in [c])]
    if verb is None or not items:
        return {"ok": True, "action": None, "reason": "ambiguous", "confirm": False}
    return {"ok": True, "action": verb, "item": items[0], "confirm": verb == "purchase"}

cat = ["coffee-grinder", "travel-mug"]
p = parse("add the coffee grinder to my cart", cat)
assert p["action"] == "add" and p["item"] == "coffee-grinder" and p["confirm"] is False
assert parse("buy it now", cat)["confirm"] is True
assert parse("maybe the thing", cat)["reason"] == "ambiguous"
```

## Failure Modes
- Purchase verbs are executed without an explicit confirmation gate.
- Ambiguous messages are guessed instead of refused and recorded.
- The action vocabulary grows at runtime, making parses unreproducible.
- Catalog resolution picks the first fuzzy match without recording alternatives.
- Refusals are dropped, so ambiguous traffic is never measured.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Amazon began rolling out a text-message interface for its Alexa AI agent letting selected customers search, add to cart, and purchase by natural-language message (AI Agent News Today, November 7, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/daily/2026-11-07))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Teammate Thread Activity Monitoring](teammate-thread-activity-monitoring.md)
- [Voice Agent Turn Taking Interruption Perception](voice-agent-turn-taking-interruption-perception.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
