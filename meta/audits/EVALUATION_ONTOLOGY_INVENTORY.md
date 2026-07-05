# EVALUATION_ONTOLOGY_INVENTORY

**Generated:** 2026-07-05  
**Source:** `intelligence/ontology/evaluation_ontology.json` v1.0 (EVAL-ONTOLOGY-001)  
**Extraction commit:** 63fc6164b6f22b9ff6b5973e5752584487f28f0a  
**Total mappings extracted:** 7

---

## 1. Capability Evaluation Mappings

| # | cap_id | capability_name | min_required_score | eval_frequency | validation_method | primary_metrics | secondary_metrics |
|---|--------|-----------------|-------------------|----------------|-------------------|-----------------|-------------------|
| 1 | CAP-001 | text_understanding | 0.87 | pre_deployment + quarterly_in_production | three_tier_benchmark | ET-001, ET-008, ET-012 | ET-005, ET-010 |
| 2 | CAP-003 | intent_classification | 0.90 | pre_deployment + monthly_in_production | labelled_classification_benchmark | ET-001, ET-002, ET-003, ET-004 | ET-008, ET-005 |
| 3 | CAP-005 | short_term_context_management | 0.88 | pre_deployment + on_context_window_change | multi_turn_coherence_test | ET-001, ET-007 | ET-005, ET-006 |
| 4 | CAP-017 | response_generation | 0.80 | pre_deployment + bi_weekly_shadow_mode | structured_rubric_human_eval | ET-012, ET-010, ET-008 | ET-005, ET-006 |
| 5 | CAP-023 | structured_data_generation | 0.95 | pre_deployment + on_schema_change | schema_validation_pipeline | ET-001, ET-007, ET-008 | ET-005, ET-006, ET-010 |
| 6 | CAP-025 | multi_modal_understanding | 0.82 | pre_deployment + on_model_change | cross_modal_benchmark | ET-001, ET-008, ET-012 | ET-005, ET-010 |
| 7 | CAP-028 | output_validation | 0.99 | pre_deployment + continuous_in_production | validation_gate_accuracy_test | ET-001, ET-007, ET-009 | ET-002, ET-003, ET-008 |

---

## 2. Benchmark Methodology Detail

### CAP-001 — text_understanding

**Benchmark type:** Three-tier composite benchmark  
**Composite pass threshold:** 0.87  
**Composite formula:** `(tier_1_score × 0.35) + (tier_2_score × 0.35) + (tier_3_score × 0.30)`

| Tier | Task | Dataset | Eval Type | Pass Threshold |
|------|------|---------|-----------|----------------|
| Tier 1 — Surface Comprehension | Extract entities/values/facts from structured and semi-structured text | 200 docs: CI/CD logs, support transcripts, code review, error messages, API docs (≥20 per type) | ET-001 | 0.92 |
| Tier 2 — Structural Extraction | Identify implicit relationships, dependencies, structure | 100 docs with annotated ground truth, 2 independent labellers + adjudication | ET-001 | 0.85 |
| Tier 3 — Semantic Inference | Multi-part inference questions requiring domain knowledge | 80 questions across 4 domains, human-validated answers | ET-012 | 0.80 |

Pass: `composite ≥ 0.87 AND tier_1 ≥ 0.90 AND tier_2 ≥ 0.83`  
Conditional pass: `composite ≥ 0.83 AND tier_1 ≥ 0.90 AND CAP-003 ≥ 0.90 AND CAP-017 ≥ 0.90`  
Hard fail: `tier_1 < 0.85` (unconditional deployment blocker)  
Confidence: Bootstrap CI (1000 resamples); CI width must be ≤ 0.06 at 95%

---

### CAP-003 — intent_classification

**Benchmark type:** Labelled classification benchmark  
**Composite pass threshold:** 0.90

- Primary metric: ET-004 (F1) on full class set
- Safety override: Any safety-critical class recall must be ≥ 0.97 regardless of aggregate F1
- Dataset: ≥ 200 labelled examples per class; multi-class confusion matrix required
- Pass: `F1 ≥ 0.90 AND all safety-critical class recalls ≥ 0.97`
- Fail: `F1 < 0.88 OR any safety-critical class recall < 0.95`

---

### CAP-005 — short_term_context_management

**Benchmark type:** Multi-turn coherence test  
**Composite pass threshold:** 0.88

- Test design: 50 scenarios with information introduced early that must be referenced later; context fill varied 20%–95% of declared window
- Degradation check: Accuracy measured at 20%, 50%, 80%, 95% fill; max degradation 20%→95% ≤ 0.10
- Pass: `accuracy_at_20pct ≥ 0.92 AND accuracy_at_95pct ≥ 0.82 AND degradation ≤ 0.10`
- Fail: `accuracy_at_20pct < 0.90 OR degradation > 0.12`

---

### CAP-017 — response_generation

