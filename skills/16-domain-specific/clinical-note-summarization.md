---
title: "Clinical Note Summarization"
category: 16-domain-specific
level: advanced
stability: stable
description: "Apply clinical note summarization in an AI workflow with explicit scope, domain constraints, validation, and documented failure handling."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-16-domain-specific-clinical-note-summarization.json)

**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Condenses clinical documentation (discharge summaries, progress notes, EHR entries) into structured SOAP-style or problem-oriented summaries. Preserves critical findings, vital signs, medication changes, and follow-up actions while discarding administrative boilerplate.

### Example
```python
import anthropic

client = anthropic.Anthropic()

def summarize_note(raw_note: str) -> dict:
    resp = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=512,
        messages=[{"role": "user", "content": (
            "Extract a structured clinical summary from this note as JSON with keys: "
            "status, vital_signs, medications_changed, red_flags, follow_up.\n\n" + raw_note
        )}]
    )
    import json
    return json.loads(resp.content[0].text)

note = "Patient 72F, SOB improving, O2 sat 97% RA, started furosemide 40mg QD, \
follow-up chest X-ray in 48h, no fever."
print(summarize_note(note))
```

### Related
- 16-domain-specific
- input-guardrails
- output-guardrails
