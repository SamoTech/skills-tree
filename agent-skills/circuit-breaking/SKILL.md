---
name: circuit-breaking
description: Stop calling a failing dependency after a threshold, fail fast while the circuit is open, and probe with trial calls before closing so one slow or broken service cannot take the caller down with it.
metadata:
  source: skills/15-orchestration/circuit-breaking.md
  category: 15-orchestration
  version: "v1"
---

# Circuit Breaking

Category: Orchestration | Level: advanced | Stability: experimental | Version: v1

## Description

Retries have a limit beyond which they become part of the outage. A circuit breaker converts persistent failure into a fast, local decision: after a threshold of consecutive failures the circuit opens and calls short-circuit immediately; after a reset window a limited probe tests the water; only a successful probe closes the circuit again. The caller sheds load and stays responsive while the dependency recovers.

## When to Use

Use around any remote dependency whose failure or latency can exhaust the caller — model APIs, databases, downstream services called on a request path.

Do not wrap workloads where every call must succeed; a breaker that skips required work turns degraded mode into silent data loss.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `dependency` | `string` | Yes | The dependency the breaker guards |
| `failure_threshold` | `number` | Yes | Consecutive failures that open the circuit |
| `reset_timeout` | `duration` | Yes | Open period before a probe is allowed |
| `probe` | `() -> result` | Yes | The single trial call used in half-open state |

## Procedure

1. Track consecutive failures per dependency, not globally; one bad endpoint should not open every circuit.
2. When the count reaches the threshold, open the circuit and fail fast — no call, no queue, no waiting.
3. While open, answer immediately with a defined degradation result, never with an exception shape callers have not agreed to.
4. After the reset timeout, move to half-open and allow exactly one probe call; the rest still fail fast.
5. Close on a successful probe and reset the counter; re-open and restart the timer on a failed probe.
6. Export circuit state as a metric; state transitions are the outage narrative.

## Outputs

| Output | Type | Description |
|---|---|---|
| `state` | `closed | open | half_open` | Current circuit state |
| `action` | `call | short_circuit | probe` | What the breaker did with this call |
| `failure_count` | `number` | Consecutive failures at decision time |

## Runnable Example

```python
class CircuitBreaker:
    def __init__(self, threshold, reset_timeout):
        self.threshold = threshold
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.opened_at = None

    def decide(self, now):
        if self.failures < self.threshold:
            return "call"
        if now - self.opened_at >= self.reset_timeout:
            return "probe"
        return "short_circuit"

    def record(self, ok, now):
        if ok:
            self.failures = 0
            self.opened_at = None
        else:
            self.failures += 1
            if self.failures == self.threshold:
                self.opened_at = now

breaker = CircuitBreaker(threshold=3, reset_timeout=60)
for outcome in [False, False, False]:
    breaker.record(outcome, now=0)
print(breaker.decide(now=10), breaker.decide(now=100))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Flapping | Threshold or timeout tuned to noise | Calibrate to the dependency's real error profile |
| No half-open state | Open circuits close on faith after the timer | Require one successful probe before closing |
| Shared breakers | One circuit for heterogeneous calls | Track per dependency and per call class |
| State lost on restart | Counters held in process memory only | Persist or re-warm counters; treat restart as probe |
| Silent degradation | Short-circuits invisible to callers and operators | Export state metrics and log every transition |

## Security and Authority Boundary

The breaker protects the caller's time and threads; it does not repair the dependency or verify its recovery. Post-incident validation of the dependency stays with its owner, and an open circuit is a degraded state, never a healthy one.

## Evidence

This skill is grounded in dated public implementation references:

1. The Circuit Breaker pattern on microservices.io (https://microservices.io/patterns/reliability/circuit-breaker.html).
2. Wikipedia's overview of fault tolerance (https://en.wikipedia.org/wiki/Fault_tolerance).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Retry Backoff](retry-backoff.md) — the bounded retry layer the breaker sits behind.
- [Event Triggers](event-triggers.md) — event paths where fast failure must not silently drop triggers.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
