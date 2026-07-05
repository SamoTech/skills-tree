# P0 EVALUATION COVERAGE REASSESSMENT
**Report ID:** P0-COVERAGE-001  
**Generated:** 2026-07-05  
**Trigger:** RCA-002 — discovery that CAP-023 and CAP-025 evaluation mappings are semantically invalid  
**Authority:** `capability_ontology.json` SHA 5cdcd58d, `evaluation_ontology.json` SHA 7cd1b696  
**Corpus base:** CORPUS-001, CORPUS-002  
**No modifications made to any file.**

---

## Section 1 — Corpus-Active P0 Capability Inventory

All capabilities marked P0 in at least one corpus entry, derived from `required_capabilities` arrays:

| CAP-ID | Canonical Name | P0 in Entry | Evaluation Mapping Exists | Mapping Valid |
|---|---|---|---|---|
| CAP-001 | text_understanding | CORPUS-001, CORPUS-002 | ✅ Yes | ✅ Yes — three_tier_benchmark |
| CAP-002 | document_parsing | CORPUS-001 | ❌ No | ❌ No |
| CAP-003 | intent_classification | CORPUS-001, CORPUS-002 | ✅ Yes | ✅ Yes — labelled_classification_benchmark |
| CAP-005 | short_term_context_management | CORPUS-001, CORPUS-002 | ✅ Yes | ✅ Yes — multi_turn_coherence_test |
| CAP-009 | chain_of_thought_reasoning | CORPUS-001 | ❌ No | ❌ No |
| CAP-011 | self_evaluation | CORPUS-001, CORPUS-002 | ❌ No | ❌ No |
| CAP-014 | tool_execution | CORPUS-002 | ❌ No | ❌ No |
| CAP-017 | response_generation | CORPUS-001, CORPUS-002 | ✅ Yes | ✅ Yes — structured_rubric_human_eval |
| CAP-022 | error_recovery | CORPUS-001 | ❌ No | ❌ No |
| CAP-025 | pii_detection_and_redaction | CORPUS-001 | ✅ Yes (by ID) | ❌ No — TYPE A mismatch (cross_modal_benchmark) |
| CAP-028 | output_validation | CORPUS-001, CORPUS-002 | ✅ Yes | ✅ Yes — validation_gate_accuracy_test |

**Total corpus-active P0 capabilities: 11**

---

## Section 2 — Pre-RCA-002 Coverage (as reported in CORPUS_ANALYSIS_V1.md)

| Metric | Value |
|---|---|
| Total corpus-active P0 capabilities | 11 |
| Reported as covered (ID-only lookup) | 6 (CAP-001, CAP-003, CAP-005, CAP-017, CAP-025, CAP-028) |
| Reported as uncovered | 5 (CAP-002, CAP-009, CAP-011, CAP-014, CAP-022) |
| **Pre-RCA-002 P0 coverage rate (ID-only)** | **6 / 11 = 54.5%** |

**False positive in prior coverage:** CAP-025 was counted as covered because an entry with that CAP-ID exists in the evaluation_ontology. The entry is semantically invalid (cross_modal_benchmark for pii_detection_and_redaction). This report reclassifies it as not-validly-covered.

---

## Section 3 — Post-RCA-002 Coverage (corrected — name-validated lookup)

| Metric | Value |
|---|---|
| Total corpus-active P0 capabilities | 11 |
| Validly covered (ID + name match) | 5 (CAP-001, CAP-003, CAP-005, CAP-017, CAP-028) |
| Invalidly covered — TYPE A mismatch | 1 (CAP-025 — ID exists, name wrong) |
| Uncovered — no mapping | 5 (CAP-002, CAP-009, CAP-011, CAP-014, CAP-022) |
| **Post-RCA-002 P0 coverage rate (name-validated)** | **5 / 11 = 45.5%** |

**Coverage delta:** −9.0 percentage points from reclassifying CAP-025 as invalid.

---

## Section 4 — Post-Repair Projected Coverage

| Action | Effect |
|---|---|
| Repair 1: Replace CAP-023 mapping with human_in_loop_escalation benchmark | CAP-023 gains valid coverage (not P0 in any current corpus entry; no change to P0 count) |
| Repair 2: Replace CAP-025 mapping with pii_detection_and_redaction benchmark | CAP-025 gains valid coverage (+1 to P0 covered count) |
| Repair 3: Fix inline CAP-009 reference | Protocol documentation corrected; no coverage count change |

