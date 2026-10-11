---
name: skill-quality-evaluation
description: Evaluate a skill or skill package against measurable quality dimensions - description fidelity, instruction actionability, runnable example validity, failure-mode coverage, and evidence strength - and produce a scored, reproducible verdict before the skill is trusted, installed, or published.
metadata:
  source: skills/09-agentic-patterns/skill-quality-evaluation.md
  category: 09-agentic-patterns
  version: "v1"
---

# Skill Quality Evaluation

Category: Agentic Patterns | Level: advanced | Stability: experimental | Version: v1

## Description

Skill quality evaluation turns "is this skill good?" into a reproducible inspection with named dimensions and an explicit verdict. It scores a candidate skill against measurable quality dimensions - description fidelity, instruction actionability, runnable-example validity, failure-mode coverage, and evidence strength - and records the findings, so trusting, installing, publishing, or rejecting a skill is a documented decision instead of an impression.

This skill is intended for agent runtimes, registries, and maintainers who must decide whether a skill is fit to use or publish. It does not replace security auditing, benchmark execution, or human review; it complements them.

## When to Use

Use when a skill is about to be installed, published, promoted, or relied on, and no current quality verdict exists for its version.

Do not use this as a substitute for a security audit of untrusted packages, or as proof that a skill works; a passing quality score is not evidence of runtime effectiveness.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `skill` | `object` | Yes | The skill under evaluation: frontmatter, body, examples, and package files |
| `criteria` | `object` | No | Quality dimensions, weights, and thresholds; defaults are used when omitted |
| `evidence` | `list` | No | Available benchmark, provenance, runtime, or review evidence for the skill |
| `comparable` | `list` | No | Similar existing skills used to judge duplication and novelty |
| `verdict_policy` | `object` | No | Rules mapping the weighted score to PASS, NEEDS-WORK, or FAIL |

## Evaluation Procedure

1. Inventory the artifact: frontmatter, body, runnable example, and any bundled package files.
2. Check description fidelity: does the declared description match what the body actually instructs?
3. Check instruction actionability: are the instructions specific and verifiable, or vague aspiration?
4. Check the runnable example: does it run, is it deterministic where determinism is claimed, and does it exercise the core contract?
5. Check failure-mode coverage: are realistic failure modes named with causes and mitigations?
6. Check evidence strength: which claims carry dated, traceable evidence, and which are unevidenced?
7. Score each dimension with the agreed weights and compute the weighted total.
8. Apply the verdict policy to produce PASS, NEEDS-WORK, or FAIL with explicit blockers.
9. Record dimension scores, findings, and the verdict as a dated review artifact.
10. Re-evaluate when the skill changes version or when new contrary evidence appears.

## Outputs

| Output | Type | Description |
|---|---|---|
| `dimension_scores` | `object` | Per-dimension score with observed findings |
| `weighted_total` | `number` | Weighted quality score for the evaluated version |
| `verdict` | `string` | `PASS`, `NEEDS-WORK`, or `FAIL` |
| `blockers` | `list` | Findings that must be resolved before trust or publication |
| `review_artifact` | `object` | Dated, reproducible record of the evaluation |

## Decision Contract

A valid evaluation must answer all of these questions:

- Which dimensions were scored, with what weights and thresholds?
- Does the description match the instructions?
- Is the example runnable and representative?
- Which failure modes are covered and which are missing?
- Which claims carry dated evidence and which do not?
- What findings block a PASS verdict?
- What change or evidence would reopen the verdict?

A skill must not be marked high-quality solely because it is popular, long, or recently updated.

## Runnable Example

```python
def evaluate_skill_quality(skill, weights, thresholds):
    """Score a skill record against weighted quality dimensions."""
    dimensions = {
        "description_fidelity": 2 if skill["description_matches_body"] else 0,
        "instruction_actionability": 2 if skill["instructions_verifiable"] else 0,
        "runnable_example": 2 if skill["example_runs"] else 0,
        "failure_modes": 2 if skill["failure_modes_documented"] else 0,
        "evidence_strength": skill["evidence_tier"],
    }
    total = sum(dimensions[d] * weights[d] for d in dimensions)
    maximum = sum(2 * weights[d] for d in dimensions)
    if dimensions["evidence_strength"] == 0 or total < thresholds["needs_work"]:
        verdict = "FAIL"
    elif total < thresholds["pass"]:
        verdict = "NEEDS-WORK"
    else:
        verdict = "PASS"
    return {"score": f"{total}/{maximum}", "verdict": verdict}

weights = {"description_fidelity": 3, "instruction_actionability": 3,
           "runnable_example": 2, "failure_modes": 1, "evidence_strength": 3}
thresholds = {"pass": 20, "needs_work": 14}

reviewed = {
    "description_matches_body": True,
    "instructions_verifiable": True,
    "example_runs": True,
    "failure_modes_documented": True,
    "evidence_tier": 1,
}
print(evaluate_skill_quality(reviewed, weights, thresholds))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Rubric gaming | Skill text is written to satisfy the checklist without real capability | Require runnable examples and dated evidence, not keyword presence |
| Description drift | Description no longer matches the body after edits | Re-evaluate on every version change |
| Single-reviewer bias | One reviewer's taste dominates the verdict | Use shared dimensions, weights, and recorded findings |
| Evidence theater | Old or irrelevant citations are presented as current proof | Require dated, claim-specific evidence |
| Missing failure modes | Only the happy path is documented | Downgrade or fail skills without documented failure modes |
| Score without action | Findings are recorded but blockers are never resolved | Tie verdicts to install and publish gates |
| Tooling false confidence | Automated checks pass while runtime behavior fails | Treat automated scores as necessary, not sufficient |

## Security and Authority Boundary

Quality evaluation grants no permissions and does not execute the skill under test beyond its own runnable example in a controlled environment. Untrusted skills must additionally pass a dedicated security audit before installation or execution.

High-impact publication or installation decisions remain subject to the governing approval controls of the consuming runtime.

## Evidence

This skill is motivated by dated public ecosystem evidence:

1. The 2026 Agent Skills ecosystem report citing SkillsBench analyzed 47,150 public skills, found an average quality score of 6.2/12, and reported that curated skills improved agent pass rates by +16.2 percentage points (https://agentman.ai/blog/agent-skills-ecosystem-report-2026).
2. A September 2026 structured review of 26 agent skills against Anthropic skill-authoring guidance and the agentskills.io specification produced 152 concrete findings (https://github.com/fabiandistler/agents/issues/325; specification: https://agentskills.io/home).

Honest boundary: these signals establish that skill quality varies measurably and that evaluation demand exists; they are not popularity or adoption data. Passing this skill's checks is not proof of safety or runtime effectiveness.

The demand evidence is recorded in `meta/MOST-WANTED-SKILLS.md`.

## Related Skills

- [Agent Skill Security Audit](../14-security/agent-skill-security-audit.md) — audits untrusted skill packages for security; this skill scores quality.
- [Capability-Based Skill Selection](../15-orchestration/capability-based-skill-selection.md) — selects skills by capability fit; this skill supplies the quality evidence that selection consumes.
- [Critic Agent](critic-agent.md) — critiques outputs generally; this skill provides a fixed, reproducible rubric for skill artifacts.
- [Evidence Verification](../15-orchestration/evidence-verification.md) — verifies change evidence; this skill requires dated evidence for quality claims.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial evidence-backed skill-quality evaluation contract |
