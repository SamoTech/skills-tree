---
name: app-readiness-probing
description: Probe a launched application with an ordered, bounded check sequence and an injectable clock so downstream computer-use actions begin only once the app verifiably accepts them.
metadata:
  source: skills/10-computer-use/app-readiness-probing.md
  category: 10-computer-use
  version: "v1"
---

# App Readiness Probing

Category: Computer Use | Level: intermediate | Stability: experimental | Version: v1

## Description

An app process being alive does not mean its UI is usable: windows take time, ports open late, and services initialize in order. Readiness probing turns “it started” into evidence — an ordered list of checks re-evaluated on a fixed schedule until every check holds within a declared budget. The probe fails loudly when the budget is spent, carrying the elapsed time and the checks that still failed.

## When to Use

Use after launching or connecting to an application — local desktop app, remote VM, or headed service — before any scripted interaction with its UI.

Do not use for continuous health monitoring of long-lived services; that is infrastructure probing, which has different lifecycle rules.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `checks` | `list[function -> boolean]` | Yes | Ordered readiness checks, evaluated in order each cycle |
| `timeout` | `number` | Yes | Total readiness budget in seconds |
| `poll_interval` | `number` | Yes | Delay between probe cycles |
| `clock` | `function -> number` | No | Injectable time source for deterministic tests |

## Procedure

1. Define each check against an externally observable condition — listening port, window present, login prompt visible — never against process liveness alone.
2. Order checks by dependency: earlier checks must hold before later ones can be meaningful.
3. Evaluate every check each cycle in a fixed order, computing readiness as all-checks-hold.
4. Return the elapsed time at first success so startup cost is measured, not guessed.
5. On budget expiry, fail with elapsed time plus the list of still-failing checks.
6. Bind the budget to an injectable clock so probes replay identically in tests.
7. Re-measure the budget after environment changes; a budget tuned once is a stale budget.

## Outputs

| Output | Type | Description |
|---|---|---|
| `ready_after` | `number | null` | Elapsed seconds when all checks passed, or null on timeout |
| `failed_checks` | `list[check]` | Checks still failing when the budget expired |
| `cycles` | `integer` | Number of probe cycles executed |

## Runnable Example

```python
class FakeClock:
    def __init__(self, start=0.0):
        self.now = start

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds

def probe_until(checks, timeout, poll_interval, clock):
    """Run ordered checks each cycle; return elapsed time when all pass."""
    start = clock()
    cycles = 0
    while clock() - start <= timeout:
        cycles += 1
        if all(check(clock() - start) for check in checks):
            return round(clock() - start, 2), cycles
        clock.advance(poll_interval)
    return None, cycles

clock = FakeClock()
checks = [lambda elapsed: elapsed >= 1.0, lambda elapsed: elapsed >= 2.5]
ready_after, cycles = probe_until(checks, timeout=10, poll_interval=0.5, clock=clock)
print("ready_after:", ready_after, "cycles:", cycles)
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Premature interaction | UI driven before services finished starting | Gate all scripted actions behind the readiness probe |
| Liveness confusion | Process existence treated as readiness | Probe observable capabilities, not process liveness |
| Unmeasured startup | Budget guessed from one machine | Record observed elapsed times and tune on evidence |
| Clock coupling | Probes read the wall clock in tests | Inject the clock for deterministic replay |
| Silent timeout | Failure swallowed by the caller | Treat probe timeout as a blocking error with diagnostics |

## Security and Authority Boundary

Probing grants no authority; it only observes. Probes must use the same authenticated session the actions will use and must not probe systems outside the automation’s declared scope.

## Evidence

This skill is grounded in dated public implementation references:

1. Kubernetes documentation for liveness, readiness, and startup probes (https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/).
2. Python’s socket module documentation for connectivity checks (https://docs.python.org/3/library/socket.html).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [App Launch](app-launch.md) — the launch operation whose completion this skill verifies before interaction.
- [VM Interaction](vm-interaction.md) — remote sessions gated by the same readiness evidence.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
