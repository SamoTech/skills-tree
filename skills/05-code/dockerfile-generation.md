---
title: "Dockerfile Generation"
category: 05-code
level: advanced
stability: stable
version: v2
description: "Generate maintainable Dockerfiles from application runtime requirements, build inputs, security constraints, and deployment targets."
added: "2026-09"
related: [dependency-management, code-execution-sandbox, documentation-generation]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-dockerfile-generation.json)

# Dockerfile Generation

**Category:** `code`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2026-09

### Description

Generate maintainable Dockerfiles from application runtime requirements, build inputs, security constraints, and deployment targets. The skill is evidence-first: inspect actual state before acting, preserve existing contracts, and verify the result before reporting completion.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | runtime | object | Language, version, build system, and entrypoint verified from the repository |
| Input | constraints | object | Base-image policy, image size, user privilege, and pinning requirements |
| Output | dockerfile | string | Layer-ordered, pinned, non-root container build definition |
| Output | verification | object | Build and container run evidence confirming startup behavior |

### Procedure
1. Verify the runtime version and dependency manifests from the repository, not from memory.
2. Pin the base image by exact version or digest; prefer minimal official images.
3. Order layers from least to most volatile so dependency layers cache.
4. Run as a non-root user; copy only required artifacts; declare ports and health semantics explicitly.
5. Build the image and run the container; verify the entrypoint behaves as documented.
6. Record the build command and verification output as evidence.

### Example

```python
plan = {'base': 'python:3.12-slim', 'layers': ['deps', 'source', 'config'], 'user': 'appuser'}
assert plan['base'].endswith('slim')
assert plan['user'] != 'root'
assert plan['layers'].index('deps') < plan['layers'].index('source')
print('dockerfile plan ordered for cache and least privilege')
```

### Related Skills

- [Dependency Management](dependency-management.md) - pin the dependencies the image installs
- [Code Execution Sandbox](code-execution-sandbox.md) - verify image behavior in isolation
- [Documentation Generation](documentation-generation.md) - document build and run commands

## Failure Modes

- Guessing runtime dependencies instead of reading the manifests.
- Using unpinned or unverified base images.
- Skipping the image build and container startup check.
- Baking secrets into layers.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic plan example, an execution procedure, and corpus-verified related links.
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
