---
name: ui-element-waiting
description: Synchronize computer-use actions on observed UI state with bounded explicit-wait loops, injected clocks, and timeout budgets instead of fixed sleeps so automation is deterministic and fails fast.
metadata:
  source: skills/10-computer-use/ui-element-waiting.md
  category: 10-computer-use
  version: "v1"
---

# UI Element Waiting

Category: Computer Use | Level: intermediate | Stability: experimental | Version: v1

## Description

A fixed sleep is a guess that wastes time when the app is fast and fails when it is slow. An explicit wait replaces the guess with a contract: poll a state predicate on a fixed interval until it holds or a declared budget expires. With an injected clock the loop is testable offline, and the wait either returns the observed ready time or fails with evidence of how much budget was spent.

## When to Use

Use whenever an automation must act on an element that appears asynchronously — after launch, navigation, or a slow update — and the failure mode of a timeout should be an explicit error rather than a mistimed click.

Do not use to mask an application bug; if a reasonable budget never suffices, fix the application or shorten the flow instead of raising timeouts.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `predicate` | `function -> boolean` | Yes | State check answering whether the element is ready |
| `timeout` | `number` | Yes | Maximum wait budget in seconds |
| `poll_interval` | `number` | Yes | Delay between predicate evaluations |
| `clock` | `function -> number` | No | Injectable time source; wall clock when omitted |

## Procedure

1. Define the readiness predicate on observable state — DOM presence, pixel match, or API flag — never on elapsed time alone.
2. Declare timeout and poll interval before starting the wait; defaults must come from policy, not from the call site’s mood.
3. Compute the deadline from the injected clock so tests run deterministically offline.
4. Evaluate the predicate at least once before advancing time, so already-ready elements return immediately.
5. On timeout, fail with the budget spent and the last observed state; a silent None return hides the evidence.
6. Record observed wait times per element so budgets are tuned on measurements, not folklore.
7. Never nest waits to synthesize longer budgets; raise the declared budget instead.

## Outputs

| Output | Type | Description |
|---|---|---|
| `ready_at` | `number | null` | Clock time when the predicate first held, or null on timeout |
| `elapsed` | `number` | Observed wait duration |
| `deadline` | `number` | The computed deadline for audit |

## Runnable Example

```python
class FakeClock:
    def __init__(self, start=0.0):
        self.now = start

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds

def wait_until(predicate, timeout, poll_interval, clock):
    """Poll predicate until it holds or the budget expires."""
    if predicate():
        return clock()
    deadline = clock() + timeout
    while clock() < deadline:
        clock.advance(poll_interval)
        if predicate():
            return clock()
    return None

clock = FakeClock()
appear_at = 3.0
predicate = lambda: clock() >= appear_at
ready_at = wait_until(predicate, timeout=10, poll_interval=0.5, clock=clock)
print("ready_at:", ready_at, "elapsed:", ready_at - 0.0)
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Flaky timing | Fixed sleeps tuned to one machine | Replace sleeps with predicate polling and measured budgets |
| Hidden timeout | Loop returns silently on expiry | Fail with the spent budget and last observed state |
| Clock coupling | Tests read the wall clock directly | Inject the clock so waits replay deterministically |
| Predicate drift | Ready check weaker than the real need | Test the predicate against the downstream action it guards |
| Runaway wait | Deadline computed inside the loop | Compute the deadline once, before polling starts |

## Security and Authority Boundary

Waiting on UI state grants no authority over the application. An automation observing readiness may act only within its permitted action set; polling must respect the target app’s load and authentication boundaries.

## Evidence

This skill is grounded in dated public implementation references:

1. Selenium’s WebDriver waits documentation (https://www.selenium.dev/documentation/webdriver/waits/).
2. Python’s time module documentation for monotonic clocks (https://docs.python.org/3/library/time.html).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Visual Element Detection](visual-element-detection.md) — supplies the readiness predicates this skill polls.
- [Screenshot Capture](screenshot-capture.md) — feeds pixel-based state checks into the same wait contract.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
