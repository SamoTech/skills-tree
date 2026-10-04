# Agent Skills Distribution Contract

## Purpose

Skills Tree is a public, trusted, machine-discoverable source of AI skills. AI agents should be able to find the right skill here, and humans should be able to discover, understand, use, share, and contribute skills easily.

The repository is the canonical source for the project's AI-agent skill registry. The repository must support two distinct consumption modes without creating competing sources of truth:

1. GitHub-native consumption from the repository.
2. Web distribution through a machine-readable registry and, in the next distribution phase, the Agent Skills discovery format.

## Canonical source

The authoritative skill content remains under `skills/`.

The generated registry at `docs/api/skills.json` is a machine-readable projection of that source. It must never become an independently edited catalog.

The repository's governance documents remain authoritative for repository operation; skill content remains authoritative for the capability definitions.

## Distribution target

The project will expose standards-compatible Agent Skills as:

```
agent-skills/
└── <skill-name>/
    └── SKILL.md
```

Each distributed `SKILL.md` must contain at least:

```yaml
---
name: skill-name
description: What the skill does and when an agent should use it.
---
```

The body contains the agent instructions. Supporting scripts, references, or assets are optional and must remain inside the skill's package.

This packaging layer is a compatibility projection. It must not replace the canonical `skills/<category>/<skill>.md` registry until a deliberate schema migration is approved.

## GitHub distribution

GitHub is already a first-class source because the repository contains version-controlled skill content. GitHub's current `gh skill` tooling discovers Agent Skills using the `skills/*/SKILL.md` convention and can install a specific skill from a repository at a pinned tag or commit.

Until the compatibility projection is complete, users must treat the legacy registry files as repository content rather than claiming that every legacy file is already a standards-compliant `SKILL.md`.

## Web distribution

The public machine-readable registry is:

`https://raw.githubusercontent.com/SamoTech/skills-tree/main/docs/api/skills.json`

The web distribution roadmap is:

1. Generate standards-compatible `SKILL.md` packages from the canonical registry.
2. Generate a discovery index at `/.well-known/agent-skills/index.json`.
3. Compute a SHA-256 digest for every published artifact.
4. Verify generated artifacts against the index in CI.
5. Publish the index and artifacts from the same build output.
6. Never hand-edit the discovery index or its digests.

The discovery index follows the current v0.2.0 shape: `$schema`, `skills[]`, `name`, `type`, `description`, `url`, and `digest`.

## Trust model

A skill is not trusted merely because it is present in this repository.

The repository quality state describes evidence about the content. Consumers must still review skills that:

- execute shell commands;
- install packages;
- access files, networks, credentials, or external services;
- change infrastructure;
- perform destructive actions;
- instruct an agent to weaken security controls.

External implementations are references, not implicit dependencies.

## Versioning and integrity

Every published skill must be traceable to:

- the canonical repository path;
- the skill version;
- the source commit or release;
- the generated artifact digest.

For high-risk skills, distribution must prefer immutable release/tag/commit references over floating branches.

## Completion gate

A distribution change is not complete until:

- canonical source is valid;
- generated registry is synchronized;
- standards-compatible artifacts validate;
- discovery index validates;
- every digest matches the served bytes;
- security scanning passes;
- documentation and current-state records are updated.

## Current state

The current generated quality report verifies 374 registry skill files: 202 battle-tested, 159 enriched, 13 stubs, and 0 invalid. The separate Agent Skills reconciliation baseline is 375 canonical entries, 258 eligible, 117 blocked, and 296 Agent Skills packages. Category-level classification is authoritative in `meta/QUALITY-REPORT.md`.

The standards-compatible distribution layer is intentionally being introduced as a separate projection so the existing corpus can be migrated incrementally without corrupting the canonical registry.


## Stub migration gate

Legacy stubs are migrated incrementally; the current count is authoritative only in the generated quality report. A migrated skill must satisfy all of these before it is treated as a completed migration:

1. The canonical `skills/<category>/<skill>.md` entry has a non-placeholder description and a real runnable example.
2. Inputs/outputs and failure modes are explicit.
3. Evidence references identify primary or authoritative documentation for the implementation claims.
4. Security-sensitive behavior is bounded and documented; credentials, private endpoints, and hard-coded secrets are prohibited.
5. A standards-compatible `agent-skills/<skill-name>/SKILL.md` package is generated from the canonical entry.
6. The package passes `tools/validate_agent_skills.py`.
7. Benchmark claims are not upgraded to "battle-tested" unless reproducible benchmark evidence exists. Documentation references alone are evidence for implementation guidance, not performance claims.
8. Migration batches are independently reviewable and rollback-safe; a failed batch does not justify lowering the gate for later batches.

The compatibility package is a projection of the canonical entry. It does not become an independently authored source of truth.
\n\n## Verified projection baseline — 2026-10-04

PR #305 merged the reconciliation hardening gate to `main` as `a9a649481c68bf0dd33447a2238174ebd8b79a4b`. The current audit scans 375 canonical entries, with 258 eligible and 117 blocked. The Agent Skills projection contains 296 packages: 258 deterministic eligible projections, 37 retained blocked packages, one intentional auxiliary package, and one legacy compatibility package. Reconciliation now runs as a hard read-only CI invariant.

The repository has a verified deterministic Agent Skills projection and reconciliation mechanism, but `/.well-known/agent-skills/index.json` is not live. Publication remains gated on generation from the same verified build output, provenance and reproducibility validation, digest-to-served-byte verification, and end-to-end publication verification.\n