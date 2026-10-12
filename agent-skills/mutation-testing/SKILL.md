---
name: mutation-testing
description: Measure test-suite strength by injecting small code mutations and checking which are caught — surviving mutants reveal tests that assert nothing meaningful.
metadata:
  source: skills/05-code/mutation-testing.md
  category: 05-code
  version: "v1"
---

# Mutation Testing

Category: Code | Level: intermediate | Stability: experimental | Version: v1

## Description

Coverage says a line ran; it does not say anyone would notice if it were wrong. Mutation testing flips the question: introduce small, mechanical changes to the code — flip a comparison, drop a call — and check whether the test suite fails. Surviving mutants are lines the suite does not actually defend, and each one is a concrete, fixable gap.

## When to Use

Use when a suite has high coverage but defects still escape — release-critical libraries, parser cores, financial logic — and the question is whether the tests assert real behavior.

Do not run mutation testing over an entire large codebase at once; it multiplies suite runtime by the mutant count, so scope it to critical modules.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `code` | `path` | Yes | The module under assessment |
| `suite` | `callable` | Yes | The test suite to measure |
| `operators` | `list` | No | Mutation operators to apply; default set |

## Procedure

1. Select the scope deliberately — critical modules first — because every mutant costs a full suite run.
2. Apply mutations one at a time: small, mechanical edits such as flipping an operator, changing a constant, or removing a call.
3. Run the suite per mutant and record the result: killed, survived, or timed out.
4. Treat timeouts as kills only when the suite is deterministic; flaky suites make mutation results noise.
5. Group surviving mutants and convert each group into a missing assertion or a new test that kills it.
6. Re-run and compare the mutation score — the fraction killed — instead of trusting coverage alone.

## Outputs

| Output | Type | Description |
|---|---|---|
| `mutants` | `list` | Applied mutations with kill status |
| `survivors` | `list` | Mutants the suite did not detect |
| `score` | `map` | Mutation score per module and overall |

## Runnable Example

```python
def make_mutants(source):
    mutants = []
    for old, new in (("<", ">="), ("+", "-"), ("and", "or")):
        if old in source:
            mutated = source.replace(old, new, 1)
            mutants.append({"operator": f"{old}->{new}", "source": mutated})
    return mutants

def score(killed, total):
    return round(killed / total, 2) if total else 1.0

source = "def check(n):\n    return n < 10 and n > 0\n"
mutants = make_mutants(source)
print([m["operator"] for m in mutants])
print(score(1, len(mutants)))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Coverage complacency | High coverage hides unasserted behavior | Measure mutation score on critical modules |
| Flaky suite noise | Timeouts and reruns corrupt kill counts | Stabilize the suite before mutating |
| Whole-codebase runs | Mutation cost explodes with suite time | Scope to critical modules |
| Survivor neglect | Survivors are recorded but never fixed | Convert each survivor into a new assertion |
| Equivalent mutants | Untestable-by-design mutants counted as gaps | Review and exclude provably equivalent mutants |

## Security and Authority Boundary

Mutation testing modifies code in working directories and can, with careless tooling, leak mutants into builds. Run it in an isolated checkout, never commit mutated files, and gate CI on the original source with mutants applied only in ephemeral workspaces.

## Evidence

This skill is grounded in dated public implementation references:

1. The mutmut mutation testing tool documentation (https://mutmut.readthedocs.io/).
2. Wikipedia's overview of mutation testing (https://en.wikipedia.org/wiki/Mutation_testing).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Unit Test Generation](unit-test-generation.md) — the suite layer this skill evaluates.
- [Property-Based Testing](property-based-testing.md) — the assertion-strength companion that also hunts survivors.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
