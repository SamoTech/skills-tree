**Category:** Creative
**Skill Level:** Intermediate
**Stability:** stable
**Added:** 2025-03

### Description
Generates original creative prose, poetry, and fiction with consistent narrative voice, plot structure, and characterisation. Supports genre-specific conventions (thriller, romance, sci-fi) and adjustable style parameters such as tone, POV, and tense.

### Example
```python
import anthropic

client = anthropic.Anthropic()

prompt = """
Write a 200-word opening to a noir detective short story.
Setting: rain-soaked 1940s Chicago.
Protagonist: a cynical private investigator named Mae Cross.
Tone: hard-boiled, first-person.
"""

message = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=512,
    messages=[{"role": "user", "content": prompt}]
)
print(message.content[0].text)
```

### Related Skills
- [Tone Adjustment](../06-communication/tone-adjustment.md)
- [Persona Adoption](../06-communication/persona-adoption.md)
- [Blog Post Writing](blog-writing.md)
