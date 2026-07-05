# P0_EVALUATION_COVERAGE_REASSESSMENT

**Generated:** 2026-07-05  
**Investigation:** RCA-002  
**Authority sources:** `capability_ontology.json`, `evaluation_ontology.json`, `CORPUS-001.json`, `CORPUS-002.json`  
**No ontology or corpus modifications made.**

---

## 1. P0 Capability Set Definition

P0 priority is assigned per corpus entry, not in `capability_ontology.json` directly. The following P0 set is derived from all current corpus entries (CORPUS-001 and CORPUS-002).

| cap_id | name | CORPUS-001 priority | CORPUS-002 priority | P0 in any entry |
|--------|------|--------------------|--------------------|------------------|
| CAP-001 | text_understanding | P0 | P0 | ✅ |
| CAP-003 | intent_classification | P0 | P0 | ✅ |
| CAP-005 | short_term_context_management | P0 | P0 | ✅ |
| CAP-017 | response_generation | P0 | P0 | ✅ |
| CAP-028 | output_validation | P0 | P0 | ✅ |
| CAP-007 | semantic_retrieval | P0 | not used | ✅ |
| CAP-014 | tool_execution | not used | P0 | ✅ |
| CAP-011 | self_evaluation | not used | P0 | ✅ |

**Total P0 capabilities across corpus:** 8

---

## 2. Evaluation Mapping Status — Pre-RCA-002 (Reported)

| cap_id | name | Eval mapping exists | Mapping name correct | Valid mapping |
|--------|------|--------------------|--------------------|---------------|
| CAP-001 | text_understanding | ✅ | ✅ | ✅ |
| CAP-003 | intent_classification | ✅ | ✅ | ✅ |
| CAP-005 | short_term_context_management | ✅ | ✅ | ✅ |
| CAP-017 | response_generation | ✅ | ✅ | ✅ |
| CAP-028 | output_validation | ✅ | ✅ | ✅ |
| CAP-007 | semantic_retrieval | ❌ | N/A | ❌ |
| CAP-014 | tool_execution | ❌ | N/A | ❌ |
| CAP-011 | self_evaluation | ❌ | N/A | ❌ |

**P0 coverage reported:** 5/8 = **62.5%**

*Note: CAP-023 and CAP-025 were counted in total eval coverage (7/28 = 25%) but are not P0 in any corpus entry, so their phantom status did not distort the P0 percentage — only the total coverage percentage.*

---

## 3. Evaluation Mapping Status — Post-Proposed-Repair (R-001 + R-002)

| cap_id | name | Eval mapping exists | Mapping name correct | Valid mapping |
|--------|------|--------------------|--------------------|---------------|
| CAP-001 | text_understanding | ✅ | ✅ | ✅ |
| CAP-003 | intent_classification | ✅ | ✅ | ✅ |
| CAP-005 | short_term_context_management | ✅ | ✅ | ✅ |
| CAP-017 | response_generation | ✅ | ✅ | ✅ |
| CAP-028 | output_validation | ✅ | ✅ | ✅ |
| CAP-007 | semantic_retrieval | ❌ | N/A | ❌ |
| CAP-014 | tool_execution | ❌ | N/A | ❌ |
| CAP-011 | self_evaluation | ❌ | N/A | ❌ |

**P0 coverage post-repair:** 5/8 = **62.5%** (unchanged)

Repairs R-001 and R-002 fix phantom mappings on non-P0 capabilities (CAP-023 and CAP-025). They do not add new P0 mappings. P0 coverage improves only when CAP-007, CAP-014, and CAP-011 receive new evaluation entries.

---

## 4. What Changes With Repair vs. What Stays the Same

| Metric | Pre-Repair | Post-Repair (proposed) | Change |
|--------|-----------|----------------------|--------|
| Total eval mappings | 7 | 7 | No change in count |
| Valid eval mappings | 5 | 7 | **+2 phantom mappings corrected** |
| Phantom (mis-named) mappings | 2 | 0 | **-2** |
| P0 mapped (valid) | 5 | 5 | No change |
| P0 unmapped | 3 | 3 | No change |
| P0 coverage | 62.5% | 62.5% | No change |
| Total coverage (valid only) | 17.9% (5/28) | 25.0% (7/28) | **+7.1 percentage points** |
| Safety-tier eval validity | ❌ CAP-025 phantom | ✅ CAP-025 correctly mapped to PII benchmark | **Safety gate restored** |

---

## 5. P0 Unmapped Gap Analysis

Three P0 capabilities have no evaluation mapping. These are the highest-priority evaluation gaps in the repository.

### CAP-007 — semantic_retrieval (P0 in CORPUS-001)

- **Tier:** memory
- **Purpose:** Semantic search over knowledge base, retrieval of relevant context
- **CORPUS-001 usage:** P0 — `knowledge_base_retrieval_accuracy` is a stated evaluation requirement in CORPUS-001 with no backing evaluation mapping
- **Recommended eval types:** ET-003 (recall), ET-001 (accuracy/precision@K), ET-005 (latency)
- **Minimum threshold implied by CORPUS-001:** retrieval accuracy ≥ 0.90

### CAP-014 — tool_execution (P0 in CORPUS-002)

- **Tier:** tool_use
- **Purpose:** Execute external tools (APIs, functions, system commands) reliably and correctly
- **CORPUS-002 usage:** P0 — `tool_call_correctness ≥ 0.99` is a stated evaluation requirement with no backing evaluation mapping
- **Recommended eval types:** ET-001 (accuracy), ET-007 (reliability), ET-009 (safety), ET-005 (latency)
- **Minimum threshold implied by CORPUS-002:** tool call correctness ≥ 0.99
- **Goal ontology usage:** Required in 8 of 12 goal classes — highest gap severity in the repository

### CAP-011 — self_evaluation (P0 in CORPUS-002)

- **Tier:** reasoning
- **Purpose:** Agent assesses its own output quality and confidence before delivery
- **CORPUS-002 usage:** P0 — `promotion_confidence_calibration` is a stated evaluation requirement with no backing evaluation mapping
- **Recommended eval types:** ET-001 (accuracy of self-assessment), ET-010 (hallucination rate correlation), calibration curve analysis
- **Minimum threshold implied by CORPUS-002:** confidence calibration ≥ 0.95
- **Goal ontology usage:** Required in 7 goal classes

---

## 6. Coverage Roadmap (Unmapped P0 Capabilities)

To achieve 100% P0 evaluation coverage, three new evaluation mappings are required:

| Priority | cap_id | name | Effort | Risk | Dependency |
|----------|--------|------|--------|------|------------|
| 1 | CAP-014 | tool_execution | Medium | High (safety-adjacent) | ET-009 safety gate must be included |
| 2 | CAP-007 | semantic_retrieval | Low | Low | Standard retrieval benchmark |
| 3 | CAP-011 | self_evaluation | High | Medium | Requires calibration methodology definition |

**Current P0 coverage:** 62.5% (5/8)  
**P0 coverage after R-001 + R-002:** 62.5% (5/8) — no change  
**P0 coverage after adding CAP-014, CAP-007, CAP-011:** 100% (8/8)
