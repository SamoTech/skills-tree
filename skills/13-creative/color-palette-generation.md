---
title: "Color Palette Generation"
category: 13-creative
level: basic
stability: experimental
description: "Generate color palettes with grounded color theory, checking contrast ratios, accessibility thresholds, and perceptual harmony so palettes work for real interfaces, not just swatches."
added: "2026-10"
version: v1
related: ["logo-design","svg-generation"]
---

# Color Palette Generation

Category: Creative | Level: basic | Stability: experimental | Version: v1

## Description

A palette is a system of roles with constraints, not a set of attractive colors. The skill covers deriving palettes from a base hue using declared harmony strategies, assigning roles such as background, surface, text, accent, and state, then verifying the assignments against WCAG contrast thresholds and the expected display contexts. A palette ships only with its measured contrast table, because the ratios are the part that makes it usable.

## When to Use

Use when an interface, brand, or document needs a coherent set of colors with known contrast behavior across text, states, and backgrounds.

Do not judge a palette by its swatches alone. Colors that look harmonious side by side can fail legibility the moment one becomes text on another.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `base_color` | `string` | Yes | Anchor color as a hex value or named reference |
| `strategy` | `enum` | No | Harmony rule: `analogous` (default), `complementary`, `triadic`, or `monochrome` |
| `roles` | `list` | No | Required palette roles; defaults to interface roles |

## Procedure

1. Convert the base color to a working space such as HSL or OKLCH and derive candidate steps.
2. Generate harmony candidates per the chosen strategy, keeping lightness and saturation controlled.
3. Assign roles: background, surface, text, accent, and state colors.
4. Compute contrast ratios for every text-on-background pairing the design needs.
5. Adjust lightness until all required pairings pass WCAG AA, or better where the brief demands.
6. Emit the palette with hex values, roles, and the measured contrast table.

## Outputs

| Output | Type | Description |
|---|---|---|
| `palette` | `array` | Colors with hex values and assigned roles |
| `contrast_table` | `table` | Measured ratio for each required pairing |
| `accessibility_verdict` | `object` | Pass or fail per pairing against the stated threshold |

## Runnable Example

```python
def relative_luminance(hex_color):
    def ch(part):
        c = int(part, 16) / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = ch(hex_color[0:2]), ch(hex_color[2:4]), ch(hex_color[4:6])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast_ratio(fg, bg):
    l1, l2 = relative_luminance(fg), relative_luminance(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return round((hi + 0.05) / (lo + 0.05), 2)

print(contrast_ratio("111111", "ffffff"))
print(contrast_ratio("9e9e9e", "ffffff"))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Illegible text pairs | Palette judged visually without measurement | Compute and enforce WCAG ratios for all pairs |
| Vibrancy-only harmony | All steps share similar lightness | Spread lightness across roles deliberately |
| Context-blind colors | Palette tuned for one background only | Verify pairings on every expected background |
| State colors ambiguous | Error, warning, and success hues too close | Separate state hues and test with color-vision simulation |
| Swatch-to-system mismatch | Colors unassigned to roles | Always emit roles with values |

## Security and Authority Boundary

Palettes carry accessibility obligations in many products. Do not soften measured thresholds to save an aesthetic, and test with color-vision deficiency simulation before shipping state colors that users must distinguish to operate safely.

## Evidence

This skill is grounded in dated public implementation references:

1. The Adobe Color harmony and accessibility tool (https://color.adobe.com/).
2. The Wikipedia article on color theory (https://en.wikipedia.org/wiki/Color_theory).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Logo Design](logo-design.md) — the brand mark that fixes the anchor color a palette grows from.
- [SVG Generation](svg-generation.md) — the vector medium where palette roles get applied as code.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
