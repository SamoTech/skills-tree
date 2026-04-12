**Category:** Creative
**Skill Level:** Intermediate
**Stability:** stable
**Added:** 2025-03

### Description
Writes song lyrics with verse/chorus/bridge structure, rhyme schemes (ABAB, AABB, ABCB), and metre. Matches genre conventions — pop hooks, rap flows, folk ballads — and can generate jingles for commercial use.

### Example
```python
import anthropic

client = anthropic.Anthropic()

prompt = """
Write a complete pop song about resilience after failure.
Structure: Verse 1 / Pre-Chorus / Chorus / Verse 2 / Pre-Chorus / Chorus / Bridge / Outro
Rhyme scheme for verses: ABAB
Metre: iambic tetrameter (4 beats per line)
Tone: uplifting, anthemic
"""

message = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)
print(message.content[0].text)
```

### Related Skills
- [Music Composition](music-composition.md)
- [Creative Writing](creative-writing.md)
- [Tone Adjustment](../06-communication/tone-adjustment.md)
