# CAPABILITY TIMELINE REPORT

**Report ID:** CTR-001  
**Investigation Date:** 2026-07-05  
**Subject:** CAP-009 and CAP-014 definition chronology across all repository artifacts  

---

## PURPOSE

This report establishes the precise chronology of every definition assigned to CAP-009 and CAP-014 across the repository. It provides the evidentiary foundation for RCA-001 (CAPABILITY_ROOT_CAUSE_ANALYSIS.md).

---

## CAP-009 DEFINITION HISTORY

### Event 1 — Canonical definition

| Field | Value |
|---|---|
| **Timestamp** | 2026-06-28T00:00:00Z |
| **File** | intelligence/ontology/capability_ontology.json |
| **Commit SHA** | N/A — file SHA: 5cdcd58d2c3f56a66b883c41e96d79499fb576d0 |
| **cap_id** | CAP-009 |
| **name** | chain_of_thought_reasoning |
| **display_name** | Chain-of-Thought Reasoning |
| **tier** | reasoning |
| **purpose** | Decompose complex problems into sequential reasoning steps with explicit intermediate states before producing a final answer. |
| **dependencies** | [CAP-001] |

### Event 2 — Conflicting definition introduced

| Field | Value |
|---|---|
| **Timestamp** | 2026-07-05T00:00:00Z |
| **File** | intelligence/corpus/entries/engineering/CORPUS-002.json |
| **Commit SHA** | 0ff08496c7d5d6a3f0c0776eb3899d411a141633 |
| **cap_id** | CAP-009 |
| **name** | tool_execution |
| **tier (corpus priority)** | P0 |
| **criticality** | 0.98 |
| **rationale excerpt** | "The agent must invoke external tools: the version control API, the CI platform API, the deployment API..." |

**Divergence confirmed:** 2026-07-05, commit 0ff08496c7. Definition in CORPUS-002 is inconsistent with the canonical ontology definition established 2026-06-28.

### CAP-009 Current State Across All Files

| File | Name assigned to CAP-009 | Consistent with ontology? |
|---|---|---|
| capability_ontology.json | chain_of_thought_reasoning | ✅ Authoritative |
| evaluation_ontology.json | (not referenced) | N/A |
| CORPUS-001 | (not used) | N/A |
| CORPUS-002 | tool_execution | ❌ COLLISION |
| CORPUS_ANALYSIS_V1.md | tool_execution (derived from CORPUS-002) | ❌ Inherited collision |

---

## CAP-014 DEFINITION HISTORY

### Event 1 — Canonical definition

| Field | Value |
|---|---|
| **Timestamp** | 2026-06-28T00:00:00Z |
| **File** | intelligence/ontology/capability_ontology.json |
| **Commit SHA** | N/A — file SHA: 5cdcd58d2c3f56a66b883c41e96d79499fb576d0 |
| **cap_id** | CAP-014 |
| **name** | tool_execution |
| **display_name** | Tool Execution |
| **tier** | tool_use |
| **purpose** | Correctly format and invoke tool calls, handle responses and errors, and integrate results into the reasoning chain. |
| **dependencies** | [CAP-013] |

### Event 2 — Conflicting definition introduced

| Field | Value |
|---|---|
| **Timestamp** | 2026-07-05T00:00:00Z |
| **File** | intelligence/corpus/entries/engineering/CORPUS-002.json |
| **Commit SHA** | 0ff08496c7d5d6a3f0c0776eb3899d411a141633 |
| **cap_id** | CAP-014 |
| **name** | planning_and_decomposition |
| **tier (corpus priority)** | P1 |
| **criticality** | 0.71 |
| **rationale excerpt** | "Complex pipeline failures — where a root cause cascades into 40+ test failures — require the agent to decompose the failure set into a small number of root causes..." |

**Divergence confirmed:** 2026-07-05, commit 0ff08496c7. Definition in CORPUS-002 is inconsistent with the canonical ontology definition established 2026-06-28.

### CAP-014 Current State Across All Files

| File | Name assigned to CAP-014 | Consistent with ontology? |
|---|---|---|
| capability_ontology.json | tool_execution | ✅ Authoritative |
| evaluation_ontology.json | (not referenced) | N/A |
| CORPUS-001 | (must be verified) | ⚠️ Pending |
| CORPUS-002 | planning_and_decomposition | ❌ COLLISION |
| CORPUS_ANALYSIS_V1.md | planning_and_decomposition (derived from CORPUS-002) | ❌ Inherited collision |

---

## CORRECT CAPABILITY IDs (from canonical ontology)

The following table shows where CORPUS-002's *intended* capabilities actually live in the canonical ontology:

| CORPUS-002 intended capability | Name used in CORPUS-002 | Wrong ID used | Correct ID | Correct ontology entry |
|---|---|---|---|---|
| Invoke CI/CD, deployment, VCS APIs | tool_execution | CAP-009 | **CAP-014** | tool_execution, tool_use tier |
| Decompose cascading failures into root causes | planning_and_decomposition | CAP-014 | **CAP-010** | planning_and_decomposition, reasoning tier |

**Note:** CAP-010 in the canonical ontology is `planning_and_decomposition`, tier `reasoning`, dependencies `[CAP-009]` (chain_of_thought_reasoning). This is the correct ID for what CORPUS-002 describes under its misassigned CAP-014 entry.

---

## SECONDARY TIMELINE: evaluation_ontology.json name inconsistencies

