# Current Architecture

This document describes the verified implementation baseline as of 2026-10-03. Historical audit sections remain historical; the runtime and consumer boundaries below describe the current architecture.

## Runtime layers

```text
Canonical sources
  meta/GOAL_TAXONOMY.md
  meta/skill-schema.json
  meta/frameworks.md
  data/SKILLS_GRAPH.json
  benchmarks/INDEX.json
  docs/api/skills.json (generated discovery projection)

Universal registry boundary
  meta/universal-registry.schema.json
  registry/universal_registry.json
  registry/runtime.py

Core implementation
  tools/architect.py
    GoalTaxonomyParser / RuntimeGoalTaxonomyParser
    SkillsGraph
    EvidenceDeriver
    ExplanationEngine
    SkillScorer
    RecommendationEngine
    BlueprintGenerator
  tools/ranking_calibrator.py

Transport
  api/main.py
  api/routes/*
  api/models.py
  mcp/tools.py
  cli/main.py
```

## Universal registry runtime slice

The registry now has a machine-readable seed containing repository-backed Goals, Capabilities, canonical Skills, audited Implementation/Adapter records, Evidence, Compatibility, Freshness metadata, and Benchmark definitions. `registry/runtime.py` provides a read-only deterministic facade for Goal → Capability → Skill resolution and rejects duplicate IDs, missing universal metadata, non-canonical skills, and dangling references.

The registry is a read-only deterministic runtime boundary. It now validates registry data, provenance/evidence links, freshness metadata, implementation/adapter contracts, benchmark definitions, compatibility facts, and the supported Universal Graph relationships. Unsupported graph relationships fail closed.

The runtime contains audited records only where repository evidence exists. Empty or absent evidence is preserved as such rather than inferred.

## Recommendation execution

1. Taxonomy resolves a goal string to a goal ID.
2. Taxonomy returns mapped skills.
3. RecommendationEngine splits skills by priority.
4. SkillsGraph supplies node metadata and dependency/learning-path information.
5. SkillScorer computes recommendation components.
6. EvidenceDeriver derives benchmark/goal/dependency/framework evidence.
7. ExplanationEngine derives explanation text from score components and evidence.
8. RecommendationEngine aggregates confidence and returns the recommendation payload.
9. API applies the ranking calibration boundary and converts the result to Pydantic summaries.

The universal registry runtime is not yet inserted into this production recommendation path. The new eligibility engine is a standalone pre-ranking boundary and does not alter existing recommendation behavior; integration remains deferred until the registry records have equivalent coverage and contract tests.

## Blueprint execution

BlueprintGenerator consumes the recommendation result and taxonomy. Architecture selection remains primarily driven by goal-category mappings. The blueprint API now propagates additive registry_context onto required and optional skill entries after generation. This context is descriptive and does not change architecture selection or ranking.

## Remaining architecture gaps

- Complete the transition from taxonomy-backed recommendation inputs to broader authoritative registry consumption without creating divergent mappings.
- Expand registry-backed consumer coverage beyond recommendation and blueprint context, especially generated machine-readable discovery/search surfaces.
- Increase evidence-backed Implementation/Adapter coverage without inferring unsupported claims.
- Define a machine-readable universal architecture output contract.
- Keep deferred graph relationships outside the trusted runtime boundary until deterministic semantics and behavioral tests exist.

## Migration constraint

Do not bulk-migrate the existing skill corpus or introduce platform-specific duplicate skills until the universal entity contract, typed graph relationships, provenance rules, and compatibility semantics have behavioral coverage.


## Eligibility execution

P1.9 adds `registry/eligibility.py` as a deterministic pre-ranking filter. It evaluates registered candidate IDs against an optional typed execution target and consumes evidence-backed compatibility facts. Compatible facts permit eligibility, conditional facts produce a conditional result, and incompatible, deprecated, unknown, or missing compatibility evidence prevent eligibility. The engine does not assign ranking scores or mutate registry data. Prerequisite evaluation remains limited until authoritative prerequisite records are available.
