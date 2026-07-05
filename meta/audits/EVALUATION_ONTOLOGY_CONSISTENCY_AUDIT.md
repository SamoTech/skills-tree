# EVALUATION ONTOLOGY CONSISTENCY AUDIT
**Report ID:** EVAL-CONSISTENCY-AUDIT-001  
**Generated:** 2026-07-05  
**Scope:** Cross-reference of `evaluation_ontology.json` against `capability_ontology.json`  
**Sources:**
- Capability ontology SHA: `5cdcd58d2c3f56a66b883c41e96d79499fb576d0`
- Evaluation ontology SHA: `7cd1b696b0ae29f32003b4f85f4e8b0450fe6fd9`
- No modifications made to either file.

---

## Section 1 — Canonical Capability Registry (from capability_ontology.json)

All 28 capabilities registered in the canonical ontology, extracted as the authoritative reference for this audit:

| CAP-ID | Canonical Name |
|---|---|
| CAP-001 | text_understanding |
| CAP-002 | document_parsing |
| CAP-003 | intent_classification |
| CAP-004 | sentiment_analysis |
| CAP-005 | short_term_context_management |
| CAP-006 | long_term_memory_storage |
| CAP-007 | semantic_retrieval |
| CAP-008 | episodic_memory |
| CAP-009 | chain_of_thought_reasoning |
| CAP-010 | planning_and_decomposition |
| CAP-011 | self_evaluation |
| CAP-012 | hypothesis_generation |
| CAP-013 | tool_selection |
| CAP-014 | tool_execution |
| CAP-015 | api_integration |
| CAP-016 | code_execution |
| CAP-017 | response_generation |
| CAP-018 | multi_turn_dialogue_management |
| CAP-019 | structured_output_generation |
| CAP-020 | summarization |
| CAP-021 | task_orchestration |
| CAP-022 | error_recovery |
| CAP-023 | human_in_loop_escalation |
| CAP-024 | multi_agent_coordination |
| CAP-025 | pii_detection_and_redaction |
| CAP-026 | hallucination_detection |
| CAP-027 | compliance_logging |
| CAP-028 | output_validation |

---

## Section 2 — Evaluation Mapping Cross-Reference

| CAP-ID | Eval Ontology Name | Canonical Name | ID Match | Name Match | Verdict |
|---|---|---|---|---|---|
| CAP-001 | text_understanding | text_understanding | ✅ | ✅ | CONSISTENT |
| CAP-003 | intent_classification | intent_classification | ✅ | ✅ | CONSISTENT |
| CAP-005 | short_term_context_management | short_term_context_management | ✅ | ✅ | CONSISTENT |
| CAP-017 | response_generation | response_generation | ✅ | ✅ | CONSISTENT |
| **CAP-023** | **structured_data_generation** | **human_in_loop_escalation** | ✅ | ❌ | **TYPE A MISMATCH** |
| **CAP-025** | **multi_modal_understanding** | **pii_detection_and_redaction** | ✅ | ❌ | **TYPE A MISMATCH** |
| CAP-028 | output_validation | output_validation | ✅ | ✅ | CONSISTENT |

---

## Section 3 — Mismatch Classification

### TYPE A — Same CAP-ID, Different Capability Name

Two confirmed TYPE A mismatches. The CAP-ID is correct but the capability name attached to it in the evaluation ontology describes a different, unrelated capability.

#### TYPE A-1: CAP-023

| Field | Value |
|---|---|
| **CAP-ID** | CAP-023 |
| **Canonical name** | `human_in_loop_escalation` |
| **Eval ontology name** | `structured_data_generation` |
| **Divergence** | The evaluation mapping was written for `structured_data_generation` (a generation capability), not `human_in_loop_escalation` (a routing/escalation capability). These are semantically unrelated. |
| **Eval content valid?** | The benchmark methodology (schema_validation_pipeline, JSON schema compliance) is appropriate for a structured output/generation capability — it is completely inapplicable to human_in_loop_escalation, which requires escalation-trigger recall and false-positive analysis. |
| **Secondary collision** | `structured_data_generation` has no registered CAP-ID in capability_ontology.json. The nearest canonical match is CAP-019 (structured_output_generation). |

#### TYPE A-2: CAP-025

| Field | Value |
|---|---|
| **CAP-ID** | CAP-025 |
| **Canonical name** | `pii_detection_and_redaction` |
| **Eval ontology name** | `multi_modal_understanding` |
| **Divergence** | The evaluation mapping was written for `multi_modal_understanding` (a perception/modality capability), not `pii_detection_and_redaction` (a data privacy capability). These are semantically unrelated. |
| **Eval content valid?** | The benchmark methodology (cross_modal_benchmark, per-modality accuracy) is appropriate for multi-modal image/chart processing — it is completely inapplicable to PII detection, which requires detection recall on PII entity types, redaction correctness, and false negative analysis. |
| **Secondary collision** | `multi_modal_understanding` has no registered CAP-ID in capability_ontology.json. It appears to be an unlisted capability that belongs in the ontology but was never registered. |

