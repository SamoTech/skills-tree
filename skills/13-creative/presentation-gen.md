**Category:** Creative
**Skill Level:** Intermediate
**Stability:** stable
**Added:** 2025-03

### Description
Generates slide deck outlines and content in Markdown, Marp, or Reveal.js format. Creates title slides, agenda, content slides with bullet points, speaker notes, and conclusion/CTA slides from a topic or document.

### Example
```python
import anthropic

client = anthropic.Anthropic()

prompt = """
Generate a 10-slide Marp presentation on 'AI Agents in 2025'.
Use Marp front matter (marp: true, theme: default).
Each slide: one H2 heading + 3-5 bullet points.
Include a title slide, 8 content slides, and a Q&A closing slide.
Add <!-- speaker notes --> under each slide.
"""

message = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=2048,
    messages=[{"role": "user", "content": prompt}]
)
with open("presentation.md", "w") as f:
    f.write(message.content[0].text)
```

### Related Skills
- [Report Writing](../06-communication/report-writing.md)
- [Structured Output](../06-communication/structured-output.md)
- [Blog Post Writing](blog-writing.md)
