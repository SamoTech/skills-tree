---
name: diagnosis-coding
description: Map clinical descriptions to standard diagnosis codes using literal text support, a supplied code index, and explicit unresolved-case flagging so every code emitted is traceable, never invented.
metadata:
  source: skills/16-domain-specific/diagnosis-coding.md
  category: 16-domain-specific
  version: "v1"
---

# Diagnosis Coding

Category: Domain-Specific | Level: advanced | Stability: experimental | Version: v1

## Description

Diagnosis coding is a lookup task with a discipline problem: the temptation to code what a clinician probably meant. This skill pins the process to text — a code may be emitted only when the clinical text literally supports it, lookups run against a supplied code index of the declared version, and cases that cannot be resolved are flagged for a human coder. Output pairs every code with its evidence span, so nothing in the coded record is unattributable.

## When to Use

Use when clinical notes or symptom descriptions must be converted to a standard code system (ICD or a supplied local variant) for administrative structuring.

Do not use to diagnose patients, and do not emit codes for what the text implies but does not say; implication is a clinical judgment, not a coding fact.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `clinical_text` | `string` | Yes | The note or description to code |
| `code_system` | `string` | Yes | The declared code system and version |
| `code_index` | `map[code -> terms]` | Yes | Supplied index mapping codes to matching terms |
| `code_scope` | `list[code]` | No | Restriction to an allowed code subset |

## Procedure

1. Declare the code system and version before lookup; codes from mixed versions do not merge into one record.
2. Normalize the clinical text conservatively — case and whitespace, not paraphrase; the evidence span must survive.
3. Match only against the supplied index, restricted to the declared scope if one is given.
4. Emit a code only with a literal evidence span from the source text; the span is part of the output.
5. Flag unresolved cases explicitly for human coding; a near-miss is a flag, not a code with a lower bar.
6. Record code, span, code system version, and confidence; audits reconstruct every decision from these fields.

## Outputs

| Output | Type | Description |
|---|---|---|
| `codes` | `list[(code, span)]` | Emitted codes with their evidence spans |
| `unresolved` | `list[code]` | Index entries needing human coding |
| `record_metadata` | `map` | Code system, version, and per-code confidence |

## Runnable Example

```python
def code_text(text, code_index):
    """Emit only codes with literal support; flag the rest."""
    emitted, unresolved = [], []
    words = set(text.lower().split())
    for segment in code_index:
        matched = segment["terms"] & words
        if matched:
            emitted.append((segment["code"], sorted(matched)))
        else:
            unresolved.append(segment["code"])
    return emitted, unresolved

index = [
    {"code": "E11", "terms": {"diabetes"}},
    {"code": "J06", "terms": {"cold", "rhinitis"}},
    {"code": "I10", "terms": {"hypertension"}},
]
print(code_text("Patient reports cold symptoms; hypertension noted.", index))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Plausible-but-unsupported codes | Coding the likely diagnosis, not the stated one | Require a literal evidence span per code |
| Category drift | Symptoms coded as diagnoses | Keep symptom codes distinct and scope-restricted |
| Mixed code versions | Codes from different releases in one record | Declare one system version per record |
| Abbreviation ambiguity | Short forms with multiple expansions | Flag ambiguous abbreviations for human coding |
| Silent substitution | Model codes where a human must | Emit flags, never substitutions, for unresolved cases |

## Security and Authority Boundary

Coding support is administrative structuring of clinical text; it is not a diagnosis and not medical advice. Diagnostic decisions stay with licensed clinicians, and coded output must be reviewed under the facility's coding compliance process.

## Evidence

This skill is grounded in dated public implementation references:

1. The WHO overview of the International Classification of Diseases (https://www.who.int/standards/classifications/classification-of-diseases).
2. Wikipedia's overview of ICD-10 (https://en.wikipedia.org/wiki/ICD-10).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Symptom Analysis](symptom-analysis.md) — upstream analysis that must not be confused with coding decisions.
- [Clinical Note Summarization](clinical-note-summarization.md) — summarization whose outputs this skill codes.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
