---
title: "Memory Consolidation"
category: 03-memory
level: advanced
stability: experimental
description: "Periodically compress episodic memories into durable semantic facts, keeping the compression lossy-but-recorded rather than silent or lossless-but-unreadable."
added: "2026-10"
version: v1
related: ["memory-summarization", "episodic-memory"]
---

# Memory Consolidation

Category: Memory | Level: advanced | Stability: experimental | Version: v1

## Description

Raw episodic history grows faster than it can be recalled: every interaction leaves traces, most of which never matter again. Consolidation turns that pile into structure — recurring observations become semantic facts, stable patterns become procedural rules, and the source episodes are cited rather than deleted. The skill covers deciding what to consolidate, what the compressed form loses, and how to audit the compression.

## When to Use

Use when long-running agents accumulate episodic records across sessions and retrieval quality degrades — noisy recall, repeated re-derivation of the same facts.

Do not consolidate silently: a compressed memory with no trace of what was compressed or lost cannot be audited or undone.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `episodes` | `list` | Yes | Raw episodic records with timestamps and provenance |
| `policy` | `map` | Yes | What counts as recurring and when consolidation triggers |
| `destination` | `enum` | No | Semantic, procedural, or profile store for the result |

## Procedure

1. Group episodes by subject and time window before extracting anything; consolidation on ungrouped history invents patterns.
2. Extract candidate generalizations only where recurrence is measured — occurrence counts, not impressions.
3. Promote a candidate to a semantic fact with its support: which episodes, how many, over what period.
4. Cite the source episodes in the consolidated record so the compression can be audited.
5. Record what the compression lost — dropped exceptions, outlier episodes — rather than presenting the fact as lossless.
6. Keep the source episodes available for a stated re-derivation window before any cleanup.

## Outputs

| Output | Type | Description |
|---|---|---|
| `facts` | `list` | Consolidated semantic facts with support citations |
| `losses` | `map` | What the compression dropped per fact |
| `candidates` | `list` | Recurring patterns below the promotion threshold |

## Runnable Example

```python
def consolidate(episodes, min_support=3):
    counts, examples = {}, {}
    for ep in episodes:
        key = ep["subject"]
        counts[key] = counts.get(key, 0) + 1
        examples.setdefault(key, []).append(ep["id"])
    facts, candidates = [], []
    for subject, n in counts.items():
        if n >= min_support:
            facts.append({"subject": subject, "support": n, "sources": examples[subject]})
        else:
            candidates.append({"subject": subject, "support": n})
    return {"facts": facts, "candidates": candidates}

episodes = [
    {"id": "e1", "subject": "prefers-terse-replies"},
    {"id": "e2", "subject": "prefers-terse-replies"},
    {"id": "e3", "subject": "prefers-terse-replies"},
    {"id": "e4", "subject": "travels-in-october"},
]
print(consolidate(episodes))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Pattern invention | A single episode becomes a generalization | Require measured recurrence |
| Silent loss | Exceptions are dropped without record | Record what each compression dropped |
| Provenance cut | Consolidated facts cite nothing | Keep source episode references in every fact |
| Over-consolidation | Distinct behaviors are merged into one rule | Group by subject before extracting |
| No re-derivation | Sources are deleted before any audit | Keep sources for a stated window |

## Security and Authority Boundary

Consolidation concentrates sensitive details into durable claims about people and systems — a summarized profile is more shareable and more permanent than its source episodes. Apply profile-level access controls and honor deletion requests against consolidated facts, not only raw episodes.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia's overview of memory consolidation, the biological process this pattern mirrors (https://en.wikipedia.org/wiki/Memory_consolidation).
2. Wikipedia's overview of semantic memory as the durable-fact store destination (https://en.wikipedia.org/wiki/Semantic_memory).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Memory Summarization](memory-summarization.md) — the compression layer this skill schedules.
- [Episodic Memory](episodic-memory.md) — the source store whose records get consolidated.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
