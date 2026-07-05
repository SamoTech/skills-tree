# EVALUATION ONTOLOGY INVENTORY
**Audit ID:** EVAL-INVENTORY-001
**Generated:** 2026-07-05
**Source file:** `intelligence/ontology/evaluation_ontology.json` (SHA: 7cd1b696b0ae29f32003b4f85f4e8b0450fe6fd9)
**Ontology version:** 1.0
**Created:** 2026-07-05T00:00:00Z
**Last reviewed:** 2026-07-05T00:00:00Z

---

## Part 1 — Evaluation Type Registry

12 evaluation types defined.

| ET-ID | Name | Metric Type | Unit | Min Threshold | Target | Excellence | Failure Trigger |
|---|---|---|---|---|---|---|---|
| ET-001 | accuracy | ratio | proportion [0–1] | 0.80 | 0.90 | 0.95 | < 0.80 → block_deployment |
| ET-002 | precision | ratio | proportion [0–1] | 0.80 | 0.88 | 0.95 | < 0.75 → block_deployment |
| ET-003 | recall | ratio | proportion [0–1] | 0.82 | 0.90 | 0.97 | < 0.80 → block_deployment |
| ET-004 | f1_score | ratio | proportion [0–1] | 0.80 | 0.88 | 0.94 | < 0.78 → block_deployment |
| ET-005 | latency | duration | milliseconds | p50≤2000ms (interactive) | — | — | p99>10000ms → scale_or_optimise |
| ET-006 | cost | currency | USD per invocation | mean≤$0.05 (interactive) | — | — | mean>$0.08 → optimise |
| ET-007 | reliability | ratio | proportion [0–1] | 0.995 | 0.999 | 0.9999 | < 0.990 → incident_response |
| ET-008 | robustness | ratio | quality_score_degradation (lower=better) | max 0.10 | 0.05 | 0.02 | > 0.15 → block_deployment |
| ET-009 | safety | ratio | safe_output_rate [0–1] | 0.98 | 0.995 | 0.999 | < 0.975 → block_deployment |
| ET-010 | hallucination_rate | ratio | hallucination_proportion (lower=better) | max 0.05 | 0.02 | 0.005 | > 0.08 → block_deployment |
| ET-011 | task_success_rate | ratio | proportion [0–1] | 0.80 | 0.88 | 0.95 | < 0.75 → block_deployment |
| ET-012 | user_satisfaction | score | normalized [0–1] | 0.75 | 0.82 | 0.90 | < 0.70 → block_deployment |

---

## Part 2 — Capability Evaluation Mappings

7 capability mappings defined in `capability_evaluation_mappings[]`.

### Mapping 1 — CAP-001

| Field | Value |
|---|---|
| cap_id | CAP-001 |
| name (as declared in eval ontology) | text_understanding |
| primary_metrics | ET-001, ET-008, ET-012 |
| secondary_metrics | ET-005, ET-010 |
| minimum_required_score | 0.87 |
| evaluation_frequency | pre_deployment + quarterly_in_production |
| validation_method | three_tier_benchmark |

**Benchmark methodology:**
- **Tier 1 — Surface Comprehension:** ET-001, 200 documents (CI/CD logs, support transcripts, code review, error messages, API docs), pass threshold 0.92
- **Tier 2 — Structural Extraction:** ET-001, 100 documents with annotated structure, pass threshold 0.85
- **Tier 3 — Semantic Inference:** ET-012, 80 inference questions across 4 domains, pass threshold 0.80
- **Composite formula:** `(tier_1 × 0.35) + (tier_2 × 0.35) + (tier_3 × 0.30)`, composite pass threshold 0.87
- **Hard fail:** tier_1_score < 0.85 is an unconditional deployment blocker

---

### Mapping 2 — CAP-003

| Field | Value |
|---|---|
| cap_id | CAP-003 |
| name (as declared in eval ontology) | intent_classification |
| primary_metrics | ET-001, ET-002, ET-003, ET-004 |
| secondary_metrics | ET-008, ET-005 |
| minimum_required_score | 0.90 |
| evaluation_frequency | pre_deployment + monthly_in_production |
| validation_method | labelled_classification_benchmark |

**Benchmark methodology:**
- Primary metric: ET-004 (F1) on full class set
- Safety override: safety-critical class recalls must be >= 0.97 regardless of aggregate F1
- Dataset: minimum 200 labelled examples per class; multi-class confusion matrix required
- Pass: F1 >= 0.90 AND all safety-critical class recalls >= 0.97
- Fail: F1 < 0.88 OR any safety-critical class recall < 0.95

---

### Mapping 3 — CAP-005

| Field | Value |
|---|---|
| cap_id | CAP-005 |
| name (as declared in eval ontology) | short_term_context_management |
| primary_metrics | ET-001, ET-007 |
| secondary_metrics | ET-005, ET-006 |
| minimum_required_score | 0.88 |
| evaluation_frequency | pre_deployment + on_context_window_change |
| validation_method | multi_turn_coherence_test |

**Benchmark methodology:**
- 50 test scenarios, context length varied from 20% to 95% of declared window capacity
- Accuracy measured at 20%, 50%, 80%, and 95% fill levels
- Maximum acceptable degradation 20%→95%: 0.10
- Pass: accuracy_at_20pct >= 0.92 AND accuracy_at_95pct >= 0.82 AND degradation <= 0.10
- Fail: accuracy_at_20pct < 0.90 OR degradation > 0.12

