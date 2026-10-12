---
title: "Dependency Integrity Verification"
category: 14-security
level: intermediate
stability: experimental
description: "Verify third-party package artifacts against pinned digests, signatures, and provenance attestations before installation so the build consumes exactly the artifacts that were reviewed."
added: "2026-10"
version: v1
related: ["secret-scanning", "sandboxed-execution"]
---

# Dependency Integrity Verification

Category: Security | Level: intermediate | Stability: experimental | Version: v1

## Description

A dependency declaration names what you want; the artifact that arrives is what you run. Integrity verification closes that gap: versions pinned to exact hashes, digests recomputed at install time, signatures checked against a known identity, and provenance attestations matched to the build that produced the artifact. Anything that cannot be verified is rejected rather than installed and inspected later.

## When to Use

Use before installing any third-party package in build, CI, or runtime environments — especially in automated pipelines that install without a human reading the output.

Do not treat integrity verification as vulnerability scanning: a verified artifact is exactly the reviewed bytes, which can still contain a reviewed vulnerability.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `package_spec` | `name@version` | Yes | The dependency to install |
| `expected_digest` | `sha256` | Yes | The pinned hash from the reviewed lockfile |
| `signature` | `bytes | null` | No | Detached signature over the artifact |
| `provenance` | `attestation | null` | No | Build provenance statement for the artifact |

## Procedure

1. Pin exact versions with hashes in the lockfile; floating ranges bypass review by construction.
2. Fetch the artifact and recompute its digest locally; never trust the registry's advertised hash alone.
3. When a signature is available, verify it against a pinned signing identity, not a key fetched at verify time.
4. When provenance is available, check that the attestation's build matches the expected source and workflow.
5. Reject on any mismatch — digest, signature, or provenance — and fail the install.
6. Record the verification result (package, digest, verdict) so the decision is auditable later.

## Outputs

| Output | Type | Description |
|---|---|---|
| `verdict` | `verified | rejected` | Whether the artifact matched its pinned integrity data |
| `reason` | `string | null` | First failed check when rejected |
| `log` | `map` | Package, version, digest, and verdict for the audit trail |

## Runnable Example

```python
import hashlib

def verify_artifact(payload, expected_digest):
    """Recompute the digest and compare in constant time."""
    digest = hashlib.sha256(payload).hexdigest()
    if not hashlib.compare_digest(digest, expected_digest):
        return {"verdict": "rejected", "reason": f"digest {digest}"}
    return {"verdict": "verified", "reason": None}

payload = b"def plugin(): return 42"
expected = hashlib.sha256(payload).hexdigest()
print(verify_artifact(payload, expected)["verdict"])
print(verify_artifact(payload + b" ", expected)["verdict"])
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Floating versions | `^1.0` ranges install whatever resolves today | Pin exact versions with hashes in the lockfile |
| Registry substitution | Artifact swapped between resolve and install | Recompute the digest at install time |
| Keys fetched at verify time | Signing key taken from the channel it vouches for | Pin the signing identity independently |
| CI cache poisoning | Cached artifacts skip verification | Verify after cache restore, not only on download |
| Mirror drift | Internal mirror serving different bytes | Verify digests from mirrors exactly like upstream |

## Security and Authority Boundary

Integrity verification proves the artifact is the one that was attested; it says nothing about the safety or quality of the code inside. Vulnerability scanning, license review, and human review remain separate, mandatory steps.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia's overview of supply chain attacks on software distribution (https://en.wikipedia.org/wiki/Supply_chain_attack).
2. The Sigstore documentation on artifact signing and verification (https://docs.sigstore.dev/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Secret Scanning](secret-scanning.md) — the paired check that no credentials ride along with the code.
- [Sandboxed Execution](sandboxed-execution.md) — containment for artifacts that pass verification but stay unproven in behavior.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
