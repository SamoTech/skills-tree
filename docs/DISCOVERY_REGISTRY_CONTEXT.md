# Machine-Readable Discovery Registry Context

The canonical skill source remains skills/. docs/api/skills.json remains a generated projection and is not an independently maintained catalog.

For skills that are explicitly registered in registry/universal_registry.json, the export includes an optional registry_context object containing:

- canonical registry ID and version;
- canonical flag;
- linked capability IDs;
- linked implementation IDs;
- evidence IDs derived from Evidence.supports;
- the registry-declared provenance;
- declared freshness when present.

Unregistered canonical skills do not receive synthetic context. The exporter does not infer registry membership, evidence, freshness, compatibility, trust, quality, or production status.

The search projection remains a search corpus and does not become a second registry catalog. CLI search consumes its deterministic lexical fields and does not depend on registry_context.

This boundary is intentionally partial because the UniversalRegistry currently contains only a small verified set of skill records. Increasing registry coverage is a separate evidence-driven task; the discovery projection must not manufacture context for uncovered skills.
