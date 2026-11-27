---
title: "Screenshot Capture"
category: 10-computer-use
level: advanced
stability: stable
version: v2
description: "Capture a screenshot of a verified screen or region for observation, evidence, or postcondition checking."
added: "2025-03"
related: [screen-ocr, computer-use-privacy-screening]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-screenshot-capture.json)

# Screenshot Capture

**Category:** `computer-use`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Capture a screenshot of a verified screen or region for observation, evidence, or postcondition checking. A capture is only useful if its source, moment, and geometry are known: verify the display and region, capture fresh, and screen for sensitive content before the image leaves the session.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | source | object | The display or region to capture, with verified geometry and scale |
| Input | privacy | object | The sensitive-content screening policy applied before the image is used |
| Output | image | object | The captured frame with its display, region, scale, and timestamp recorded |
| Output | check | object | Freshness and privacy-screening result |

### Procedure
1. Resolve the target display/region against the live geometry (correct display, scale, no straddle).
2. Capture a fresh frame at the moment of observation; record the timestamp.
3. Verify the captured geometry matches the declared region (right display, right scale).
4. Run the privacy screen for sensitive content before storing or transmitting the image.
5. Report the image with its provenance, or an explicit failure (capture blocked, secure desktop).

### Example

```python
source = {"display": "DP-1", "region": {"x": 0, "y": 0, "w": 2560, "h": 1440}, "scale": 1.0}
frame = {"captured_at": "t0", "geometry": {"w": 2560, "h": 1440}, "display": "DP-1"}
assert frame["geometry"]["w"] == source["region"]["w"], "captured geometry mismatch"
assert frame["display"] == source["display"], "captured the wrong display"
privacy = {"screened": True, "findings": []}
assert privacy["screened"], "privacy screening must run before the image leaves the session"
print({"captured": True, "display": frame["display"], "privacy_findings": privacy["findings"]})
```

### Related Skills

- [Screen Ocr](screen-ocr.md) - read text from the captured frame
- [Computer Use Privacy Screening](computer-use-privacy-screening.md) - screen captures for sensitive content
- [Screenshot Diff Verification](screenshot-diff-verification.md) - compare captures over time

## Failure Modes

- The capture comes from the wrong display or region in a multi-monitor setup.
- The frame catches a mid-transition animation and is read as a stable state.
- Sensitive content (credentials, private data) is captured without screening.
- DPI scaling mismatches make downstream coordinate math wrong.
- Capture is blocked by a secure desktop, DRM surface, or headless session and a blank frame is treated as a valid state.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/output-guardrails/self-category pointers).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
