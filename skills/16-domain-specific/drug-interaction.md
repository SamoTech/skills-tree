---
title: "Drug Interaction"
category: 16-domain-specific
level: advanced
stability: stable
description: "Apply drug interaction in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-16-domain-specific-drug-interaction.json)

**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Detects clinically significant drug-drug and drug-food interactions by checking pairs and combinations against curated interaction databases. Classifies severity (contraindicated / major / moderate / minor), explains the mechanism, and suggests safe alternatives where available.

### Example
```python
DRUG_DB = {
    frozenset(["warfarin", "ibuprofen"]): {"severity": "major", "effect": "increased bleeding risk"},
    frozenset(["ssri", "tramadol"]): {"severity": "contraindicated", "effect": "serotonin syndrome"},
    frozenset(["metformin", "alcohol"]): {"severity": "moderate", "effect": "lactic acidosis risk"},
}

def check_interactions(drugs: list[str]) -> list[dict]:
    drugs = [d.lower() for d in drugs]
    findings = []
    for pair, info in DRUG_DB.items():
        if pair.issubset(set(drugs)):
            findings.append({"pair": list(pair), **info})
    return findings or [{"result": "no known interactions"}]

print(check_interactions(["Warfarin", "Ibuprofen", "Metformin"]))
```

### Related Skills
- [Symptom Analysis](symptom-analysis.md)
- [Medical Literature Search](medical-literature-search.md)
- [Fact Verification Memory](../03-memory/fact-verification-memory.md)
