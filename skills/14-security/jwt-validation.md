---
title: "JWT Validation"
category: 14-security
level: advanced
stability: experimental
description: "Validate JSON Web Tokens by verifying the declared algorithm, signature, and claims in a fixed order so access decisions rest on cryptographic evidence instead of unverified payload strings."
added: "2026-10"
version: v1
related: ["mcp-oauth-authentication", "permission-checking"]
---

# JWT Validation

Category: Security | Level: advanced | Stability: experimental | Version: v1

## Description

A JWT is three base64url parts and a lot of trust. Skipping the verification order — algorithm, signature, then claims — is how alg=none and algorithm-confusion attacks happen. This skill defines validation as a fail-closed sequence: pin the expected algorithm, verify the signature with a constant-time comparison, then evaluate claims (expiry, audience, issuer) with an injectable clock.

## When to Use

Use whenever an agent or service accepts a JWT as evidence of identity or authorization, before any decision is made on its contents.

Do not use JWTs as long-term session storage; validation is per-request evidence, and revocation needs server-side state.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `token` | `string` | Yes | The compact serialized JWT |
| `secret_or_key` | `bytes | key` | Yes | The verification key for the pinned algorithm |
| `expected_alg` | `string` | Yes | The single algorithm accepted; anything else is rejected |
| `now` | `number` | No | Injectable clock for expiry claim evaluation |

## Procedure

1. Pin the expected algorithm in configuration; accept only that value from the token header.
2. Reject tokens whose header declares a different algorithm, a missing algorithm, or none — before any signature math runs.
3. Verify the signature over the exact signing input (header.payload) with a constant-time comparison.
4. Only after the signature holds, parse the payload and evaluate claims: expiry against the injected clock, audience, issuer.
5. Fail closed on every check; a token that fails any step is rejected without partial trust.
6. Log the validation outcome — verified or rejected with reason — without logging the token itself.
7. Never decode the payload for authorization before the signature check passes; unsigned payload is attacker input.

## Outputs

| Output | Type | Description |
|---|---|---|
| `claims` | `map[claim -> value]` | The verified payload claims |
| `valid` | `boolean` | Whether the token passed the full sequence |
| `reject_reason` | `string | null` | First failed check when rejected |

## Runnable Example

```python
import base64
import hashlib
import hmac
import json

def b64url_decode(data):
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)

def verify_jwt(token, secret, expected_alg="HS256"):
    header_b64, payload_b64, signature_b64 = token.split(".")
    header = json.loads(b64url_decode(header_b64))
    if header.get("alg") != expected_alg:
        raise ValueError(f"unexpected algorithm: {header.get('alg')!r}")
    signing_input = f"{header_b64}.{payload_b64}".encode()
    expected = hmac.new(secret, signing_input, hashlib.sha256).digest()
    if not hmac.compare_digest(expected, b64url_decode(signature_b64)):
        raise ValueError("signature mismatch")
    return json.loads(b64url_decode(payload_b64))

secret = b"shared-key-for-tests"
header = base64.urlsafe_b64encode(b'{"alg":"HS256"}').rstrip(b"=")
payload = base64.urlsafe_b64encode(b'{"sub":"agent-1"}').rstrip(b"=")
signing = header + b"." + payload
signature = base64.urlsafe_b64encode(
    hmac.new(secret, signing, hashlib.sha256).digest()).rstrip(b"=")
token = signing.decode() + "." + signature.decode()
print(verify_jwt(token, secret))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Algorithm confusion | Attacker-chosen alg trusted from the header | Pin one expected algorithm in configuration |
| alg=none acceptance | Unsigned tokens treated as valid | Reject missing or none algorithms before signature math |
| Claim skipping | Payload trusted without signature verification | Verify the signature before parsing any claims |
| Expiry clock skew | Wall clock read during validation | Inject the clock and evaluate exp deterministically |
| Token leakage in logs | Rejected tokens logged verbatim | Log outcomes and reasons, never the token string |

## Security and Authority Boundary

Token validation is the enforcement point, not the policy. A cryptographically valid token still bounds only what its claims assert: authority comes from the issuer’s policy, and every downstream action must pass its own permission checks.

## Evidence

This skill is grounded in dated public implementation references:

1. RFC 7519 defining JSON Web Tokens (https://www.rfc-editor.org/rfc/rfc7519).
2. The jwt.io introduction to JWT structure and signature verification (https://jwt.io/introduction).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [MCP OAuth Authentication](mcp-oauth-authentication.md) — an authorization flow that issues tokens this skill verifies.
- [Permission Checking](permission-checking.md) — the policy layer that consumes verified claims for decisions.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
