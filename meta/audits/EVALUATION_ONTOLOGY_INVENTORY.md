# EVALUATION ONTOLOGY INVENTORY
**Report ID:** EVAL-INVENTORY-001  
**Generated:** 2026-07-05  
**Source:** `intelligence/ontology/evaluation_ontology.json` (SHA: 7cd1b696b0ae29f32003b4f85f4e8b0450fe6fd9)  
**Scope:** All evaluation types and capability evaluation mappings extracted verbatim.  

---

## Part A — Evaluation Type Registry (12 types)

| ET-ID | Name | Metric Type | Unit | Min Threshold | Target | Excellence | Failure Gate |
|---|---|---|---|---|---|---|---|
| ET-001 | accuracy | ratio | proportion [0–1] | 0.80 | 0.90 | 0.95 | < 0.80 → block |
| ET-002 | precision | ratio | proportion [0–1] | 0.80 | 0.88 | 0.95 | < 0.75 → block |
| ET-003 | recall | ratio | proportion [0–1] | 0.82 | 0.90 | 0.97 | < 0.80 → block |
| ET-004 | f1_score | ratio | proportion [0–1] | 0.80 | 0.88 | 0.94 | < 0.78 → block |
| ET-005 | latency | duration | milliseconds | p95 ≤ 5000ms (interactive) | — | — | p99 > 10000ms → block |
| ET-006 | cost | currency | USD/invocation | mean ≤ $0.05 (interactive) | — | — | mean > $0.08 → block |
| ET-007 | reliability | ratio | proportion [0–1] | 0.995 | 0.999 | 0.9999 | < 0.990 → incident |
| ET-008 | robustness | ratio | degradation [0–1, lower better] | max degradation 0.10 | 0.05 | 0.02 | > 0.15 → block |
| ET-009 | safety | ratio | safe_output_rate [0–1] | 0.98 | 0.995 | 0.999 | < 0.975 → block |
| ET-010 | hallucination_rate | ratio | hallucination_proportion [0–1, lower better] | max 0.05 | 0.02 | 0.005 | > 0.08 → block |
| ET-011 | task_success_rate | ratio | proportion [0–1] | 0.80 | 0.88 | 0.95 | < 0.75 → block |
| ET-012 | user_satisfaction | score | normalized [0–1] | 0.75 | 0.82 | 0.90 | < 0.70 → block |

---

## Part B — Capability Evaluation Mappings (7 entries)

### CAP-001 — text_understanding

| Field | Value |
|---|---|
| **cap_id** | CAP-001 |
| **name in eval_ontology** | text_understanding |
| **Primary metrics** | ET-001, ET-008, ET-012 |
| **Secondary metrics** | ET-005, ET-010 |
| **Minimum required score** | 0.87 (composite) |
| **Evaluation frequency** | pre_deployment + quarterly_in_production |
| **Validation method** | three_tier_benchmark |

**Benchmark methodology:**

| Tier | Task | Dataset | Eval Type | Pass Threshold |
|---|---|---|---|---|
| Tier 1 — Surface Comprehension | Entity/value extraction from CI logs, support transcripts, error messages | 200 documents (20+ per type) | ET-001 | 0.92 |
| Tier 2 — Structural Extraction | Identify implicit relationships, dependency order, escalation paths | 100 annotated docs, 2 independent labellers | ET-001 | 0.85 |
| Tier 3 — Semantic Inference | Inference questions requiring multi-part doc synthesis + domain knowledge | 80 questions across 4 domains | ET-012 | 0.80 |

**Composite formula:** `(T1 × 0.35) + (T2 × 0.35) + (T3 × 0.30)`  
**Pass:** composite ≥ 0.87 AND T1 ≥ 0.90 AND T2 ≥ 0.83  
**Hard fail:** T1 < 0.85 (unconditional deployment blocker)  
**Confidence:** Bootstrap CI (1000 resamples), required CI width ≤ 0.06

---

### CAP-003 — intent_classification

| Field | Value |
|---|---|
| **cap_id** | CAP-003 |
| **name in eval_ontology** | intent_classification |
| **Primary metrics** | ET-001, ET-002, ET-003, ET-004 |
| **Secondary metrics** | ET-008, ET-005 |
| **Minimum required score** | 0.90 |
| **Evaluation frequency** | pre_deployment + monthly_in_production |
| **Validation method** | labelled_classification_benchmark |

**Benchmark methodology:**  
- Primary metric: ET-004 (F1) on full class set  
- Safety override: recall ≥ 0.97 for security_finding, escalation_required, compliance_violation classes  
- Dataset: minimum 200 labelled examples per class  
- Pass: F1 ≥ 0.90 AND all safety-critical class recalls ≥ 0.97  
- Fail: F1 < 0.88 OR any safety-critical class recall < 0.95

---

### CAP-005 — short_term_context_management

| Field | Value |
|---|---|
| **cap_id** | CAP-005 |
| **name in eval_ontology** | short_term_context_management |
| **Primary metrics** | ET-001, ET-007 |
| **Secondary metrics** | ET-005, ET-006 |
| **Minimum required score** | 0.88 |
| **Evaluation frequency** | pre_deployment + on_context_window_change |
| **Validation method** | multi_turn_coherence_test |

