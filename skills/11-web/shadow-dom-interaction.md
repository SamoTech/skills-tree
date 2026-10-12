---
title: "Shadow DOM Interaction"
category: 11-web
level: intermediate
stability: experimental
description: "Query and act on elements inside shadow roots during browser automation, handling open and closed shadow boundaries, nested hosts, and slot-projected content."
added: "2026-10"
version: v1
related: ["dom-inspection","js-execution"]
---

# Shadow DOM Interaction

Category: Web | Level: intermediate | Stability: experimental | Version: v1

## Description

Shadow DOM hides component internals behind a boundary that ordinary selectors cannot cross. The skill covers probing for shadow roots, composing locator chains across each boundary, asserting that a composed chain resolves to exactly one element, and respecting closed roots by interacting only through the interfaces a component exposes. Every boundary crossed is recorded so a failure can be traced to the correct layer.

## When to Use

Use when component libraries or web components encapsulate markup in shadow roots and standard selectors cannot reach the interactive elements inside them.

Do not force open closed shadow roots through internal framework APIs. A closed root is a component contract; interact through its exposed methods and attributes only.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `root_locator` | `string` | Yes | Selector for the host element whose shadow root is targeted |
| `target` | `string` | Yes | Selector for the element inside the shadow root |
| `mode` | `enum` | No | `pierce` (default) or `manual` for engines without shadow-piercing locators |

## Procedure

1. Probe candidate hosts to determine which ones carry shadow roots and whether each root is open or closed.
2. Choose piercing mode when the automation engine supports it; otherwise walk each shadow boundary explicitly.
3. Compose a locator chain across the boundaries and record the full path from the page root to the target.
4. Assert the composed chain resolves to exactly one element; zero or many results both mean the chain is wrong.
5. Interact through exposed methods or attributes when the root is closed instead of bypassing the boundary.
6. Record every boundary crossed so failures can be attributed to the correct layer of the component tree.

## Outputs

| Output | Type | Description |
|---|---|---|
| `boundary_path` | `list` | Hosts and shadow boundaries traversed, in order |
| `located_elements` | `array` | Elements resolved inside the shadow root |
| `interaction_result` | `object` | Outcome of the action performed on the target element |

## Runnable Example

```python
def compose_shadow_path(boundaries):
    """boundaries: [(host, mode)]"""
    path = []
    for host, mode in boundaries:
        if mode == "closed" and len(path) > 0:
            return {"path": None, "reason": "closed root behind an open chain"}
        path.append(host)
    return {"path": " >> ".join(path), "depth": len(path)}

print(compose_shadow_path([("app-shell", "open"), ("dropdown-widget", "open")]))
print(compose_shadow_path([("app-shell", "open"), ("pay-card", "closed"), ("inner", "open")]))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Selector misses the target | Element lives behind a shadow boundary | Probe hosts and compose chains across each boundary |
| Closed root blocks access | Component refuses internal inspection | Use exposed interfaces; do not bypass the boundary |
| Nested depth exceeded | Chain stops one boundary short | Record and follow the full host path |
| Slot content mislocated | Projected content resolves in a different root | Resolve through the slot, not the light DOM |
| Stale host after re-render | Component re-created the shadow tree | Re-probe and recompose the chain before acting |

## Security and Authority Boundary

Shadow DOM is an encapsulation boundary that some components rely on for security assumptions. Bypassing it can expose internal state that the component author intended to hide; probe only what the task requires and never exfiltrate internals beyond the run.

## Evidence

This skill is grounded in dated public implementation references:

1. The MDN guide on using shadow DOM (https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_shadow_DOM).
2. The Playwright locators documentation (https://playwright.dev/python/docs/locators).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [DOM Inspection](dom-inspection.md) — the outer document layer where shadow hosts are first identified.
- [JS Execution](js-execution.md) — the in-page mechanism for probing shadow root attachment state.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
