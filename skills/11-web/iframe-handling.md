---
title: "Iframe Handling"
category: 11-web
level: intermediate
stability: experimental
description: "Locate, enter, and act inside nested iframe documents during browser automation, resolving frame identity, cross-origin limits, and stale frame references deterministically."
added: "2026-10"
version: v1
related: ["dom-inspection","js-execution"]
---

# Iframe Handling

Category: Web | Level: intermediate | Stability: experimental | Version: v1

## Description

Iframe handling turns a flat page into a tree of documents. The skill covers enumerating frames, resolving the target frame by identity rather than by selector alone, re-scoping lookups to the frame document, and proving the current scope before and after every action. The core discipline is that a selector never identifies an element on its own in a framed page; a (frame, selector) pair does.

## When to Use

Use when a target page embeds content in one or more iframes: embedded forms, payment widgets, media players, sandboxed previews, or third-party embeds that must be automated or audited.

Do not assume a single flat DOM. The same selector can resolve in several frames, and acting inside the wrong frame produces plausible-looking but incorrect results.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `page` | `object` | Yes | Live browser page or session object |
| `frame_locator` | `string` | Yes | Selector, frame name, or URL pattern identifying the target frame |
| `mode` | `enum` | No | `strict` (default) or `chain` when nested frames must be traversed in order |

## Procedure

1. Enumerate all frames in the page with their name, URL, and nesting depth before any interaction.
2. Resolve the target frame by selector, name, or URL pattern; prefer URL identity when selectors collide.
3. Enter the frame and re-scope all subsequent lookups to its document root.
4. Assert a frame-specific element exists before acting; a missing anchor means the scope is wrong.
5. Perform the action inside the frame, treating every lookup as frame-relative, never global.
6. Exit to the top document explicitly and re-assert scope before continuing with other tasks.

## Outputs

| Output | Type | Description |
|---|---|---|
| `frame_inventory` | `array` | Ordered list of frames with identity, URL, and nesting depth |
| `scoped_result` | `object` | Outcome of the action performed inside the target frame |
| `scope_log` | `list` | Entered and exited frame chain recorded in order |

## Runnable Example

```python
def resolve_frame_chain(frames, pattern):
    """frames: [(name, url, depth)]"""
    matches = [f for f in frames if pattern in f[0] or pattern in f[1]]
    if not matches:
        return {"resolved": False, "reason": "no frame matches pattern"}
    frame = sorted(matches, key=lambda f: f[2])[0]
    chain = [f[0] for f in frames if f[2] < frame[2]]
    return {"resolved": True, "chain": chain + [frame[0]], "url": frame[1]}

print(resolve_frame_chain(
    [("top", "https://example.com/app", 0),
     ("widget", "https://cdn.example.com/pay", 1),
     ("inner", "https://cdn.example.com/pay/frame", 2)],
    "pay",
))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Wrong frame selected | Duplicate selectors across frames | Resolve by URL or nesting chain, not selector alone |
| Stale frame reference | Frame reloaded after navigation | Re-resolve the frame before each action batch |
| Cross-origin access blocked | Same-origin policy limits direct inspection | Drive the frame through automation APIs, not raw DOM access |
| Silent frame exit | Actions continue on the parent document | Assert frame scope before every action |
| Detached frame timing | Frame mounts late or asynchronously | Wait for frame availability with a bounded timeout |

## Security and Authority Boundary

Iframes frequently embed third-party content, and entering a frame moves input across an origin boundary. Verify the frame origin before typing anything into it, never inject credentials into unverified origins, and record which origins received input as part of the audit trail.

## Evidence

This skill is grounded in dated public implementation references:

1. The MDN reference for the HTML iframe element (https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe).
2. The Playwright frames documentation (https://playwright.dev/python/docs/frames).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [DOM Inspection](dom-inspection.md) — the document inventory that reveals embedded frames and their origins.
- [JS Execution](js-execution.md) — the in-page mechanism used to probe frame state when locators alone are insufficient.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
