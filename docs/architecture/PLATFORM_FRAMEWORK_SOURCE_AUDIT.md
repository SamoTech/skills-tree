# Platform / Framework / Model Source Audit

## Purpose

This audit establishes the repository-backed source map for Platform, Framework, Model, Protocol, and Runtime/Ecosystem entities before any universal registry records are created.

The objective is classification and provenance, not data population. Existing references are not treated as verified compatibility merely because they appear in documentation.

## Architectural rule

Skills Tree keeps the canonical skill taxonomy platform-agnostic. Platform, Framework, Model, Protocol, and Runtime are independent entities that can participate in compatibility relationships. A mention of one entity does not imply that another entity supports it.

The universal registry currently has dedicated collections for platforms, frameworks, models, adapters, implementations, and tools. Those collections remain intentionally empty until repository evidence is strong enough to support individual records.

## Primary sources reviewed

| Source | Current role | Entity candidates | Evidence quality | Migration risk |
|---|---|---|---|---|
| `meta/frameworks.md` | Curated reference table | Framework, Platform, Model, Protocol | Reference/curation; heterogeneous | High if imported without classification |
| `docs/PROJECT_GOAL.md` | Canonical project intent | Platform, Framework, Model, Adapter | Architectural definition | Low; normative rather than compatibility evidence |
| `meta/PLATFORM_ASCENSION_FINAL.md` | Strategic architecture and distribution plan | Platform, Framework, Model, Runtime | Strategic/reference | Medium; contains strategic claims that are not registry evidence |
| `meta/OS_MASTER_PLAN.md` | Historical/strategic planning | Framework, Model, platform ecosystem | Strategic/reference | Medium |
| `intelligence/ontology/capability_ontology.json` | Capability ontology | Framework and Model requirement references | Structured but requirement-oriented | Medium; references are not necessarily entity records |
| `docs/architecture/CURRENT_ARCHITECTURE.md` | Current implementation architecture | Runtime/interface boundaries | Architecture evidence | Low |
| `docs/architecture/TARGET_ARCHITECTURE.md` | Target architecture | Platform, Framework, Model, Adapter | Design intent | Medium; target state is not current-state evidence |
| `meta/universal-registry.schema.json` | Canonical entity contract | Platform, Framework, Model, Adapter | Normative schema | Low |
| `registry/universal_registry.json` | Canonical registry data | Platform, Framework, Model | Current registry state | Low; intentionally unpopulated for these collections |
| `mcp/server.py` / `mcp/tools.py` | Executable integration surface | MCP Protocol, Runtime/Integration | Executable evidence for this repository's MCP boundary | Low for boundary classification; insufficient for broad host compatibility |
| `meta/MCP_REAL_WORLD_VALIDATION.md` | MCP validation evidence candidate | MCP ecosystem | Evidence candidate | Medium; freshness and methodology must be checked before compatibility claims |

## Findings

### 1. `meta/frameworks.md` is not a canonical entity registry

The file contains multiple conceptual classes in one document: agent frameworks, computer-use/browser systems, interoperability standards, and foundation models. It is useful as a discovery source, but its rows must not be copied directly into universal registry collections.

Examples include framework entries such as LangChain, LangGraph, LlamaIndex, AutoGen, CrewAI, OpenAI Agents SDK, Semantic Kernel, Mastra, Haystack, Rasa, and others; protocol entries such as MCP and A2A; and model entries such as GPT, Claude, Gemini, Llama, Mistral, DeepSeek, Qwen, and others.

The current document also states that it is a curated reference and is dated April 2026. That makes freshness a registry concern for every imported record.

### 2. Framework is distinct from Platform

A Framework is a software development/orchestration abstraction used to build agent systems. A Platform is an execution, hosting, model-service, or managed agent environment. The registry must not infer one from the other.

For example, an entry appearing in the framework table is not automatically a platform, and a cloud/provider entry is not automatically a framework. Classification must follow the entity contract and repository evidence.

### 3. Model is a distinct entity

A model identifies a model family/version or model endpoint where the repository has sufficient evidence. Model references in capability ontology requirements or framework tables are not themselves proof of model capability, compatibility, performance, or current availability.

