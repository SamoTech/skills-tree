**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Transforms product attributes, specs, and selling points into persuasive, audience-aware copy for e-commerce listings. Adapts tone, length, and keyword strategy per channel (Amazon, Shopify, Google Shopping) and generates multiple variants for A/B testing.

### Example
```python
import anthropic

client = anthropic.Anthropic()

def write_product_copy(product: dict, channel: str = "amazon") -> str:
    attrs = ", ".join(f"{k}: {v}" for k, v in product.items())
    prompt = (
        f"Write a compelling {channel} product listing for this item.\n"
        "Include a punchy title, 5 bullet benefits, and a short description (80 words).\n"
        f"Attributes: {attrs}"
    )
    resp = client.messages.create(
        model="claude-opus-4-5", max_tokens=600,
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.content[0].text

print(write_product_copy({"name": "Mechanical Keyboard",
                           "switch": "Cherry MX Red", "connectivity": "Bluetooth 5.0"}))
```

### Related Skills
- [SEO Optimization](seo-optimization.md)
- [Copywriting](../13-creative/copywriting.md)
- [Ad Copy Generation](ad-copy.md)
