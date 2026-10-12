---
name: password-hashing
description: Store passwords as salted, iterated hashes with a declared cost parameter and constant-time verification so credential material is never stored in recoverable form.
metadata:
  source: skills/14-security/password-hashing.md
  category: 14-security
  version: "v1"
---

# Password Hashing

Category: Security | Level: basic | Stability: experimental | Version: v1

## Description

A password stored in plaintext is a breach waiting for a date; a password hashed once without salt is a rainbow-table lookup. This skill defines credential storage as a contract: a per-user random salt, a slow memory-hard or iterated hash function, a declared cost parameter, and constant-time comparison on verification. The stored record keeps the algorithm and cost with the digest so migration to stronger parameters is possible.

## When to Use

Use whenever a system stores a user-provided secret for later verification — passwords, PINs, API secrets — and must never recover the plaintext.

Do not use for non-recoverable-but-high-entropy tokens like OAuth client secrets; those can be stored as plain fast hashes since entropy does the work.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `password` | `string` | Yes | The secret being stored or verified |
| `salt` | `bytes` | Yes | Per-user random salt, generated at first store |
| `cost` | `integer` | Yes | Iteration count or hardness parameter, declared in policy |
| `stored` | `(salt, cost, digest)` | Yes | The existing record for verification |

## Procedure

1. Generate a fresh random salt per credential at first store; reuse of salts across users is a defect.
2. Derive the digest with a salted slow hash and a cost parameter declared in policy, never chosen per call.
3. Store the salt, cost, and algorithm identifier alongside the digest so verification and migration are unambiguous.
4. Verify by re-deriving with the stored parameters and comparing in constant time; early-exit comparison leaks timing.
5. Reject passwords below the declared minimum entropy policy before hashing; the hash cannot repair a weak secret.
6. Rehash transparently on next successful login when the policy cost rises, and record the migration.
7. Never log the password, its digest, or the comparison result beyond pass/fail.

## Outputs

| Output | Type | Description |
|---|---|---|
| `record` | `(salt, cost, digest)` | The stored credential record |
| `verified` | `boolean` | Constant-time comparison result |

## Runnable Example

```python
import hashlib
import os

def hash_password(password, salt, iterations):
    """PBKDF2-HMAC-SHA256 with a per-user salt and declared cost."""
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    return digest

def verify_password(password, salt, iterations, stored_digest):
    candidate = hash_password(password, salt, iterations)
    return candidate == stored_digest

salt = os.urandom(16)
iterations = 1000  # demonstration cost; production policy is far higher
stored = hash_password("correct horse", salt, iterations)
print("match:", verify_password("correct horse", salt, iterations, stored))
print("mismatch:", verify_password("hunter2", salt, iterations, stored))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Rainbow-table recovery | Digests computed without per-user salt | Generate a random salt per credential |
| Cost stagnation | Iteration count frozen as hardware speeds up | Raise the policy cost and rehash on next login |
| Timing leaks | Comparison short-circuits on first mismatch | Compare derived digests in constant time |
| Weak secrets admitted | Short passwords hashed as-is | Enforce a minimum-length and entropy policy before hashing |
| Digest logging | Credential records written to logs | Log only pass/fail outcomes, never the material |

## Security and Authority Boundary

Hashing protects stored credentials, not the channel or the policy: transport still needs TLS, verification still needs rate limiting, and a verified password grants only what its account’s policy allows.

## Evidence

This skill is grounded in dated public implementation references:

1. The OWASP Password Storage Cheat Sheet (https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html).
2. Wikipedia’s overview of Argon2, the winner of the Password Hashing Competition (https://en.wikipedia.org/wiki/Argon2).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Input Sanitization](input-sanitization.md) — the boundary handling that precedes credential processing.
- [Secret Scanning](secret-scanning.md) — the detector that catches credential material before it lands in code.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
