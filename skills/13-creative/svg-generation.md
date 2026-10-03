---
title: "SVG Generation"
category: 13-creative
level: advanced
stability: stable
version: v2
added: "2025-03"
updated: "2026-10-03"
description: "Generate and validate SVG markup for icons, diagrams, and simple illustrations with explicit viewBox, element, accessibility, and sanitization constraints."
---

# SVG Generation

## Purpose

Produce SVG documents that are structurally valid and constrained for their intended rendering context. Generation and validation are separate steps.

## Inputs / Outputs

| Item | Type | Required | Notes |
|---|---|---:|---|
| SVG specification | dict | yes | Dimensions, viewBox, allowed elements |
| Content | SVG string | yes | Generated document |
| Validation result | bool | yes | Structural/policy checks |
| Sanitized SVG | SVG string | recommended | Safe output for untrusted contexts |

## Runnable Example

```python
from xml.etree import ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"

def validate_svg(svg: str) -> bool:
    root = ET.fromstring(svg)
    if root.tag != f"{{{SVG_NS}}}svg":
        raise ValueError("root is not svg")
    if not root.get("viewBox"):
        raise ValueError("viewBox is required")
    allowed = {"svg", "path", "circle", "rect", "g", "title", "desc"}
    for element in root.iter():
        name = element.tag.rsplit("}", 1)[-1]
        if name not in allowed:
            raise ValueError(f"unsupported element: {name}")
    return True

svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><title>Node</title><circle cx="32" cy="32" r="16"/></svg>'
print(validate_svg(svg))
```

## Security Rules

- Treat generated SVG as untrusted when it can originate from users or models.
- Apply an allowlist of elements and attributes for untrusted contexts.
- Remove active content or external references when the rendering environment does not permit them.
- Validate namespace, dimensions, and viewBox before publishing.
- Keep accessibility metadata such as title/description where appropriate.

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Invalid XML | Malformed generation | Parse before use |
| Unsafe content | Active/external SVG features | Sanitize with an explicit allowlist |
| Broken scaling | Missing or inconsistent viewBox | Require and validate viewBox |
| Accessibility loss | Missing title/description | Validate required metadata for the target context |

## Evidence

- SVG specification overview: https://www.w3.org/TR/SVG2/
- XML parsing documentation: https://docs.python.org/3/library/xml.etree.elementtree.html

Evidence status: references support the structural guidance. No rendering compatibility guarantee is made.

## Related Skills

- image-generation
- logo-design
- code-generation

## Changelog

| Version | Date | Change |
|---|---|---|
| v1 | 2025-03 | Initial entry |
| v2 | 2026-10 | Added validation, security boundaries, and deterministic example |
