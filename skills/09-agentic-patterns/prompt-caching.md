---
title: "Prompt Caching"
category: 09-agentic-patterns
level: intermediate
stability: experimental
description: "Order prompts so stable content forms a cacheable prefix, place cache breakpoints deliberately, and measure the achieved hit rate instead of assuming caching pays for itself."
added: "2026-10"
version: v1
related: ["budget-management", "context-compaction", "progressive-skill-loading"]
---

# Prompt Caching

Category: Agentic Patterns | Level: intermediate | Stability: experimental | Version: v1

## Description

Prompt caching only pays when the stable content is ordered first and the volatile content last, and it only keeps paying while someone measures the hit rate. This skill defines the ordering contract, breakpoint placement, and the measurement loop that decides whether caching is worth its constraints for a given workload.

## When to Use

Use when an agent workload sends a large stable prefix every turn and the provider prices cached input below fresh input.

Do not use for single-shot prompts or workloads where the prefix changes every turn; caching adds constraints without return.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `system_text` | `string` | Yes | Stable system instructions, changed rarely |
| `tool_definitions` | `string` | Yes | Tool schemas that change on deployment boundaries |
| `history` | `list` | Yes | Turns eligible for the cached portion |
| `user_text` | `string` | Yes | The volatile per-turn suffix |
| `price_table` | `object` | No | Cached and fresh per-unit prices for cost estimation |

## Procedure

1. Order the prompt so the stablest content comes first: system text, then tool definitions, then history.
2. Place the volatile user request strictly last; anything after it cannot be cached on the next turn.
3. Declare cache breakpoints at the boundaries between stability tiers, not at arbitrary token counts.
4. Estimate cost with the cached and fresh prices before rollout; an unmeasured saving is an assumed one.
5. Measure the achieved hit rate over real turns, not synthetic ones.
6. Re-measure whenever system text or tool definitions change; a prefix change invalidates the cache at that breakpoint.
7. Keep the prefix genuinely stable; mostly stable content pays the fresh price every turn.
8. Report cached and non-cached cost separately in the budget so the saving is auditable.

## Outputs

| Output | Type | Description |
|---|---|---|
| `prompt` | `object` | Ordered prompt parts with the cached portion marked |
| `breakpoints` | `list` | Declared cache boundaries between stability tiers |
| `estimated_cost` | `number` | Pre-rollout cost estimate under the price table |
| `measured_hit_rate` | `number` | Hits divided by turns over the measured window |

## Runnable Example

```python
def build_cached_prompt(system_text, tools_text, history, user_text):
    """Order a prompt so the stable prefix precedes the volatile suffix."""
    stable_prefix = system_text + "\n" + tools_text
    cached_portion = stable_prefix + "\n" + "\n".join(history)
    return {"prefix": stable_prefix, "cached": cached_portion, "suffix": user_text}

def estimate_cost(prompt, cached_price, fresh_price):
    """Estimate cost from the stable, cached-history, and fresh portions."""
    stable_units = len(prompt["prefix"])
    history_units = max(len(prompt["cached"]) - stable_units, 0)
    fresh_units = len(prompt["suffix"])
    return stable_units * cached_price + (history_units + fresh_units) * fresh_price

def measured_hit_rate(turns):
    """Return the achieved cache hit rate over the measured turns."""
    if not turns:
        return 0.0
    hits = sum(1 for turn in turns if turn.get("cache_hit"))
    return round(hits / len(turns), 2)

prompt = build_cached_prompt("system v3", "tool list v3", ["turn 1"], "latest question")
print(estimate_cost(prompt, 0.001, 0.003))
print(measured_hit_rate([{"cache_hit": True}, {"cache_hit": True}, {"cache_hit": False}]))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Prefix churn | A timestamp or random id sits inside the prefix | Audit prefix content for volatile fields |
| Misplaced suffix | The user request precedes the history | Keep the request strictly last |
| Assumed savings | Rollout happens without hit-rate measurement | Measure over real turns first |
| Breakpoint drift | Stability tiers change silently | Re-verify breakpoints on every content change |
| Hidden coupling | System text depends on the request | Decouple the tiers or accept fresh pricing |

## Security and Authority Boundary

Caching prompt content grants no authority to relax data handling. Cached segments may persist on the provider side beyond the request; content subject to retention or confidentiality limits must not be placed in cacheable positions without an explicit policy decision.

## Evidence

This skill is grounded in dated public implementation references:

1. Anthropic’s prompt caching documentation (https://docs.claude.com/en/docs/build-with-claude/prompt-caching).
2. OpenAI’s prompt caching documentation (https://platform.openai.com/docs/guides/prompt-caching).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Budget Management](../15-orchestration/budget-management.md) — enforces declared resource budgets; cached and fresh cost are reported separately under it.
- [Context Compaction](../03-memory/context-compaction.md) — shrinks history after the fact; this skill avoids re-sending stable content in the first place.
- [Progressive Skill Loading](../03-memory/progressive-skill-loading.md) — bounds the skill layer’s token cost; this skill prices what is still sent.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
