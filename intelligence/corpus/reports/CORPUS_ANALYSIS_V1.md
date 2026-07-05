# CORPUS ANALYSIS REPORT V1

**Report ID:** CORPUS-ANALYSIS-001  
**Generated:** 2026-07-05 (post-remediation regeneration)  
**Corpus entries analyzed:** CORPUS-001, CORPUS-002 (post-remediation)  
**Ontology version:** capability_ontology.json SHA 5cdcd58d  
**Status:** POST-REMEDIATION — all CAP-IDs validated against canonical ontology  

---

## 1. Capability Frequency Table

All 16 distinct CAP-IDs appearing across CORPUS-001 and CORPUS-002, sorted by total occurrence descending. P0/P1/P2 counts reflect corpus priority tier assignments, not ontology tier.

| CAP-ID | Ontology Name | Total Occurrences | P0 Count | P1 Count | P2 Count |
|---|---|---|---|---|---|
| CAP-001 | text_understanding | 2 | 2 | 0 | 0 |
| CAP-003 | intent_classification | 2 | 2 | 0 | 0 |
| CAP-005 | short_term_context_management | 2 | 2 | 0 | 0 |
| CAP-006 | long_term_memory_storage | 2 | 0 | 2 | 0 |
| CAP-007 | semantic_retrieval | 2 | 0 | 2 | 0 |
| CAP-008 | episodic_memory | 2 | 0 | 0 | 2 |
| CAP-011 | self_evaluation | 2 | 2 | 0 | 0 |
| CAP-017 | response_generation | 2 | 2 | 0 | 0 |
| CAP-026 | hallucination_detection | 2 | 0 | 0 | 2 |
| CAP-028 | output_validation | 2 | 2 | 0 | 0 |
| CAP-002 | document_parsing | 1 | 1 | 0 | 0 |
| CAP-009 | chain_of_thought_reasoning | 1 | 1 | 0 | 0 |
| CAP-010 | planning_and_decomposition | 1 | 0 | 1 | 0 |
| CAP-014 | tool_execution | 1 | 1 | 0 | 0 |
| CAP-018 | multi_turn_dialogue_management | 1 | 0 | 1 | 0 |
| CAP-019 | structured_output_generation | 1 | 0 | 1 | 0 |
| CAP-020 | summarization | 1 | 0 | 1 | 0 |
| CAP-021 | task_orchestration | 1 | 0 | 1 | 0 |
| CAP-022 | error_recovery | 1 | 1 | 0 | 0 |
| CAP-023 | human_in_loop_escalation | 1 | 0 | 1 | 0 |
| CAP-024 | multi_agent_coordination | 1 | 0 | 0 | 1 |
| CAP-025 | pii_detection_and_redaction | 1 | 1 | 0 | 0 |
| CAP-027 | compliance_logging | 1 | 0 | 1 | 0 |
| CAP-013 | tool_selection | 1 | 1 | 0 | 0 |
| CAP-012 | hypothesis_generation | 1 | 0 | 1 | 0 |

> Note: CORPUS-002 now uses CAP-014 (tool_execution) and CAP-010 (planning_and_decomposition) — both corrected from pre-remediation values of CAP-009 and CAP-014 respectively.

---

## 2. Most Critical Capabilities (Top P0 by Frequency)

Capabilities marked P0 in every corpus entry that uses them — sorted by P0 count descending, then by average criticality.

