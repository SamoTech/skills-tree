---
name: package-publishing-actions
description: Publish packages to registries with version checks, provenance metadata, and pre-publish verification, and refuse to overwrite an existing published version.
metadata:
  source: skills/04-action-execution/package-publishing-actions.md
  category: 04-action-execution
  version: "v1"
---

# Package Publishing Actions

## Description
Publish packages to registries with version checks, provenance metadata, and pre-publish verification, and refuse to overwrite an existing published version. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a package must be published to a registry as a verified, immutable release before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for package publishing actions work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the package publishing actions steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def can_publish(existing, next_version):
    if next_version in existing:
        return False, "version already published"
    return True, "ok"

assert can_publish(["1.0.0", "1.1.0"], "1.2.0") == (True, "ok")
assert can_publish(["1.0.0"], "1.0.0")[0] is False

def bump(part, version):
    major, minor, patch = (int(x) for x in version.split("."))
    return {"major": "%d.0.0" % (major + 1), "minor": "%d.%d.0" % (major, minor + 1), "patch": "%d.%d.%d" % (major, minor, patch + 1)}[part]

assert bump("patch", "1.2.3") == "1.2.4"
```

## Failure Modes
- Publishing over an existing version.
- Publishing without provenance metadata.
- Skipping pre-publish verification to save time.
- Publishing from a dirty working tree.
- Trusting a tag that was never verified against the build.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Supply-chain hardening for package publishes is a documented 2026 ecosystem concern in public coverage; this is a dated signal, not an adoption metric.

## Related
- api-call.md
- action-result-verification.md
- background-job-submission.md
