---
name: data-labeling
description: Apply data labeling in an AI workflow with explicit scope, domain constraints, validation, and documented failure handling.
metadata:
  source: skills/16-domain-specific/data-labeling.md
  category: 16-domain-specific
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-16-domain-specific-data-labeling.json)

**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Assigns category labels, span annotations, bounding boxes, or structured metadata to datasets for supervised ML training. Manages taxonomy versioning, confidence scoring, and inter-annotator consistency checks at scale.

### Example
```python
import anthropic, json

client = anthropic.Anthropic()

TAXONOMY = ["billing", "technical_support", "feature_request", "complaint", "compliment"]

def label_batch(texts: list[str]) -> list[dict]:
    batch = json.dumps(texts)
    prompt = (
        f"Classify each text into one of: {TAXONOMY}.\n"
        "Return JSON array: [{{text, label, confidence_0_to_1}}].\n\n"
        f"Texts: {batch}"
    )
    resp = client.messages.create(
        model="claude-opus-4-5", max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(resp.content[0].text)

samples = ["I can't log into my account", "Loving the new dashboard!", "Please add dark mode"]
print(label_batch(samples))
```

## Failure Modes

- **Guideline ambiguity:** under-specified instructions producing label drift between annotators; resolve ambiguity through calibration examples before scaling.
- **Taxonomy drift:** labels produced against an outdated taxonomy version; every batch must record its taxonomy version.
- **Consistency theater:** high overall agreement on easy cases masking systematic disagreement on hard ones; measure agreement per class and diffi
culty band.
- **Confidence misuse:** self-reported annotator confidence treated as measured accuracy; calibrate confidence against adjudicated ground truth.
- **Imbalance blindness:** majority-class dominance hiding poor minority-class quality; report per-class metrics, not only aggregate agreement.

## Evidence
The canonical skill file is the authoritative repository implementation. Repository schema, validation workflows, and the Agent Skills projection contract define structural conformance. Domain-specific factual claims must remain traceable to supplied or independently verified authoritative sources.

### Related
- 16-domain-specific
- input-guardrails
- output-guardrails
