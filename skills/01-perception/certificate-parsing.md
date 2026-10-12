---
title: "Certificate Parsing"
category: 01-perception
level: intermediate
stability: experimental
description: "Parse X.509 certificates into structured fields — subject, issuer, validity, key usage — with explicit expiry checking and stated chain-validation boundaries."
added: "2026-10"
version: v1
related: ["network-traffic-reading", "structured-data-reading"]
---

# Certificate Parsing

Category: Perception | Level: intermediate | Stability: experimental | Version: v1

## Description

A certificate is a signed claim about an identity, and most TLS mistakes come from reading one field of it in isolation. This skill parses a certificate into its material fields, checks validity windows and key usage against the operation at hand, and states clearly what a leaf certificate cannot tell you: whether its chain actually anchors to a trust store.

## When to Use

Use when a workflow receives a certificate and needs its identity, expiry, or purpose fields — inventory of deployed certificates, pre-flight checks, incident triage of a TLS failure.

Do not use field parsing as chain validation; a parsed, unexpired, purpose-matching certificate can still be untrusted, self-signed, or revoked.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `certificate` | `pem-or-der` | Yes | The certificate to parse |
| `reference_time` | `datetime` | No | Clock to evaluate validity against; default is now |
| `required_usage` | `enum` | No | Key usage the operation needs, such as server auth |

## Procedure

1. Decode PEM or DER into the certificate structure, reporting the encoding and size.
2. Extract the material fields — subject, issuer, serial, validity window, signature algorithm, key usage, subject alternative names.
3. Evaluate the validity window against the reference time and report days remaining, not just a boolean.
4. Check key usage and subject alternative names against the operation the certificate is being assessed for.
5. Report self-signed and wildcard states explicitly; they change what the fields can support.
6. State the boundary: chain building, revocation, and trust-store anchoring are separate validation steps.

## Outputs

| Output | Type | Description |
|---|---|---|
| `fields` | `map` | Parsed certificate fields |
| `validity` | `map` | Not-before, not-after, and days remaining at reference time |
| `cautions` | `list` | Self-signed, wildcard, weak-algorithm, and boundary cautions |

## Runnable Example

```python
def der_length(der):
    if der[0] != 0x30:
        raise ValueError("not a certificate: missing SEQUENCE tag")
    length = der[1]
    if length & 0x80:
        nbytes = length & 0x7F
        length = int.from_bytes(der[2:2 + nbytes], "big")
    return length

def summarize(raw_hex, reference):
    der = bytes.fromhex(raw_hex)
    return {"der_bytes": len(der), "declared_body": der_length(der), "reference_time": reference}

print(summarize("308201a4" + "00" * 420, "2026-10-12T05:00:00Z"))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Parsing used as validation | An untrusted chain is treated as trusted because fields look correct | Keep chain validation a separate explicit step |
| Expiry checked once | A certificate expires between check and use | Report days remaining and re-check at use time |
| Weak algorithms missed | A signature algorithm is accepted without review | Flag weak hashes and small keys |
| Purpose mismatch | A certificate is used for an operation its key usage forbids | Match key usage and names to the operation |
| Encoding errors | Truncated DER is parsed as a shorter record | Verify declared lengths against actual size |

## Security and Authority Boundary

Certificates authenticate identities, not intentions. This skill reports what a certificate claims; it must not be used to grant access, and private keys must never travel through the same parsing path as public certificates.

## Evidence

This skill is grounded in dated public implementation references:

1. The OpenSSL documentation for certificate handling (https://docs.openssl.org/).
2. The Python ssl module reference (https://docs.python.org/3/library/ssl.html).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Network Traffic Reading](network-traffic-reading.md) — the transport-analysis layer where certificates appear in handshakes.
- [Structured Data Reading](structured-data-reading.md) — the bounded-structure discipline applied here to ASN.1 records.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
