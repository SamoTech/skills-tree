# EVALUATION_ONTOLOGY_RCA_002

**Investigation ID:** RCA-002  
**Generated:** 2026-07-05  
**Status:** COMPLETE  
**Scope:** CAP-023 and CAP-025 name mismatches between evaluation_ontology.json and capability_ontology.json  
**No ontology modifications made. No corpus modifications made. Investigation only.**

---

## SECTION 1: Evaluation Inventory

**Source:** `intelligence/ontology/evaluation_ontology.json` v1.0 (EVAL-ONTOLOGY-001)  
**Full inventory:** see `meta/audits/EVALUATION_ONTOLOGY_INVENTORY.md`  
**Summary:**

| cap_id | name_in_eval_ontology | min_score | validation_method |
|--------|----------------------|-----------|-------------------|
| CAP-001 | text_understanding | 0.87 | three_tier_benchmark |
| CAP-003 | intent_classification | 0.90 | labelled_classification_benchmark |
| CAP-005 | short_term_context_management | 0.88 | multi_turn_coherence_test |
| CAP-017 | response_generation | 0.80 | structured_rubric_human_eval |
| CAP-023 | structured_data_generation | 0.95 | schema_validation_pipeline |
| CAP-025 | multi_modal_understanding | 0.82 | cross_modal_benchmark |
| CAP-028 | output_validation | 0.99 | validation_gate_accuracy_test |

---

## SECTION 2: Detected Mismatches

### Mismatch Summary

| mismatch_id | cap_id | cap_name (canonical) | eval_name (erroneous) | type |
|-------------|--------|----------------------|-----------------------|------|
| M-001 | CAP-023 | human_in_loop_escalation | structured_data_generation | TYPE A |
| M-002 | CAP-025 | pii_detection_and_redaction | multi_modal_understanding | TYPE A |

**TYPE A definition:** Same CAP-ID, different capability name. The eval ontology holds the wrong name for a valid CAP-ID.

### Evidence

**CAP-023:**
- `capability_ontology.json` binding: `"cap_id": "CAP-023", "name": "human_in_loop_escalation", "tier": "execution"`
- `evaluation_ontology.json` binding: `"cap_id": "CAP-023", "name": "structured_data_generation"`
- Purpose gap: Capability purpose is escalation trigger logic. Evaluation methodology is schema compliance pipeline. These are unrelated.
- Ghost name `structured_data_generation` does not exist in `capability_ontology.json` under any CAP-ID.

**CAP-025:**
- `capability_ontology.json` binding: `"cap_id": "CAP-025", "name": "pii_detection_and_redaction", "tier": "safety"`
- `evaluation_ontology.json` binding: `"cap_id": "CAP-025", "name": "multi_modal_understanding"`
- Purpose gap: Capability purpose is PII recall ≥ 0.99 with cross-jurisdiction redaction. Evaluation methodology is cross-modal extraction benchmark. These are unrelated.
- Ghost name `multi_modal_understanding` maps semantically to CAP-004 (`multimodal_perception`), not CAP-025.

---

## SECTION 3: Root Cause Attribution

### Divergence Point

There is exactly **one commit** in the history of `intelligence/ontology/evaluation_ontology.json`:

| Commit SHA | Date | Author | Message |
|-----------|------|--------|----------|
| `63fc6164b6f22b9ff6b5973e5752584487f28f0a` | 2026-07-05T12:19:59Z | Ossama Hashim | feat(ontology): add evaluation_ontology.json v1 + compatibility audit |

Both mismatches were introduced in the **file's initial creation commit**. There is no prior version, no second commit, and no divergence over time. The mismatches were present from line 1 of the file's existence.

The accompanying `EVALUATION_ONTOLOGY_COMPATIBILITY.md` (same commit) incorrectly asserted both CAP-023 and CAP-025 as **COMPATIBLE**, confirming the error was not caught during authoring of the compatibility audit.

---

### CAP-023 Root Cause

**Verdict: COPY/PASTE ERROR**

1. The evaluation benchmark content under CAP-023 (schema_validation_pipeline, JSON Schema compliance, field accuracy) is self-consistent and coherent — it is a complete evaluation for a capability called `structured_data_generation`.
2. `structured_data_generation` is not registered in `capability_ontology.json`. Closest registered name is CAP-019 `structured_output_generation` (communication tier).
3. The CAP-ID `023` was assigned to this evaluation block without verifying which capability `023` resolves to in the canonical ontology. The author either wrote evaluation content first and numerically assigned a CAP-ID, or copied from a draft capability list that predated the final numbering.
4. The canonical CAP-023 (`human_in_loop_escalation`) is correct in all other files — the mismatch is one-directional: `evaluation_ontology.json` is the sole erroneous document.

**Affected reports:** `EVALUATION_ONTOLOGY_COMPATIBILITY.md` (incorrectly marked COMPATIBLE), `CORPUS_ANALYSIS_V1.md` (evaluation coverage inflated)  
**Affected workflows:** Pre-deployment gate for agents requiring `human_in_loop_escalation` — no valid evaluation exists. Schema compliance gate for `structured_data_generation` — unanchored.

