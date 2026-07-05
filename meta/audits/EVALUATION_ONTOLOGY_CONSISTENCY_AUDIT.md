# EVALUATION_ONTOLOGY_CONSISTENCY_AUDIT

**Generated:** 2026-07-05  
**Ontology under audit:** `intelligence/ontology/evaluation_ontology.json` v1.0  
**Cross-reference authority:** `intelligence/ontology/capability_ontology.json` v1.0  
**Total CAP-IDs in capability ontology:** 28  
**Total CAP-IDs in evaluation ontology:** 7  
**Investigation scope:** RCA-002

---

## 1. Full Cross-Reference Table

Every evaluation mapping checked against the canonical capability ontology.

| cap_id | eval_name | cap_name | cap_id_exists | name_match | semantic_match | classification |
|--------|-----------|----------|---------------|------------|----------------|----------------|
| CAP-001 | text_understanding | text_understanding | ✅ | ✅ | ✅ | VALID |
| CAP-003 | intent_classification | intent_classification | ✅ | ✅ | ✅ | VALID |
| CAP-005 | short_term_context_management | short_term_context_management | ✅ | ✅ | ✅ | VALID |
| CAP-017 | response_generation | response_generation | ✅ | ✅ | ✅ | VALID |
| CAP-023 | structured_data_generation | human_in_loop_escalation | ✅ | ❌ | ❌ | **TYPE A** |
| CAP-025 | multi_modal_understanding | pii_detection_and_redaction | ✅ | ❌ | ❌ | **TYPE A** |
| CAP-028 | output_validation | output_validation | ✅ | ✅ | ✅ | VALID |

**Valid mappings:** 5  
**Type A mismatches:** 2 (CAP-023, CAP-025)  
**Type B mismatches:** 0  
**Type C errors:** 0  
**Type D gaps (capability with no evaluation):** 21

---

## 2. Mismatch Classification Definitions

| Type | Definition |
|------|------------|
| TYPE A | Same CAP-ID, different capability name in eval ontology vs. capability ontology |
| TYPE B | Same capability name, different CAP-ID assigned in each ontology |
| TYPE C | Evaluation mapping references a CAP-ID that does not exist in capability ontology |
| TYPE D | Capability exists in capability ontology but has no entry in evaluation ontology |

---

## 3. TYPE A — Detailed Mismatch Records

### Mismatch A-001: CAP-023

| Field | Capability Ontology | Evaluation Ontology |
|-------|--------------------|---------  ---------|
| cap_id | CAP-023 | CAP-023 |
| name | `human_in_loop_escalation` | `structured_data_generation` |
| tier | execution | (not declared in eval ontology) |
| purpose | Detect when agent confidence is below threshold or action risk exceeds authorization level, and escalate to human review | Schema compliance + field accuracy for structured JSON/data output |
| validation_method | escalation_calibration_test | schema_validation_pipeline |
| min_required_score | not mapped | 0.95 |
| primary_metrics | not mapped | ET-001, ET-007, ET-008 |
| semantic_match | — | ❌ Completely different domain (execution safety vs. output generation) |

**Ghost identity in evaluation ontology:** `structured_data_generation`  
**Canonical identity per capability ontology:** `human_in_loop_escalation`  
**Corresponding canonical CAP-ID for `structured_data_generation`:** NOT FOUND in capability_ontology.json — this name does not exist as any registered capability.

---

### Mismatch A-002: CAP-025

| Field | Capability Ontology | Evaluation Ontology |
|-------|--------------------|---------  ---------|
| cap_id | CAP-025 | CAP-025 |
| name | `pii_detection_and_redaction` | `multi_modal_understanding` |
| tier | safety | (not declared in eval ontology) |
| purpose | Identify and redact PII in inputs and outputs before processing or delivery | Cross-modal extraction: text from image, data from chart, entity from diagram |
| validation_method | PII recall benchmark + cross-jurisdiction coverage | cross_modal_benchmark |
| min_required_score | not mapped | 0.82 |
| primary_metrics | not mapped | ET-001, ET-008, ET-012 |
| semantic_match | — | ❌ Completely different domain (safety/compliance vs. perception/multimodal) |

**Ghost identity in evaluation ontology:** `multi_modal_understanding`  
**Canonical identity per capability ontology:** `pii_detection_and_redaction`  
**Corresponding canonical CAP-ID for `multi_modal_understanding`:** CAP-004 (`multimodal_perception`) — closest match but not identical.

