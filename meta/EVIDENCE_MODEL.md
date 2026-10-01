# Evidence and Lifecycle Model

> Authoritative model for capability evidence, lifecycle, provenance, and freshness.

## Evidence tiers

| Tier | Meaning | Typical evidence |
|---|---|---|
| E0 | Unverified | proposal, hypothesis, incomplete source |
| E1 | Documented | clear contract, scope, inputs/outputs, limitations |
| E2 | Validated | automated schema/structural/behavioral checks |
| E3 | Reproducible | repeatable implementation or evaluation |
| E4 | Empirically Evaluated | controlled benchmark with recorded methodology/results |
| E5 | Ecosystem Evidence | documented external integration, usage, or adoption evidence |

Evidence tiers are descriptive. They are not a universal quality score.

A higher tier does not automatically mean a capability is appropriate for every use case.

## Evidence rules

- Every non-trivial claim should be traceable to evidence.
- Repository existence is not adoption evidence.
- Automated validation is not production evidence.
- Classifier labels are not benchmark results.
- Documentation references establish implementation guidance, not performance.
- External adoption claims require identifiable public evidence.
- Evidence must retain source, date, scope, and verification status where available.
- Unsupported claims must be removed or downgraded rather than hidden.

## Lifecycle

```
proposed
  ↓
documented
  ↓
validated
  ↓
enriched
  ↓
evaluated
  ↓
maintained
  ↓
deprecated
  ↓
archived
```

Not every capability must reach every state. Experimental or niche capabilities may remain at an earlier state when that is the accurate representation.

## Provenance

Meaningful transformations should record:

- canonical source path
- source revision/commit where relevant
- transformation tool/version where relevant
- evidence references
- verification date
- generated artifact digest where published

Generated projections must be reproducible from canonical sources.

## Freshness

Where external facts, dependencies, APIs, or frameworks materially affect a skill, record:

- last reviewed
- review due
- freshness basis
- known stale conditions

Staleness is a maintenance state, not an implicit quality failure.

## Security evidence

Security-sensitive skills must identify relevant:

- authority boundary
- credential/secret boundary
- network boundary
- destructive-action boundary
- data sensitivity
- validation/postcondition requirements

Security validation does not mean a skill is universally secure.

## Compatibility evidence

Compatibility is recorded only when supported by documentation, tests, or reproducible integration evidence. Conceptual similarity is not interoperability.

## Migration gate

A migration is complete only when the canonical skill, required projection, evidence boundary, validation, and documentation agree. Frontmatter-only edits are not migrations.

## Machine-readable evolution

The existing schema remains authoritative for current compatibility. New evidence/lifecycle fields should be introduced incrementally with schema versioning and fixtures rather than forcing an unsafe corpus-wide rewrite.
