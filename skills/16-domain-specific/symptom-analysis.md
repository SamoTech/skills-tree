![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-16-domain-specific-symptom-analysis.json)

**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Maps reported symptoms to differential diagnosis candidates, urgency tiers, and recommended next steps using structured medical reasoning. Integrates evidence-based triage heuristics, red-flag detection, and explicit uncertainty signalling to support (not replace) clinician review.

### Example
```python
from dataclasses import dataclass
from typing import List

@dataclass
class TriageResult:
    urgency: str
    differentials: List[str]
    red_flags: List[str]
    next_step: str

RED_FLAGS = ["chest pain", "confusion", "shortness of breath", "sudden weakness"]

def triage(symptoms: List[str]) -> TriageResult:
    flags = [s for s in symptoms if s in RED_FLAGS]
    urgency = "URGENT" if flags else "ROUTINE"
    differentials = ["viral URI", "influenza"] if "fever" in symptoms else ["evaluate further"]
    return TriageResult(urgency=urgency, differentials=differentials,
                        red_flags=flags, next_step="Seek immediate care" if flags else "GP visit")

print(triage(["fever", "cough", "fatigue"]))
```

### Related Skills
- [Decision Making](../02-reasoning/decision-making.md)
- [Risk Assessment](../02-reasoning/risk-assessment.md)
- [Drug Interaction Check](drug-interaction.md)
- [Clinical Note Summarization](clinical-note-summarization.md)
