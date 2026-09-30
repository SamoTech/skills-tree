---
title: "Automation Review"
category: 15-orchestration
level: advanced
stability: stable
description: "Audit repository automation for duplicate writers, unsafe triggers, permissions, concurrency, and preserved outputs before automation changes."
added: "2026-09"
related:
  - repository-state-load
  - evidence-verification
  - documentation-drift-resolution
---

# Automation Review

## Description

Inspect repository automation before changing it. Inventory workflows, triggers, writers, permissions, concurrency, and release paths. Consolidation is safe only when every required output and trigger remains represented and the resulting CI behavior is verified.

1. Inventory all workflow files and their triggers.
2. Identify workflows that write repository state, publish artifacts, deploy pages, or release packages.
3. Detect duplicate writers and competing publishers.
4. Compare permissions and concurrency behavior before consolidation.
5. Preserve every required output path when merging workflows.
6. Verify changed workflows through actual CI runs after the change.
7. Record material automation decisions in the repository decision log.

## Runnable example

```bash
find .github/workflows -maxdepth 1 -type f -name '*.yml' -print
grep -RniE 'git push|contents: write|pages: write|workflow_dispatch|schedule:' .github/workflows
git diff -- .github/workflows
```

## Inputs / outputs / failure modes

| Input | Output | Failure mode |
|---|---|---|
| Workflow inventory | Complete automation map | A workflow is overlooked |
| Trigger definitions | Preserved event coverage | Trigger behavior changes unintentionally |
| Permissions and writers | Reduced conflict risk | Multiple writers compete |
| Publish/release paths | Preserved outputs | Artifact or site output disappears |
| CI results | Post-change evidence | Workflow is assumed healthy without a run |

## Failure modes

- Removing a workflow without mapping its outputs.
- Preserving duplicate writers that can race.
- Broadening permissions without a documented need.
- Assuming a successful YAML parse means the automation behavior is correct.
- Declaring consolidation complete before the affected workflows execute successfully.

## Related

- `repository-state-load.md`
- `evidence-verification.md`
- `documentation-drift-resolution.md`

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- meta/AGENT_OPERATING_MODEL.md
- meta/CURRENT-STATE.md
- GitHub Actions workflow runs
