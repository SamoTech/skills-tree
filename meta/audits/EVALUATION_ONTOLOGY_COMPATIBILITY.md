# Evaluation Ontology Compatibility Report

**Generated:** 2026-07-05  
**Ontology version audited:** EVAL-ONTOLOGY-001 v1.0  
**Files cross-checked:**
- `intelligence/ontology/capability_ontology.json`
- `intelligence/ontology/goal_ontology.json`
- `intelligence/corpus/entries/support/CORPUS-001.json`
- `intelligence/corpus/entries/engineering/CORPUS-002.json`

---

## 1. Compatible Capabilities

The following capabilities have full evaluation mappings in `evaluation_ontology.json` and are referenced correctly across all checked files.

| CAP ID | Name | Mapped in Eval Ontology | Used in Corpus | Used in Goal Ontology | Status |
|--------|------|-----------------------|----------------|----------------------|--------|
| CAP-001 | text_understanding | ✅ Full model (3-tier) | CORPUS-001, CORPUS-002 (P0 both) | 12/12 goal classes | **COMPATIBLE** |
| CAP-003 | intent_classification | ✅ Full model | CORPUS-001, CORPUS-002 (P0 both) | 10/12 goal classes | **COMPATIBLE** |
| CAP-005 | short_term_context_management | ✅ Full model | CORPUS-001, CORPUS-002 (P0 both) | 11/12 goal classes | **COMPATIBLE** |
| CAP-017 | response_generation | ✅ Full model (rubric) | CORPUS-001, CORPUS-002 (P0 both) | 12/12 goal classes | **COMPATIBLE** |
| CAP-023 | structured_data_generation | ✅ Full model | Not in current corpus | workflow_agent (optional) | **COMPATIBLE — no corpus use yet** |
| CAP-025 | multi_modal_understanding | ✅ Full model | Not in current corpus | Not in goal_ontology | **COMPATIBLE — no corpus or goal use yet** |
| CAP-028 | output_validation | ✅ Full model | CORPUS-001, CORPUS-002 (P0 both) | 10/12 goal classes | **COMPATIBLE** |

---

## 2. Missing Mappings

The following capabilities appear in corpus entries or goal_ontology.json but have **no entry in evaluation_ontology.json**.

| CAP ID | Name | Appears In | Missing From | Gap Severity |
|--------|------|------------|--------------|-------------|
| CAP-006 | long_term_memory_storage | CORPUS-001 (P1), CORPUS-002 (P1), goal_ontology (assistant_agent required) | evaluation_ontology capability_mappings | **Medium** |
| CAP-007 | semantic_retrieval | CORPUS-001 (P0), CORPUS-002 (P1), goal_ontology (support_agent required) | evaluation_ontology capability_mappings | **Medium** |
| CAP-008 | episodic_memory | CORPUS-001 (P2), CORPUS-002 (P2) | evaluation_ontology capability_mappings | **Low** |
| CAP-009 | tool_execution | CORPUS-002 (P0), goal_ontology (8 goal classes required) | evaluation_ontology capability_mappings | **High** |
| CAP-011 | self_evaluation | CORPUS-001 (P1), CORPUS-002 (P0), goal_ontology (7 goal classes required) | evaluation_ontology capability_mappings | **High** |
| CAP-014 | planning_and_decomposition | CORPUS-002 (P1), goal_ontology (autonomous_agent required) | evaluation_ontology capability_mappings | **Medium** |
| CAP-026 | hallucination_detection | CORPUS-001 (P1), CORPUS-002 (P2), goal_ontology (evaluation_agent required) | evaluation_ontology capability_mappings | **High** |

**Summary:** 7 capabilities used in the corpus and goal ontology have no evaluation mapping in v1.0. CAP-009, CAP-011, and CAP-026 are High-severity gaps because they are required capabilities in multiple goal classes with active corpus entries.

---

## 3. Evaluation Type Coverage

All 12 evaluation types (ET-001 through ET-012) defined in `evaluation_ontology.json` are valid and self-consistent. The following table maps which types are currently used in capability mappings.

