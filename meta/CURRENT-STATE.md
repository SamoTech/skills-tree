# Skills Tree — Live Repository State

> Maintained as a point-in-time operational snapshot. This file records verified state used for engineering and governance decisions.

## Verified snapshot

- Snapshot date: 2026-10-01
- Verified live main HEAD: `5b2eda286020289bc73c57a079187e882098bdcc` — current live main after documentation synchronization PR #224.
- Main HEAD: `5b2eda286020289bc73c57a079187e882098bdcc`.
- PR #223 remains the implementation baseline for the post-P2.2 Evidence runtime slice, merged as `642e968879e9b6bfc8e7f9b2a44d12544585fc18`.
- PR #224 merged as `5b2eda286020289bc73c57a079187e882098bdcc` and synchronized the affected P2 architecture, development knowledge, audit, decision memory, and current-state documentation.
- Quality report: generated counts pending the post-merge quality writer; last verified report remains the documented prior verification point. These figures are not treated as current live counts unless regenerated and verified.
- Invalid: 0 at the last verified quality-report point.

## Current verified architecture state

- The canonical skill source is `skills/`.
- The universal registry is a read-only, deterministic machine-readable capability layer with typed runtime access.
- P2.1 Implementation ontology contract unification is verified.
- P2.2 typed Implementation runtime access and contract validation are verified.
- The post-P2.2 Evidence runtime slice is verified: `UniversalRegistry` exposes typed deterministic `resolve_evidence()` and `evidence_for_entity()` access through the existing validated `EvidenceRuntime`.
- The Evidence slice added no new Evidence records, provenance claims, compatibility facts, provider/platform/framework/model claims, or MCP classifications.
- No numbered P2.3 requirement is currently defined. The next Phase 2 slice must come from a fresh architecture audit.

## Governance and documentation state

- `AI_CONSTITUTION.md` is the authoritative governance model.
- `AGENTS.md` is the AI-agent entrypoint.
- `meta/COO_MASTER_MISSION.md` is the strategic mission.
- `meta/memory/DECISIONS.md` is the durable decision record.
- `meta/ROADMAP.md` is the execution direction and must remain synchronized with verified state.
- `meta/DEVELOPMENT_KNOWLEDGE.md` records verified development progression.
- `meta/AGENT_HANDOFF_PROTOCOL.md` defines repository handoff requirements.
- Documentation is a completion gate: implementation without synchronized documentation is not COMPLETE.

## Automation state

- Release authority: `zero-touch-release.yml` is the production release pipeline; `release.yml` is retained as manual recovery.
- Pages authority: `deploy-pages.yml` is the single repository-controlled Pages deployment workflow.
- Confirmed direct-main generated writers use the shared `auto-commit-main` serialization group with `cancel-in-progress: false`.
- The remaining Phase 0 work is the evidence-backed workflow-by-workflow classification, duplicate/unused automation disposition, permissions/security reconciliation, and explicit documentation of connector control-plane limitations.

## Source of truth

- Canonical source: GitHub repository `SamoTech/skills-tree`.
- Public source guide: `README.md`.
- Operational state: `meta/CURRENT-STATE.md` plus live GitHub CI/PR state.
- Strategic decisions: `meta/memory/DECISIONS.md`.
- Quality evidence: generated repository reports.
- External dashboards and Vercel deployments are not authoritative.

## Next mandatory action

Perform a fresh universal-registry runtime architecture audit after the verified Evidence runtime integration. Identify the highest-value missing invariant or runtime capability, confirm it is not already covered by the contract, registry, graph, evidence, compatibility, or consumer layers, then implement the smallest evidence-backed schema → runtime → behavioral-test slice.

Do not invent a numbered P2.3 requirement, reopen completed P1 work, or expand scope merely to create activity.

## Handoff

A future agent must re-read the authoritative documents and verify live GitHub state before continuing. The repository, not this snapshot alone, remains the final source of truth.
