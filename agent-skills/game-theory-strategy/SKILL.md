---
name: game-theory-strategy
description: Model multi-agent interactions as games with explicit payoff matrices, identify equilibria and dominant strategies, and choose actions under strategic interdependence with stated assumptions about opponent rationality.
metadata:
  source: skills/02-reasoning/game-theory-strategy.md
  category: 02-reasoning
  version: "v1"
---

# Game-Theoretic Strategy Reasoning

Category: Reasoning | Level: intermediate | Stability: experimental | Version: v1

## Description

When outcomes depend on what other deciding agents do, choosing the best action requires modeling their incentives, not just your own. This skill covers representing an interaction as a game (players, strategies, payoffs), finding dominant strategies and Nash equilibria, and deciding what to do when opponents are not perfectly rational. The model is a decision aid; real counterparties deviate from equilibrium.

## When to Use

Use when two or more adaptive parties make interdependent choices: negotiation, competitive positioning, mechanism evaluation, adversarial planning.

Do not apply to a counterpart that is a fixed procedure with no strategy of its own — a plain optimization problem needs no game theory.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `players` | `list` | Yes | Deciding parties, each with a strategy set |
| `payoffs` | `map` | Yes | Utility for every strategy profile (per player) |
| `rationality` | `enum` | No | `perfect` (default), `bounded`, or `empirical` |

## Procedure

1. Enumerate players and their discrete strategy sets; merge continuous choices into named options.
2. Build the payoff matrix, sourcing each utility from evidence, not intuition, and record uncertainty.
3. Check each player for dominant strategies; a dominant strategy overrides equilibrium search for that player.
4. Find pure-strategy Nash equilibria: profiles where every strategy is a best response to the others.
5. If none exist, compute mixed-strategy equilibria and treat them as long-run frequencies, not one-shot advice.
6. Sanity-check against the rationality assumption: ask what a boundedly rational or spiteful opponent would do, and pick the action that survives both models.

## Outputs

| Output | Type | Description |
|---|---|---|
| `equilibria` | `list` | Pure and mixed equilibria with payoffs |
| `recommendation` | `object` | Chosen strategy with rationale |
| `exploitability` | `object` | Worst-case loss if opponents deviate from the model |

## Runnable Example

```python
def pure_nash equilibria_placeholder(): pass
```
```python
def best_responses(payoffs, profile, player):
    strategies = {s for p in payoffs for s in p}
    me = profile[player]
    other = profile[1 - player]
    gains = {s: payoffs[(s, other)][player] for s in strategies}
    best = max(gains.values())
    return {s for s, g in gains.items() if g == best}

def pure_equilibria(payoffs):
    out = []
    for profile in payoffs:
        if all(profile[i] in best_responses(payoffs, profile, i) for i in (0, 1)):
            out.append(profile)
    return out

game = {("coop", "coop"): (3, 3), ("coop", "defect"): (0, 5),
        ("defect", "coop"): (5, 0), ("defect", "defect"): (1, 1)}
print(pure_equilibria(game))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Equilibrium assumed to be behavior | Real actors err, bluff, and act spitefully | Check recommendations under bounded rationality too |
| Guessed payoffs | Utilities invented without evidence | Record payoff sources and uncertainty per cell |
| Wrong game class | Repeated or signaling structure flattened to one-shot | State the game horizon and information structure |
| Mixed equilibrium misread | Frequencies treated as a single-action recipe | Present mixed equilibria as long-run rates only |
| Ignored collusion space | Games with more than two players admit coalitions | Extend the model or restrict the claim |

## Security and Authority Boundary

Strategic reasoning about other parties must stay within the task's authority. It must not be used to manipulate, deceive, or socially engineer real people, and adversarial modeling of a user is out of scope for an assistant agent.

## Evidence

This skill is grounded in dated public implementation references:

1. The Nashpy library for computing equilibria of two-player games (https://pypi.org/project/nashpy/).
2. The Nash equilibrium reference article (https://en.wikipedia.org/wiki/Nash_equilibrium).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Decision Making](decision-making.md) — the single-agent counterpart once opponents are modeled as fixed.
- [Probabilistic Reasoning](probabilistic-reasoning.md) — the uncertainty machinery payoff estimates rely on.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