---

### CAP-025 Root Cause

**Verdict: COPY/PASTE ERROR**

1. The evaluation benchmark content under CAP-025 (cross_modal_benchmark, per-modality accuracy, degradation vs text-only) is self-consistent — it is a complete evaluation for `multi_modal_understanding` / `multimodal_perception`.
2. `multi_modal_understanding` is not registered in `capability_ontology.json`. Closest registered name is CAP-004 `multimodal_perception` (perception tier). The evaluation content semantically matches CAP-004's purpose.
3. The canonical CAP-025 (`pii_detection_and_redaction`) has a completely orthogonal evaluation domain: PII recall, false positive rate, cross-jurisdiction coverage. None of these dimensions appear in the evaluation block committed under CAP-025.
4. Same authoring error pattern as CAP-023: evaluation content authored for an unregistered name, committed under a numerically selected CAP-ID that resolves to a different capability in the canonical ontology.

**Affected reports:** `EVALUATION_ONTOLOGY_COMPATIBILITY.md` (incorrectly marked COMPATIBLE), `CORPUS_ANALYSIS_V1.md` (evaluation coverage inflated)  
**Affected workflows:** Pre-deployment safety gate for `pii_detection_and_redaction` — no valid PII evaluation exists. Multimodal evaluation (CAP-004) — content exists but unanchored.

---

## SECTION 4: Impact Analysis

| Dimension | CAP-023 Impact | CAP-025 Impact | Combined |
|-----------|---------------|---------------|----------|
| Evaluation coverage metrics | Coverage overcounted by 1/7 entries | Coverage overcounted by 1/7 entries | 2 of 7 mapped capabilities are phantom |
| Corpus analytics | CAP-023 listed as eval-mapped; human_in_loop_escalation has zero real coverage | CAP-025 listed as eval-mapped; pii_detection_and_redaction has zero real coverage | Coverage gap in CORPUS_ANALYSIS_V1 understated |
| Validation workflows | Agents requiring CAP-023 pass pre-deployment gate without valid evaluation | Agents requiring CAP-025 (PII safety) pass gate without valid PII evaluation | Deployment gate structurally bypassed for both |
| Recommendation engine | CAP-023 not recommended for new evaluation (appears covered) | CAP-025 not recommended (appears covered) | Four capability evaluation gaps misrepresented |
| Architecture readiness | human_in_loop_escalation readiness unverifiable | pii_detection_and_redaction readiness unverifiable — safety-tier capability | Safety tier evaluation integrity compromised |

### Severity Classification

| Mismatch | Severity | Rationale |
|----------|----------|-----------|
| CAP-023 (human_in_loop_escalation has no valid evaluation) | **HIGH** | Execution-tier capability; escalation behavior cannot be deployment-gated |
| CAP-025 (pii_detection_and_redaction has no valid evaluation) | **CRITICAL** | Safety-tier capability; PII recall ≥ 0.99 requirement exists but zero evaluation methodology; any agent with CAP-025 required passes the evaluation gate without a valid PII benchmark |
| CAP-004 (multimodal_perception) evaluation unanchored | **MEDIUM** | Valid evaluation content exists under wrong ID; not deployed to corpus yet |
| CAP-019 (structured_output_generation) evaluation unanchored | **MEDIUM** | Valid evaluation content exists under wrong ID; not deployed to corpus yet |

---

## SECTION 5: Repair Specification

**DO NOT APPLY. Specification only.**

### Repair R-001: CAP-023

| Field | Current State | Required Correction |
|-------|--------------|---------------------|
| File | `intelligence/ontology/evaluation_ontology.json` | Same |
| CAP-ID in mapping | `CAP-023` | Retain `CAP-023` |
| name in mapping | `structured_data_generation` | Change to `human_in_loop_escalation` |
| evaluation_model | schema_validation_pipeline (JSON compliance) | Replace with escalation calibration benchmark: escalation decision accuracy vs. human judgment on 200 cases; false escalation rate ≤ 15%; missed escalation rate ≤ 5%; latency ≤ 5s |
| primary_metrics | ET-001, ET-007, ET-008 | ET-003 (recall), ET-002 (precision), ET-005 (latency) |
| min_required_score | 0.95 | ~0.85 (escalation calibration) |
| validation_method | schema_validation_pipeline | escalation_calibration_benchmark |

The evaluation content currently under CAP-023 (schema validation) should be re-homed to a CAP-019 mapping or held pending registration of `structured_data_generation` as a new capability.

**Files affected:** `evaluation_ontology.json`, `EVALUATION_ONTOLOGY_COMPATIBILITY.md`  
**Estimated effort:** 2 hours  
**Migration risk:** LOW — CAP-023 not yet used in any corpus evaluation requirement

---

### Repair R-002: CAP-025

