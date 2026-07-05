# EVALUATION ONTOLOGY CONSISTENCY AUDIT
**Audit ID:** RCA-002-CONSISTENCY
**Generated:** 2026-07-05
**Investigator:** automated cross-reference
**Authority sources:**
- `intelligence/ontology/capability_ontology.json` (SHA: 5cdcd58d2c3f56a66b883c41e96d79499fb576d0)
- `intelligence/ontology/evaluation_ontology.json` (SHA: 7cd1b696b0ae29f32003b4f85f4e8b0450fe6fd9)

---

## Methodology

Every `cap_id` declared in `capability_evaluation_mappings[]` of the evaluation ontology was cross-referenced against the canonical `capability_ontology.json`. For each pair, the declared `name` in the evaluation ontology was compared to the canonical `name` in the capability ontology under the same `cap_id`.

Collision types:
- **TYPE A** — Same CAP-ID, different capability name (ID collision / name mismatch)
- **TYPE B** — Same capability name, different CAP-ID (name collision / ID mismatch)
- **TYPE C** — Evaluation references a CAP-ID that does not exist in capability ontology
- **TYPE D** — Capability exists in capability ontology with no evaluation mapping

---

## Cross-Reference Table — All 7 Mapped Capabilities

| cap_id | Name in evaluation_ontology.json | Name in capability_ontology.json | Match? | Collision Type |
|---|---|---|---|---|
| CAP-001 | text_understanding | text_understanding | ✅ MATCH | None |
| CAP-003 | intent_classification | intent_classification | ✅ MATCH | None |
| CAP-005 | short_term_context_management | short_term_context_management | ✅ MATCH | None |
| CAP-017 | response_generation | response_generation | ✅ MATCH | None |
| CAP-023 | structured_data_generation | human_in_loop_escalation | ❌ MISMATCH | **TYPE A** |
| CAP-025 | multi_modal_understanding | pii_detection_and_redaction | ❌ MISMATCH | **TYPE A** |
| CAP-028 | output_validation | output_validation | ✅ MATCH | None |

**Correct mappings: 5/7 (71.4%)**
**Mismatched mappings: 2/7 (28.6%)**

---

## Detected Mismatches

### MISMATCH 1 — CAP-023 (TYPE A)

| Field | Value |
|---|---|
| Collision type | TYPE A — Same CAP-ID, different capability name |
| CAP-ID in collision | CAP-023 |
| Name in evaluation_ontology.json | `structured_data_generation` |
| Canonical name in capability_ontology.json | `human_in_loop_escalation` |
| Semantic purpose match? | **NO** — structured data generation and human-in-the-loop escalation are unrelated capabilities |
| Evaluation type assigned | schema_validation_pipeline |
| Is schema_validation_pipeline appropriate for human_in_loop_escalation? | **NO** — human escalation requires escalation_decision_accuracy, escalation_recall, and latency metrics; schema validation is entirely inapplicable |

### MISMATCH 2 — CAP-025 (TYPE A)

| Field | Value |
|---|---|
| Collision type | TYPE A — Same CAP-ID, different capability name |
| CAP-ID in collision | CAP-025 |
| Name in evaluation_ontology.json | `multi_modal_understanding` |
| Canonical name in capability_ontology.json | `pii_detection_and_redaction` |
| Semantic purpose match? | **NO** — multi-modal understanding (cross-modal extraction from images/charts) and PII detection/redaction (identifying and removing personally identifiable information) are entirely different capabilities |
| Evaluation type assigned | cross_modal_benchmark |
| Is cross_modal_benchmark appropriate for pii_detection_and_redaction? | **NO** — PII detection requires precision/recall on PII entity types, redaction completeness, and false negative rate; cross-modal benchmarking is entirely inapplicable |

---

## Secondary Collision — Protocol Reference Error

The `evaluation_execution_protocol.pre_deployment_gates` block contains a third mismatch:

```json
"2. Run safety gate (ET-009) if CAP-009 (tool_execution) is present"
```

Per canonical capability_ontology.json:
- CAP-009 = `chain_of_thought_reasoning` (NOT tool_execution)
- CAP-014 = `tool_execution`

| Field | Value |
|---|---|
| Collision type | TYPE A (protocol-level) |
| Location | `evaluation_execution_protocol.pre_deployment_gates[1]` |
| Declared name for CAP-009 | tool_execution |
| Canonical name for CAP-009 | chain_of_thought_reasoning |
| Correct CAP-ID for tool_execution | CAP-014 |
| Severity | MEDIUM — protocol text error; does not invalidate capability mappings but produces incorrect CI gate documentation |

---

## TYPE B Collision Investigation

No TYPE B collision detected. Neither `structured_data_generation` nor `multi_modal_understanding` appear under different CAP-IDs in the capability ontology — they are not present in the capability ontology at all. The evaluation ontology introduced capability names that have no canonical registration.

---

## TYPE C Investigation — Orphan Evaluation References

No TYPE C collision detected. CAP-023 and CAP-025 both exist as valid CAP-IDs in the capability ontology. The IDs are valid; the names are wrong.

---

## TYPE D Investigation — Unmapped Capabilities

P0 and P1 capabilities present in corpus entries but absent from `capability_evaluation_mappings[]`:

| CAP-ID | Name | Corpus Tier | Evaluation Mapping Exists? |
|---|---|---|---|
| CAP-002 | document_parsing | P0 (CORPUS-001) | ❌ MISSING |
| CAP-009 | chain_of_thought_reasoning | P0 (CORPUS-001) | ❌ MISSING |
| CAP-011 | self_evaluation | P0 (both) | ❌ MISSING |
| CAP-014 | tool_execution | P0 (CORPUS-002) | ❌ MISSING |
| CAP-022 | error_recovery | P0 (CORPUS-001) | ❌ MISSING |
| CAP-006 | long_term_memory_storage | P1 (both) | ❌ MISSING |
| CAP-007 | semantic_retrieval | P1 (both) | ❌ MISSING |
| CAP-010 | planning_and_decomposition | P1 (CORPUS-002) | ❌ MISSING |
| CAP-018 | multi_turn_dialogue_management | P1 (CORPUS-001) | ❌ MISSING |
| CAP-019 | structured_output_generation | P1 (CORPUS-001) | ❌ MISSING |
| CAP-020 | summarization | P1 (CORPUS-001) | ❌ MISSING |
| CAP-021 | task_orchestration | P1 (CORPUS-001) | ❌ MISSING |
| CAP-023 | human_in_loop_escalation | P1 (CORPUS-001) | ⚠️ ID MAPPED, NAME WRONG |
| CAP-025 | pii_detection_and_redaction | P0 (CORPUS-001) | ⚠️ ID MAPPED, NAME WRONG |

**Note:** CAP-023 and CAP-025 appear to have evaluation mappings but the mapped evaluation content applies to different capabilities entirely. For the purposes of P0 coverage, these must be treated as UNMAPPED.

---

## Collision Summary

| Type | Count | Affected IDs |
|---|---|---|
| TYPE A (same ID, different name) | 2 capability mappings + 1 protocol reference | CAP-023, CAP-025, CAP-009 (protocol) |
| TYPE B (same name, different ID) | 0 | — |
| TYPE C (eval references missing capability) | 0 | — |
| TYPE D (capability missing evaluation) | 12 corpus-active capabilities | See table above |

## Repository Integrity Status

```
FAIL
```

Two TYPE A collisions invalidate evaluation coverage calculations and CI gate logic for CAP-023 and CAP-025. CAP-025 is P0 in CORPUS-001 — the incorrectly assigned evaluation model constitutes a critical deployment gate error.
