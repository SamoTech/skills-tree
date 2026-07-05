# P0 EVALUATION COVERAGE REASSESSMENT
**Audit ID:** RCA-002-P0-COVERAGE
**Generated:** 2026-07-05
**Basis:** Post-RCA-002 recalculation using canonical capability_ontology.json
**Constraint:** No fixes applied. Reassessment reports pre-repair and post-repair-if-applied states.

---

## Scope Definition

P0 capabilities are those assigned tier `P0` in any active corpus entry (CORPUS-001 or CORPUS-002).
A capability is considered **validly mapped** only if its `cap_id` exists in `capability_evaluation_mappings[]` AND the `name` field in that mapping matches the canonical name in `capability_ontology.json`.

---

## P0 Capability Inventory (All Corpus Entries)

| CAP-ID | Name | Source Entry | Criticality |
|---|---|---|---|
| CAP-001 | text_understanding | CORPUS-001, CORPUS-002 | 0.97 / 0.96 |
| CAP-002 | document_parsing | CORPUS-001 | 0.95 |
| CAP-003 | intent_classification | CORPUS-001, CORPUS-002 | 0.92 / 0.93 |
| CAP-005 | short_term_context_management | CORPUS-001, CORPUS-002 | 0.88 / 0.89 |
| CAP-009 | chain_of_thought_reasoning | CORPUS-001 | 0.92 |
| CAP-011 | self_evaluation | CORPUS-001, CORPUS-002 | 0.83 / 0.91 |
| CAP-013 | tool_selection | CORPUS-001 | 0.86 |
| CAP-014 | tool_execution | CORPUS-002 | 0.98 |
| CAP-017 | response_generation | CORPUS-001, CORPUS-002 | 0.93 / 0.94 |
| CAP-022 | error_recovery | CORPUS-001 | 0.88 |
| CAP-025 | pii_detection_and_redaction | CORPUS-001 | 0.91 |
| CAP-028 | output_validation | CORPUS-001, CORPUS-002 | 0.89 / 0.92 |

**Total distinct P0 capabilities across corpus: 12**

---

## Coverage Before RCA-002 (As Reported)

| CAP-ID | Name | Had Mapping? (Pre-RCA) | Mapping Valid? |
|---|---|---|---|
| CAP-001 | text_understanding | ✅ Yes | ✅ Yes |
| CAP-002 | document_parsing | ❌ No | — |
| CAP-003 | intent_classification | ✅ Yes | ✅ Yes |
| CAP-005 | short_term_context_management | ✅ Yes | ✅ Yes |
| CAP-009 | chain_of_thought_reasoning | ❌ No | — |
| CAP-011 | self_evaluation | ❌ No | — |
| CAP-013 | tool_selection | ❌ No | — |
| CAP-014 | tool_execution | ❌ No | — |
| CAP-017 | response_generation | ✅ Yes | ✅ Yes |
| CAP-022 | error_recovery | ❌ No | — |
| CAP-025 | pii_detection_and_redaction | ✅ Yes (INVALID — mapped as multi_modal_understanding) | ❌ No |
| CAP-028 | output_validation | ✅ Yes | ✅ Yes |

**Corrected pre-repair P0 valid coverage: 5 of 12 = 41.7%**
(Previously overcounted as 6/12 = 50.0% by including the invalid CAP-025 mapping)

---

## Coverage After Proposed Repair (Projected)

| CAP-ID | Name | Mapping After Repair |
|---|---|---|
| CAP-001 | text_understanding | ✅ Valid |
| CAP-002 | document_parsing | ❌ Still missing |
| CAP-003 | intent_classification | ✅ Valid |
| CAP-005 | short_term_context_management | ✅ Valid |
| CAP-009 | chain_of_thought_reasoning | ❌ Still missing |
| CAP-011 | self_evaluation | ❌ Still missing |
| CAP-013 | tool_selection | ❌ Still missing |
| CAP-014 | tool_execution | ❌ Still missing |
| CAP-017 | response_generation | ✅ Valid |
| CAP-022 | error_recovery | ❌ Still missing |
| CAP-025 | pii_detection_and_redaction | ✅ Valid (after repair) |
| CAP-028 | output_validation | ✅ Valid |

**Post-repair P0 valid coverage: 6 of 12 = 50.0%**

---

## Coverage Delta

| Metric | Pre-RCA (reported) | Pre-RCA (corrected) | Post-Repair (projected) |
|---|---|---|---|
| P0 capabilities in corpus | 12 | 12 | 12 |
| Validly mapped P0 capabilities | 6 (overcounted) | **5** | **6** |
| Unmapped P0 capabilities | 6 (undercounted) | **7** | **6** |
| P0 coverage rate | 50.0% (wrong) | **41.7%** | **50.0%** |
| Delta from repair | — | — | +8.3 pp |

---

## Corpus Quality Score Recalculation

| Dimension | Weight | Corrected Score | Weighted |
|---|---|---|---|
| Ontology consistency (5/7 eval mappings correct; was 1.00) | 0.30 | 0.857 | 0.257 |
| Risk coverage (unchanged) | 0.20 | 0.95 | 0.190 |
| Evaluation coverage (50.7% vs 70% target; was 0.68 normalized) | 0.20 | 0.68 | 0.136 |
| Schema completeness (unchanged) | 0.15 | 1.00 | 0.150 |
| Dependency order validity (unchanged) | 0.15 | 1.00 | 0.150 |
| **Corrected Total** | **1.00** | | **0.883** |

**Corrected Corpus Quality Score: 0.883 / 1.0**
**Previously reported: 0.952**
**Delta: −0.069**
**Primary drag:** ontology consistency reduced from 1.00 → 0.857 (TYPE A collisions)

---

## Priority Evaluation Mapping Gaps (P0, Ranked)

| Priority | CAP-ID | Name | Rationale |
|---|---|---|---|
| 1 | CAP-025 | pii_detection_and_redaction | P0 in CORPUS-001; current mapping is invalid; highest severity mismatch from RCA-002 |
| 2 | CAP-014 | tool_execution | P0 in CORPUS-002; no mapping exists; tool execution is a deployment-critical capability |
| 3 | CAP-011 | self_evaluation | P0 in both entries; no mapping; self-evaluation is the confidence gate before every output |
| 4 | CAP-002 | document_parsing | P0 in CORPUS-001; no mapping |
| 5 | CAP-022 | error_recovery | P0 in CORPUS-001; no mapping |
| 6 | CAP-009 | chain_of_thought_reasoning | P0 in CORPUS-001; no mapping |
| 7 | CAP-013 | tool_selection | P0 in CORPUS-001; no mapping; also an ontology dependency of CAP-014 |
