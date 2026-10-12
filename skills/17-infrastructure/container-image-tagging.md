---
title: "Container Image Tagging"
category: 17-infrastructure
level: intermediate
stability: experimental
description: "Tag container images with immutable, traceable identifiers — semantic version tags, registry digests, and build provenance — so deployments reference an exact artifact auditable after the fact."
added: "2026-10"
version: v1
related: ["kubernetes-deployment", "dependency-auditor"]
---

# Container Image Tagging

Category: Infrastructure | Level: intermediate | Stability: experimental | Version: v1

## Description

A tag is a label someone can move; a digest is an identity they cannot. This skill pins that difference into the pipeline: builds get version tags once, deployments reference images by digest, a tag is never reassigned to different bytes, and every artifact carries build provenance — source commit, build definition, timestamp. The result is that any deployed environment can answer "exactly which bytes are running, and where did they come from".

## When to Use

Use for any container image that reaches a deployment — application services, tooling images, CI runner environments.

Do not deploy floating tags such as `latest` or a bare branch name; a deployment that cannot name its bytes cannot be rolled back to them either.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `image` | `name` | Yes | The image being built and tagged |
| `version` | `semver` | Yes | The release version this build belongs to |
| `digest` | `sha256` | Yes | The content-addressed identity from the registry |
| `provenance` | `map` | Yes | Source commit, build definition, and timestamp |

## Procedure

1. Build once per version; the artifact from one build receives all its tags at creation time.
2. Tag with the semantic version; tags are claims about content, applied once and never retagged.
3. Record the registry digest; deployments pin by digest, with the version tag kept for humans.
4. Attach provenance to the artifact — source commit, build definition, build time — as metadata or attestation.
5. Reject retag requests: a tag that points at new bytes is a new version, whatever it is called.
6. Keep tag-to-digest mappings queryable so an environment's running bytes can be resolved historically.

## Outputs

| Output | Type | Description |
|---|---|---|
| `release` | `map` | Version tag, digest, and provenance per image |
| `pin` | `digest` | The digest deployments reference |
| `audit_line` | `map` | Who tagged what, when, from which build |

## Runnable Example

```python
class TagRegistry:
    def __init__(self):
        self.tags = {}

    def push(self, tag, digest):
        if tag in self.tags and self.tags[tag] != digest:
            raise ValueError(f"retag refused: {tag} already names different bytes")
        self.tags[tag] = digest

    def resolve(self, tag):
        return self.tags.get(tag)

registry = TagRegistry()
registry.push("api-v2.4.0", "sha256:aaa1")
registry.push("api-latest", "sha256:aaa1")
try:
    registry.push("api-v2.4.0", "sha256:bbb2")
except ValueError as err:
    print(err)
print(registry.resolve("api-v2.4.0"))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| `latest` in production | Environments reference a moving tag | Pin deployments to digests |
| Retagged versions | The same version label naming different bytes | Refuse retags; new bytes get a new version |
| Tag-only references | Digest never recorded at release time | Store tag-to-digest mappings per release |
| Missing provenance | Artifact cannot be traced to source or build | Attach source commit and build definition |
| Cross-registry drift | The same tag resolves differently per registry | Resolve and compare digests, not tag names |

## Security and Authority Boundary

Tagging identifies artifacts; it does not make them safe. Vulnerability scanning and signature verification are separate steps whose verdicts attach to the digest, not to the label.

## Evidence

This skill is grounded in dated public implementation references:

1. The Docker CLI reference for image tagging (https://docs.docker.com/reference/cli/docker/image/tag/).
2. Wikipedia's overview of immutable objects (https://en.wikipedia.org/wiki/Immutable_object).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Kubernetes Deployment](kubernetes-deployment.md) — the deployment layer that pins these digests.
- [Dependency Auditor](dependency-auditor.md) — the pipeline that audits what images contain.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
