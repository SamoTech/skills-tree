**Category:** Creative
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2025-03

### Description
Produces well-structured blog articles with a clear title, introduction, H2/H3 subheadings, body sections, and conclusion. Adapts length, reading level, and SEO keyword density based on user instructions.

### Example
```python
import anthropic

client = anthropic.Anthropic()

prompt = """
Write a 600-word blog post titled:
'5 Ways AI Agents Are Changing Software Development in 2025'

Include:
- An engaging intro paragraph
- 5 numbered sections with a subheading each
- A short conclusion with a CTA to subscribe
Tone: conversational but authoritative.
"""

message = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)
print(message.content[0].text)
```

### Related Skills
- [Creative Writing](creative-writing.md)
- [Summarization](../06-communication/summarization.md)
- [Structured Output](../06-communication/structured-output.md)
