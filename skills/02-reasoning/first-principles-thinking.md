---
title: "First Principles Thinking"
category: 02-reasoning
level: intermediate
stability: experimental
description: "Decompose a problem into verified foundational facts, rebuild the solution upward from those facts, and record which borrowed assumptions were kept or dropped so the plan stays auditable."
added: "2026-10"
version: v1
related: ["deductive-reasoning", "root-cause-analysis", "trade-off-analysis"]
---

# First Principles Thinking

Category: Reasoning | Level: intermediate | Stability: experimental | Version: v1

## Description

Plans inherit assumptions by analogy — a design or estimate is carried over because it worked last time — and those assumptions are rarely re-checked. This skill defines a rebuild contract: state the goal, list the facts that are actually verified, list the assumptions being borrowed, and derive the plan from the facts with an explicit verdict for every assumption. It is a reasoning procedure, not a source of new facts; verification still happens through evidence gathering.

## When to Use

Use when a plan, design, or estimate keeps inheriting unexamined defaults and the cost of a wrong inherited assumption is high.

Do not use for routine execution where the constraints are already verified; a direct procedure is cheaper than a rebuild.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `goal` | `string` | Yes | The outcome phrased as a single testable sentence |
| `facts` | `list` | Yes | Statements with a verification flag and their source |
| `assumptions` | `list` | Yes | Borrowed claims with the evidence that would support them |
| `constraints` | `list` | No | Hard limits the rebuild must respect |

## Procedure

1. State the goal as a single testable sentence; reject goals that cannot be phrased as an outcome.
2. List every foundation the plan currently rests on, separating verified facts from borrowed assumptions.
3. For each fact, record how it was verified; entries without verification are reclassified as assumptions.
4. For each assumption, record what evidence would confirm it and mark it kept only when that evidence exists or the plan explicitly tolerates its failure.
5. Derive requirements from the facts alone; every requirement must trace to at least one fact.
6. Rebuild the plan upward: foundations first, then requirements, then steps, then schedule estimates.
7. Record the kept and dropped assumption verdicts next to the plan so a reviewer can audit the derivation.
8. Re-run the rebuild whenever a foundation changes; a plan is only as current as its facts.

## Outputs

| Output | Type | Description |
|---|---|---|
| `plan` | `object` | Steps derived from foundations and requirements |
| `foundations` | `list` | Verified facts the plan rests on, with their sources |
| `assumption_verdicts` | `list` | Kept or dropped verdicts with the deciding evidence |
| `unverified_facts` | `list` | Entries reclassified from facts to assumptions |

## Runnable Example

```python
def rebuild_from_principles(goal, facts, assumptions):
    """Rebuild a plan upward from verified facts, recording assumption verdicts."""
    verified = [f for f in facts if f.get("verified")]
    decisions = []
    for item in assumptions:
        if item.get("evidence"):
            decisions.append((item["claim"], "kept"))
        else:
            decisions.append((item["claim"], "dropped - no supporting evidence"))
    plan = {
        "goal": goal,
        "foundations": [f["statement"] for f in verified],
        "assumption_verdicts": decisions,
        "steps": [
            "verify each foundation",
            "derive requirements from facts only",
            "review dropped assumptions before committing",
        ],
    }
    return plan

plan = rebuild_from_principles(
    "ship a configuration loader",
    [
        {"statement": "files are read at startup", "verified": True},
        {"statement": "all values are strings", "verified": True},
    ],
    [
        {"claim": "users always edit files by hand", "evidence": False},
        {"claim": "values need type coercion", "evidence": True},
    ],
)
print(plan["foundations"])
print(plan["assumption_verdicts"])
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Analogy smuggling | A last-time practice recorded as a fact | Reclassify it as an assumption and give it a verdict |
| Untestable goal | The goal is phrased as an activity, not an outcome | Rephrase as a single testable sentence |
| Verdict theater | Assumptions marked kept with no supporting evidence | Require the evidence or an explicit tolerance for failure |
| Rebuild fan-out | Everything is rebuilt from scratch | Rebuild only what the changed foundations touch |
| Stale rebuild | Foundations changed after the plan was written | Re-run the rebuild on every foundation change |

## Security and Authority Boundary

Rebuilding a plan from first principles grants no authority to bypass review or existing controls. Dropping an assumption is an analytical verdict, not a decision: changes to scope, budget, or commitments still require the normal approval boundaries.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia’s article on Aristotle, the classical source of the first-principles method (https://en.wikipedia.org/wiki/Aristotle).
2. Wikipedia’s article on first principles (https://en.wikipedia.org/wiki/First_principle).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Deductive Reasoning](deductive-reasoning.md) — derives conclusions from premises; this skill disciplines which premises are allowed in.
- [Root Cause Analysis](root-cause-analysis.md) — drills down to a verified cause; this skill rebuilds upward from verified causes.
- [Trade-off Analysis](trade-off-analysis.md) — records decision trade-offs that the assumption verdicts feed into.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
