---
title: "Hypothesis Generation"
category: 02-reasoning
level: advanced
stability: stable
version: v3
description: "Generate multiple testable explanations for an observation, compare them using stated evidence, and identify discriminating checks."
added: "2025-03"
related: [abductive, causal, inductive-reasoning]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-hypothesis-generation.json)

# Hypothesis Generation

**Category:** `reasoning`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Generate multiple testable explanations for an observation, compare them using stated evidence, and identify discriminating checks. Hypotheses are candidates, not conclusions: each one states what evidence supports it and what observation would refute it.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | observation | object | The observed facts, separated from interpretation |
| Input | constraints | list of string | Known boundaries (domain, resources, timeline) that candidates must respect |
| Output | hypotheses | list of object | Ranked candidates, each with supporting evidence and a discriminating check |
| Output | next_evidence | list of string | The observations that would best separate the top candidates |

### Procedure
1. State the observation and explicitly separate observed facts from interpretation.
2. Generate at least three distinct candidate explanations; no single-cause commitment.
3. For each candidate, list the evidence that supports it and the assumptions it requires.
4. Define a discriminating check for each leading candidate: the observation that would refute it.
5. Rank the candidates and report the next evidence to collect, not a verdict.

### Example

```python
observation = {"fact": "API error rate spiked at 14:00", "interpretation_free": True}
hypotheses = [
    {"id": "H1", "claim": "13:58 deployment introduced a regression",
     "discriminating_check": "deploy log diff + error fingerprint match"},
    {"id": "H2", "claim": "upstream provider outage",
     "discriminating_check": "provider status page + direct probe"},
    {"id": "H3", "claim": "traffic surge exceeded rate limits",
     "discriminating_check": "request-rate graph vs limit"},
]
assert len(hypotheses) >= 3, "single-cause commitment is a failure mode"
assert all(h["discriminating_check"] for h in hypotheses), "each candidate needs a refuting check"
print({"observation": observation["fact"], "candidates": [h["id"] for h in hypotheses],
       "next": "run discriminating checks before concluding"})
```

### Related Skills

- [Abductive Reasoning](abductive.md) - inference to the best explanation
- [Causal Reasoning](causal.md) - cause-effect analysis
- [Inductive Reasoning](inductive-reasoning.md) - generalization with sample limits

## Failure Modes

- Generating a single explanation and defending it instead of comparing candidates.
- Hypotheses without discriminating checks, so no evidence could ever refute them.
- Interpretation smuggled into the observation, biasing all candidates the same way.
- Resource explosion: unbounded candidate counts or unbounded evidence collection.
- Treating a plausible hypothesis as a conclusion without running the discriminating check.

## Changelog
- v3 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links.
- v2 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