**Benchmark methodology:**  
- 50 test scenarios; information seeded early in context, referenced late  
- Context fill levels: 20%, 50%, 80%, 95%  
- Max degradation 20%→95%: ≤ 0.10 (ET-008 threshold)  
- Pass: accuracy@20% ≥ 0.92 AND accuracy@95% ≥ 0.82 AND degradation ≤ 0.10  
- Fail: accuracy@20% < 0.90 OR degradation > 0.12

---

### CAP-017 — response_generation

| Field | Value |
|---|---|
| **cap_id** | CAP-017 |
| **name in eval_ontology** | response_generation |
| **Primary metrics** | ET-012, ET-010, ET-008 |
| **Secondary metrics** | ET-005, ET-006 |
| **Minimum required score** | 0.80 |
| **Evaluation frequency** | pre_deployment + bi_weekly_shadow_mode |
| **Validation method** | structured_rubric_human_eval |

**Rubric dimensions:**

| Dimension | Weight | Description |
|---|---|---|
| relevance | 0.25 | Output directly addresses the input |
| accuracy | 0.30 | All factual claims correct and grounded |
| completeness | 0.20 | All required aspects covered |
| actionability | 0.15 | Enables concrete next step |
| appropriate_length | 0.10 | Not truncated or padded |

- Pass: mean_composite ≥ 0.80 AND accuracy_dimension ≥ 0.85 AND ET-010 ≤ 0.05  
- Fail: mean_composite < 0.75 OR accuracy_dimension < 0.80 OR ET-010 > 0.08  
- Min 2 independent evaluators; Cohen's kappa ≥ 0.72

---

### CAP-023 — (mapped as "structured_data_generation" in eval_ontology)

| Field | Value |
|---|---|
| **cap_id** | CAP-023 |
| **name in eval_ontology** | **structured_data_generation** ← MISMATCH |
| **Primary metrics** | ET-001, ET-007, ET-008 |
| **Secondary metrics** | ET-005, ET-006, ET-010 |
| **Minimum required score** | 0.95 |
| **Evaluation frequency** | pre_deployment + on_schema_change |
| **Validation method** | schema_validation_pipeline |

**Benchmark methodology:**  
- Primary: ET-001 — schema compliance rate (output validates against JSON schema)  
- Secondary: ET-010 — hallucination rate within structured fields  
- Pass: schema_compliance ≥ 0.99 AND field_accuracy ≥ 0.93 AND hallucination_rate ≤ 0.04  
- Fail: schema_compliance < 0.97 OR field_accuracy < 0.90  
- Automated gate: schema compliance via JSON Schema validation (no human review needed for structural compliance)

---

### CAP-025 — (mapped as "multi_modal_understanding" in eval_ontology)

| Field | Value |
|---|---|
| **cap_id** | CAP-025 |
| **name in eval_ontology** | **multi_modal_understanding** ← MISMATCH |
| **Primary metrics** | ET-001, ET-008, ET-012 |
| **Secondary metrics** | ET-005, ET-010 |
| **Minimum required score** | 0.82 |
| **Evaluation frequency** | pre_deployment + on_model_change |
| **Validation method** | cross_modal_benchmark |

**Benchmark methodology:**  
- Primary: ET-001 — accuracy on cross-modal extraction (text from image, data from chart, entity from diagram)  
- Min 40 examples per modality  
- Max degradation vs text-only baseline: 0.12 (ET-008 threshold)  
- Pass: overall_accuracy ≥ 0.82 AND per_modality_accuracy ≥ 0.78 AND degradation ≤ 0.12  
- Fail: overall_accuracy < 0.78 OR any_modality_accuracy < 0.72

---

### CAP-028 — output_validation

| Field | Value |
|---|---|
| **cap_id** | CAP-028 |
| **name in eval_ontology** | output_validation |
| **Primary metrics** | ET-001, ET-007, ET-009 |
| **Secondary metrics** | ET-002, ET-003, ET-008 |
| **Minimum required score** | 0.99 |
| **Evaluation frequency** | pre_deployment + continuous_in_production |
| **Validation method** | validation_gate_accuracy_test |

**Benchmark methodology:**  
- 200 defective outputs + 200 valid outputs injected  
- Detection recall (ET-003): minimum 0.99  
- False positive rate (ET-002): maximum 0.005  
- Pass: defect_detection_recall ≥ 0.99 AND false_positive_rate ≤ 0.005  
- Fail: recall < 0.97 OR FP rate > 0.01  
- Hard fail: any safety_violation or incorrect_deployment_trigger not caught → unconditional deployment blocker

---

## Part C — Evaluation Execution Protocol Summary

**Pre-deployment gate order:**
1. ET-001 (accuracy) baseline on all mapped capabilities
2. ET-009 (safety) gate if CAP-009 (tool_execution) present — **NOTE: ET-009 notes reference CAP-009 for tool execution; canonical ontology uses CAP-014**
3. ET-010 (hallucination) on all generation capabilities
4. ET-005, ET-006 (latency, cost) benchmarks
5. ET-011 (task_success_rate) end-to-end
6. ET-012 (user_satisfaction) shadow mode

**Production monitoring:**
- Continuous: ET-007, ET-006, ET-005
- Weekly: ET-010, ET-012
- Monthly: ET-001, ET-009
- Quarterly: full benchmark rerun + CAP-001 three-tier refresh

**Automatic rollback triggers:** ET-007 < 0.990 OR ET-009 < 0.975

---

*Source: `intelligence/ontology/evaluation_ontology.json` SHA 7cd1b696b0ae29f32003b4f85f4e8b0450fe6fd9. No modifications made to source.*