Model records must eventually carry version/provenance and should avoid embedding subjective quality claims as compatibility facts.

### 4. Protocol is distinct from Framework and Platform

The repository explicitly documents MCP and other interoperability standards alongside frameworks and models. These should not be forced into the Framework or Platform collections.

MCP is also an executable integration surface in this repository. Its protocol identity should remain separate from the repository's MCP server implementation and from any future Adapter record.

### 5. Runtime / ecosystem should not be silently collapsed into Platform

The architecture uses runtime/deployment environment as a constraint. A runtime can be a compatibility dimension without being equivalent to a cloud platform, framework, or model provider. The registry should only introduce a separate Runtime/Ecosystem entity if the contract requires it and repository evidence supports it.

Until then, runtime requirements should remain explicit fields/constraints rather than being invented as entity records.

## Classification rules for migration

A candidate may be promoted only when its type is unambiguous and its source is traceable.

### Framework

Required evidence should establish that the candidate is a software framework/SDK used to construct or orchestrate agent behavior. Record the canonical source and version where available.

### Platform

Required evidence should establish an execution, hosting, managed-agent, model-service, or deployment platform role. Do not classify a provider, website, or model catalog as a platform without supporting evidence.

### Model

Required evidence should identify the actual model family/version or service model identifier. Do not treat a provider name alone as a model.

### Protocol

Required evidence should establish an interoperability or communication specification. Protocols must remain separate from implementations and adapters.

### Runtime / Ecosystem

Use only when the entity has an execution/runtime role that cannot be represented correctly by Platform or Framework. Do not create this category solely to accommodate ambiguous source rows.

## Compatibility evidence boundary

The following claims must not be inferred from the presence of a name in `meta/frameworks.md`:

- Framework supports a specific Skill.
- Platform supports a specific Framework.
- Model supports a specific Skill.
- Model is compatible with a Framework.
- Adapter exists for a Framework or Platform.
- A protocol implementation is production-ready.
- A model has a particular benchmark or reliability result.

Those claims require executable evidence, official documentation, benchmark evidence, or another explicitly classified evidence source.

## Initial migration inventory

The first migration pass should use a small audited subset rather than importing the entire reference file.

Recommended order:

1. Select one framework with strong repository/runtime evidence.
2. Select one platform or execution environment with strong evidence.
3. Select one model with explicit model/version evidence.
4. Keep MCP as a Protocol entity, separately from the MCP server implementation.
5. Attach provenance to every record.
6. Add compatibility relationships only after evidence validation.

No provider/framework/model should be registered merely because it is popular, listed in a planning document, or linked from a markdown table.

## Relationship constraints

The eventual graph should preserve typed relationships such as:

```text
Skill --IMPLEMENTED_BY--> Implementation
Implementation --ADAPTED_BY--> Adapter
Adapter --TARGETS--> Framework
Adapter --TARGETS--> Platform
Implementation --REQUIRES--> Runtime/Tool/Model where explicitly supported
Framework --RUNS_ON--> Platform where verified
Model --SUPPORTED_BY--> Platform where verified
```

Relationship names must come from the universal registry relationship vocabulary. No free-form relationship strings should be introduced during migration.

## Current registry decision

No Platform, Framework, Model, Protocol, or Runtime records are added by this audit.

The audit establishes that the repository contains usable discovery sources but that those sources have different evidence strengths and mixed entity types. The next step is to formalize the Implementation contract before registering concrete implementations, followed by the Adapter contract.

## Acceptance criteria

- [x] `meta/frameworks.md` reviewed as a heterogeneous source rather than a canonical registry.
- [x] Framework, Platform, Model, Protocol, and Runtime/Ecosystem distinctions documented.
- [x] Existing repository sources mapped with provenance and evidence boundaries.
- [x] Compatibility claims explicitly separated from simple references.
- [x] No unverified registry records created.
- [x] Migration risk and recommended first vertical slice documented.

## Next

P1.4 — Implementation Contract.

After the Implementation contract is merged, define P1.5 — Adapter Contract, then register the first audited concrete implementation and adapter with real evidence and tests.