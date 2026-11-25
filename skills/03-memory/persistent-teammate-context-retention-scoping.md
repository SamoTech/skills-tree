---
title: "Persistent Teammate Context Retention Scoping"
category: 03-memory
level: advanced
stability: experimental
description: "Scope what a persistent teammate agent may retain across sessions, bounding memory by need-to-know rather than ambient capture."
added: "2026-11"
version: v1
related: [need-to-know-memory-scoping, memory-ttl]
tags: [memory, retention, teammates]
---

# Persistent Teammate Context Retention Scoping

## Description
Scope what a persistent teammate agent may retain across sessions, bounding memory by need-to-know rather than ambient capture. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A persistent agent is granted memory across sessions.
- A retention policy must bound what an always-on agent keeps.
- An audit must show what a teammate retained and why.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The teammate task description, its data sources, and the retention boundaries approved for the role. |
| Outputs | A retention scope naming retained categories, expiry terms, and the prohibited-capture list. |
| Safety | Fail closed by blocking retention of any category not named in the approved scope. |

## Procedure
1. Derive the minimum information categories the assigned task requires.
2. Map each category to its approved retention term.
3. List prohibited captures including secrets, unrelated channels, and out-of-scope content.
4. Define expiry and purge behavior for each retained category.
5. Define the audit trail that reconstructs what was retained and why.
6. Emit the retention scope and wire it into the memory gate.

## Outputs
| Area | Contract |
|---|---|
| Primary | A retention scope naming retained categories, expiry terms, and the prohibited-capture list. |
| Verification | The recorded inputs and intermediate values that reproduce the primary output from the runnable example. |
| Failure | A fail-closed hold naming the unmet precondition and the withheld primary output. |

## Runnable Example
```python
def scope(task_categories, approved):
    allowed = [c for c in task_categories if c in approved]
    prohibited = [c for c in approved if c not in task_categories]
    return {"allowed": allowed, "prohibited": prohibited}

r = scope(["thread-summary", "calendar"], ["thread-summary", "calendar", "raw-messages"])
assert r["allowed"] == ["thread-summary", "calendar"]
assert r["prohibited"] == ["raw-messages"]
```

## Failure Modes
- Retention defaults to everything the agent observes..
- Prohibited captures are implied rather than listed..
- Expiry terms are defined but never wired into the memory gate..
- The audit trail records outcomes but not retention reasons..
- Scope grows with each new task without re-approval..

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Perplexity introduced Teammates, persistent AI agents that retain project context and keep working when the user is away, limited to the 200-dollar-per-month Max plan (AI Agent News Today, November 8, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/daily/2026-11-08))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Need To Know Memory Scoping](need-to-know-memory-scoping.md)
- [Memory Ttl](memory-ttl.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