| Field | Current State | Required Correction |
|-------|--------------|---------------------|
| File | `intelligence/ontology/evaluation_ontology.json` | Same |
| CAP-ID in mapping | `CAP-025` | Retain `CAP-025` |
| name in mapping | `multi_modal_understanding` | Change to `pii_detection_and_redaction` |
| evaluation_model | cross_modal_benchmark (modality accuracy) | Replace with PII evaluation benchmark: recall ≥ 0.99 on synthetic PII test set; false positive rate ≤ 5%; cross-jurisdiction coverage (US, EU, APAC); edge case test (embedded PII, reformatted PII, PII in code) |
| primary_metrics | ET-001, ET-008, ET-012 | ET-003 (recall, primary), ET-002 (precision), ET-009 (safety) |
| min_required_score | 0.82 | 0.99 (recall is the critical metric per cap_ontology notes) |
| validation_method | cross_modal_benchmark | pii_recall_benchmark |

The evaluation content currently under CAP-025 (cross-modal benchmark) should be re-homed to a CAP-004 mapping entry.

**Files affected:** `evaluation_ontology.json`, `EVALUATION_ONTOLOGY_COMPATIBILITY.md`  
**Estimated effort:** 2 hours  
**Migration risk:** MEDIUM — CAP-025 is safety-tier; repair required before first `security_agent` or `assistant_agent` corpus entry

---

### Optional Repair R-003: Re-home Ghost Evaluations

| Ghost Name | Current Location | Correct Location |
|------------|-----------------|------------------|
| structured_data_generation | CAP-023 (wrong) | New CAP-019 mapping or new capability registration |
| multi_modal_understanding | CAP-025 (wrong) | New CAP-004 mapping (rename to `multimodal_perception`) |

**Files affected:** `evaluation_ontology.json`  
**Estimated effort:** 1 hour  
**Migration risk:** LOW

---

## SECTION 6: P0 Coverage Reassessment

**Full detail:** see `meta/audits/P0_EVALUATION_COVERAGE_REASSESSMENT.md`

### P0 Capabilities Across Corpus

| cap_id | name | P0 in corpus | Eval mapped | Mapping valid |
|--------|------|-------------|-------------|---------------|
| CAP-001 | text_understanding | ✅ both | ✅ | ✅ |
| CAP-003 | intent_classification | ✅ both | ✅ | ✅ |
| CAP-005 | short_term_context_management | ✅ both | ✅ | ✅ |
| CAP-017 | response_generation | ✅ both | ✅ | ✅ |
| CAP-028 | output_validation | ✅ both | ✅ | ✅ |
| CAP-007 | semantic_retrieval | ✅ CORPUS-001 | ❌ | N/A |
| CAP-014 | tool_execution | ✅ CORPUS-002 | ❌ | N/A |
| CAP-011 | self_evaluation | ✅ CORPUS-002 | ❌ | N/A |

| Coverage metric | Before repair | After R-001+R-002 | After +CAP-007,011,014 |
|----------------|--------------|-------------------|------------------------|
| P0 coverage | 62.5% (5/8) | 62.5% (5/8) | 100% (8/8) |
| Total valid coverage | 17.9% (5/28) | 25.0% (7/28) | 28.6% (8/28) |
| Phantom mappings | 2 | 0 | 0 |

---

## SECTION 7: Repository Risk Level

| Risk Dimension | Level | Evidence |
|----------------|-------|----------|
| Evaluation data integrity | **HIGH** | 2 of 7 eval mappings are phantom — 28.6% of the evaluation ontology is mis-mapped |
| Safety evaluation coverage | **CRITICAL** | CAP-025 (`pii_detection_and_redaction`) is safety-tier with zero valid evaluation; any PII agent passes deployment gate without a PII benchmark |
| Execution evaluation coverage | **HIGH** | CAP-023 (`human_in_loop_escalation`) escalation behavior cannot be evaluated against canonical definition |
| Compatibility audit trustworthiness | **HIGH** | `EVALUATION_ONTOLOGY_COMPATIBILITY.md` declared both mismatches COMPATIBLE — must be re-issued after repair |
| Corpus analytics accuracy | **MEDIUM** | CORPUS_ANALYSIS_V1 evaluation coverage metrics inflated by 2 phantom mappings |
| Overall evaluation readiness | **HIGH** | True valid coverage is 17.9% (5/28), not 25.0% (7/28) as previously reported |

**Repository risk level: HIGH**  
Blocker for any deployment requiring `pii_detection_and_redaction` (CAP-025). Repairs R-001 and R-002 must be executed before the evaluation ontology can serve as a deployment gate authority.

---

## SECTION 8: Files Created

| File | Path |
|------|------|
| Evaluation inventory | `meta/audits/EVALUATION_ONTOLOGY_INVENTORY.md` |
| Consistency audit | `meta/audits/EVALUATION_ONTOLOGY_CONSISTENCY_AUDIT.md` |
| P0 coverage reassessment | `meta/audits/P0_EVALUATION_COVERAGE_REASSESSMENT.md` |
| RCA report | `meta/audits/EVALUATION_ONTOLOGY_RCA_002.md` |
