---
title: "Analogy Generation"
category: 02-reasoning
level: intermediate
stability: stable
version: v3
description: "Generate structural analogies that map a source concept to a target concept while explicitly checking which relationships transfer and which do not."
added: "2025-03"
related: []
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-analogy-generation.json)

# Analogy Generation

## Description
Generate structural analogies that explain a complex target concept by mapping structure from a familiar source domain, and verify explicitly which relationships transfer and which break down.

## When to Use
- Explaining an unfamiliar technical concept using a domain the audience already knows
- Testing whether two systems are structurally similar before reusing a solution pattern
- Teaching material where a wrong analogy is worse than no analogy

## Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | `target` | string | The concept to be explained |
| Input | `audience` | string | Who the analogy is for; sets vocabulary and depth |
| Input | `source_domain` | optional string | Preferred source domain, when the caller has one |
| Output | `analogy` | string | The analogy with its source-to-target mapping made explicit |
| Output | `transfers` | list of string | Relationships that genuinely carry over |
| Output | `breaks` | list of string | Known disanalogies; where the mapping must not be pushed |

## Example
```python
def check_analogy(mappings: list[tuple[str, str, bool]]) -> dict:
    """Validate a proposed analogy's relation-by-relation transfers.

    mappings: (source_relation, target_relation, holds) triples, e.g.
        ("electrons pushed by voltage", "money pushed by pressure", True)
    """
    transfers = [f"{s} -> {t}" for s, t, ok in mappings if ok]
    breaks = [f"{s} !-> {t}" for s, t, ok in mappings if not ok]
    return {"transfers": transfers, "breaks": breaks,
            "usable": len(transfers) >= 2 and len(breaks) <= len(transfers)}

result = check_analogy([
    ("voltage drives current", "pressure drives flow", True),
    ("resistance dissipates energy", "friction dissipates energy", True),
    ("current is consumed by devices", "fuel is consumed by engines", False),
])
print(result)
```

## Procedure
1. Identify the target concept and the specific relationships that matter for the audience.
2. Select a source domain the audience demonstrably knows; confirm with the caller when unsure.
3. Map each salient relation individually instead of borrowing the source wholesale.
4. Verify each mapping: mark which relationships transfer and which do not.
5. Discard or replace analogies whose central relations do not transfer.
6. Present the analogy with its stated limits, not as an identity.

## Failure Modes
- False analogies that mislead more than clarify: verify each mapped relation and discard analogies whose central relations break.
- Over-stretching the analogy beyond its valid mapping: state the boundaries explicitly in the output.
- Audience-unknown source domain: confirm the audience actually knows the source before building on it.
- Loading the analogy with conclusions it does not support: separate the explanatory mapping from any inference drawn from it.

## Related
- [Analogical Reasoning](analogical.md)
- [Commonsense Reasoning](commonsense.md)

## Changelog
- v3 (2026-11): Structural modernization; added the input/output contract table, procedure, deterministic transfer-checking example, and expanded failure modes.
- v1 (2026-04): Initial entry.

## Evidence

- https://agentskills.io/specification
- https://github.com/openai/openai-python

Evidence status: references support implementation guidance; no performance benchmark is claimed without reproducible benchmark evidence.
