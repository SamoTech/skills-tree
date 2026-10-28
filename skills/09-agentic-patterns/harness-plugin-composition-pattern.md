---
title: "Harness Plugin Composition Pattern"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Harness Plugin Composition Pattern contract with bounded inputs, recorded verification, and fail-closed handling."
added: "2026-10"
version: v1
related: [agent-harness-assembly, harness-plugin-architecture-patterns]
tags: [harness, plugin, composition, pattern]
---

# Harness Plugin Composition Pattern

## Description
Harness Plugin Composition Pattern contract with bounded inputs, recorded verification, and fail-closed handling. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent must compose multiple plugins into one harness session with declared interfaces and no hidden cross-plugin state.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Declare each plugin interface: inputs, outputs, and side-effect class.
2. Define the composition contract: which plugin may call which, and through what interface.
3. Wire the composition explicitly and forbid hidden global state between plugins.
4. Test the composition with a fixture that exercises every declared edge.
5. Fail the composition when a plugin expands its declared interface at runtime.
6. Emit the composition manifest with the plugin versions and the tested edges.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def compose(plugins, allowed_edges):
    calls = [(a, b) for a in plugins for b in plugins[a]["calls"] if a != b]
    illegal = [e for e in calls if e not in allowed_edges]
    return {"composition_valid": not illegal, "illegal_edges": illegal}
r = compose({"p1": {"calls": ["p2"]}, "p2": {"calls": []}}, [("p1", "p2")])
assert r == {"composition_valid": True, "illegal_edges": []}
```

## Failure Modes
- Plugins communicate through undeclared globals so the composition cannot be tested.
- The composition is verified by a demo run instead of a fixture covering every edge.
- A plugin quietly expands its interface and the composition keeps passing review.
- Plugin versions are not pinned so a green composition is unreproducible.
- Side-effect classes are undeclared so ordering bugs surface only in production.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The the October 12 fall-2026 review describing harness runtimes where models, tools, skills, and UI are all plugins above the model is the dated public signal for this contract. ([public signal](https://dreaming.press/posts/ai-agent-frameworks-whats-changed-fall-2026.html))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Harness Assembly](../09-agentic-patterns/agent-harness-assembly.md)
- [Harness Plugin Architecture Patterns](../09-agentic-patterns/harness-plugin-architecture-patterns.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
