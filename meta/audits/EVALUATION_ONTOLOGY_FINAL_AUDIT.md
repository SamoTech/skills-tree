# EVALUATION_ONTOLOGY_FINAL_AUDIT

**Workstream:** A — Evaluation Ontology Integrity  
**Sprint:** Phase 2 — Repository Maturity Sprint  
**Generated:** 2026-07-05  
**Status:** COMPLETE  
**Preceding Work:** RCA-002 (meta/audits/EVALUATION_ONTOLOGY_RCA_002.md)  
**Constraint:** No ontology modifications. No corpus modifications. Audit and correction mappings only.

---

## SECTION 1: Executive Summary

RCA-002 confirmed two TYPE A mismatches — same CAP-ID, wrong capability name — in `intelligence/ontology/evaluation_ontology.json`. Both were introduced in the file's initial commit and were incorrectly declared COMPATIBLE in the accompanying `EVALUATION_ONTOLOGY_COMPATIBILITY.md`.

This final audit documents:
1. The corrected mappings required to resolve both mismatches
2. Validation evidence confirming what the correct bindings must be
3. Full impact across all downstream documents, workflows, and coverage metrics
4. Residual risks after correction

---

## SECTION 2: Mismatch Registry (Final)

| Mismatch ID | CAP-ID | Canonical Name (capability_ontology.json) | Wrong Name (evaluation_ontology.json) | Severity | Status |
|-------------|--------|------------------------------------------|---------------------------------------|----------|--------|
| M-001 | CAP-023 | `human_in_loop_escalation` | `structured_data_generation` | HIGH | REQUIRES CORRECTION |
| M-002 | CAP-025 | `pii_detection_and_redaction` | `multi_modal_understanding` | CRITICAL | REQUIRES CORRECTION |

---

## SECTION 3: Corrected Mappings

### Correction C-001 — CAP-023

**File:** `intelligence/ontology/evaluation_ontology.json`  
**Change:** Replace name field for CAP-023 entry

| Field | Current (Erroneous) | Corrected |
|-------|--------------------|-----------|
| `name` | `structured_data_generation` | `human_in_loop_escalation` |
| `evaluation_model` | `schema_validation_pipeline` | `escalation_calibration_benchmark` |
| `primary_metrics` | ET-001, ET-007, ET-008 | ET-003, ET-002, ET-005 |
| `min_required_score` | 0.95 | 0.85 |
| `validation_method` | `schema_validation_pipeline` | `escalation_calibration_benchmark` |
| `tier` | (implicit) | execution |

**Validation Evidence:**
- `capability_ontology.json` unambiguously assigns `human_in_loop_escalation` to CAP-023 with tier `execution`
- The current evaluation content (schema compliance, JSON field accuracy) is semantically unrelated to escalation decision logic
- CAP-023 is **not P0** in any current corpus entry — migration risk is LOW
- Ghost name `structured_data_generation` must be re-homed to CAP-019 mapping or held pending capability registration

**Disposition of ghost evaluation content:**  
The `schema_validation_pipeline` evaluation block currently attached to CAP-023 should be preserved and re-homed to a CAP-019 entry (`structured_output_generation`) as an optional enhancement. It must not be deleted.

---

### Correction C-002 — CAP-025

**File:** `intelligence/ontology/evaluation_ontology.json`  
**Change:** Replace name field for CAP-025 entry

| Field | Current (Erroneous) | Corrected |
|-------|--------------------|-----------|
| `name` | `multi_modal_understanding` | `pii_detection_and_redaction` |
| `evaluation_model` | `cross_modal_benchmark` | `pii_recall_benchmark` |
| `primary_metrics` | ET-001, ET-008, ET-012 | ET-003, ET-002, ET-009 |
| `min_required_score` | 0.82 | 0.99 |
| `validation_method` | `cross_modal_benchmark` | `pii_recall_benchmark` |
| `tier` | (implicit) | safety |

**Validation Evidence:**
- `capability_ontology.json` unambiguously assigns `pii_detection_and_redaction` to CAP-025 with tier `safety`
- PII recall ≥ 0.99 requirement exists in capability notes; the current 0.82 threshold is for cross-modal extraction, not PII recall — these are different tasks with different acceptable error rates
- CAP-025 is **safety-tier** — this is the most critical correction in the sprint. Any agent requiring CAP-025 currently passes the deployment evaluation gate without a valid PII benchmark
- Ghost name `multi_modal_understanding` maps semantically to CAP-004 (`multimodal_perception`) and must be re-homed there

**Disposition of ghost evaluation content:**  
The `cross_modal_benchmark` evaluation block currently attached to CAP-025 should be re-homed to a CAP-004 entry (`multimodal_perception`). This content is complete and valid — it is only attached to the wrong CAP-ID.

