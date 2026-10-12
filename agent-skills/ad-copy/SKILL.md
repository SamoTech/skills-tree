---
name: ad-copy
description: Apply ad copy in an AI workflow with explicit scope, domain constraints, validation, and documented failure handling.
metadata:
  source: skills/16-domain-specific/ad-copy.md
  category: 16-domain-specific
---

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

## Failure Modes

- **Policy violations:** generated copy breaching platform ad policies (unsubstantiated claims, restricted categories) that would get ads rejected; check every variant against the live policy for its channel.
- **Limit miscounting:** variants exceeding character limits after placeholder expansion or emoji width; measure the final rendered length, not the template.
- **Fal
se claims:** implying results, statistics, or endorsements the product cannot substantiate; every claim must trace to approved source material.
- **Brand-voice drift:** tone or claim style inconsistent with the documented brand voice and disclaimers.
- **Audience mismatch:** fluent copy built for the wrong targeting segment or funnel stage.

## Evidence
The canonical skill file is the authoritative repository implementation. Repository schema, validation workflows, and the Agent Skills projection contract define structural conformance. Domain-specific factual claims must remain traceable to supplied or independently verified authoritative sources.

### Related
- 16-domain-specific
- input-guardrails
- output-guardrails
