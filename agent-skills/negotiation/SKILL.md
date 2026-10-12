---
name: negotiation
description: Prepare and conduct negotiations by mapping the interests behind stated positions, quantifying reservation values and alternatives, and trading on differences to reach agreements that hold.
metadata:
  source: skills/06-communication/negotiation.md
  category: 06-communication
  version: "v1"
---

# Negotiation

Category: Communication | Level: advanced | Stability: experimental | Version: v1

## Description

Negotiation is reaching agreement when parties' interests partly conflict. The reliable core is preparation: separating positions from interests, knowing your reservation value and best alternative to a negotiated agreement (BATNA), and identifying differences that can be traded instead of split. This skill covers that preparation and the conduct of exchanges that produce precise, verifiable terms — without fabricating leverage or inventing concessions.

## When to Use

Use when terms must be agreed with a party that has its own interests: scope and price discussions, vendor terms, resource allocation between teams.

Do not use it to manipulate or deceive a counterpart; commitments made must be within your actual mandate.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `my_interests` | `list` | Yes | Ranked underlying interests, not opening positions |
| `constraints` | `map` | Yes | Hard limits: budget, deadline, authority scope |
| `counterpart_context` | `map` | No | Known interests and pressures of the other side |
| `alternatives` | `map` | No | What happens if no agreement is reached (BATNA) |

## Procedure

1. Convert each stated position into the interest behind it; list them in priority order.
2. Quantify the reservation value: the worst acceptable outcome, derived from constraints and BATNA, not from hope.
3. Inventory tradable differences: things cheap for you and valuable to them, and vice versa.
4. Propose packages across several issues rather than conceding issue by issue.
5. Test every emerging agreement against both sides' alternatives; an agreement worse than a party's BATNA will not hold.
6. Close with precise terms: who, what, when, and how verification happens.

## Outputs

| Output | Type | Description |
|---|---|---|
| `agreement_terms` | `object` | Precise, verifiable commitments |
| `concession_log` | `list` | What was offered and traded, with rationale |
| `walk_away` | `bool` | Whether the reservation value was breached |

## Runnable Example

```python
def within_reservation(offer, reservation):
    """reservation values are minimum acceptable levels per issue."""
    breaches = {k: offer[k] for k, v in reservation.items() if k in offer and offer[k] < v}
    return {"acceptable": not breaches, "breaches": list(breaches)}

offer = {"price": 120, "warranty_months": 6, "support_hours": 40}
reservation = {"price": 100, "support_hours": 30}
print(within_reservation(offer, reservation))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Single-issue tunnel vision | Everything reduced to price or one headline term | Negotiate packages across multiple issues |
| Fabricated leverage | Bluffs collapse and destroy trust when called | Represent only real alternatives and constraints |
| Unverifiable agreement | Terms too vague to check delivery | Close with measurable terms and verification steps |
| Ignored stakeholders | The counterparty's principal is not at the table | Confirm who can actually commit |
| Sunk-cost drift | Conceding past the reservation value to save the deal | Recheck the reservation value before each concession |

## Security and Authority Boundary

An agent negotiates only within an explicit mandate from its principal. Never commit beyond that scope, never share confidential information beyond what the mandate permits, and surface the walk-away recommendation instead of agreeing to terms outside the reservation envelope.

## Evidence

This skill is grounded in dated public implementation references:

1. The Program on Negotiation at Harvard Law School (https://www.pon.harvard.edu/).
2. The negotiation reference article (https://en.wikipedia.org/wiki/Negotiation).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Argument Construction](argument-construction.md) — building the individual claims exchanged during negotiation.
- [Audience Analysis](audience-analysis.md) — modeling the counterpart before the first exchange.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
