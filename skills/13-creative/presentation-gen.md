**Category:** Creative
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2025-03

### Description
Builds presentation outlines and slide-by-slide content with titles, bullet points, speaker notes, and visual suggestions. Adapts structure to pitch decks, educational slides, or technical deep-dives.

### Example
```python
import anthropic, json

client = anthropic.Anthropic()

def generate_deck(topic: str, slides: int = 8) -> list[dict]:
    resp = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1200,
        messages=[{"role": "user", "content": (
            f"Create a {slides}-slide presentation on '{topic}'.\n"
            "Return JSON array: [{slide_number, title, bullets: [str], speaker_note, visual_idea}]."
        )}]
    )
    return json.loads(resp.content[0].text)

deck = generate_deck("Why RAG beats fine-tuning for enterprise LLMs")
for s in deck[:2]:
    print(s["title"], s["bullets"])
```

### Related Skills
- [Blog Writing](blog-writing.md)
- [Structured Output](../06-communication/structured-output.md)
