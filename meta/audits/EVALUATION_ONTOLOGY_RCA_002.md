# EVALUATION ONTOLOGY ROOT CAUSE ANALYSIS — RCA-002
**Report ID:** RCA-002  
**Generated:** 2026-07-05  
**Trigger:** Known capability-name mismatches in `evaluation_ontology.json` for CAP-023 and CAP-025  
**Authority:** `capability_ontology.json` (SHA: 5cdcd58d2c3f56a66b883c41e96d79499fb576d0)  
**Investigator:** Automated RCA engine  
**Modifications to ontologies:** NONE — investigation only  

---

## Phase 1 — Evaluation Inventory Reference

See `meta/audits/EVALUATION_ONTOLOGY_INVENTORY.md` for complete extraction of all 7 evaluation mappings with full benchmark methodologies, thresholds, and metrics.

---

## Phase 2 — Mismatch Summary

Two primary TYPE A mismatches confirmed (same CAP-ID, different capability name):

| CAP-ID | Canonical Name | Eval Ontology Name | Benchmark Applicability |
|---|---|---|---|
| CAP-023 | human_in_loop_escalation | structured_data_generation | 0% — schema validation is inapplicable to escalation routing |
| CAP-025 | pii_detection_and_redaction | multi_modal_understanding | 0% — cross-modal benchmark is inapplicable to PII detection |

One inline TYPE A reference error:

| Location | Content | Error |
|---|---|---|
| `evaluation_execution_protocol.pre_deployment_gates[1]` | `CAP-009 (tool_execution)` | CAP-009 = chain_of_thought_reasoning; tool_execution = CAP-014 |

---

## Phase 3 — Root Cause Analysis

### RCA for CAP-023 Mismatch

**First evidence point:**  
`evaluation_ontology.json` was created as a single authoring event on 2026-07-05 (as recorded by `created_at` and `last_reviewed_at` fields). There is no commit history showing a divergence from a previously correct state — this is an original authoring error, not a drift event.

**Mechanism:**  
The capability ontology registers 28 capabilities with sequential IDs. CAP-023 = `human_in_loop_escalation`. The evaluation ontology author appears to have written the benchmark content for `structured_data_generation` and then assigned it the wrong CAP-ID. The validation_method `schema_validation_pipeline` and the benchmark focus on JSON schema compliance, field accuracy, and hallucination rate within structured fields are precisely correct for a structured generation capability — but are completely inapplicable to an escalation routing capability.

**Most probable origin:**  
The evaluation mappings were authored in a different ordering than the canonical CAP-ID sequence. `structured_data_generation` was likely intended to map to CAP-019 (`structured_output_generation` — the nearest canonical equivalent), but was incorrectly assigned CAP-023. The capability `structured_data_generation` does not exist under that name in capability_ontology.json.

**Secondary evidence:**  
The benchmark threshold of 0.95 minimum score and `schema_compliance >= 0.99` are both consistent with a structured output evaluation. No element of the benchmark is consistent with human escalation routing (which would require precision/recall on escalation trigger classification, false escalation rate analysis, and escalation latency measurement).

**Verdict: AUTHORING ERROR + COPY/PASTE ERROR**  
The benchmark content was authored for the correct semantic purpose (structured output evaluation) but assigned to the wrong CAP-ID. The CAP-023 entry in the evaluation ontology is a misplaced block that belongs at CAP-019 or under a newly registered `structured_data_generation` capability ID.

**Affected reports:**  
- `CORPUS_ANALYSIS_V1.md` Section 6 marks CAP-023 as having no evaluation coverage — this is correct from the canonical perspective (CAP-023 = human_in_loop_escalation has no valid evaluation), but the existing mismapped entry would falsely indicate coverage in any automated tool that resolves by CAP-ID without name validation.
- Any validation workflow that checks "does CAP-023 have an evaluation mapping" returns TRUE — but the evaluation it resolves to is semantically invalid.

**Affected workflows:**  
- Corpus validation CI: if it checks only CAP-ID existence in evaluation_ontology, it reports CAP-023 as covered — false positive.
- Evaluation coverage metrics in CORPUS_ANALYSIS_V1.md: CAP-023 is listed as having no evaluation (correct); the mismapped entry is not currently used by any corpus entry.
- Architecture readiness score: if CAP-023 is added to a future corpus entry, the wrong benchmark will be applied.

---

### RCA for CAP-025 Mismatch

**First evidence point:**  
Same single-authoring-event origin as CAP-023 mismatch. No prior correct state to diverge from.

