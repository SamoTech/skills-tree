![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-16-domain-specific-ad-copy.json)

**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Generates channel-specific ad copy variants for Google Search, Meta, LinkedIn, and TikTok while respecting character limits, platform policies, and audience targeting parameters. Supports multi-variant generation for A/B testing.

### Example
```python
import anthropic

client = anthropic.Anthropic()

PLATFORM_LIMITS = {
    "google": {"headline": 30, "description": 90},
    "meta": {"headline": 40, "body": 125},
    "linkedin": {"headline": 70, "description": 150},
}

def generate_ad(product: str, platform: str, n_variants: int = 3) -> list[dict]:
    limits = PLATFORM_LIMITS[platform]
    prompt = (
        f"Write {n_variants} {platform} ad variants for '{product}'.\n"
        f"Limits: {limits}. Return JSON array: [{{headline, body/description}}]."
    )
    resp = client.messages.create(
        model="claude-opus-4-5", max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )
    import json; return json.loads(resp.content[0].text)

print(generate_ad("AI-powered note-taking app", "google"))
```

### Related Skills
- [Product Description Writing](product-description.md)
- [Copywriting](../13-creative/copywriting.md)