---

### TYPE B — Same Capability, Different CAP-ID

No TYPE B mismatches detected in the 7 evaluation mappings.

---

### TYPE C — Evaluation References Missing Capability

Confirmed: The `evaluation_execution_protocol.pre_deployment_gates` section contains:

> *"Run safety gate (ET-009) if CAP-009 (tool_execution) is present"*

**CAP-009 in the canonical ontology = `chain_of_thought_reasoning`, NOT `tool_execution`.**  
`tool_execution` = CAP-014.

This is an inline TYPE A reference error embedded in the protocol definition, not a mapping entry. It is a secondary collision distinct from the two primary TYPE A mismatches.

| Location | Erroneous Reference | Should Be |
|---|---|---|
| `evaluation_execution_protocol.pre_deployment_gates[1]` | `CAP-009 (tool_execution)` | `CAP-014 (tool_execution)` |

---

### TYPE D — Capability Missing Evaluation Mapping

The following P0 and P1 capabilities appear in corpus entries but have no evaluation mapping in `evaluation_ontology.json`:

| CAP-ID | Canonical Name | Corpus Presence | Priority | Evaluation Coverage |
|---|---|---|---|---|
| CAP-002 | document_parsing | CORPUS-001 | P0 | ❌ No mapping |
| CAP-006 | long_term_memory_storage | CORPUS-001, CORPUS-002 | P1 | ❌ No mapping |
| CAP-007 | semantic_retrieval | CORPUS-001, CORPUS-002 | P1 | ❌ No mapping |
| CAP-008 | episodic_memory | CORPUS-001, CORPUS-002 | P2 | ❌ No mapping |
| CAP-009 | chain_of_thought_reasoning | CORPUS-001 | P0 | ❌ No mapping |
| CAP-010 | planning_and_decomposition | CORPUS-002 | P1 | ❌ No mapping |
| CAP-011 | self_evaluation | CORPUS-001, CORPUS-002 | P0 | ❌ No mapping |
| CAP-014 | tool_execution | CORPUS-002 | P0 | ❌ No mapping |
| CAP-018 | multi_turn_dialogue_management | CORPUS-001 | P1 | ❌ No mapping |
| CAP-019 | structured_output_generation | CORPUS-001 | P1 | ❌ No mapping |
| CAP-020 | summarization | CORPUS-001 | P1 | ❌ No mapping |
| CAP-021 | task_orchestration | CORPUS-001 | P1 | ❌ No mapping |
| CAP-022 | error_recovery | CORPUS-001 | P0 | ❌ No mapping |
| CAP-024 | multi_agent_coordination | CORPUS-001 | P2 | ❌ No mapping |
| CAP-026 | hallucination_detection | CORPUS-001, CORPUS-002 | P2 | ❌ No mapping |
| CAP-027 | compliance_logging | CORPUS-001 | P1 | ❌ No mapping |
| CAP-023 | human_in_loop_escalation | CORPUS-001 | P1 | ❌ Incorrectly mapped (TYPE A) |
| CAP-025 | pii_detection_and_redaction | CORPUS-001 | P0 | ❌ Incorrectly mapped (TYPE A) |

**Total TYPE D:** 18 corpus-active capabilities have no valid evaluation mapping.

---

## Section 4 — Mismatch Summary

| Type | Count | Affected CAP-IDs | Severity |
|---|---|---|---|
| TYPE A (same ID, wrong name) | 2 primary + 1 inline | CAP-023, CAP-025, protocol ref to CAP-009 | HIGH |
| TYPE B (same name, wrong ID) | 0 | — | — |
| TYPE C (eval ref to missing capability) | 1 inline | `structured_data_generation`, `multi_modal_understanding` as unmapped names | MEDIUM |
| TYPE D (capability missing evaluation) | 18 | See table above | HIGH |

---

## Section 5 — Ontology Integrity Status

```
INTEGRITY STATUS: DEGRADED
Primary mismatches: 2 (TYPE A — CAP-023, CAP-025)
Inline protocol error: 1 (CAP-009 referenced as tool_execution)
TYPE D coverage gaps: 18 capabilities unmapped
Overall evaluation coverage: 5 correctly mapped / 28 total capabilities = 17.9%
P0 evaluation coverage (corpus-active P0s): 4 correctly mapped / 9 corpus-active P0s = 44.4% (with CAP-025 falsely reported as 5/9 = 55.6% in ID-only systems)
```

---

*No modifications made to any ontology file. This document is investigation output only.*
