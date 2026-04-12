**Category:** Creative
**Skill Level:** Basic
**Stability:** stable
**Added:** 2025-03

### Description
Generates platform-appropriate social media content for Twitter/X, LinkedIn, Instagram, and Threads. Applies platform-specific character limits, hashtag strategies, emoji usage, and tone conventions.

### Example
```python
import anthropic

client = anthropic.Anthropic()

platform_specs = {
    "twitter": "280 chars max, 2-3 hashtags, punchy",
    "linkedin": "Up to 3000 chars, professional, story hook",
    "instagram": "Caption + 10 hashtags, emoji-friendly",
}

for platform, spec in platform_specs.items():
    prompt = f"Write a {platform} post announcing the launch of FocusFlow, an AI productivity app. Spec: {spec}"
    msg = anthropic.Anthropic().messages.create(
        model="claude-opus-4-5",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}]
    )
    print(f"--- {platform.upper()} ---\n{msg.content[0].text}\n")
```

### Related Skills
- [Copywriting](copywriting.md)
- [Tone Adjustment](../06-communication/tone-adjustment.md)
- [Multilingual Output](../06-communication/multilingual-output.md)
