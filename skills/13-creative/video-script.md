![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-13-creative-video-script.json)

**Category:** Creative
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2025-03

### Description
Writes video scripts with hooks, pacing notes, on-screen text cues, B-roll suggestions, and calls to action. Adapts to YouTube, TikTok, course content, and product demo formats.

### Example
```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1000,
    messages=[{"role": "user", "content": (
        "Write a 90-second YouTube script explaining how RAG works to developers. "
        "Include: hook (0-5s), problem setup (5-20s), explanation with analogy (20-70s), "
        "demo teaser (70-80s), CTA (80-90s). Add [B-ROLL] notes inline."
    )}]
)
print(message.content[0].text)
```

### Related Skills
- [Blog Writing](blog-writing.md)
- [Presentation Generation](presentation-gen.md)
