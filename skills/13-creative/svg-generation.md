![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-13-creative-svg-generation.json)

**Category:** Creative
**Skill Level:** Advanced
**Stability:** stable
**Added:** 2025-03

### Description
Produces valid, optimised SVG markup for icons, illustrations, data charts, and infographics. Understands SVG path commands (`M`, `L`, `C`, `A`), `<defs>`, `<use>`, gradients, masks, and SMIL/CSS animations.

### Example
```python
import anthropic

client = anthropic.Anthropic()

prompt = """
Generate a minimal SVG logo for a company called 'Nexus' — a tech startup.
Requirements:
- viewBox="0 0 64 64"
- Uses only path and circle elements
- Monochrome (currentColor)
- Represents interconnected nodes
- Output ONLY the SVG markup, no explanation
"""

message = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)

svg_code = message.content[0].text
with open("nexus-logo.svg", "w") as f:
    f.write(svg_code)
print("SVG saved to nexus-logo.svg")
```

### Related Skills
- [Image Generation](../08-multimodal/image-generation.md)
- [Logo/Brand Design](logo-design.md)
- [Code Generation](../05-code/code-generation.md)
