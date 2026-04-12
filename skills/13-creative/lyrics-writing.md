**Category:** Creative
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2025-03

### Description
Composes song lyrics with verse/chorus/bridge structure, rhyme schemes, metre, and thematic consistency. Adapts to genre conventions from pop to hip-hop to folk and can match a provided melody or chord progression.

### Example
```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=600,
    messages=[{"role": "user", "content": (
        "Write a complete indie-pop song about leaving a city you love. "
        "Structure: Verse 1 (8 lines, ABAB rhyme), Chorus (4 lines, AABB), "
        "Verse 2 (8 lines), Chorus, Bridge (4 lines), final Chorus."
    )}]
)
print(message.content[0].text)
```

### Related Skills
- [Creative Writing](creative-writing.md)
- [Tone Adjustment](../06-communication/tone-adjustment.md)
