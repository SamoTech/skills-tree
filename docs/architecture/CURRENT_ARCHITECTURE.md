# Current Architecture

This document describes the implementation observed at the 2026-09-17 audit baseline and the first incremental universal-registry runtime slice.

## Runtime layers

```text
Canonical sources
  meta/GOAL_TAXONOMY.md
  meta/skill-schema.json
  meta/frameworks.md
  data/SKILLS_GRAPH.json
  benchmarks/INDEX.json

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

The registry now has a small machine-readable seed containing real repository-backed Goals, Capabilities, and canonical Skills. `registry/runtime.py` provides a read-only deterministic facade for Goal → Capability → Skill resolution and rejects duplicate IDs, missing universal metadata, non-canonical skills, and dangling references.

This is intentionally an additive compatibility layer. Existing skill files, graph generation, recommendation behavior, API contracts, and MCP contracts remain unchanged.

Implementations, Tools, Models, Platforms, Frameworks, Adapters, Evidence, Benchmarks, and Architectures are present as empty typed collections in the seed until audited source records can be introduced. Empty is preferred to invented compatibility claims.

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

The universal registry runtime is not yet inserted into this production recommendation path. That integration is deferred until the registry records have equivalent coverage and contract tests.

## Blueprint execution

BlueprintGenerator consumes the recommendation result and taxonomy. Architecture selection is still primarily driven by goal-category mappings. The universal capability graph is not yet the primary architecture path.

## Remaining P1 gaps

- Promote Capability from taxonomy-derived data to authoritative registry data without creating divergent mappings.
- Introduce first audited Implementation and Adapter records with provenance.
- Add typed cross-entity graph edges and deterministic generation rules.
- Add registry-backed eligibility and compatibility filtering before recommendation ranking.
- Define versioned evidence and benchmark records.
- Introduce a machine-readable universal architecture output contract.

## Migration constraint

Do not bulk-migrate the existing skill corpus or introduce platform-specific duplicate skills until the universal entity contract, typed graph relationships, provenance rules, and compatibility semantics have behavioral coverage.
