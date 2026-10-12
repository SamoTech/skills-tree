---
title: "Screen Region Mapping"
category: 10-computer-use
level: intermediate
stability: experimental
description: "Map normalized screen coordinates onto integer pixel regions across logical resolutions and device pixel ratios so UI targets stay stable when displays or zoom levels change."
added: "2026-10"
version: v1
related: ["screen-ocr", "multi-monitor"]
---

# Screen Region Mapping

Category: Computer Use | Level: intermediate | Stability: experimental | Version: v1

## Description

Pixel coordinates are a fragile basis for automation: change the display scale or resolution and every stored target breaks. Normalized coordinates — 0..1 fractions of the logical screen — survive both. This skill defines the mapping contract in both directions: normalized to pixels for acting, pixels to normalized for recording, with the device pixel ratio explicit in every conversion so HiDPI displays compute correctly.

## When to Use

Use when recorded UI targets must survive resolution, monitor, or zoom changes, or when screenshots from different device pixel ratios must be compared against one logical layout.

Do not use for text-based targets; element identifiers and accessibility trees are more stable than any coordinate scheme.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `normalized` | `(x, y, w, h)` | Yes | Region in 0..1 fractions of the logical screen |
| `logical_size` | `(width, height)` | Yes | Logical resolution of the screen or window |
| `dpr` | `number` | Yes | Device pixel ratio, default 1 |

## Procedure

1. Store automation targets in normalized units; treat pixel coordinates as derived, disposable values.
2. Carry the device pixel ratio in every conversion; omitting it silently halves or doubles regions on HiDPI displays.
3. Convert each coordinate by multiplying normalized value, logical size, and dpr, rounding half away from zero.
4. Clamp pixel results to the physical screen bounds; off-screen regions are rejected, not wrapped.
5. Round-trip check critical regions: convert to pixels and back, and reject mappings that drift beyond a declared tolerance.
6. On multi-monitor setups, anchor normalized coordinates to the specific monitor’s logical size, never to the union of screens.

## Outputs

| Output | Type | Description |
|---|---|---|
| `pixel_rect` | `(x, y, w, h)` | Integer pixel region in physical coordinates |
| `normalized_rect` | `(x, y, w, h)` | Normalized region recovered from pixels |

## Runnable Example

```python
def to_pixel_rect(normalized, width, height, dpr=1):
    """(x, y, w, h) in 0..1 units -> integer pixel rectangle."""
    x, y, w, h = normalized
    return (round(x * width * dpr), round(y * height * dpr),
            round(w * width * dpr), round(h * height * dpr))

def to_normalized_rect(rect, width, height, dpr=1):
    px, py, pw, ph = rect
    return (px / (width * dpr), py / (height * dpr),
            pw / (width * dpr), ph / (height * dpr))

region = (0.25, 0.5, 0.5, 0.25)
for dpr in (1, 2):
    px = to_pixel_rect(region, 1920, 1080, dpr)
    back = tuple(round(v, 4) for v in to_normalized_rect(px, 1920, 1080, dpr))
    print("dpr", dpr, "pixels:", px, "round-trip:", back)
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| HiDPI drift | Device pixel ratio omitted from conversion | Carry dpr through every mapping explicitly |
| Monitor confusion | Coordinates anchored to the union of screens | Anchor to the specific monitor’s logical size |
| Rounding drift | Half-pixel rounding differs by runtime | Use one documented rounding rule and round-trip check |
| Off-screen targets | Regions computed outside the bounds | Clamp and reject instead of wrapping or truncating |
| Scale dependence | Targets stored in pixels | Store normalized targets and derive pixels per session |

## Security and Authority Boundary

Screen regions describe where to act, not what may be acted on. Mapping grants no authority: every action derived from a region still passes the permission checks of the underlying automation.

## Evidence

This skill is grounded in dated public implementation references:

1. MDN documentation for window.devicePixelRatio (https://developer.mozilla.org/en-US/docs/Web/API/Window/devicePixelRatio).
2. Python’s round() documentation for rounding behavior (https://docs.python.org/3/library/functions.html#round).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Screen OCR](screen-ocr.md) — reads text inside the regions this skill maps from logical targets.
- [Multi Monitor](multi-monitor.md) — defines the per-monitor anchoring this mapping depends on.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
