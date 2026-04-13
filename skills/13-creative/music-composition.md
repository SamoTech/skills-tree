---
title: "Pipe to abc2midi or abcjs for playback"
category: 13-creative
level: advanced
stability: experimental
description: "Apply pipe to abc2midi or abcjs for playback in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-13-creative-music-composition.json)

**Category:** Creative
**Skill Level:** Advanced
**Stability:** experimental
**Added:** 2025-03

### Description
Generates musical compositions in ABC notation, MusicXML, or MIDI event sequences from text descriptions. Applies music theory: key signatures, chord progressions, rhythmic patterns, and dynamic markings.

### Example
```python
import anthropic

client = anthropic.Anthropic()

prompt = """
Compose a 16-bar piano piece in ABC notation with these specs:
- Key: C major
- Time: 4/4
- Tempo: Andante (76 BPM)
- Mood: nostalgic, gentle
- Use a I-V-vi-IV chord progression
Output ONLY the ABC notation, starting with X:1
"""

message = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)
print(message.content[0].text)
# Pipe to abc2midi or abcjs for playback
```

### Related Skills
- [Lyrics Writing](lyrics-writing.md)
- [Creative Writing](creative-writing.md)
- [Structured Output](../06-communication/structured-output.md)
