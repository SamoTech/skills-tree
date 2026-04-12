**Category:** Creative
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2025-03

### Description
Crafts platform-native social media posts for Twitter/X, LinkedIn, Instagram, and TikTok. Applies character limits, hashtag strategy, hook writing, and engagement-optimised formatting for each channel.

### Example
```python
import anthropic, json

client = anthropic.Anthropic()

def write_posts(topic: str, platforms: list[str]) -> dict:
    resp = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=800,
        messages=[{"role": "user", "content": (
            f"Write social media posts about '{topic}' for: {', '.join(platforms)}.\n"
            "Follow each platform's style and limits. Return JSON: {{platform: post_text}}."
        )}]
    )
    return json.loads(resp.content[0].text)

print(write_posts("Launching an open-source AI skills tree", ["twitter", "linkedin"]))
```

### Related Skills
- [Copywriting](copywriting.md)
- [Tone Adjustment](../06-communication/tone-adjustment.md)
