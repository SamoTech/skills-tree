![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-16-domain-specific-legal-research.json)

**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Locates relevant statutes, regulations, case law, and secondary sources for a legal issue. Uses jurisdiction-aware query strategies, citation chaining, and source credibility ranking to surface authoritative precedents and current law.

### Example
```python
import anthropic

client = anthropic.Anthropic()

def legal_research(issue: str, jurisdiction: str = "US") -> str:
    prompt = (
        f"You are a legal research assistant. For the issue: '{issue}' in {jurisdiction},\n"
        "list: 1) Key statutes or regulations, 2) Landmark cases, 3) Current trend. "
        "Cite sources precisely."
    )
    resp = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.content[0].text

print(legal_research("non-compete enforceability", "California"))
```

### Related Skills
- [Contract Review](contract-review.md)
- [Citation Attribution](../06-communication/citation-attribution.md)
- [Web Search](../11-web/web-search.md)
