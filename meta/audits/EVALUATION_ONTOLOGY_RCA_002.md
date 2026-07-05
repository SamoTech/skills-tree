# EVALUATION ONTOLOGY ROOT CAUSE ANALYSIS — RCA-002
**Audit ID:** RCA-002
**Generated:** 2026-07-05
**Scope:** CAP-023 and CAP-025 capability-name mismatches in evaluation_ontology.json
**Constraint:** No ontology modifications. No corpus modifications. Investigation and repair specification only.

---

## Phase 1 — Evidence Collection

### Commit History

The evaluation_ontology.json was introduced in exactly **one commit**:

| Field | Value |
|---|---|
| Commit SHA | `63fc6164b6f22b9ff6b5973e5752584487f28f0a` |
| Commit date | 2026-07-05T12:19:59Z |
| Commit message | `feat(ontology): add evaluation_ontology.json v1 + compatibility audit` |
| Author | Ossama Hashim (SamoTech) |
| Files in commit | `intelligence/ontology/evaluation_ontology.json`, `meta/audits/EVALUATION_ONTOLOGY_COMPATIBILITY.md` |
| Prior commits modifying this file | 0 |

**Finding:** Both mismatches were introduced in the initial creation commit. There is no prior state to compare against — this is not drift from a previously correct version. The mismatches originated at authoring time.

---

## Phase 2 — CAP-023 Root Cause

### Evidence

| Layer | CAP-023 Value |
|---|---|
| capability_ontology.json | `human_in_loop_escalation` |
| evaluation_ontology.json name field | `structured_data_generation` |
| evaluation_ontology.json validation_method | `schema_validation_pipeline` |
| evaluation_ontology.json scoring_model | schema compliance, field accuracy, JSON Schema validation |
| Semantic overlap | Zero — human escalation and structured data generation are unrelated |

### Divergence Point

The evaluation ontology was authored separately from the capability ontology and used a different capability name set when writing the CAP-023 mapping. The `structured_data_generation` concept and the `schema_validation_pipeline` methodology are internally consistent with each other — the evaluation model is coherent for structured data generation. This indicates the mapping block was written for a real capability, but assigned to the wrong CAP-ID.

### Most Likely Explanation

The capability ontology places `structured_output_generation` at **CAP-019** and `human_in_loop_escalation` at **CAP-023**. The evaluation ontology author:
1. Wrote a mapping block for a structured-data/schema-generation capability
2. Assigned it CAP-023 instead of CAP-019
3. Used the label `structured_data_generation` (a near-synonym of `structured_output_generation` / CAP-019)

The likely mechanism: the author had a list of capabilities to map ordered by theme (structured output → escalation) and assigned the structured-data evaluation block to the next ID slot (CAP-023) rather than looking up the canonical ID for `structured_output_generation`.

### Verdict

**AUTHORING ERROR** — The evaluation content was written for a capability similar to CAP-019 (`structured_output_generation`) and incorrectly assigned to CAP-023 (`human_in_loop_escalation`). This is not ontology drift (no prior version existed) and not schema evolution (the schema was not changed).

### Affected Artifacts

| Artifact | Impact |
|---|---|
| `intelligence/ontology/evaluation_ontology.json` | CAP-023 mapping applies wrong evaluation model and wrong capability name |
| `meta/audits/EVALUATION_ONTOLOGY_COMPATIBILITY.md` | Compatibility audit run against defective mapping; conclusions about CAP-023 coverage are invalid |
| `intelligence/corpus/reports/CORPUS_ANALYSIS_V1.md` | Section 6 shows CAP-023 as "✅ Mapped in eval_ontology" — incorrect; mapping applies to wrong capability |
| CI validation workflow | Any gate checking "does CAP-023 have an evaluation mapping?" returns true incorrectly |

---

## Phase 3 — CAP-025 Root Cause

### Evidence

| Layer | CAP-025 Value |
|---|---|
| capability_ontology.json | `pii_detection_and_redaction` |
| evaluation_ontology.json name field | `multi_modal_understanding` |
| evaluation_ontology.json validation_method | `cross_modal_benchmark` |
| evaluation_ontology.json scoring_model | cross-modal extraction accuracy, per-modality accuracy, degradation vs text-only |
| Semantic overlap | Zero — PII detection/redaction and multi-modal understanding are unrelated |

### Divergence Point

Same authoring session as CAP-023. The evaluation ontology was created in a single commit with no iterative revision. The `multi_modal_understanding` concept and `cross_modal_benchmark` methodology are internally consistent — this is a coherent evaluation model written for a real capability but assigned to the wrong CAP-ID.

### Most Likely Explanation

`multi_modal_understanding` does not appear anywhere in the capability_ontology.json under any CAP-ID — it is not a registered capability name. The evaluation author invented or imported this capability concept from an external taxonomy, assigned it CAP-025, and wrote a complete evaluation model for it.

