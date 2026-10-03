# Consumer Runtime Audit — 2026-10-03

## Mission

Audit the live Universal Registry consumer surface after the benchmark, anti-slop, freshness, graph-integrity, provenance/evidence, and documentation-synchronization slices.

## Verified finding

The Universal Registry is already consumed by the recommendation path through RegistryRecommendationEngine and EligibilityEngine. Registered candidates can therefore be filtered by evidence-backed compatibility before legacy ranking.

The consumer boundary was incomplete: the recommendation API did not expose the registry context that justified or constrained a registered skill. A consumer receiving a recommendation had to perform a second implicit registry lookup to inspect canonical provenance, registry evidence, freshness, or registered implementations.

## Implemented slice

The recommendation response now carries an additive registry_context for registered canonical skills.

The context contains:
- canonical_id
- version
- canonical flag
- repository provenance
- explicitly registered evidence references and sources
- declared freshness when present
- registered implementation IDs

The context is descriptive. It does not create a trust score, ranking score, production-readiness claim, or inferred evidence.

Unregistered legacy recommendation entries may retain a null registry_context. This preserves backward compatibility and makes registry coverage visible rather than fabricating coverage.

## Invariants

1. Registry context is derived only from UniversalRegistry runtime records.
2. Evidence is returned only when the registry explicitly links it to the skill.
3. Missing evidence remains an empty list.
4. Freshness is returned only when declared by the registry.
5. Canonical identity is resolved through the existing registry normalization boundary.
6. Existing recommendation ranking and calibration remain authoritative.
7. The new context is additive to the API contract.

## Validation

Required validation:
- API response-shape regression coverage.
- Registry context must be present for at least one registered recommendation.
- Provenance source must be present.
- Evidence must remain a list and cannot be fabricated.
- Full repository CI/security/build gates must pass at the exact PR HEAD.

## Remaining gap

The next evidence-backed consumer audit should inspect BlueprintGenerator and other machine-readable discovery surfaces for equivalent registry-context propagation. No trust ranking should be introduced merely to make the context look more complete.

## Source of truth

- registry/runtime.py
- registry/recommendation.py
- api/routes/recommend.py
- api/models.py
- meta/EVIDENCE_MODEL.md
- docs/architecture/CURRENT_ARCHITECTURE.md