| Metric | Value |
|---|---|
| Validly covered P0s post-repair | 6 (CAP-001, CAP-003, CAP-005, CAP-017, CAP-025, CAP-028) |
| **Projected P0 coverage rate** | **6 / 11 = 54.5%** |

Projected coverage recovers to the pre-RCA-002 reported rate — but now accurately, not inflated by a false positive.

---

## Section 5 — Coverage by Entry

### CORPUS-001 P0 Coverage

| CAP-ID | Name | Valid Evaluation | Notes |
|---|---|---|---|
| CAP-001 | text_understanding | ✅ | three_tier_benchmark |
| CAP-002 | document_parsing | ❌ | No mapping exists |
| CAP-003 | intent_classification | ✅ | labelled_classification_benchmark |
| CAP-005 | short_term_context_management | ✅ | multi_turn_coherence_test |
| CAP-009 | chain_of_thought_reasoning | ❌ | No mapping exists |
| CAP-011 | self_evaluation | ❌ | No mapping exists |
| CAP-017 | response_generation | ✅ | structured_rubric_human_eval |
| CAP-022 | error_recovery | ❌ | No mapping exists |
| CAP-025 | pii_detection_and_redaction | ❌ | TYPE A mismatch — cross_modal_benchmark is invalid |
| CAP-028 | output_validation | ✅ | validation_gate_accuracy_test |

**CORPUS-001 P0 coverage: 5 / 10 = 50.0%** (pre-RCA reported: 60.0% — CAP-025 was falsely counted)

### CORPUS-002 P0 Coverage

| CAP-ID | Name | Valid Evaluation | Notes |
|---|---|---|---|
| CAP-001 | text_understanding | ✅ | three_tier_benchmark |
| CAP-003 | intent_classification | ✅ | labelled_classification_benchmark |
| CAP-005 | short_term_context_management | ✅ | multi_turn_coherence_test |
| CAP-011 | self_evaluation | ❌ | No mapping exists |
| CAP-014 | tool_execution | ❌ | No mapping exists |
| CAP-017 | response_generation | ✅ | structured_rubric_human_eval |
| CAP-028 | output_validation | ✅ | validation_gate_accuracy_test |

**CORPUS-002 P0 coverage: 5 / 7 = 71.4%** (unchanged — CAP-025 is not in CORPUS-002)

---

## Section 6 — Corpus Quality Score Impact

| Entry | Pre-RCA eval coverage score | Post-RCA corrected score |
|---|---|---|
| CORPUS-001 | 0.60 (6/10 P0 covered) | 0.50 (5/10 P0 covered) |
| CORPUS-002 | 0.71 (5/7 P0 covered) | 0.71 (unchanged) |
| Average | 0.655 | 0.605 |

**Revised evaluation coverage weighted contribution (weight = 0.20):** 0.605 × 0.20 = 0.121 (was 0.131)

**Revised Corpus Quality Score:** 0.952 − 0.010 = **0.942 / 1.0**

This is the accurate score reflecting that CAP-025's evaluation mapping is semantically invalid.

---

## Section 7 — Repository Risk Level

| Dimension | Risk | Justification |
|---|---|---|
| P0 evaluation coverage accuracy | HIGH | CAP-025 (P0 in CORPUS-001) has no valid benchmark; any CAP-025 deployment cannot be properly validated |
| Corpus Quality Score integrity | MEDIUM | Score was 0.952; corrected score is 0.942 — delta is small but origin is a false positive |
| Validation workflow false positives | HIGH | Any ID-only CI check reports CAP-023 and CAP-025 as covered; this masks a genuine evaluation gap |
| Future corpus entry risk | HIGH | Any new corpus entry declaring CAP-023 or CAP-025 will be assigned an incorrect evaluation benchmark unless the ontology is repaired first |

```
REPOSITORY RISK LEVEL: HIGH
Primary driver: CAP-025 (P0 in CORPUS-001) has no semantically valid evaluation benchmark.
Secondary driver: Validation workflows using ID-only lookup produce false-positive coverage reports.
```

---

*No modifications made to any ontology or corpus file. This document is investigation output only.*
