---
title: Pipeline Test Fixture
category: 00-sandbox
level: basic
stability: experimental
version: v1
added: 2026-06-22
prerequisites:
  - 02-reasoning/chain-of-thought
---

# Pipeline Test Fixture

**INITIATIVE-004 pilot validation fixture.**
This file exists solely to verify that the `prerequisites` frontmatter field
generates a REQUIRES edge during `build_graph.py` execution.

Do NOT use this skill in production.
This file should be removed after INITIATIVE-005 confirms the pipeline is live
with real skill prerequisites.

## Purpose

Verify end-to-end pipeline:
1. `prerequisites: [02-reasoning/chain-of-thought]` in frontmatter
2. `build_graph.py` reads field via `parse_frontmatter()`
3. `build_node()` stores list in `node["prerequisites"]`
4. `build_prerequisite_edges()` emits REQUIRES edge
5. Edge appears in `data/SKILLS_GRAPH.json` with `type: REQUIRES`