| Eval Type | Name | Used in Mappings | Coverage |
|-----------|------|-----------------|----------|
| ET-001 | accuracy | CAP-001, CAP-003, CAP-005, CAP-023, CAP-025, CAP-028 | 6/7 mappings |
| ET-002 | precision | CAP-003, CAP-028 | 2/7 mappings |
| ET-003 | recall | CAP-003, CAP-028 | 2/7 mappings |
| ET-004 | f1_score | CAP-003 | 1/7 mappings |
| ET-005 | latency | CAP-001, CAP-005, CAP-017, CAP-023, CAP-025 | 5/7 mappings |
| ET-006 | cost | CAP-017, CAP-023, CAP-025 | 3/7 mappings |
| ET-007 | reliability | CAP-005, CAP-023, CAP-028 | 3/7 mappings |
| ET-008 | robustness | CAP-001, CAP-003, CAP-017, CAP-023, CAP-025, CAP-028 | 6/7 mappings |
| ET-009 | safety | CAP-028 | 1/7 mappings |
| ET-010 | hallucination_rate | CAP-001, CAP-017, CAP-023, CAP-025 | 4/7 mappings |
| ET-011 | task_success_rate | Not yet used in capability mappings | 0/7 mappings |
| ET-012 | user_satisfaction | CAP-001, CAP-017, CAP-025 | 3/7 mappings |

**ET-011 (task_success_rate) has zero capability mappings.** It is defined in the execution protocol as a pre-deployment gate but is not yet bound to a specific capability. This is an acceptable v1.0 state; ET-011 is a system-level metric rather than a per-capability metric.

---

## 4. Goal Ontology Cross-Check

All 21 `eval_id` references in `goal_ontology.json` use `method` names (e.g., `intent_classification_accuracy`, `response_quality_human_eval`). These method names are human-readable descriptions, not machine IDs. The `evaluation_ontology.json` resolves the mapping via `evaluation_type` IDs (ET-001 through ET-012).

**Alignment status by goal class:**

| Goal Class | Eval Requirements | Maps to Eval Types | Conflict |
|------------|-------------------|-------------------|----------|
| reactive_agent | EVAL-REACT-001 (CAP-003, ET-001/ET-004), EVAL-REACT-002 (CAP-017, ET-012), EVAL-REACT-003 (CAP-028, ET-001) | All resolve | **NONE** |
| assistant_agent | EVAL-ASST-001 (CAP-005, ET-001), EVAL-ASST-002 (CAP-006, no mapping), EVAL-ASST-003 (CAP-017, ET-012) | CAP-006 unresolved | **GAP: CAP-006** |
| autonomous_agent | EVAL-AUTO-001 (CAP-014, no mapping), EVAL-AUTO-002 (CAP-011, no mapping), EVAL-AUTO-003 (CAP-009, no mapping), EVAL-AUTO-004 (CAP-026, no mapping) | All 4 unresolved | **GAP: CAP-009, CAP-011, CAP-014, CAP-026** |
| workflow_agent | EVAL-WKFL-001 (CAP-009, no mapping), EVAL-WKFL-002 (CAP-028, ET-001) | CAP-009 unresolved | **GAP: CAP-009** |
| orchestrator_agent | EVAL-ORCH-001 (CAP-014, no mapping), EVAL-ORCH-002 (CAP-011, no mapping) | Both unresolved | **GAP: CAP-011, CAP-014** |
| evaluation_agent | EVAL-EVLAG-001 (CAP-011, no mapping), EVAL-EVLAG-002 (CAP-026, no mapping) | Both unresolved | **GAP: CAP-011, CAP-026** |
| research_agent | EVAL-RES-001 (CAP-007, no mapping), EVAL-RES-002 (CAP-026, no mapping), EVAL-RES-003 (CAP-017, ET-012) | 2 unresolved | **GAP: CAP-007, CAP-026** |
| coding_agent | EVAL-CODE-001 (CAP-017, ET-012), EVAL-CODE-002 (CAP-026, no mapping), EVAL-CODE-003 (CAP-009, no mapping) | 2 unresolved | **GAP: CAP-009, CAP-026** |
| support_agent | EVAL-SUP-001 (CAP-003, ET-004), EVAL-SUP-002 (CAP-007, no mapping), EVAL-SUP-003 (CAP-017, ET-012) | 1 unresolved | **GAP: CAP-007** |
| security_agent | EVAL-SEC-001 (CAP-003, ET-003), EVAL-SEC-002 (CAP-026, no mapping) | 1 unresolved | **GAP: CAP-026** |
| analytics_agent | EVAL-ANA-001 (CAP-009, no mapping), EVAL-ANA-002 (CAP-017, ET-012) | 1 unresolved | **GAP: CAP-009** |
| content_agent | EVAL-CONT-001 (CAP-017, ET-012), EVAL-CONT-002 (CAP-011, no mapping) | 1 unresolved | **GAP: CAP-011** |

