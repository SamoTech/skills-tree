**Category:** Creative
**Skill Level:** Advanced
**Stability:** experimental
**Added:** 2025-03

### Description
Generates game level designs as 2D tile maps (CSV/JSON), room descriptions for text adventures, or procedural generation parameter sets. Applies game design principles: pacing, challenge curves, player flow, and reward placement.

### Example
```python
import anthropic
import json

client = anthropic.Anthropic()

prompt = """
Generate a 20x15 tile map for a top-down RPG dungeon level in JSON format.
Tile legend:
  0 = floor, 1 = wall, 2 = door, 3 = chest, 4 = enemy spawn, 5 = exit
Rules:
- Surrounded by walls (1)
- 3 rooms connected by corridors
- 1 exit (5), 2 chests (3), 3 enemy spawns (4)
- Output ONLY the JSON: {"width": 20, "height": 15, "tiles": [[...], ...]}
"""

message = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=2048,
    messages=[{"role": "user", "content": prompt}]
)
level = json.loads(message.content[0].text)
print(f"Level size: {level['width']}x{level['height']}")
```

### Related Skills
- [SVG/Vector Art Generation](svg-generation.md)
- [Structured Output](../06-communication/structured-output.md)
- [Algorithm Design](../05-code/algorithm-design.md)