---

## SECTION 4: Validation Evidence Matrix

| Evidence Source | CAP-023 Confirms Correction | CAP-025 Confirms Correction |
|----------------|----------------------------|-----------------------------|
| `capability_ontology.json` CAP-ID → name binding | ✅ canonical name = `human_in_loop_escalation` | ✅ canonical name = `pii_detection_and_redaction` |
| Capability tier in ontology | ✅ tier = execution | ✅ tier = safety |
| Evaluation content semantic fit to current name | ❌ schema pipeline ≠ escalation logic | ❌ cross-modal extraction ≠ PII detection |
| Ghost name registered in ontology | ❌ `structured_data_generation` not in capability_ontology | ❌ `multi_modal_understanding` not in capability_ontology |
| Ghost name semantic match to another valid CAP-ID | CAP-019 `structured_output_generation` (similar) | CAP-004 `multimodal_perception` (exact semantic match) |
| P0 corpus exposure | CAP-023 not P0 — LOW deployment risk | CAP-025 not currently P0 — but safety-tier, CRITICAL risk regardless |
| RCA finding | M-001 COPY/PASTE ERROR | M-002 COPY/PASTE ERROR |

---

## SECTION 5: Impact Report

### Documents Requiring Re-issue After Correction

| Document | Current State | Required Update |
|----------|--------------|------------------|
| `meta/audits/EVALUATION_ONTOLOGY_COMPATIBILITY.md` | Incorrectly marks CAP-023, CAP-025 as COMPATIBLE | Must be re-issued as MISMATCH after correction is applied |
| `meta/audits/POST_REMEDIATION_CONSISTENCY_CHECK.md` | May reference phantom names | Must be reviewed and updated |
| Any CORPUS_ANALYSIS reports citing evaluation coverage | Overcounts coverage by 2/7 (28.6% phantom rate) | Must be recalculated after repair |

### Workflow Impact

| Workflow | Impact Before Correction | Impact After Correction |
|----------|-------------------------|-------------------------|
| Pre-deployment gate for `human_in_loop_escalation` (CAP-023) | No valid evaluation exists; gate structurally bypassed | Escalation calibration benchmark activated |
| Pre-deployment safety gate for `pii_detection_and_redaction` (CAP-025) | No valid PII evaluation; safety gate bypassed — CRITICAL | PII recall benchmark activated; min_score 0.99 enforced |
| `validate-evaluations.yml` (new, Workstream C) | Would immediately flag both mismatches | Would pass after correction |

### Coverage Metric Impact

| Metric | Before Repair | After Repair |
|--------|-------------|-------------|
| Total evaluation mappings | 7 | 7 (count unchanged) |
| Valid evaluation mappings | 5 | 7 (+2) |
| Phantom mappings | 2 | 0 |
| Total valid coverage (7/28) | 17.9% | 25.0% |
| P0 coverage | 62.5% (5/8) | 62.5% (unchanged — P0 gap is in CAP-007, 011, 014) |
| Safety-tier evaluation integrity | ❌ BROKEN | ✅ RESTORED |

---

## SECTION 6: Residual Risks After Correction

| Risk | Level | Mitigation |
|------|-------|------------|
| Ghost evaluation content (schema_validation, cross_modal) not re-homed | MEDIUM | Execute optional Repair R-003 (RCA-002, Section 5) |
| P0 capabilities CAP-007, CAP-011, CAP-014 still unmapped | HIGH | Workstream B actions required |
| `EVALUATION_ONTOLOGY_COMPATIBILITY.md` not yet updated | MEDIUM | Re-issue after correction applied |
| Correction not yet applied to `evaluation_ontology.json` | **BLOCKER** | Apply C-001 and C-002 before next deployment gate run |

---

## SECTION 7: Audit Verdict

| Item | Status |
|------|--------|
| Root cause identified | ✅ COPY/PASTE ERROR (both mismatches, initial commit only) |
| Corrected mappings specified | ✅ C-001 (CAP-023), C-002 (CAP-025) |
| Validation evidence documented | ✅ 7-point evidence matrix per mismatch |
| Impact report complete | ✅ Documents, workflows, and metrics assessed |
| Ghost content disposition specified | ✅ Re-home to CAP-019 and CAP-004 |
| Corrections applied to source file | ❌ PENDING — not in scope of this audit sprint |

**Overall Evaluation Ontology Integrity: REQUIRES REPAIR — specifications complete, application pending.**

---

*Generated: 2026-07-05. Evidence: repository state at commit `0752a72afcb2d659dc0219ec1d385840b7e69186`.*  
*Supersedes: EVALUATION_ONTOLOGY_RCA_002.md (remains valid as evidence source)*
