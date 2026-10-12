---
title: "Name Generation"
category: 13-creative
level: basic
stability: experimental
description: "Generate candidate names systematically from declared inventories with pattern, collision, and exclusion checks so naming is explored deliberately and recorded reproducibly."
added: "2026-10"
version: v1
related: ["logo-design", "copywriting"]
---

# Name Generation

Category: Creative | Level: basic | Stability: experimental | Version: v1

## Description

Naming by staring at a blank page produces the first defensible option; naming by generation produces the space of options and then chooses. This skill defines name generation as a constrained search: a morpheme inventory, a construction pattern, a banned list, and collision checks against existing names — producing a reproducible candidate set instead of a lucky guess.

## When to Use

Use when a product, character, place, or brand needs a name and the process should explore the option space deliberately rather than seize the first idea.

Do not use where naming is externally fixed by standards, clients, or convention; constrained search cannot substitute for a mandated name.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `inventory` | `(prefixes, suffixes)` | Yes | Declared morpheme inventories for construction |
| `pattern` | `regex` | Yes | Shape rule a candidate must satisfy |
| `banned` | `list[string]` | Yes | Substrings and collisions excluded from results |

## Procedure

1. Declare the inventories and construction rules before generating; free-form generation cannot be reproduced or audited.
2. Generate the full candidate set from the inventories under the construction rules.
3. Filter by the declared pattern so shape violations never reach review.
4. Apply the banned list and collision checks against existing names before presenting candidates.
5. Present candidates with their construction provenance — which morphemes and rules produced them.
6. Record the chosen name with the generator settings so the decision is reproducible later.

## Outputs

| Output | Type | Description |
|---|---|---|
| `candidates` | `list[string]` | Filtered, ordered candidate names |
| `rejected` | `list[(candidate, reason)]` | Candidates removed by pattern or exclusion rules |

## Runnable Example

```python
import itertools
import re

def generate_names(prefixes, suffixes, banned, pattern):
    """Constrained morpheme combination with shape and exclusion filters."""
    candidates, rejected = [], []
    for prefix, suffix in itertools.product(prefixes, suffixes):
        candidate = prefix + suffix
        if not pattern.fullmatch(candidate):
            rejected.append((candidate, "shape"))
            continue
        if any(part in candidate for part in banned):
            rejected.append((candidate, "excluded"))
            continue
        candidates.append(candidate)
    return sorted(candidates), rejected

candidates, rejected = generate_names(
    ["nor", "vel", "kry"], ["dane", "mont", "vane"],
    banned=["vane"], pattern=re.compile(r"[a-z]{5,9}"))
print("candidates:", candidates)
print("rejected:", rejected)
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| First-idea capture | The first plausible name ends the search | Generate the candidate space before choosing |
| Unrecorded settings | The choice cannot be reproduced later | Keep inventories, patterns, and rules with the decision |
| Silent collisions | Existing names never checked | Screen candidates against known names before review |
| Unvetted meaning | Morphemes carry unintended readings | Check candidates for unfortunate meanings across audiences |
| Pattern drift | Construction rules loosened to force a favorite | Keep the pattern fixed and let candidates compete |

## Security and Authority Boundary

Generated names can collide with trademarks and communities. Generation produces candidates, not clearances; legal and cultural vetting remains a required step before any public use.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia’s overview of onomastics, the study of names (https://en.wikipedia.org/wiki/Onomastics).
2. Wikipedia’s overview of naming conventions (https://en.wikipedia.org/wiki/Naming_convention).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Logo Design](logo-design.md) — the visual identity that a chosen name must fit and reinforce.
- [Copywriting](copywriting.md) — the messaging craft that puts the chosen name to work in text.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
