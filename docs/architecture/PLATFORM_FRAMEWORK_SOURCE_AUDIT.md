# Platform / Framework / Model Source Audit

This audit inventories repository-backed sources for Platform, Framework, Model, Protocol, and Runtime/Ecosystem entities before universal registry records are created. It is a classification/provenance step, not data population.

## Architectural rule

Skills Tree keeps the canonical skill taxonomy platform-agnostic. Platform, Framework, Model, Protocol, and Runtime are distinct concepts. A reference to one does not imply compatibility with another.

The universal registry has dedicated collections for platforms, frameworks, models, adapters, implementations, and tools. These collections remain intentionally empty until evidence supports individual records.

## Primary sources

| Source | Role | Candidates | Evidence quality | Migration risk |
|---|---|---|---|---|
| `meta/frameworks.md` | Curated reference table | Framework, Platform, Model, Protocol | Heterogeneous reference/curation | High if imported without classification |
| `docs/PROJECT_GOAL.md` | Canonical project intent | Platform, Framework, Model, Adapter | Architectural definition | Low; normative, not compatibility evidence |
| `meta/PLATFORM_ASCENSION_FINAL.md` | Strategic architecture | Platform, Framework, Model, Runtime | Strategic/reference | Medium |
| `meta/OS_MASTER_PLAN.md` | Historical/strategic planning | Framework, Model, platform ecosystem | Strategic/reference | Medium |
| `intelligence/ontology/capability_ontology.json` | Capability ontology | Framework and Model requirements | Structured requirements | Medium; references are not entity records |
| `docs/architecture/CURRENT_ARCHITECTURE.md` | Current implementation architecture | Runtime/interface boundaries | Architecture evidence | Low |
| `docs/architecture/TARGET_ARCHITECTURE.md` | Target architecture | Platform, Framework, Model, Adapter | Design intent | Medium |
| `meta/universal-registry.schema.json` | Canonical registry contract | Platform, Framework, Model, Adapter | Normative schema | Low |
| `registry/universal_registry.json` | Canonical registry data | Platform, Framework, Model | Current state | Low; collections intentionally unpopulated |
| `mcp/server.py` / `mcp/tools.py` | Executable integration | MCP Protocol, runtime/integration | Executable repository evidence | Low for boundary classification; insufficient for broad host compatibility |
| `meta/MCP_REAL_WORLD_VALIDATION.md` | Validation evidence candidate | MCP ecosystem | Evidence candidate | Medium; freshness/methodology required |

## Findings

### `meta/frameworks.md` is not a canonical entity registry

The file contains multiple conceptual classes: agent frameworks, computer-use/browser systems, interoperability standards, and foundation models. It is a discovery source, not a registry. Rows must be classified before migration.

The file is also dated April 2026, so freshness must be treated as a registry concern for every imported record.

### Framework is distinct from Platform

A Framework is a software framework or SDK used to construct/orchestrate agent behavior. A Platform is an execution, hosting, model-service, managed-agent, or deployment environment. The registry must not infer one from the other.

### Model is distinct

A Model identifies a model family/version or model endpoint where evidence is sufficient. A model reference does not prove capability, compatibility, performance, or current availability.

### Protocol is distinct

MCP and other interoperability standards must not be forced into Framework or Platform collections. MCP's protocol identity is separate from this repository's MCP implementation and any future Adapter record.

### Runtime/Ecosystem is distinct

Runtime/deployment environment is a compatibility dimension but is not automatically a Platform or Framework. Do not invent a separate Runtime entity solely to accommodate ambiguous references.

## Migration rules

A candidate may be promoted only when its type is unambiguous and its source is traceable.

- Framework: evidence establishes a software framework/SDK role.
- Platform: evidence establishes execution, hosting, managed-agent, model-service, or deployment role.
- Model: evidence identifies the actual model family/version or service model identifier.
- Protocol: evidence establishes an interoperability or communication specification.
- Runtime/Ecosystem: use only where the execution role cannot be represented correctly by another supported entity type.

## Compatibility evidence boundary

The presence of a name in `meta/frameworks.md` must not be used to infer:

- Framework supports a specific Skill.
- Platform supports a specific Framework.
- Model supports a specific Skill.
- Model is compatible with a Framework.
- An Adapter exists.
- A protocol implementation is production-ready.
- A model has a benchmark or reliability result.

Those claims require executable evidence, official documentation, benchmark evidence, or another explicitly classified evidence source.

## Initial migration inventory

Use a small audited subset rather than importing the entire reference file:

1. One framework with strong repository/runtime evidence.
2. One platform or execution environment with strong evidence.
3. One model with explicit model/version evidence.
4. Keep MCP as a Protocol, separate from the MCP server implementation.
5. Attach provenance to every record.
6. Add compatibility relationships only after evidence validation.

## Relationship constraints

The eventual graph should use typed relationships only, for example:

```text
Skill --IMPLEMENTED_BY--> Implementation
Implementation --ADAPTED_BY--> Adapter
Adapter --TARGETS--> Framework
Adapter --TARGETS--> Platform
Implementation --REQUIRES--> Runtime/Tool/Model
Framework --RUNS_ON--> Platform
Model --SUPPORTED_BY--> Platform
```

Relationship names must come from the universal registry relationship vocabulary. No free-form relationship strings should be introduced during migration.

## Current registry decision

No Platform, Framework, Model, Protocol, or Runtime records are added by this audit. Existing discovery sources have different evidence strengths and mixed entity types. The next step is to formalize the Implementation contract, followed by the Adapter contract.

## Acceptance criteria

- [x] Major sources reviewed.
- [x] Heterogeneous source categories classified.
- [x] Canonical versus contextual sources distinguished.
- [x] Provenance and evidence boundaries documented.
- [x] No unverified registry records created.
- [x] Migration risks documented.

## Next

P1.4 — Implementation Contract.

After the Implementation contract is merged, define P1.5 — Adapter Contract, then register the first audited concrete implementation and adapter with real evidence and tests.