**Mechanism:**  
CAP-025 = `pii_detection_and_redaction`. The evaluation ontology maps CAP-025 to `multi_modal_understanding` with a `cross_modal_benchmark` validation method covering image/chart/diagram extraction accuracy. `multi_modal_understanding` has no CAP-ID in the canonical ontology — it is an unregistered capability name.

**Most probable origin:**  
The author maintained a parallel working list of capabilities not yet registered in capability_ontology.json (including `multi_modal_understanding`) and mistakenly assigned this unregistered capability's benchmark to CAP-025. The intended target was either (a) a new capability `multi_modal_understanding` that was never registered, or (b) the benchmark was written speculatively for future use and incorrectly anchored to an existing CAP-ID.

**Secondary evidence:**  
PII detection evaluation requires: named entity recognition (NER) recall on PII entity types, redaction correctness rate, false negative rate (PII present but not redacted), and false positive rate (non-PII redacted). None of these appear in the CAP-025 evaluation mapping. The cross_modal_benchmark methodology is consistent with a vision or document understanding capability and bears no relationship to privacy detection.

**Additionally:** The evaluation_ontology's `evaluation_execution_protocol.pre_deployment_gates` step 2 reads: *"Run safety gate (ET-009) if CAP-009 (tool_execution) is present"* — but CAP-009 = `chain_of_thought_reasoning` in the canonical ontology. Tool execution is CAP-014. This is a third authoring error in the same document, reinforcing that the evaluation_ontology was authored with an out-of-sync or pre-remediation capability ID reference sheet.

**Verdict: AUTHORING ERROR — Unregistered capability benchmark incorrectly anchored to existing CAP-ID**  
The benchmark content for an unregistered `multi_modal_understanding` capability was written and then assigned CAP-025 (pii_detection_and_redaction) in error. The capability `multi_modal_understanding` should have been registered in capability_ontology.json before being mapped in evaluation_ontology.json.

**Affected reports:**  
- `CORPUS_ANALYSIS_V1.md` Section 6 shows CAP-025 evaluation as "✅ Mapped in eval_ontology" based on ID-only lookup. This is a FALSE POSITIVE — the mapping exists by ID but is semantically invalid.
- Any system checking "is CAP-025 evaluated?" by ID returns TRUE incorrectly.

**Affected workflows:**  
- Corpus validation CI: if checking by CAP-ID presence, reports CAP-025 as covered — false positive.
- CORPUS-001 uses CAP-025 (pii_detection_and_redaction) as a P0 capability. The currently mapped evaluation benchmark (cross_modal_benchmark) cannot be used to validate PII detection performance. This means CORPUS-001's P0 evaluation requirement for CAP-025 has no valid benchmark, and the architecture readiness score computed in prior reports is inflated.

---

## Phase 4 — Impact Analysis

### Impact by Category

| Category | Impact | Severity |
|---|---|---|
| **Evaluation coverage metrics** | CAP-025 is falsely reported as covered. CAP-023 is correctly reported as uncovered in CORPUS_ANALYSIS_V1.md but would be falsely covered in any ID-only lookup system. Effective P0 coverage drops from 54.5% (ID-only) to 45.5% (name-validated) when mismatches are excluded. | HIGH |
| **Corpus analytics** | CORPUS_ANALYSIS_V1.md Section 6 marks CAP-025 as "✅ Mapped in eval_ontology" — this is false. The entry for CAP-025 is for `multi_modal_understanding`, not `pii_detection_and_redaction`. Corpus Quality Score (0.952) is inflated by ~0.010. Corrected score: 0.942. | HIGH |
| **Validation workflows** | Any automated CI check that validates corpus entries by resolving cap_id → evaluation_ontology by ID only will incorrectly report CAP-023 and CAP-025 as having valid evaluations. The validator must be extended to check name consistency, not just ID existence. | HIGH |
| **Recommendation engine assumptions** | CORPUS_ANALYSIS_V1.md Recommendation #5 suggests a Compliance Audit Agent using CAP-025 as primary. Any such agent will currently be evaluated with a cross-modal benchmark — an incorrect methodology. | MEDIUM |
| **Architecture readiness score** | CORPUS-001 declares CAP-025 as P0. The evaluation_ontology is supposed to provide its benchmark. It currently provides a semantically invalid benchmark. Architecture readiness for CORPUS-001 is overstated. | HIGH |

### Severity Summary

| Finding | Severity |
|---|---|
| CAP-025 mapped to wrong benchmark — affects CORPUS-001 P0 evaluation | HIGH |
| CAP-023 mapped to wrong benchmark — no corpus entry currently affected, but any future use will be incorrectly validated | HIGH |
| Inline protocol error (CAP-009 vs CAP-014) — affects safety gate triggering logic documentation | MEDIUM |
| TYPE D gaps (18 unmapped capabilities) — evaluation coverage 17.9% | HIGH |

