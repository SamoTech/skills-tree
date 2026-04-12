**Category:** Creative
**Skill Level:** Intermediate
**Stability:** experimental
**Added:** 2025-03

### Description
Generates meme concepts with template selection (Drake, Distracted Boyfriend, Two Buttons, etc.), top/bottom text, and optionally produces a rendered image using the Imgflip API or by overlaying text on a base image with Pillow.

### Example
```python
import anthropic
import requests

client = anthropic.Anthropic()

# Step 1: choose a template and write captions
idea = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=256,
    messages=[{"role": "user", "content": (
        "Pick the best meme template and write top/bottom text for: "
        "developers who fix a bug but create three new ones. "
        "Output JSON: {template, top_text, bottom_text}"
    )}]
)
print(idea.content[0].text)

# Step 2: render via Imgflip (requires free account)
# POST to https://api.imgflip.com/caption_image with template_id + text
```

### Related Skills
- [Image Generation (Prompt)](image-gen-prompt.md)
- [Copywriting](copywriting.md)
- [Social Media Post Generation](social-media-post.md)