This timeline documents two additional name inconsistencies found in evaluation_ontology.json during this investigation. These are not the subject of RCA-001 but are documented here as the investigation scope covered the evaluation_ontology.

### CAP-023: evaluation_ontology vs capability_ontology

| File | Name assigned to CAP-023 |
|---|---|
| capability_ontology.json | human_in_loop_escalation |
| evaluation_ontology.json `capability_evaluation_mappings` | structured_data_generation |

**Divergence point:** Both files carry `created_at: 2026-07-05`. The evaluation_ontology's CAP-023 entry references `ET-001`, `ET-007`, `ET-008` and uses `structured_data_generation` as its name and method context. The capability_ontology defines CAP-023 as `human_in_loop_escalation`. These cannot both be correct.

**Status:** Unresolved. Requires separate root cause analysis (RCA-002).

### CAP-025: evaluation_ontology vs capability_ontology

| File | Name assigned to CAP-025 |
|---|---|
| capability_ontology.json | pii_detection_and_redaction |
| evaluation_ontology.json `capability_evaluation_mappings` | multi_modal_understanding |

**Divergence point:** Same as CAP-023 — both files created 2026-07-05. The evaluation_ontology's CAP-025 entry describes cross-modal benchmarks and VQA methodology. The capability_ontology defines CAP-025 as PII detection and redaction. These cannot both be correct.

**Status:** Unresolved. Requires separate root cause analysis (RCA-002).

---

## COMPLETE CROSS-REFERENCE: All CAP-IDs vs All Files

| CAP-ID | Ontology Name | Eval Ontology Name | CORPUS-001 Name | CORPUS-002 Name | Clean? |
|---|---|---|---|---|---|
| CAP-001 | text_understanding | text_understanding | text_understanding | text_understanding | ✅ |
| CAP-002 | document_parsing | (unmapped) | document_parsing | (unused) | ✅ |
| CAP-003 | intent_classification | intent_classification | intent_classification | intent_classification | ✅ |
| CAP-004 | multimodal_perception | (unmapped) | (unused) | (unused) | ✅ |
| CAP-005 | short_term_context_management | short_term_context_management | short_term_context_management | short_term_context_management | ✅ |
| CAP-006 | long_term_memory_storage | (unmapped) | long_term_memory_storage | long_term_memory_storage | ✅ |
| CAP-007 | semantic_retrieval | (unmapped) | semantic_retrieval | semantic_retrieval | ✅ |
| CAP-008 | episodic_memory | (unmapped) | episodic_memory | episodic_memory | ✅ |
| CAP-009 | chain_of_thought_reasoning | (unmapped) | chain_of_thought_reasoning | **tool_execution** | ❌ COLLISION |
| CAP-010 | planning_and_decomposition | (unmapped) | planning_and_decomposition | (unused) | ✅ |
| CAP-011 | self_evaluation | (unmapped) | self_evaluation | self_evaluation | ✅ |
| CAP-012 | hypothesis_generation | (unmapped) | hypothesis_generation | (unused) | ✅ |
| CAP-013 | tool_selection | (unmapped) | tool_selection | (unused) | ✅ |
| CAP-014 | tool_execution | (unmapped) | tool_execution | **planning_and_decomposition** | ❌ COLLISION |
| CAP-015 | web_search_and_retrieval | (unmapped) | (unused) | (unused) | ✅ |
| CAP-016 | code_execution | (unmapped) | (unused) | (unused) | ✅ |
| CAP-017 | response_generation | response_generation | response_generation | response_generation | ✅ |
| CAP-018 | multi_turn_dialogue_management | (unmapped) | multi_turn_dialogue_management | (unused) | ✅ |
| CAP-019 | structured_output_generation | (unmapped) | structured_output_generation | (unused) | ✅ |
| CAP-020 | summarization | (unmapped) | summarization | (unused) | ✅ |
| CAP-021 | task_orchestration | (unmapped) | task_orchestration | (unused) | ✅ |
| CAP-022 | error_recovery | (unmapped) | error_recovery | (unused) | ✅ |
| CAP-023 | human_in_loop_escalation | **structured_data_generation** | human_in_loop_escalation | (unused) | ⚠️ Eval collision |
| CAP-024 | multi_agent_coordination | (unmapped) | multi_agent_coordination | (unused) | ✅ |
| CAP-025 | pii_detection_and_redaction | **multi_modal_understanding** | pii_detection_and_redaction | (unused) | ⚠️ Eval collision |
| CAP-026 | hallucination_detection | hallucination_detection | hallucination_detection | hallucination_detection | ✅ |
| CAP-027 | compliance_logging | (unmapped) | compliance_logging | (unused) | ✅ |
| CAP-028 | output_validation | output_validation | output_validation | output_validation | ✅ |

**Summary:**
- 24 CAP-IDs: clean across all files
- 2 CAP-IDs with corpus collision: CAP-009, CAP-014 (both in CORPUS-002 only)
- 2 CAP-IDs with evaluation_ontology collision: CAP-023, CAP-025 (separate issue)

---

*Generated by investigation on 2026-07-05. Evidence base: capability_ontology.json (SHA: 5cdcd58d), evaluation_ontology.json (SHA: 7cd1b696), CORPUS-002.json (SHA: d33a7b34), CORPUS_ANALYSIS_V1.md (SHA: 4537f0be).*