---

### Mapping 4 — CAP-017

| Field | Value |
|---|---|
| cap_id | CAP-017 |
| name (as declared in eval ontology) | response_generation |
| primary_metrics | ET-012, ET-010, ET-008 |
| secondary_metrics | ET-005, ET-006 |
| minimum_required_score | 0.80 |
| evaluation_frequency | pre_deployment + bi_weekly_shadow_mode |
| validation_method | structured_rubric_human_eval |

**Benchmark methodology:**
- Rubric: relevance (0.25), accuracy (0.30), completeness (0.20), actionability (0.15), appropriate_length (0.10)
- Composite: `sum(dimension_score × weight)`
- Pass: mean_composite >= 0.80 AND accuracy_dimension >= 0.85 AND hallucination_rate <= 0.05
- Fail: mean_composite < 0.75 OR accuracy_dimension < 0.80 OR hallucination_rate > 0.08
- Evaluator requirements: ≥ 2 independent evaluators per output; Cohen's kappa >= 0.72

---

### Mapping 5 — CAP-023 ⚠️ MISMATCH DETECTED

| Field | Value |
|---|---|
| cap_id | CAP-023 |
| name (as declared in eval ontology) | **structured_data_generation** ← MISMATCH (canonical: human_in_loop_escalation) |
| primary_metrics | ET-001, ET-007, ET-008 |
| secondary_metrics | ET-005, ET-006, ET-010 |
| minimum_required_score | 0.95 |
| evaluation_frequency | pre_deployment + on_schema_change |
| validation_method | schema_validation_pipeline |

**Benchmark methodology:**
- Primary metric: ET-001 — schema compliance rate (output validates against declared JSON/structured schema)
- Secondary metric: ET-010 — hallucination rate within structured fields
- Pass: schema_compliance >= 0.99 AND field_accuracy >= 0.93 AND hallucination_rate <= 0.04
- Fail: schema_compliance < 0.97 OR field_accuracy < 0.90
- Automated gate: schema compliance evaluated automatically via JSON Schema validation

> **RCA-002 Finding:** This evaluation model describes `structured_data_generation` / `structured_output_generation` (similar to CAP-019). The canonical capability at CAP-023 is `human_in_loop_escalation`. This evaluation is entirely inapplicable to human escalation decisions.

---

### Mapping 6 — CAP-025 ⚠️ MISMATCH DETECTED

| Field | Value |
|---|---|
| cap_id | CAP-025 |
| name (as declared in eval ontology) | **multi_modal_understanding** ← MISMATCH (canonical: pii_detection_and_redaction) |
| primary_metrics | ET-001, ET-008, ET-012 |
| secondary_metrics | ET-005, ET-010 |
| minimum_required_score | 0.82 |
| evaluation_frequency | pre_deployment + on_model_change |
| validation_method | cross_modal_benchmark |

**Benchmark methodology:**
- Primary metric: ET-001 — accuracy on cross-modal extraction tasks (text from image, data from chart, entity from diagram)
- Minimum 40 examples per modality
- Maximum acceptable degradation vs text-only baseline: 0.12
- Pass: overall_accuracy >= 0.82 AND per_modality_accuracy >= 0.78 AND degradation_vs_text_only <= 0.12
- Fail: overall_accuracy < 0.78 OR any_modality_accuracy < 0.72

> **RCA-002 Finding:** This evaluation model describes `multi_modal_understanding`, a capability not registered in capability_ontology.json. The canonical capability at CAP-025 is `pii_detection_and_redaction`. This evaluation is entirely inapplicable to PII detection/redaction.

---

### Mapping 7 — CAP-028

| Field | Value |
|---|---|
| cap_id | CAP-028 |
| name (as declared in eval ontology) | output_validation |
| primary_metrics | ET-001, ET-007, ET-009 |
| secondary_metrics | ET-002, ET-003, ET-008 |
| minimum_required_score | 0.99 |
| evaluation_frequency | pre_deployment + continuous_in_production |
| validation_method | validation_gate_accuracy_test |

**Benchmark methodology:**
- Primary: ET-001 — rate of correctly catching schema/quality-gate violations
- Detection recall: ET-003 — minimum recall 0.99 on injected defective outputs
- False positive: ET-002 — maximum valid-output rejection rate 0.005
- Test design: inject 200 defective + 200 valid outputs
- Pass: defect_detection_recall >= 0.99 AND false_positive_rate <= 0.005
- Fail: defect_detection_recall < 0.97 OR false_positive_rate > 0.01
- Hard fail: any missed safety_violation or incorrect_deployment_trigger is an unconditional deployment blocker

---

## Part 3 — Execution Protocol Summary

**Pre-deployment gate order:**
1. ET-001 baseline on all mapped capabilities
2. ET-009 (safety) if CAP-009 present ← *note: ontology references CAP-009 for safety gate trigger; canonical CAP-009 = chain_of_thought_reasoning; correct reference should be CAP-014 (tool_execution)*
3. ET-010 hallucination gate on all generation capabilities
4. ET-005, ET-006 latency and cost benchmarks
5. ET-011 end-to-end task success
6. ET-012 user satisfaction in shadow mode

**Production monitoring:**
- Continuous: ET-007, ET-006, ET-005
- Weekly: ET-010, ET-012
- Monthly: ET-001, ET-009
- Quarterly: full benchmark rerun

**Automatic rollback triggers:** ET-007 < 0.990 OR ET-009 < 0.975
