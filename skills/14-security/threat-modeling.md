---
title: "Threat Modeling"
category: 14-security
level: intermediate
stability: experimental
description: "Model a system’s components against a structured threat taxonomy with per-interaction mitigations so security work is driven by an enumerated, reviewable threat list instead of ad-hoc paranoia."
added: "2026-10"
version: v1
related: ["harm-detection", "agent-skill-security-audit"]
---

# Threat Modeling

Category: Security | Level: intermediate | Stability: experimental | Version: v1

## Description

Security without enumeration becomes either paralysis or theater. Threat modeling imposes order: decompose the system into components and interactions, walk a fixed taxonomy — spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege — per component, and record a mitigation or an explicit acceptance for every threat found. The model is the artifact; fixes are tracked against it.

## When to Use

Use when designing or changing a system that handles untrusted input, credentials, or privileged operations, and when the security posture must be explainable to a reviewer.

Do not use as a substitute for testing; a model guides where to test and review, and unverified mitigations are intentions, not protections.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `components` | `list[name]` | Yes | System decomposition under review |
| `interactions` | `list[(threat, entry_point, mitigation)]` | Yes | Recorded threats and their handling per component |
| `taxonomy` | `list[threat]` | Yes | The threat classes walked per component |

## Procedure

1. Decompose the system into components and their interactions before naming a single threat.
2. Walk the declared taxonomy for every component, in a fixed order, so classes are never skipped silently.
3. Record each threat with its entry point and a mitigation, or an explicit accepted-risk note — never an empty cell.
4. Treat missing mitigations as findings with owners and deadlines, not as future hopes.
5. Update the model whenever the decomposition changes; a model of the old system protects nothing.
6. Re-test mitigations that the model claims; an untested mitigation is a documented guess.

## Outputs

| Output | Type | Description |
|---|---|---|
| `findings` | `list[(threat, component, status)]` | Enumerated threats and their handling status |
| `uncovered` | `list[threat]` | Taxonomy classes with no recorded interaction |

## Runnable Example

```python
STRIDE = ["spoofing", "tampering", "repudiation",
         "information-disclosure", "denial-of-service",
         "elevation-of-privilege"]

def model_component(component, interactions):
    """Report which taxonomy classes the recorded interactions cover."""
    covered = {threat for threat, _entry, _mitigation in interactions}
    return {
        "component": component,
        "covered": sorted(covered),
        "uncovered": [t for t in STRIDE if t not in covered],
    }

interactions = [
    ("spoofing", "api token accepted", "bind token to device fingerprint"),
    ("tampering", "config edited locally", "signed config verified at load"),
    ("elevation-of-privilege", "plugin executes code", "sandbox with allowlist"),
]
report = model_component("skill-loader", interactions)
print("covered:", report["covered"])
print("uncovered:", report["uncovered"])
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Taxonomy skipping | Only familiar threat classes examined | Walk the full taxonomy per component in fixed order |
| Empty-cell acceptance | Threats noted without mitigation or decision | Require a mitigation or an explicit accepted-risk note |
| Stale model | System changed, model unchanged | Re-model on every decomposition change |
| Untested mitigations | Controls recorded but never verified | Track mitigations as testable findings with owners |
| Paralysis inversion | Enumeration replaces remediation | Every finding needs an owner and a deadline |

## Security and Authority Boundary

The model itself is sensitive: it enumerates exactly where the system is soft. Treat threat models as need-to-know artifacts and protect them with the same care as the codebase.

## Evidence

This skill is grounded in dated public implementation references:

1. The OWASP Threat Modeling Cheat Sheet (https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html).
2. Wikipedia’s overview of the STRIDE threat classification (https://en.wikipedia.org/wiki/STRIDE_(security)).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Harm Detection](harm-detection.md) — runtime harm signals that validate what this model predicted.
- [Agent Skill Security Audit](agent-skill-security-audit.md) — the audit practice that consumes these enumerated findings.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