The canonical CAP-025 = `pii_detection_and_redaction`. The required mapping should include precision/recall on PII entity types (person names, emails, phone numbers, financial identifiers), redaction completeness, false negative rate (missed PII), and redaction accuracy (non-PII incorrectly redacted).

### Verdict

**AUTHORING ERROR — UNREGISTERED CAPABILITY INJECTION.** The author wrote an evaluation model for `multi_modal_understanding`, a capability not present in the canonical ontology, and assigned it the CAP-025 slot occupied by `pii_detection_and_redaction`. This is more severe than the CAP-023 mismatch: CAP-023 at least maps to a registered capability (CAP-019); the CAP-025 mapping introduces a capability name with no canonical registration at all.

### Affected Artifacts

| Artifact | Impact |
|---|---|
| `intelligence/ontology/evaluation_ontology.json` | CAP-025 mapping applies wrong evaluation model, wrong capability name, and references an unregistered capability |
| `meta/audits/EVALUATION_ONTOLOGY_COMPATIBILITY.md` | Conclusions about CAP-025 coverage are invalid |
| `intelligence/corpus/reports/CORPUS_ANALYSIS_V1.md` | CAP-025 shown as "✅ Mapped" — incorrect; pii_detection_and_redaction has no valid mapping |
| CI validation | CAP-025 evaluation gate returns true incorrectly for pii_detection_and_redaction |

---

## Phase 4 — Impact Analysis

| Domain | Impact | Severity |
|---|---|---|
| Evaluation coverage metrics | Coverage reported as 7/7 for mapped capabilities. Actual valid coverage: 5/7. P0 coverage overstated. | HIGH |
| Corpus analytics (CORPUS_ANALYSIS_V1.md) | CAP-023 and CAP-025 incorrectly marked as mapped. CORPUS-001 P0 coverage overstated. | HIGH |
| CI validation workflows | CAP-025 is P0 in CORPUS-001 — evaluation gate passes incorrectly, constituting a deployment gate failure | CRITICAL |
| Recommendation engine | Unmapped capability count understated by 2; recommendation priority list incomplete | MEDIUM |
| Architecture readiness / corpus quality score | Quality score inflated; corrected score 0.883 vs reported 0.952 | MEDIUM |
| Execution protocol | Pre-deployment gate references CAP-009 as tool_execution (wrong; CAP-014 is tool_execution) | MEDIUM |

---

## Phase 5 — Repair Specification

**REPAIR NOT APPLIED. Specification only.**

### Repair 1 — CAP-023

| Field | Value |
|---|---|
| Canonical capability | `human_in_loop_escalation` (CAP-023) |
| Current mapping | name: `structured_data_generation`, validation_method: `schema_validation_pipeline` |
| Required correction | Replace mapping with evaluation model for human-in-the-loop escalation: metrics = escalation_decision_accuracy (ET-001), escalation_recall on high-severity inputs (ET-003), false escalation rate (ET-002), latency to escalation decision (ET-005) |
| Files affected | `intelligence/ontology/evaluation_ontology.json` |
| Secondary action | Determine whether `structured_data_generation` content belongs under CAP-019 (`structured_output_generation`) and add that mapping separately |
| Estimated effort | 2–4 hours |
| Migration risk | LOW — CAP-023 is P1; no corpus entry has a hard deployment gate on this evaluation |

### Repair 2 — CAP-025

| Field | Value |
|---|---|
| Canonical capability | `pii_detection_and_redaction` (CAP-025) |
| Current mapping | name: `multi_modal_understanding`, validation_method: `cross_modal_benchmark` |
| Required correction | Replace mapping with evaluation model for PII detection/redaction: metrics = PII entity recall by type (ET-003), false positive rate on non-PII (ET-002), redaction completeness rate (ET-001), safety rate on adversarial PII injection (ET-009) |
| Files affected | `intelligence/ontology/evaluation_ontology.json` |
| Secondary action | Determine whether `multi_modal_understanding` should be registered as a new capability in capability_ontology.json with a new CAP-ID |
| Estimated effort | 4–6 hours (PII taxonomy definition required) |
| Migration risk | HIGH — CAP-025 is P0 in CORPUS-001; once correct evaluation model is in place, CORPUS-001 must be re-evaluated against new thresholds before any deployment gate can pass |

### Repair 3 — Protocol Reference

| Field | Value |
|---|---|
| Current text | `"Run safety gate (ET-009) if CAP-009 (tool_execution) is present"` |
| Required correction | Change `CAP-009 (tool_execution)` to `CAP-014 (tool_execution)` |
| Files affected | `intelligence/ontology/evaluation_ontology.json`, field `evaluation_execution_protocol.pre_deployment_gates[1]` |
| Estimated effort | 5 minutes |
| Migration risk | NONE — text correction only |
