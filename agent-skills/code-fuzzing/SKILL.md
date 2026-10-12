---
name: code-fuzzing
description: Feed generated, malformed, and adversarial inputs to a target until it fails, then minimize the failure into a reproducible defect report using coverage feedback.
metadata:
  source: skills/05-code/code-fuzzing.md
  category: 05-code
  version: "v1"
---

# Code Fuzzing

Category: Code | Level: advanced | Stability: experimental | Version: v1

## Description

Fuzzing is automated guessing about where code breaks. Instead of hand-picking edge cases, a fuzzer generates many inputs — mutated, malformed, structure-aware — and keeps the ones that reach new code or new failures. This skill covers running a fuzzer with feedback, triaging what it finds, and minimizing a failing input into a defect report a maintainer can reproduce.

## When to Use

Use on parsers, decoders, and anything that consumes untrusted input, where the input surface is too large for hand-written cases and crashes or memory corruption are real risks.

Do not fuzz as a one-off: coverage-guided fuzzing finds defects with sustained runtime and a corpus that grows, not with a single short run.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `target` | `callable` | Yes | The function or binary under test |
| `harness` | `callable` | Yes | Entry point that feeds generated inputs to the target |
| `corpus` | `list` | No | Seed inputs to start from |
| `budget` | `map` | No | Time or iteration limit |

## Procedure

1. Write a harness that calls the target with a generated input and turns any crash, hang, or assertion violation into a recorded failure — the harness is the contract.
2. Seed the corpus with realistic and boundary inputs so the fuzzer starts near interesting code.
3. Run coverage-guided generation: keep inputs that reach new paths and mutate them further.
4. Record every unique failure with its input, stack trace, and the coverage state that produced it.
5. Minimize each failing input — strip bytes and simplify structure — while confirming the failure persists.
6. Deduplicate by root cause rather than by input: a hundred crashes from one null dereference are one defect report.

## Outputs

| Output | Type | Description |
|---|---|---|
| `failures` | `list` | Unique failures with inputs and traces |
| `minimized` | `map` | Reduced reproducer per failure |
| `stats` | `map` | Coverage, executions, and time budget spent |

## Runnable Example

```python
import random

def fuzz(target, seeds, rounds=200):
    corpus, failures = list(seeds), []
    for _ in range(rounds):
        candidate = bytearray(random.choice(corpus))
        if candidate:
            pos = random.randrange(len(candidate))
            candidate[pos] ^= 1 << random.randrange(8)
        data = bytes(candidate)
        try:
            target(data)
            corpus.append(data)
        except ValueError as err:
            report = (data, str(err))
            if report not in failures:
                failures.append(report)
    return failures

def parse(data):
    if len(data) < 4:
        raise ValueError("short header")
    if data[0] == 255:
        raise ValueError("reserved flag set")

print(fuzz(parse, [b"AAAA", b"\x10\x00\x00\x01"])[:3])
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Harness blind spots | Failures the harness never observes | Write the harness against the crash contract, then review it |
| Empty seeds | Fuzzing starts from nothing and stalls | Seed with realistic and boundary inputs |
| Crash-only triage | Hangs and assertion violations go unreported | Record timeouts and invariants, not only crashes |
| Unminimized reports | Maintainers receive giant inputs | Minimize while the failure persists |
| Root-cause pileup | One defect is filed many times | Deduplicate failures by cause |

## Security and Authority Boundary

Fuzzing cuts both ways: the same harness that finds defects in your code can be pointed at systems you do not own. Run fuzzers only against targets you own or are authorized to test, and treat findings in third-party code as responsible-disclosure material.

## Evidence

This skill is grounded in dated public implementation references:

1. The OSS-Fuzz continuous fuzzing platform documentation (https://google.github.io/oss-fuzz/).
2. Wikipedia's overview of fuzzing (https://en.wikipedia.org/wiki/Fuzzing).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Property-Based Testing](property-based-testing.md) — the invariant-first cousin that checks specifications rather than crashes.
- [Security Scanning](security-scanning.md) — the known-vulnerability layer complementing input-level discovery.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
