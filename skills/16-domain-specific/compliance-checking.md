![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-16-domain-specific-compliance-checking.json)

**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Verifies that documents, configurations, or processes conform to specified regulatory or policy frameworks such as GDPR, HIPAA, SOC 2, or internal standards. Produces a gap report with severity levels and remediation steps.

### Example
```python
GDPR_CONTROLS = [
    "privacy_policy_published",
    "data_retention_policy",
    "consent_mechanism",
    "breach_notification_procedure",
    "dpa_agreements",
]

def gdpr_gap_check(implemented: list[str]) -> dict:
    missing = [c for c in GDPR_CONTROLS if c not in implemented]
    score = (len(GDPR_CONTROLS) - len(missing)) / len(GDPR_CONTROLS)
    return {"compliance_score": round(score, 2), "gaps": missing,
            "status": "PASS" if not missing else "FAIL"}

print(gdpr_gap_check(["privacy_policy_published", "consent_mechanism"]))
```

### Related Skills
- [Contract Review](contract-review.md)
- [Risk Assessment](../02-reasoning/risk-assessment.md)
- [Assertion](../04-action-execution/assertion.md)
