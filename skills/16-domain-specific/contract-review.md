![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-16-domain-specific-contract-review.json)

**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Reviews legal contracts to extract key clauses (termination, liability, IP, payment, dispute resolution), flag high-risk provisions, compare against standard policy positions, and produce a structured risk report with recommended redlines.

### Example
```python
CLAUSE_PATTERNS = {
    "liability_cap": r"liability.{0,30}capped|limited to.{0,20}fees",
    "auto_renewal": r"auto.?renew|automatically renew",
    "unilateral_change": r"(may|can|reserves the right).{0,40}(modify|amend|change)",
}

import re

def flag_clauses(text: str) -> dict:
    findings = {}
    for risk, pattern in CLAUSE_PATTERNS.items():
        match = re.search(pattern, text, re.I)
        if match:
            findings[risk] = match.group(0)
    return findings

contract = "Liability is capped at fees paid. Company may modify terms at any time."
print(flag_clauses(contract))
```

### Related Skills
- [Legal Research](legal-research.md)
- [Compliance Checking](compliance-checking.md)
- [Document Parsing](../01-perception/document-parsing.md)
