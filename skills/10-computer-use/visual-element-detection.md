---
title: "Visual Element Detection"
category: 10-computer-use
level: advanced
stability: stable
version: v2
description: "Identify visible UI elements from a verified screenshot or screen region and return bounded candidate targets."
added: "2025-03"
related: [screenshot-capture, gui-element-anchoring-stability]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-visual-element-detection.json)

# Visual Element Detection

**Category:** `computer-use`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Identify visible UI elements from a verified screenshot or screen region and return bounded candidate targets. Detection results are candidates, not facts: each candidate carries its evidence and ambiguity, and downstream actions re-verify the chosen target before acting on it.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | source | object | A verified, fresh screenshot or region to analyze |
| Input | query | object | The element description or template to locate |
| Output | candidates | object | Bounded candidate list with per-candidate confidence and region |
| Output | check | object | Ambiguity assessment (unique match, multiple, none) |

### Procedure
1. Start from a fresh, verified capture; record its geometry and scale.
2. Detect candidate elements matching the query; cap the candidate list.
3. Score and sort candidates by confidence; record the evidence for each.
4. Declare ambiguity explicitly when multiple candidates tie or none clears the threshold.
5. Hand the single best-verified candidate to the action step, which re-verifies before acting.

### Example

```python
query = {"element": "primary action button", "region": {"x": 0, "y": 800, "w": 1280, "h": 200}}
candidates = [
    {"id": "btn-save", "conf": 0.91, "box": {"x": 900, "y": 860}},
    {"id": "btn-cancel", "conf": 0.55, "box": {"x": 700, "y": 860}},
]
assert len(candidates) <= 5, "candidate list must stay bounded"
best = max(candidates, key=lambda c: c["conf"])
ambiguous = sum(1 for c in candidates if best["conf"] - c["conf"] < 0.1) > 1
verdict = "ambiguous" if ambiguous else best["id"]
print({"best": best["id"], "conf": best["conf"], "verdict": verdict})
```

### Related Skills

- [Screenshot Capture](screenshot-capture.md) - the fresh frame detection reads
- [Gui Element Anchoring Stability](gui-element-anchoring-stability.md) - keep anchors stable across renders
- [Screen Ocr](screen-ocr.md) - read text rather than detect elements

## Failure Modes

- Multiple visually similar candidates tie and the detector silently picks one.
- A theme or density change invalidates template matching without notice.
- Occlusion or overlap hides the target and a wrong element matches.
- Icon-only elements match by pixels but carry no semantic identity.
- The underlying content re-renders between detection and the action that uses the coordinates.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/output-guardrails/self-category pointers).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