---

## 4. TYPE D — Unmapped Capabilities (21 total)

Capabilities present in `capability_ontology.json` with no evaluation mapping.

| cap_id | name | tier | Corpus Usage | Goal Ontology Usage | Gap Severity |
|--------|------|------|--------------|--------------------:|-------------|
| CAP-002 | document_parsing | perception | none | partial | Low |
| CAP-004 | multimodal_perception | perception | none | partial | Low |
| CAP-006 | long_term_memory_storage | memory | CORPUS-001 P1, CORPUS-002 P1 | assistant_agent required | Medium |
| CAP-007 | semantic_retrieval | memory | CORPUS-001 P0 | support_agent, research_agent | **High** |
| CAP-008 | episodic_memory | memory | CORPUS-001 P2, CORPUS-002 P2 | none | Low |
| CAP-009 | chain_of_thought_reasoning | reasoning | none | autonomous_agent | Medium |
| CAP-010 | planning_and_decomposition | reasoning | CORPUS-002 P1 | autonomous_agent, orchestrator | **High** |
| CAP-011 | self_evaluation | reasoning | CORPUS-001 P1, CORPUS-002 P0 | 7 goal classes | **High** |
| CAP-012 | hypothesis_generation | reasoning | none | none | Low |
| CAP-013 | tool_selection | tool_use | none | partial | Low |
| CAP-014 | tool_execution | tool_use | CORPUS-002 P0 | 8 goal classes | **Critical** |
| CAP-015 | web_search_and_retrieval | tool_use | none | research_agent | Low |
| CAP-016 | code_execution | tool_use | none | coding_agent | Medium |
| CAP-018 | multi_turn_dialogue_management | communication | none | assistant_agent | Low |
| CAP-019 | structured_output_generation | communication | none | workflow_agent | Medium |
| CAP-020 | summarization | communication | none | content_agent | Low |
| CAP-021 | task_orchestration | execution | none | orchestrator_agent | Medium |
| CAP-022 | error_recovery | execution | none | autonomous_agent | Medium |
| CAP-024 | multi_agent_coordination | execution | none | orchestrator_agent | Medium |
| CAP-026 | hallucination_detection | safety | CORPUS-001 P1, CORPUS-002 P2 | evaluation_agent, security_agent | **High** |
| CAP-027 | compliance_logging | safety | none | security_agent | Low |

**Critical gaps (corpus-used P0 with no evaluation):**
- CAP-014 (tool_execution) — P0 in CORPUS-002, required in 8 goal classes, zero evaluation coverage
- CAP-011 (self_evaluation) — P0 in CORPUS-002, P1 in CORPUS-001, required in 7 goal classes

**High gaps (corpus-used with no evaluation):**
- CAP-007 (semantic_retrieval) — P0 in CORPUS-001
- CAP-010 (planning_and_decomposition) — P1 in CORPUS-002
- CAP-026 (hallucination_detection) — used in both corpus entries

---

## 5. Ghost Capability Analysis

Two capability names appear in `evaluation_ontology.json` that have **no existence in `capability_ontology.json`**:

| Ghost Name | Attached to CAP-ID | Closest real capability | Distance |
|------------|--------------------|------------------------|----------|
| `structured_data_generation` | CAP-023 | CAP-019 `structured_output_generation` | Semantic overlap ~60%; different purpose (generation vs. validation) |
| `multi_modal_understanding` | CAP-025 | CAP-004 `multimodal_perception` | Semantic overlap ~70%; evaluation content describes cross-modal extraction tasks matching CAP-004 |

Neither ghost name is a registered capability. Both names describe real capabilities that exist in the ontology under different IDs.

---

## 6. Summary Statistics

| Metric | Value |
|--------|-------|
| Total CAP-IDs in capability_ontology | 28 |
| Total CAP-IDs in evaluation_ontology | 7 |
| Valid mappings (name + semantic match) | 5 |
| TYPE A mismatches | 2 |
| TYPE B mismatches | 0 |
| TYPE C errors (missing CAP-ID) | 0 |
| TYPE D gaps (unmapped capabilities) | 21 |
| Ghost capability names in eval ontology | 2 |
| Evaluation coverage rate (7/28) | 25.0% |
| Evaluation coverage rate (correct only, 5/28) | 17.9% |
