---
title: "Macro Recording"
category: 10-computer-use
level: basic
stability: experimental
description: "Record, normalize, and replay user-interface event sequences with deterministic compression of redundant input so repeated computer-use flows replay identically every time."
added: "2026-10"
version: v1
related: ["keyboard-type", "mouse-click"]
---

# Macro Recording

Category: Computer Use | Level: basic | Stability: experimental | Version: v1

## Description

A recorded input sequence is only useful if it replays the same way twice. Raw event streams contain noise — intermediate mouse moves, doubled clicks, retraced paths — that makes replay fragile. This skill defines macro recording as a normalizing pipeline: capture typed events, compress redundant ones by explicit rules, store the script with its rules version, and replay from the normalized form only.

## When to Use

Use when a repeated UI flow — setup, smoke checks, or form entry — should be captured once from real interaction and then replayed identically on demand.

Do not use to record credentials or one-time authorization flows; those inputs belong in secret stores, not in macro scripts.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `events` | `list[(type, target, arg)]` | Yes | Raw input events in capture order |
| `rules_version` | `string` | Yes | Version of the normalization rules applied |
| `tolerance` | `number` | No | Time window within which repeated clicks merge |

## Procedure

1. Capture events as typed tuples — event type, target identifier, argument — in strict occurrence order.
2. Compress intermediate mouse-move events to the last position per continuous drag; never store every sampled point.
3. Merge rapid repeated clicks on one target into a double-click by the declared tolerance rule.
4. Keep the normalization rules versioned inside the macro; replay applies exactly the recorded version.
5. Replay strictly from the normalized script; raw captures are inputs, never the replay source.
6. Verify replay by a post-run state check, not by assuming the script worked.

## Outputs

| Output | Type | Description |
|---|---|---|
| `script` | `list[(type, target, arg)]` | The normalized, replayable event sequence |
| `compressed` | `integer` | Number of raw events removed by normalization |

## Runnable Example

```python
def normalize(events):
    """Compress mouse-move chains and merge repeated clicks into double-clicks."""
    script = []
    for etype, target, arg in events:
        if etype == "move" and script and script[-1][0] == "move":
            script[-1] = ("move", target, arg)
            continue
        if etype == "click" and script and script[-1][0] == "click" and script[-1][1] == target:
            script[-1] = ("double-click", target, arg)
            continue
        script.append((etype, target, arg))
    return script

events = [("move", "canvas", 10), ("move", "canvas", 20),
          ("click", "save", None), ("click", "save", None), ("type", "save", "ok")]
script = normalize(events)
print(script)
print("compressed:", len(events) - len(script))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Fragile replay | Raw capture replayed unfiltered | Normalize before storing and replay from the script |
| Accidental secrets | Credentials captured into the macro | Exclude secret fields at capture time and audit scripts |
| Silent merge errors | Double-click rule fires across targets | Merge only on identical targets within tolerance |
| Ambiguous targets | Identifiers break after UI change | Record stable element identifiers, not coordinates alone |
| Unverified replay | Success assumed from script completion | Assert post-run application state after replay |

## Security and Authority Boundary

A macro is a recorded capability grant: it performs whatever its recording could perform. Keep macro scripts out of shared storage, exclude secrets at capture time, and scope replay to the environment it was recorded in.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia’s overview of macros in computing (https://en.wikipedia.org/wiki/Macro_(computer_science)).
2. Python’s pickle module security note on untrusted data (https://docs.python.org/3/library/pickle.html).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Keyboard Type](keyboard-type.md) — the typed events captured here follow that skill’s typing contract.
- [Mouse Click](mouse-click.md) — the click semantics this skill’s merge rules normalize.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
