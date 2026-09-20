# Skills Tree — Live Repository State

> Maintained as a point-in-time operational snapshot. Generated artifacts and historical project-memory documents may describe earlier repository states; this file records the verified state used for engineering decisions.

## Verified snapshot

- Snapshot date: 2026-09-20
- Main HEAD: `dfe4b9117e4f5d247ef0adb16dc5554434fb6f2d`
- Skill files: 369
- Battle-tested: 60
- Enriched: 3
- Stubs: 303
- Invalid: 3
- Active content PR: #146 (`skills/promote-enriched-batch-20260920`)
- PR #146 HEAD: `4ffccaf6bf54122bb070c58ed899baab00a8d7d0`

## Validation state

PR #146 has completed successfully for the repository validation workflows attached to its exact HEAD, including Test Suite, Test & Coverage, Security Scan, Validate Skills, Validate Skills Graph, Schema Enforcement, Skill Quality Report, AST Sweep, Build & Verify Wheel, Check Links, PR Checks, and Skill Upgrade Detector.

The Vercel commit status for the exact PR #146 HEAD is currently failing with `Deployment rate limited — retry in 24 hours`. This is an external deployment-quota condition, not a repository test failure. The PR must remain unmerged until the required deployment status is green or repository policy is explicitly changed and validated.

## Corpus modernization priority

The current quality distribution makes the remaining 303 stubs the dominant modernization target. Category `01-perception` contains 26 stubs; `09-agentic-patterns` contains 15 stubs and 2 invalid skills; `05-code` contains 23 stubs. Work should remain incremental and evidence-driven rather than attempting a corpus-wide rewrite.

## Integrity audit capability

`tools/audit_skill_corpus.py` is now part of the repository. It conservatively audits every skill file for duplicate normalized titles/descriptions, self-contradictory version declarations, missing related-skill targets, and Python fenced-code syntax errors. Its `stale` classification is intentionally evidence-based: it is emitted only when a skill's own changelog documents a version newer than its declared version.

The audit complements, rather than replaces, `tools/check_skill_quality.py` and the generated `meta/QUALITY-REPORT.md`.

## Operational rule

Do not treat a historical snapshot in `PROJECT_MEMORY.md` or older audit documents as current truth when it conflicts with the live quality report, current main SHA, current PR metadata, or current CI results. Preserve historical documents for provenance; use this snapshot and repository-generated artifacts for present-state decisions.
