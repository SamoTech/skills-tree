---
name: dockerfile-generation
description: Generate maintainable Dockerfiles from application runtime requirements, build inputs, security constraints, and deployment targets.
license: MIT
metadata:
  source: skills/05-code/dockerfile-generation.md
  version: "v2"
---

# Dockerfile Generation

1. Inspect runtime, build, dependency, and deployment requirements.
2. Identify required build artifacts and startup behavior.
3. Define a deterministic container build with only required inputs.
4. Preserve repository security and runtime constraints.
5. Build and validate the image and startup behavior.
6. Record verification evidence.

## Failure modes
- Missing runtime assets.
- Incorrect startup configuration.
- Non-reproducible build assumptions.
- Incomplete image verification.

## Evidence
Canonical skill: skills/05-code/dockerfile-generation.md
Repository governance: AI_CONSTITUTION.md
