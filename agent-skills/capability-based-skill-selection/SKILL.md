---
name: capability-based-skill-selection
description: Select and sequence canonical skills for a task by matching required capabilities, discriminating competing candidates, checking eligibility and dependencies, and using execution evidence to choose the next skill.
metadata:
  source: skills/15-orchestration/capability-based-skill-selection.md
  category: 15-orchestration
  version: "v1"
---

# Capability-Based Skill Selection

Category: Orchestration | Level: advanced | Stability: experimental | Version: v1

## Description

Capability-based skill selection turns a task into an explicit skill decision rather than treating retrieval as selection. It identifies the capabilities required by the current task, compares competing canonical skills, checks evidence, compatibility, authority, and prerequisites, then selects an executable skill and determines what should happen next from the observed result.

This skill is intended for agent runtimes and orchestrators that consume a canonical skill registry. It does not replace search, the registry, dependency graph, or execution runtime.

## When to Use

Use when an agent must decide which skill to invoke for a concrete task and more than one plausible skill may match.

Do not use this as a substitute for simple deterministic lookup when the canonical skill ID is already known.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `task` | `string` / `object` | Yes | Current task, objective, or unresolved subtask |
| `context` | `object` | Yes | Project state, constraints, environment, prior results, and available tools |
| `candidates` | `list` | Yes | Candidate canonical skills discovered from the registry/search boundary |
| `capabilities` | `list` | No | Required capabilities already inferred by an upstream goal/capability resolver |
| `completed_skills` | `list` | No | Skills already executed successfully for the current task |
| `evidence` | `object` | No | Available benchmark, provenance, freshness, compatibility, or runtime evidence |

## Selection Procedure

1. Normalize the task into the capabilities required to make progress.
2. Resolve candidate skills through the canonical registry and reject unknown or non-canonical IDs.
3. Separate direct matches from merely related skills.
4. Compare competing candidates using task fit, required capability coverage, eligibility, compatibility, evidence quality, freshness, and known limitations.
5. Resolve mandatory prerequisites before selecting a dependent skill.
6. Prefer the smallest sufficient skill set; do not select skills merely because they are related.
7. Produce an explicit selection rationale and rejected-candidate reasons.
8. Invoke the selected executable skill only when its prerequisites and authority conditions are satisfied.
9. Verify the result against the task acceptance criteria.
10. If verification fails, classify the failure and select the next justified skill or recovery action rather than blindly repeating the same invocation.
11. Stop when the task is verified complete, blocked by an external condition, or requires escalation.

## Outputs

| Output | Type | Description |
|---|---|---|
| `selected_skill` | `object` | Canonical skill ID/version selected for the current step |
| `required_prerequisites` | `list` | Dependencies that must be satisfied before invocation |
| `rejected_candidates` | `list` | Plausible candidates rejected with explicit reasons |
| `next_action` | `object` | Next invocation, verification, recovery, escalation, or terminal decision |
| `evidence_requirements` | `list` | Evidence needed to verify the selected action |
| `status` | `string` | `CONTINUE`, `BLOCKED`, or `DONE` |

## Decision Contract

A valid selection must answer all of these questions:

- What capability is required now?
- Which canonical skill satisfies it?
- Why is it better than the competing candidates?
- Which prerequisites must run first?
- Is the skill eligible in the current context?
- What evidence will verify the invocation?
- What result causes the agent to invoke the next skill?
- What result causes recovery, substitution, escalation, or termination?

A skill must not be selected solely because it contains matching keywords.

## Runnable Example

```python
candidates = [
    {"id": "15-orchestration/specialist-agent-routing", "capabilities": ["agent-routing"]},
    {"id": "15-orchestration/capability-based-skill-selection", "capabilities": ["skill-selection"]},
]

task = {
    "objective": "Choose the correct specialist skill and continue after its result",
    "required_capabilities": ["skill-selection"],
}

selected = next(
    item for item in candidates
    if set(task["required_capabilities"]).issubset(item["capabilities"])
)

result = {
    "selected_skill": selected["id"],
    "status": "CONTINUE",
    "next_action": "invoke_selected_skill",
}

print(result)
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Retrieval mistaken for selection | Top search result is treated as authoritative | Evaluate competing candidates against task requirements |
| Ambiguous candidates | Several skills satisfy overlapping capabilities | Require explicit discrimination reasons and tie-break evidence |
| Hidden prerequisite | Dependent skill selected before required capability exists | Resolve prerequisite/dependency graph before invocation |
| Stale or weak evidence | Candidate has outdated or insufficient proof | Prefer fresher, provenance-backed evidence and surface the gap |
| Ineligible candidate | Compatibility, authority, or runtime constraints are unmet | Reject candidate and continue with an eligible alternative |
| Repeated failed invocation | Same action is retried without new evidence | Classify failure and choose recovery, substitution, or escalation |
| Premature completion | Selection succeeds but task outcome is unverified | Require outcome evidence before `DONE` |
| Over-selection | Agent invokes related skills without causal need | Select the smallest sufficient skill set |

## Security and Authority Boundary

Skill selection does not grant permissions. The selected skill must execute only within its declared authority, security boundary, compatibility constraints, and available runtime permissions.

High-impact or irreversible actions must remain subject to the governing approval and policy controls of the consuming agent runtime.

## Evidence

This skill is motivated by two complementary evidence classes:

1. Public demand signals around automated task breakdown, agent orchestration, and assignment based on skills/performance.
2. Skills Tree's current behavioral evaluation gap: retrieval quality is now measured, but task-specific skill discrimination, dependency-aware selection, invocation, and next-skill decisions are not yet comprehensively benchmarked.

The demand evidence is recorded in `meta/MOST-WANTED-SKILLS.md`; it is not treated as popularity or adoption data.

## Related Skills

- [Specialist Agent Routing](specialist-agent-routing.md) — routes requests to specialist agents; this skill selects canonical skills within an agent capability space.
- [Role Assignment](role-assignment.md) — assigns responsibilities and authority; this skill chooses the concrete skill for the current task step.
- [Conditional Branching](conditional-branching.md) — provides workflow branching after a result.
- [Agent Handoff](agent-handoff.md) — transfers execution context when another agent or skill must continue.
- [Subagent Delegation](../09-agentic-patterns/subagent-delegation.md) — delegates bounded work to another agent.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial evidence-backed skill-selection contract |