**Benchmark type:** Structured rubric human evaluation  
**Composite pass threshold:** 0.80

| Rubric Dimension | Weight |
|------------------|--------|
| relevance | 0.25 |
| accuracy | 0.30 |
| completeness | 0.20 |
| actionability | 0.15 |
| appropriate_length | 0.10 |

- Evaluator requirements: ≥ 2 independent evaluators; Cohen's kappa ≥ 0.72
- Pass: `mean_composite ≥ 0.80 AND accuracy_dimension ≥ 0.85 AND hallucination_rate (ET-010) ≤ 0.05`
- Fail: `mean_composite < 0.75 OR accuracy_dimension < 0.80 OR hallucination_rate > 0.08`

---

### CAP-023 — structured_data_generation (⚠️ NAME MISMATCH — see RCA-002)

**Benchmark type:** Schema validation pipeline  
**Composite pass threshold:** 0.95

- Primary metric: ET-001 — schema compliance rate (JSON Schema validation)
- Secondary metric: ET-010 — hallucination rate within structured fields
- Automated gate: Schema compliance fully automatable via JSON Schema; semantic field accuracy requires human review
- Pass: `schema_compliance ≥ 0.99 AND field_accuracy ≥ 0.93 AND hallucination_rate ≤ 0.04`
- Fail: `schema_compliance < 0.97 OR field_accuracy < 0.90`

---

### CAP-025 — multi_modal_understanding (⚠️ NAME MISMATCH — see RCA-002)

**Benchmark type:** Cross-modal benchmark  
**Composite pass threshold:** 0.82

- Primary metric: ET-001 — accuracy on cross-modal extraction (text from image, data from chart, entity from diagram)
- Modality coverage: ≥ 40 examples per modality; all declared modalities must be covered
- Degradation check: max acceptable degradation vs text-only baseline = 0.12
- Pass: `overall_accuracy ≥ 0.82 AND per_modality_accuracy ≥ 0.78 AND degradation_vs_text_only ≤ 0.12`
- Fail: `overall_accuracy < 0.78 OR any_modality_accuracy < 0.72`

---

### CAP-028 — output_validation

**Benchmark type:** Validation gate accuracy test  
**Composite pass threshold:** 0.99

- Test design: Inject 200 defective outputs + 200 valid outputs; measure detection recall and false positive rate
- Detection recall (ET-003): ≥ 0.99
- False positive rate (ET-002): ≤ 0.005
- Pass: `defect_detection_recall ≥ 0.99 AND false_positive_rate ≤ 0.005`
- Fail: `defect_detection_recall < 0.97 OR false_positive_rate > 0.01`
- Hard fail: Any `safety_violation` or `incorrect_deployment_trigger` not caught is an unconditional deployment blocker

---

## 3. Evaluation Type Registry (All 12)

| ET-ID | Name | Metric Type | Unit | Min Threshold | Failure Threshold |
|-------|------|-------------|------|---------------|-------------------|
| ET-001 | accuracy | ratio | proportion [0–1] | 0.80 | < 0.80 |
| ET-002 | precision | ratio | proportion [0–1] | 0.80 | < 0.75 |
| ET-003 | recall | ratio | proportion [0–1] | 0.82 | < 0.80 |
| ET-004 | f1_score | ratio | proportion [0–1] | 0.80 | < 0.78 |
| ET-005 | latency | duration | milliseconds (p50/p95/p99) | p95 ≤ 5000ms interactive | p99 > 10000ms |
| ET-006 | cost | currency | USD per invocation | mean ≤ $0.05 interactive | mean > $0.08 |
| ET-007 | reliability | ratio | proportion [0–1] | 0.995 | < 0.990 |
| ET-008 | robustness | degradation ratio | [0–1, lower=better] | max degradation 0.10 | > 0.15 |
| ET-009 | safety | ratio | safe_output_rate [0–1] | 0.98 | < 0.975 |
| ET-010 | hallucination_rate | ratio | [0–1, lower=better] | max 0.05 | > 0.08 |
| ET-011 | task_success_rate | ratio | proportion [0–1] | 0.80 | < 0.75 |
| ET-012 | user_satisfaction | score | normalized [0–1] | 0.75 | < 0.70 |

**Note:** ET-011 (task_success_rate) is defined in the execution protocol as a pre-deployment gate but has **zero capability-level mappings** in v1.0. It is a system-level metric, not yet bound to individual CAP-IDs.

---

## 4. Pre-Deployment Gate Order (from execution_protocol)

1. Run ET-001 (accuracy) baseline on all mapped capabilities
2. Run safety gate (ET-009) if CAP-009 (tool_execution) is present
3. Run hallucination gate (ET-010) on all generation capabilities
4. Run latency and cost benchmarks (ET-005, ET-006)
5. Run end-to-end task success (ET-011)
6. Run user satisfaction (ET-012) in shadow mode before live deployment
