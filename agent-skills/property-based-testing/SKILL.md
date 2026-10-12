---
name: property-based-testing
description: Test executable invariants over generated inputs instead of fixed examples, then shrink failing cases toward minimal counterexamples that reproduce the defect with the least context.
metadata:
  source: skills/05-code/property-based-testing.md
  category: 05-code
  version: "v1"
---

# Property Based Testing

Category: Code | Level: intermediate | Stability: experimental | Version: v1

## Description

Example-based tests check the cases someone thought of; property-based tests state invariants and let a generator search the input domain for violations. When a generated case fails, shrinking reduces it toward the smallest reproducer, which becomes the bug report and a permanent regression test. This skill covers that loop — declare invariants, generate, shrink, repair — as a reviewable engineering procedure.

## When to Use

Use when a function or service has a checkable invariant over a wide input space and hand-written examples cover only a thin slice of it.

Do not use for exact-output specifications or UI flows; deterministic example tests fit those better.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `invariants` | `list` | Yes | Predicates that must hold for every generated input |
| `generators` | `object` | Yes | Input-domain definitions including edge cases |
| `shrink_budget` | `integer` | No | Maximum shrinking steps per counterexample |
| `seed` | `integer` | No | Deterministic seed for reproducible runs |

## Procedure

1. State each invariant as a predicate over generated inputs; an invariant that cannot be phrased as a predicate is a smell.
2. Define the input domain explicitly, including boundaries: empty, zero, negative, and maximum-shaped cases.
3. Run generated cases against each invariant and collect every failing input.
4. Shrink each failing input toward a minimal reproducer; the shrunk case is what gets reported.
5. Pin the shrunk counterexample as a permanent deterministic example test.
6. Repair the defect, re-run the full property, and only then remove any temporary filters.
7. Rotate seeds on a schedule; a fixed seed set forever is just a slow example suite.
8. Record which invariants ran; an unexercised invariant is untested behavior.

## Outputs

| Output | Type | Description |
|---|---|---|
| `counterexamples` | `list` | Generated inputs that violated an invariant |
| `shrunk` | `list` | Minimal reproducers suitable for regression tests |
| `invariant_status` | `object` | Pass or fail state per declared invariant |
| `runs` | `integer` | Number of generated cases executed |

## Runnable Example

```python
def clamp(value, low, high):
    """Buggy function under test: it forgets the lower bound."""
    return min(high, value)

def property_clamp_stays_in_range(value, low, high):
    """Invariant: the clamped result must stay inside [low, high]."""
    result = clamp(value, low, high)
    return low <= result <= high

def find_counterexamples(candidates):
    """Generate failing inputs for the declared invariant."""
    return [c for c in candidates if not property_clamp_stays_in_range(*c)]

def shrink_toward_zero(counterexample, low, high):
    """Shrink a failing input toward a minimal reproducer."""
    value = counterexample[0]
    while value < low and value < 0:
        value = value // 2
        if property_clamp_stays_in_range(value, low, high):
            return value
    return low

candidates = [(v, -2, 3) for v in range(-8, 6)]
failures = find_counterexamples(candidates)
print("counterexamples:", failures[:4])
print("shrunk:", [shrink_toward_zero(f, -2, 3) for f in failures[:4]])
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Weak invariant | The property restates the implementation | Derive invariants from the specification, not the code |
| No shrinking | The first random failure is reported as-is | Shrink toward minimal inputs before reporting |
| Shrunk-case loss | The counterexample is never pinned | Add the shrunk case as a deterministic regression test |
| Fixed-seed blindness | The same seed runs forever | Rotate seeds while keeping failures reproducible |
| Generator gaps | The domain excludes edge values | Include empty, zero, negative, and maximum cases |

## Security and Authority Boundary

Property-based testing grants no authority to run generated inputs against production systems. Generators produce untrusted data: targets under test must be sandboxed, and shrinking must never reduce toward inputs that trigger real side effects.

## Evidence

This skill is grounded in dated public implementation references:

1. The Hypothesis property-based testing documentation (https://hypothesis.readthedocs.io/en/latest/).
2. Python’s unittest documentation (https://docs.python.org/3/library/unittest.html).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Unit Test Generation](unit-test-generation.md) — writes example tests; this skill generates the inputs those tests miss.
- [Integration Test Writing](integration-test-writing.md) — covers component seams; this skill stresses single-contract invariants.
- [Assertion](../04-action-execution/assertion.md) — states single checks; this skill states invariants over whole domains.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
