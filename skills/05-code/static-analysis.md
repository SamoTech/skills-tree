---
title: "Static Analysis"
category: 05-code
level: intermediate
stability: experimental
description: "Find defects without executing code — dataflow, taint paths, and lint rules — triaging true positives from noise with a stated, documented rule inventory."
added: "2026-10"
version: v1
related: ["code-review", "security-scanning"]
---

# Static Analysis

Category: Code | Level: intermediate | Stability: experimental | Version: v1

## Description

Static analysis reads code the way a reviewer with infinite patience would: every path, every assignment, every tainted flow from input to dangerous sink. Its problem is signal — tools over-report, and untriaged findings train teams to ignore them. This skill covers configuring analyzers, triaging output honestly, and maintaining a rule inventory that documents why each rule earns its noise.

## When to Use

Use as a continuous gate on changed code and as a periodic deep pass — taint analysis on untrusted-input paths, security rules on everything that handles data.

Do not run analyzers in default configuration over legacy code and report thousands of findings at once; that output gets archived rather than acted on.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `code` | `path` | Yes | The codebase or module to analyze |
| `profile` | `map` | Yes | Rule set and severity thresholds in force |
| `baseline` | `list` | No | Previously triaged and waived findings |

## Procedure

1. Configure a profile for the codebase: enabled rules, severities, and the reasoning that each noisy rule is worth its cost.
2. Analyze the whole program where the tool supports it — cross-function taint paths die at file scope.
3. Triage every finding against the baseline: confirm, waive with a reason, or fix now; never leave untriaged findings in the gate.
4. Distinguish findings by kind — real defect, style preference, false positive — and adjust rules to shrink the third category.
5. Feed confirmed security findings to the defect queue with the taint path attached, not just the line number.
6. Re-baseline after fixes: the baseline records what was consciously accepted, not what was ignored.

## Outputs

| Output | Type | Description |
|---|---|---|
| `findings` | `list` | Confirmed defects with locations and paths |
| `waivers` | `list` | Accepted findings with reasons and expiry |
| `metrics` | `map` | Counts by severity, rule, and status over time |

## Runnable Example

```python
def taint_flows(assignments, sources, sinks):
    tainted = set(sources)
    for var, expr in assignments:
        if any(t in expr for t in tainted):
            tainted.add(var)
    flows = []
    for var, expr in assignments:
        sink = next((s for s in sinks if s in expr), None)
        if sink and var in tainted:
            flows.append((var, sink))
    return sorted(set(flows))

assignments = [("query", "user_input"), ("cursor", "execute(query)")]
print(taint_flows(assignments, {"user_input"}, {"execute"}))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Alert fatigue | Untriaged findings train ignore-first behavior | Triage everything and waive with reasons |
| Default profiles | Stock rules mismatch the codebase | Configure and document the rule profile |
| File-scope blindness | Cross-file taint paths are missed | Use whole-program analysis where available |
| Frozen baselines | Waivers never expire or get revisited | Put expiry dates on waivers |
| Findings without paths | A line number with no dataflow context | Attach the taint or value-flow path to each finding |

## Security and Authority Boundary

Static analysis is itself a security control, and its output is sensitive: a triaged findings list is a map of known weaknesses. Restrict access to findings, share waivers with the team that owns the code, and do not publish detailed weakness inventories for unfixed systems.

## Evidence

This skill is grounded in dated public implementation references:

1. The Bandit security linter documentation for Python (https://bandit.readthedocs.io/).
2. Wikipedia's overview of static program analysis (https://en.wikipedia.org/wiki/Static_program_analysis).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Code Review](code-review.md) — the human judgment layer that consumes these findings.
- [Security Scanning](security-scanning.md) — the dependency and known-CVE layer that complements source analysis.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
