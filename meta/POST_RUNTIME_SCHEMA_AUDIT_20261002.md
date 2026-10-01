# Universal Registry Runtime Data-Schema Audit — 2026-10-02

## Finding

The UniversalRegistry runtime loaded `registry/universal_registry.json` and performed semantic integrity, entity-specific contract, evidence, compatibility, and graph validation, but lacked a structural schema boundary for the loaded registry document.

The repository already contained `meta/universal-registry.schema.json`, but that schema defines the universal registry ontology/contract vocabulary: its required top-level fields are `schema_version`, `entity_types`, and `relationship_types`. The actual serialized registry uses `registry_version` and `entities`. Therefore that schema must not be used as the instance schema for the seed.

## Selected slice

Introduce `meta/universal-registry-data.schema.json` as the normative instance schema and validate it immediately after JSON load.

The data schema covers:
- registry version and entity collections
- common entity identity/version/provenance shape
- Goal, Capability, and Skill structures
- Evidence and Compatibility structures
- Implementation and Adapter structures through their dedicated contracts

The runtime resolves cross-schema resources locally with `referencing.Registry`. No network fetch is required during validation.

## Validation responsibilities

Structural schema validation handles data shape and field types.

Existing semantic validation remains responsible for:
- traceable provenance source requirements
- reference integrity and symmetry
- evidence support relationships
- compatibility semantics
- graph relationships
- entity-specific contract rules

This separation preserves established error behavior and avoids duplicating semantic policy in the data schema.

## Verification

PR #241 final head: `8ad05dfc995db49da847ea479e06e13bec80d2e1`

- Security Scan: passed
- PR Checks: passed
- Test Suite: passed on Python 3.11, 3.12, and 3.13
- Build & Verify Wheel: passed
- Auto Label: passed
- Dependabot Review Gate: skipped
- Merge commit: `93c50c3616a7c558b483f341f44a91509ed032ca`

## Outcome

The UniversalRegistry now has an explicit structural validation boundary for its canonical serialized seed without changing registry records or ontology claims.

Next work must come from a fresh runtime/consumer invariant audit. No numbered P2.3 requirement is introduced.
