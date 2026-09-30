---
title: "Repository State Load"
category: 15-orchestration
level: advanced
stability: stable
description: "Load and reconcile authoritative repository state before meaningful AI execution."
added: "2026-09"
---

# Repository State Load

Before meaningful work, load the repository constitution, agent entrypoint, operating model, current state, decisions, handoff protocol, and task-relevant architecture/testing/security/deployment documents.

1. Establish the current main SHA from GitHub.
2. Read authoritative governance and state documents.
3. Compare documented state with live GitHub metadata and generated reports.
4. Treat live repository evidence as authoritative when historical snapshots conflict.
5. Record material divergence before making consequential changes.
6. Do not execute against incomplete or contradictory state without resolving or escalating the divergence.

## Failure modes

- Stale CURRENT-STATE data: refresh it before declaring state.
- Historical decision mistaken for current state: verify against current main and PR/CI evidence.
- Missing authoritative document: record the blocker and escalate.
- Partial retrieval: do not infer unseen repository state.

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- meta/AGENT_OPERATING_MODEL.md
- meta/CURRENT-STATE.md
- meta/memory/DECISIONS.md
