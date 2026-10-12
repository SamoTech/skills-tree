---
title: "Error Handling Design"
category: 05-code
level: intermediate
stability: experimental
description: "Design the failure path as deliberately as the happy path — typed error classes, explicit boundaries, and recovery decisions made where the context lives."
added: "2026-10"
version: v1
related: ["code-review", "debugging"]
---

# Error Handling Design

Category: Code | Level: intermediate | Stability: experimental | Version: v1

## Description

Most systems get their error handling designed by accident: catch blocks appear where crashes were once observed, each with its own policy. This skill designs the failure path deliberately — classify errors by what recovery is possible, translate them at boundaries, and decide retry, fallback, or fail-fast where the context to decide actually lives.

## When to Use

Use when designing or reviewing any module that can fail meaningfully — network calls, parsers, transactions, agents — especially where multiple layers could each independently retry or swallow errors.

Do not catch broadly and continue; a swallowed error is a delayed failure with a lost cause.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `operations` | `list` | Yes | The failing operations to design for |
| `boundaries` | `list` | Yes | Layer or system boundaries where errors translate |
| `policy` | `map` | Yes | Recovery rule per error class |

## Procedure

1. Enumerate the error classes per operation — transient, permanent, resource, integrity — before writing any handler; recovery decisions follow the class.
2. Fail fast on integrity and configuration errors; retrying a deterministic failure multiplies cost without changing the result.
3. Retry only transient errors, with backoff and a stated cap, and treat ambiguous outcomes as pending rather than failed.
4. Translate errors at boundaries: map internal classes to a documented contract with status, cause, and correlation id.
5. Attach context at the raise site — what operation, on what input class, at what stage — rather than reconstructing it later from strings.
6. Handle or propagate, and record which one happened where; an empty return after a caught error hides the failure from its caller.

## Outputs

| Output | Type | Description |
|---|---|---|
| `contract` | `map` | Error classes, meanings, and boundary translations |
| `handlers` | `list` | Recovery decisions per class with justification |
| `trace` | `map` | Correlation ids linking cause to observed failure |

## Runnable Example

```python
class Transient(Exception):
    pass

class Permanent(Exception):
    pass

def decide(err, attempt, cap=3):
    if isinstance(err, Permanent):
        return "fail-fast"
    if isinstance(err, Transient) and attempt < cap:
        return "retry"
    if isinstance(err, Transient):
        return "exhausted"
    return "translate-at-boundary"

for err in (Permanent("bad input"), Transient("timeout"), ValueError("other")):
    print(type(err).__name__, decide(err, attempt=2))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Swallowed errors | Catch-all blocks continue with broken state | Handle or propagate; do not silently continue |
| Retry everything | Deterministic failures retry to the cap | Classify before deciding recovery |
| Lost cause chains | Context is stripped at the first boundary | Translate with cause and correlation id |
| Empty returns after errors | Callers see empty results and no reason | Return the error or a documented default, with a record of which |
| Boundary policy conflict | Two layers both retry, multiplying attempts | Decide retry ownership once per chain |

## Security and Authority Boundary

Error messages are a disclosure channel: stack traces, query fragments, and file paths leak internals to callers and logs. Sanitize at trust boundaries, log the detail internally, and do not echo raw framework or driver errors to untrusted callers.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia's overview of exception handling (https://en.wikipedia.org/wiki/Exception_handling).
2. The OWASP Top 10 for large language model applications, whose failure-mode guidance this skill operationalizes (https://owasp.org/www-project-top-10-for-large-language-model-applications/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Code Review](code-review.md) — the review layer where failure-path quality is judged.
- [Debugging](debugging.md) — the investigation that well-designed errors make short.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