---

## Phase 5 — Repair Specification

**NOTE: No fixes are applied in this document. Specification only.**

### Repair 1 — CAP-023 Evaluation Mapping

| Field | Value |
|---|---|
| **Canonical capability** | CAP-023 = `human_in_loop_escalation` |
| **Current mapping** | `structured_data_generation` — schema_validation_pipeline benchmark at 0.95 threshold |
| **Required correction** | Replace the `capability_evaluation_mappings` entry for CAP-023 with a benchmark appropriate for human escalation routing: classification-based evaluation of escalation trigger accuracy (ET-001, ET-002, ET-003), false escalation rate, and escalation latency (ET-005) |
| **Disposition of current content** | The existing `structured_data_generation` benchmark content at CAP-023 should be relocated. If `structured_data_generation` is intended as a capability, register it in capability_ontology.json and assign it the next available CAP-ID. If it maps to CAP-019 (`structured_output_generation`), relocate the benchmark to CAP-019. |
| **Files affected** | `intelligence/ontology/evaluation_ontology.json` only |
| **Estimated effort** | 2–4 hours: write escalation routing evaluation benchmark, relocate structured_data_generation content, update cross-references |
| **Migration risk** | LOW — CAP-023 is not currently present in any corpus entry as the primary evaluated capability. No existing corpus evaluation_requirements reference this mapping. |

### Repair 2 — CAP-025 Evaluation Mapping

| Field | Value |
|---|---|
| **Canonical capability** | CAP-025 = `pii_detection_and_redaction` |
| **Current mapping** | `multi_modal_understanding` — cross_modal_benchmark at 0.82 threshold |
| **Required correction** | Replace the `capability_evaluation_mappings` entry for CAP-025 with a PII-detection benchmark: NER recall on PII entity types (ET-003), redaction correctness (ET-001), false negative rate (missed PII), false positive rate (over-redaction), and compliance with data category requirements |
| **Disposition of current content** | Register `multi_modal_understanding` in capability_ontology.json with a new CAP-ID (next available after CAP-028), then relocate the cross_modal_benchmark content to that new entry |
| **Files affected** | `intelligence/ontology/evaluation_ontology.json` (primary), `intelligence/ontology/capability_ontology.json` (to register multi_modal_understanding) |
| **Estimated effort** | 4–6 hours: write PII detection benchmark, register new capability, relocate cross-modal content, validate CORPUS-001 evaluation_requirements resolve correctly |
| **Migration risk** | MEDIUM — CORPUS-001 uses CAP-025 as P0 with a declared evaluation requirement. After correction, the evaluation benchmark changes; CORPUS-001's evaluation methodology must be re-verified. |

### Repair 3 — Inline Protocol Reference Error

| Field | Value |
|---|---|
| **Location** | `evaluation_execution_protocol.pre_deployment_gates[1]` |
| **Current text** | `"Run ET-009 (safety) gate if CAP-009 (tool_execution) is present"` |
| **Required correction** | Change `CAP-009 (tool_execution)` to `CAP-014 (tool_execution)` |
| **Files affected** | `intelligence/ontology/evaluation_ontology.json` only |
| **Estimated effort** | 5 minutes — single string substitution |
| **Migration risk** | NEGLIGIBLE — inline documentation string only; no tooling currently parses this field for CAP-ID routing |

---

## Phase 6 — P0 Coverage Recalculation

See `meta/audits/P0_EVALUATION_COVERAGE_REASSESSMENT.md` for full calculation.

Summary:
- **Pre-repair (ID-only, false positive included):** 6 / 11 corpus-active P0s = 54.5%
- **Post-RCA corrected (name-validated):** 5 / 11 corpus-active P0s = 45.5%
- **Post-repair projected:** 6 / 11 corpus-active P0s = 54.5% (recovered, now accurate)

---

## Verdict Summary

| Mismatch | Root Cause | Confidence |
|---|---|---|
| CAP-023 → structured_data_generation | Authoring error: benchmark written for wrong capability, incorrect CAP-ID assignment | HIGH |
| CAP-025 → multi_modal_understanding | Authoring error: unregistered capability benchmark anchored to existing CAP-ID | HIGH |
| Protocol reference CAP-009 as tool_execution | Copy/paste error from pre-remediation ontology state | HIGH |

All three errors originate in the initial authoring of `evaluation_ontology.json`. No evidence of ontology drift (no prior correct state exists to drift from). Classification: **AUTHORING ERROR** for all three findings.

---

*No modifications made to any ontology file. This document is investigation output only.*
