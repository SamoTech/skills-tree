**Category:** Creative
**Skill Level:** Intermediate
**Stability:** stable
**Added:** 2025-03

### Description
Produces formatted video scripts with scene headings, on-screen text (B-roll), voiceover narration, speaker labels, and timestamps. Supports YouTube explainers, product demos, documentary segments, and short-form vertical video (Reels/Shorts).

### Example
```python
import anthropic

client = anthropic.Anthropic()

prompt = """
Write a 90-second YouTube explainer script on 'How LLM tokenisation works'.
Format:
- [TIME] SCENE: description
- VO: voiceover line
- ON-SCREEN: text overlay
Target audience: developers new to AI.
Tone: clear, slightly informal.
"""

message = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)
print(message.content[0].text)
```

### Related Skills
- [Blog Post Writing](blog-writing.md)
- [Structured Output](../06-communication/structured-output.md)
- [Presentation Generation](presentation-gen.md)
