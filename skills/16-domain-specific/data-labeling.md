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

### Related Skills
- [Data Cleaning](../12-data/data-cleaning.md)
- [Structured Output](../06-communication/structured-output.md)
- [Embedding Generation](../12-data/embedding-generation.md)
