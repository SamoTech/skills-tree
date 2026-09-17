# Universal Implementation Contract

## Purpose

An **Implementation** is a concrete realization of a canonical Skill using one or more models, APIs, libraries, tools, runtimes, or services.

Implementation is intentionally separate from Skill, Tool, Platform, Framework, Model, and Adapter.

## Contract

Each Implementation record MUST have:

- `id` — stable unique identifier.
- `version` — implementation contract/data version.
- `name` — human-readable name.
- `skill` — canonical Skill ID implemented by this record.
- `type` — implementation class such as `library`, `api`, `service`, `tool`, `runtime`, or `composite`.
- `provider` — provider/maintainer identity where known.
- `interface` — concrete invocation/interface mechanism.
- `inputs` — accepted input contract.
- `outputs` — produced output contract.
- `requirements` — required models, tools, runtime features, credentials, or environment constraints.
- `constraints` — known compatibility or operational constraints.
- `limitations` — known functional limitations and failure boundaries.
- `provenance` — source paths or authoritative sources supporting the record.
- `evidence` — references to validated evidence when available.
- `status` — lifecycle state such as `candidate`, `verified`, `deprecated`, or `experimental`.

## Required semantics

### Skill linkage

`skill` MUST resolve to a canonical Skill in the universal registry. An Implementation cannot redefine the canonical skill taxonomy.

### Versioning

Implementation version identifies the registry record/implementation contract state. A provider's software/model version may additionally be represented in requirements or evidence where the schema supports it. Do not collapse provider version and registry record version.

### Interface

The interface must describe how the implementation is actually invoked or integrated, for example HTTP API, Python library, CLI, MCP tool, SDK, or local runtime.

### Requirements

Requirements describe dependencies needed to execute the implementation. They are not compatibility claims by themselves.

### Constraints and limitations

Constraints explain when the implementation is not eligible or has reduced applicability. Limitations describe known functional boundaries and failure modes.

### Provenance and evidence

Provenance establishes where the registry record came from. Evidence supports claims about behavior, compatibility, quality, or operational status. A source mention without supporting evidence must not be upgraded into a verified compatibility claim.

## Lifecycle

```text
candidate → verified → deprecated
      \→ experimental
```

`candidate` means the repository has identified a concrete implementation but has not completed validation. `verified` means the claims represented by the record have passed the repository's applicable validation/evidence gates. `experimental` means the implementation is intentionally usable for exploration but evidence is incomplete. `deprecated` means it should not be selected for new recommendations unless explicitly requested.

## Separation rules

- A Skill describes **what/how** capability is performed at the canonical knowledge level.
- An Implementation describes **a concrete realization** of that Skill.
- A Tool is an executable dependency or interface consumed by an Implementation.
- A Model is a model entity required or used by an Implementation.
- A Platform is an execution/hosting environment.
- A Framework is a software construction/orchestration environment.
- An Adapter maps an Implementation into a target ecosystem.

Do not create an Implementation record solely because a framework, model, platform, protocol, or documentation page mentions a capability.

## Validation requirements

Before an Implementation becomes `verified`, validate at minimum:

1. `skill` exists and is canonical.
2. All referenced entity IDs resolve.
3. Interface behavior is supported by executable evidence where applicable.
4. Inputs and outputs are consistent with the actual implementation boundary.
5. Requirements, constraints, and limitations are not invented.
6. Provenance sources exist and are traceable.
7. Evidence supports any compatibility or quality claims.
8. Registry serialization is schema-valid and deterministic.

## Registry example

```json
{
  "id": "implementation/example-web-search",
  "version": "1",
  "name": "Example Web Search Implementation",
  "skill": "11-web/web-search",
  "type": "api",
  "provider": "example-provider",
  "interface": "https",
  "inputs": ["query"],
  "outputs": ["search_results"],
  "requirements": [],
  "constraints": [],
  "limitations": [],
  "provenance": ["docs/example.md"],
  "evidence": [],
  "status": "candidate"
}
```

This is a structural example only. It is not evidence for a real provider and MUST NOT be inserted into the production registry as a real implementation.

## Acceptance criteria

The contract is complete when the schema can represent a real implementation without conflating it with a framework, platform, model, tool, or adapter, and when tests can validate references, provenance, status, and deterministic serialization.