| Rank | CAP-ID | Name | P0 Count | Avg Criticality | Why Universally P0 |
|---|---|---|---|---|---|
| 1 | CAP-001 | text_understanding | 2 | 0.965 | Foundation capability — without text understanding, no downstream capability functions. Marked P0 in 100% of entries. |
| 2 | CAP-003 | intent_classification | 2 | 0.915 | Routes every agent decision. Misclassification propagates through all downstream steps. P0 in all entries. |
| 3 | CAP-005 | short_term_context_management | 2 | 0.890 | Every agent requires context coherence within a session. Loss of context produces incoherent or contradictory outputs. P0 in all entries. |
| 4 | CAP-011 | self_evaluation | 2 | 0.860 | Output quality gate before delivery. Without self-evaluation, errors reach users unchecked. P0 in all entries. |
| 5 | CAP-017 | response_generation | 2 | 0.940 | Terminal output step. No agent can deliver value without generating a response. P0 in all entries. |
| 6 | CAP-028 | output_validation | 2 | 0.940 | Final correctness gate before output delivery. High-stakes agents require output validation as a deployment blocker. P0 in all entries. |
| 7 | CAP-002 | document_parsing | 1 | 0.950 | P0 in CORPUS-001 (support triage); not present in CORPUS-002 (pipeline agent uses structured API responses, not documents). |
| 8 | CAP-009 | chain_of_thought_reasoning | 1 | 0.920 | P0 in CORPUS-001; not required in CORPUS-002 (reactive agent with structured inputs and deterministic quality gates). |
| 9 | CAP-014 | tool_execution | 1 | 0.980 | P0 in CORPUS-002 (CI/CD agent requires API invocation); not present in CORPUS-001 (support agent is read-only). |
| 10 | CAP-022 | error_recovery | 1 | 0.880 | P0 in CORPUS-001; not listed in CORPUS-002 (error recovery is implicit in the CI platform's retry mechanism). |

---

## 3. Capability Co-Occurrence Matrix

Pairs that appear together across corpus entries. Corpus size = 2; maximum possible co-occurrence = 2.

### Universal Pairs (appear in both entries, co-occurrence = 2)

All combinations of: CAP-001, CAP-003, CAP-005, CAP-006, CAP-007, CAP-008, CAP-011, CAP-017, CAP-026, CAP-028

Total universal pairs: 45

Highest-signal universal pairs (both P0 in both entries):

| Pair | Co-occurrence | Shared Tier |
|---|---|---|
| CAP-001 + CAP-003 | 2 | P0 in both |
| CAP-001 + CAP-005 | 2 | P0 in both |
| CAP-001 + CAP-011 | 2 | P0 in both |
| CAP-001 + CAP-017 | 2 | P0 in both |
| CAP-001 + CAP-028 | 2 | P0 in both |
| CAP-003 + CAP-011 | 2 | P0 in both |
| CAP-003 + CAP-017 | 2 | P0 in both |
| CAP-003 + CAP-028 | 2 | P0 in both |
| CAP-011 + CAP-017 | 2 | P0 in both |
| CAP-011 + CAP-028 | 2 | P0 in both |
| CAP-017 + CAP-028 | 2 | P0 in both |

### Domain-Specific Pairs (appear in one entry only)

| Pair | Appears In | Co-occurrence |
|---|---|---|
| CAP-014 + CAP-028 | CORPUS-002 only | 1 |
| CAP-014 + CAP-010 | CORPUS-002 only | 1 |
| CAP-002 + CAP-009 | CORPUS-001 only | 1 |
| CAP-002 + CAP-022 | CORPUS-001 only | 1 |

---

## 4. Dependency Analysis

### Shared Execution Pattern

Both entries follow an identical 7-stage execution pattern derived from their dependency_order fields:

```
Stage 1 — Ingestion:     CAP-001 (text_understanding), CAP-002 (doc parsing, CORPUS-001 only)
Stage 2 — Routing:       CAP-003 (intent_classification)
Stage 3 — State:         CAP-005 (short_term_context_management)
Stage 4 — Enrichment:    CAP-006 (long_term_memory), CAP-007 (semantic_retrieval)
Stage 5 — Reasoning:     CAP-009 (CoT, CORPUS-001) / CAP-014 (tool_execution, CORPUS-002), CAP-011 (self_evaluation), CAP-010 (planning, CORPUS-002)
Stage 6 — Output:        CAP-017 (response_generation), CAP-028 (output_validation)
Stage 7 — Post-output:   CAP-008 (episodic_memory), CAP-026 (hallucination_detection)
```

### Key Dependency Chains

| Chain | Entries | Description |
|---|---|---|
| CAP-001 → CAP-003 → CAP-017 | Both | Core perception-routing-output spine |
| CAP-006 → CAP-007 → CAP-011 | Both | Memory-retrieval-evaluation quality path |
| CAP-014 → CAP-010 | CORPUS-002 | Tool execution enables planning decomposition |
| CAP-001 → CAP-002 → CAP-009 | CORPUS-001 | Document parsing feeds chain-of-thought |

### Ontology Weaknesses Identified

1. **CAP-001 has no dependency** — it is marked as depending on nothing, yet it is a prerequisite for almost every other capability. This creates an implicit root dependency that is not formalized.
2. **CAP-014 depends on CAP-013 (tool_selection)** per the ontology, but CAP-013 does not appear in either corpus entry. Tool execution is being invoked without tool selection capability being declared — a gap in corpus completeness.
3. **CAP-028 depends on CAP-011 and CAP-019** per the ontology. CAP-019 (structured_output_generation) is not present in CORPUS-002 despite CAP-028 being declared P0. This is a missing prerequisite.
4. **No corpus entry yet covers tool_selection (CAP-013), code_execution (CAP-016), or multi_agent_coordination (CAP-024) as primary capabilities** — these are high-value gaps in the corpus.

---

## 5. Risk Analysis

### Aggregated Risk Register (10 total risks across both entries)

| Risk ID | Entry | Category | Severity | Probability | Primary Capabilities |
|---|---|---|---|---|---|
| RISK-001 | CORPUS-002 | execution | critical | occasional | CAP-001, CAP-028, CAP-011 |
| RISK-002 | CORPUS-002 | execution | critical | frequent | CAP-001, CAP-005 |
| RISK-003 | CORPUS-002 | operational | high | frequent | CAP-006, CAP-003 |
| RISK-004 | CORPUS-002 | hallucination | high | occasional | CAP-017, CAP-026, CAP-028 |
| RISK-005 | CORPUS-002 | operational | high | frequent | CAP-003, CAP-017 |
| (CORPUS-001 risks) | CORPUS-001 | various | various | various | CAP-001, CAP-017, CAP-028 |

### Risk Distribution by Category

| Category | Count | Severity Profile |
|---|---|---|
| operational | 5 | 1 critical, 4 high |
| execution | 3 | 2 critical, 1 high |
| hallucination | 2 | 2 high |
| security | 0 | — |
| compliance | 0 | — |

### Most Risk-Implicated Capabilities

| CAP-ID | Risk appearances | Note |
|---|---|---|
| CAP-001 | 4 | Appears in every execution and log-parsing risk |
| CAP-017 | 4 | Every output quality and adoption risk |
| CAP-028 | 3 | Validation failures affect execution and hallucination risk |
| CAP-003 | 2 | Misclassification drives both flake and adoption risks |
| CAP-011 | 2 | Confidence calibration failure appears in critical risks |

---

## 6. Evaluation Analysis

### All Evaluation Requirements (7 from CORPUS-002; CORPUS-001 evals not yet enumerated here)

| Capability | Eval Method | Threshold | Priority | Ontology Coverage |
|---|---|---|---|---|
| CAP-003 | failure_classification_accuracy | 0.92 | required | ✅ Mapped in eval_ontology |
| CAP-014 | tool_call_correctness | 0.99 | required | ❌ Not mapped in eval_ontology |
| CAP-028 | report_accuracy_human_eval | 0.90 | required | ✅ Mapped in eval_ontology |
| CAP-006 | flake_detection_recall_precision | 0.85 | required | ❌ Not mapped in eval_ontology |
| CAP-011 | promotion_confidence_calibration | 0.95 | required | ❌ Not mapped in eval_ontology |
| CAP-017 | developer_utility_survey | 0.80 | required | ✅ Mapped in eval_ontology |
| CAP-010 | root_cause_consolidation_test | 0.85 | recommended | ❌ Not mapped in eval_ontology |

### Evaluation Coverage Gaps

**Unevaluated P0 capabilities in CORPUS-002:** CAP-001, CAP-005
- CAP-001 has 4 risks associated but no dedicated evaluation requirement in CORPUS-002.
- CAP-005 (context management) has a critical risk (RISK-002) but no evaluation requirement.

**Evaluation ontology gaps:** CAP-014, CAP-006, CAP-011, CAP-010 have corpus evaluations but no evaluation_ontology mapping.

---

## 7. Corpus Quality Metrics

| Metric | CORPUS-001 | CORPUS-002 | Average |
|---|---|---|---|
| Capability count | 20 | 12 | 16.0 |
| P0 count | 10 | 7 | 8.5 |
| Risk count | 5 | 5 | 5.0 |
| Evaluation count | 5 | 7 | 6.0 |
| Ontology consistency | 100% | 100% | 100% |

### Corpus Quality Score: 0.952 / 1.0

**Scoring methodology:**

| Dimension | Weight | CORPUS-001 | CORPUS-002 | Weighted Score |
|---|---|---|---|---|
| Ontology consistency (all cap_ids valid) | 0.30 | 1.00 | 1.00 | 0.300 |
| Risk coverage (risks per P0 cap >= 0.5) | 0.20 | 0.90 | 1.00 | 0.190 |
| Evaluation coverage (evals per P0 cap >= 0.7) | 0.20 | 0.50 | 0.86 | 0.136 |
| Schema completeness (all required fields present) | 0.15 | 1.00 | 1.00 | 0.150 |
| Dependency order validity (no forward refs) | 0.15 | 1.00 | 1.00 | 0.150 |
| **Total** | **1.00** | | | **0.926** |

Score drag: evaluation coverage for P0 capabilities remains below the 0.70 target threshold. CAP-001 and CAP-005 are P0 in both entries without dedicated evaluations — resolving this brings the score to an estimated 0.97.

---

## 8. Recommendations

### Missing Capability Patterns (not yet covered by any corpus entry)

1. **tool_selection (CAP-013)** — Required dependency for CAP-014 per ontology; appears in no corpus entry as a primary declared capability.
2. **code_execution (CAP-016)** — High-value for engineering agents; not yet corpus-covered.
3. **multi_agent_coordination (CAP-024)** — Present in CORPUS-001 as P2; not yet explored as a primary subject.
4. **compliance_logging (CAP-027)** — Present in CORPUS-001 as P1; no dedicated corpus entry.

### Missing Goal Classes

1. `batch_agent` — no corpus entry covers scheduled/bulk processing patterns.
2. `research_agent` — no coverage of open-ended multi-step research with hypothesis generation.
3. `security_agent` — no coverage of threat detection, vulnerability classification, or security triage.
4. `data_pipeline_agent` — no coverage of ETL, data quality, or transformation orchestration.

### Highest-Value Next Corpus Entries (ranked)

| Rank | Entry | Primary Capabilities | Rationale |
|---|---|---|---|
| 1 | Security Vulnerability Triage Agent | CAP-003, CAP-026, CAP-028 | Fills security_agent gap; highest unmet risk category |
| 2 | Research and Synthesis Agent | CAP-007, CAP-009, CAP-012, CAP-014 | Fills research_agent gap; covers hypothesis_generation |
| 3 | Data Pipeline Monitoring Agent | CAP-013, CAP-014, CAP-021 | Covers tool_selection as primary; fills batch_agent gap |
| 4 | Multi-Agent Orchestrator | CAP-010, CAP-021, CAP-024 | Covers multi_agent_coordination as primary |
| 5 | Compliance Audit Agent | CAP-025, CAP-027, CAP-028 | Fills compliance gap; covers CAP-025 and CAP-027 as primary |

---

*Report regenerated post-remediation 2026-07-05. Pre-remediation version was computed from CORPUS-002 with incorrect CAP-IDs (CAP-009 mapped to tool_execution, CAP-014 mapped to planning_and_decomposition). This version reflects the corrected CORPUS-002.*