---

## 5. Corpus Entry Cross-Check

### CORPUS-001 (support/enterprise, reactive_agent)

| Eval Requirement | Capability | Eval Type Resolved | Status |
|-----------------|------------|-------------------|--------|
| failure_classification_accuracy | CAP-003 | ET-001 / ET-004 | ✅ RESOLVED |
| knowledge_base_retrieval_accuracy | CAP-007 | **No mapping** | ⚠️ UNRESOLVED |
| response_quality_human_eval | CAP-017 | ET-012 | ✅ RESOLVED |
| escalation_precision_recall | CAP-003 | ET-002 / ET-003 | ✅ RESOLVED |
| output_schema_compliance | CAP-028 | ET-001 | ✅ RESOLVED |
| context_retention_accuracy | CAP-005 | ET-001 | ✅ RESOLVED |
| csat_survey_score | CAP-017 | ET-012 | ✅ RESOLVED |

**CORPUS-001 unresolved: 1/7 (CAP-007)**

### CORPUS-002 (engineering/devops, reactive_agent)

| Eval Requirement | Capability | Eval Type Resolved | Status |
|-----------------|------------|-------------------|--------|
| failure_classification_accuracy | CAP-003 | ET-001 / ET-004 | ✅ RESOLVED |
| tool_call_correctness | CAP-009 | **No mapping** | ⚠️ UNRESOLVED |
| report_accuracy_human_eval | CAP-028 | ET-001 / ET-012 | ✅ RESOLVED |
| flake_detection_recall_precision | CAP-006 | **No mapping** | ⚠️ UNRESOLVED |
| promotion_confidence_calibration | CAP-011 | **No mapping** | ⚠️ UNRESOLVED |
| developer_utility_survey | CAP-017 | ET-012 | ✅ RESOLVED |
| root_cause_consolidation_test | CAP-014 | **No mapping** | ⚠️ UNRESOLVED |

**CORPUS-002 unresolved: 4/7 (CAP-009, CAP-006, CAP-011, CAP-014)**

---

## 6. Ontology Conflicts

No hard conflicts found. All threshold values in `evaluation_ontology.json` are consistent with pass_threshold values declared in corpus entries and goal_ontology.json. No circular references. No duplicate evaluation_ids.

**Threshold consistency check:**

| Reference | Corpus/Goal Threshold | Eval Ontology Threshold | Consistent |
|-----------|----------------------|------------------------|------------|
| CORPUS-002: CAP-003 failure_classification >= 0.92 | 0.92 | ET-001 acceptable minimum 0.80, target 0.90 | ✅ Corpus is stricter — valid |
| CORPUS-002: CAP-009 tool_call_correctness >= 0.99 | 0.99 | No mapping | N/A |
| CORPUS-001: CAP-017 response_quality >= 0.80 | 0.80 | ET-012 minimum 0.75 | ✅ Corpus is stricter — valid |
| goal_ontology: EVAL-REACT-003 CAP-028 >= 0.99 | 0.99 | CAP-028 mapping minimum 0.99 | ✅ EXACT MATCH |
| goal_ontology: EVAL-AUTO-003 CAP-009 >= 0.97 | 0.97 | No mapping | N/A |

**Finding:** All resolvable threshold pairs are consistent. No corpus or goal ontology entry declares a threshold below the evaluation_ontology floor. No conflicts.

---

## 7. Summary

| Dimension | Result |
|-----------|--------|
| Evaluation types defined | 12 |
| Capability mappings defined | 7 |
| Capabilities with full mapping | 7 |
| Capabilities with missing mapping | 7 (CAP-006, CAP-007, CAP-008, CAP-009, CAP-011, CAP-014, CAP-026) |
| Goal classes fully resolved | 1 (reactive_agent) |
| Goal classes with gaps | 11 |
| Corpus entries fully resolved | 0 |
| Corpus entries partially resolved | 2 |
| Threshold conflicts | 0 |
| Hard ontology conflicts | 0 |

**Compatibility verdict:** EVAL-ONTOLOGY-001 v1.0 is internally consistent and conflict-free. It resolves all evaluation requirements for `reactive_agent` and for capabilities CAP-001, CAP-003, CAP-005, CAP-017, CAP-023, CAP-025, and CAP-028. The 7 unmapped capabilities represent the evaluation debt that must be resolved before goal classes beyond `reactive_agent` can be fully evaluated.
