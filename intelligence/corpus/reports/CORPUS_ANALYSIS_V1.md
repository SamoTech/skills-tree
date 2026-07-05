# CORPUS_ANALYSIS_V1 — Intelligence Extraction Report

**Generated:** 2026-07-05  
**Corpus version analyzed:** v1.0  
**Entries analyzed:** CORPUS-001 (support/enterprise), CORPUS-002 (engineering/devops)  
**Total capabilities inventoried:** 16 distinct capability IDs  
**Total risks inventoried:** 10  
**Total evaluation requirements:** 16  

---

## 1. Capability Frequency Table

All 16 distinct capabilities observed across both corpus entries, sorted by occurrence count descending, then by P0 count.

| capability_id | name | occurrences | P0 | P1 | P2 | avg_criticality |
|---|---|---|---|---|---|---|
| CAP-001 | text_understanding | 2 | 2 | 0 | 0 | 0.94 |
| CAP-003 | intent_classification | 2 | 2 | 0 | 0 | 0.95 |
| CAP-005 | short_term_context_management | 2 | 2 | 0 | 0 | 0.90 |
| CAP-017 | response_generation | 2 | 2 | 0 | 0 | 0.94 |
| CAP-006 | long_term_memory_storage | 2 | 0 | 2 | 0 | 0.81 |
| CAP-007 | semantic_retrieval | 2 | 1 | 1 | 0 | 0.85 |
| CAP-008 | episodic_memory | 2 | 0 | 0 | 2 | 0.53 |
| CAP-011 | self_evaluation | 2 | 1 | 1 | 0 | 0.82 |
| CAP-026 | hallucination_detection | 2 | 0 | 0 | 2 | 0.62 |
| CAP-028 | output_validation | 2 | 1 | 1 | 0 | 0.87 |
| CAP-009 | tool_execution | 1 | 1 | 0 | 0 | 0.98 |
| CAP-014 | planning_and_decomposition | 1 | 0 | 1 | 0 | 0.71 |
| CAP-018 | multi_turn_dialogue_management | 1 | 1 | 0 | 0 | 0.96 |
| CAP-023 | human_in_loop_escalation | 1 | 1 | 0 | 0 | 0.95 |
| CAP-025 | pii_detection_and_redaction | 1 | 1 | 0 | 0 | 0.99 |
| CAP-027 | compliance_logging | 1 | 1 | 0 | 0 | 0.98 |

**Observation:** 10 of 16 capabilities appear in both entries. The 4 universal capabilities (CAP-001, CAP-003, CAP-005, CAP-017) are P0 in every entry they appear in — these form the evident capability core of the corpus.

---

## 2. Most Critical Capabilities — Top P0 by Frequency

The following 12 capabilities received P0 designation at least once, ranked by P0 frequency then average criticality:

| rank | capability_id | name | P0_count | avg_criticality | rationale summary |
|---|---|---|---|---|---|
| 1 | CAP-003 | intent_classification | 2 | 0.95 | Routing gate: wrong classification poisons every downstream step |
| 2 | CAP-001 | text_understanding | 2 | 0.94 | Foundation: all other caps degrade proportionally without it |
| 3 | CAP-017 | response_generation | 2 | 0.94 | Terminal output: no output without it; quality determines adoption |
| 4 | CAP-005 | short_term_context_management | 2 | 0.90 | State continuity: stateless agents fail within 5–8 turns or 1 log parse |
| 5 | CAP-025 | pii_detection_and_redaction | 1 | 0.99 | Compliance gate: must execute first in any pipeline touching PII |
| 6 | CAP-027 | compliance_logging | 1 | 0.98 | Audit requirement: missing logs are SOC2 findings, not degradations |
| 7 | CAP-009 | tool_execution | 1 | 0.98 | Integration enabler: agent is read-only without it |
| 8 | CAP-018 | multi_turn_dialogue_management | 1 | 0.96 | Conversation coherence: support conversations are multi-turn by nature |
| 9 | CAP-023 | human_in_loop_escalation | 1 | 0.95 | Safety gate: deterministic escalation is a hard enterprise requirement |
| 10 | CAP-028 | output_validation | 1 | 0.87 | Pre-delivery gate: prevents hallucinated claims from reaching end users |
| 11 | CAP-007 | semantic_retrieval | 1 | 0.85 | Grounding: without it, responses are stale training-data only |
| 12 | CAP-011 | self_evaluation | 1 | 0.82 | Confidence gating: enables dynamic escalation and promotion thresholds |

**Pattern:** CAP-025 and CAP-027 achieve the highest criticality scores in the corpus (0.99, 0.98) but appear only once. This is domain-specific amplification — compliance requirements convert certain capabilities from optional to existential. CAP-009 (tool_execution, 0.98) has the same property in the engineering domain. The 4 universal P0 caps (CAP-001, CAP-003, CAP-005, CAP-017) are the floor beneath every agent regardless of domain.

---

## 3. Capability Co-Occurrence Matrix

With 2 corpus entries, all co-occurring pairs appear at count=2 (universal co-occurrence) or count=1 (single-entry pair). The meaningful signal is which pairs appear universally across both entries.

### Universal Co-Occurrences (count = 2)

All pairs involving CAP-001, CAP-003, CAP-005, CAP-006, CAP-007, CAP-008, CAP-011, CAP-017, CAP-026, CAP-028 co-occur in both entries. The 45 such pairs represent the stable core cluster of the current corpus. High-signal pairs within this cluster:

| pair | count | significance |
|---|---|---|
| CAP-001 + CAP-003 | 2 | Understanding precedes classification universally |
| CAP-001 + CAP-017 | 2 | Input understanding + output generation: the minimal agent loop |
| CAP-003 + CAP-017 | 2 | Classify → generate: direct cause-effect in every reactive agent |
| CAP-005 + CAP-006 | 2 | Short + long memory: co-deployed across all entries |
| CAP-017 + CAP-028 | 2 | Generate + validate: output always requires a validation step |
| CAP-026 + CAP-028 | 2 | Hallucination detection + output validation: always co-deployed |
| CAP-011 + CAP-028 | 2 | Self-evaluation + output validation: confidence and correctness gating co-occur |

### Single-Entry Pairs (count = 1)

These pairs are domain-specific. They will become analytically significant once additional entries establish a pattern:

| pair | entry | domain |
|---|---|---|
| CAP-023 + CAP-025 | CORPUS-001 | enterprise safety: escalation requires PII-clean context |
| CAP-018 + CAP-005 | CORPUS-001 | dialogue management + context: conversation-specific stack |
| CAP-009 + CAP-014 | CORPUS-002 | tool execution + planning: action-capable agents need decomposition |
| CAP-003 + CAP-006 | CORPUS-002 | classification + memory: flake detection pattern (CI/CD specific) |

---

## 4. Dependency Analysis

### Dependency Execution Order — Normalized Position (0.0 = first, 1.0 = last)

| capability_id | name | avg_normalized_position | entries | phase |
|---|---|---|---|---|
| CAP-001 | text_understanding | 0.00 | 2 | ingestion |
| CAP-025 | pii_detection_and_redaction | 0.08 | 1 | ingestion |
| CAP-003 | intent_classification | 0.12 | 2 | routing |
| CAP-005 | short_term_context_management | 0.21 | 2 | state |
| CAP-006 | long_term_memory_storage | 0.33 | 2 | state |
| CAP-007 | semantic_retrieval | 0.34 | 2 | enrichment |
| CAP-009 | tool_execution | 0.45 | 1 | action |
| CAP-011 | self_evaluation | 0.50 | 2 | reasoning |
| CAP-018 | multi_turn_dialogue_management | 0.54 | 1 | reasoning |
| CAP-014 | planning_and_decomposition | 0.64 | 1 | reasoning |
| CAP-017 | response_generation | 0.67 | 2 | output |
| CAP-028 | output_validation | 0.80 | 2 | output |
| CAP-023 | human_in_loop_escalation | 0.77 | 1 | output |
| CAP-026 | hallucination_detection | 0.83 | 2 | output |
| CAP-008 | episodic_memory | 0.96 | 2 | post-output |
| CAP-027 | compliance_logging | 1.00 | 1 | post-output |

### Recurring Execution Pattern

Both entries share an identical 5-stage dependency structure:

```
[INGESTION] CAP-001 → [ROUTING] CAP-003 → [STATE] CAP-005 → CAP-006
→ [ENRICHMENT] CAP-007 → [REASONING] CAP-011
→ [OUTPUT] CAP-017 → CAP-028 → CAP-026
→ [POST-OUTPUT] CAP-008
```

The pattern is stable across both domains. CAP-001 always executes first. CAP-008 (episodic memory) always executes last — used for persistence, not generation. CAP-027 (compliance logging) occupies the final position in CORPUS-001, acting as an audit sink after all other processing completes.

### Ontology Weaknesses

1. **CAP-009 (tool_execution) has no upstream dependency defined** in CORPUS-001, where it does not appear. When it enters in CORPUS-002, it is placed mid-chain (position 0.45) but its relationship to CAP-003 (intent must precede action) is not formalized in the ontology.
2. **CAP-006 and CAP-007 occupy the same normalized position (0.33, 0.34)** across both entries, indicating they are co-equal enrichment steps. The ontology does not currently model parallel execution lanes — both are listed sequentially, which may introduce unnecessary latency in implementations.
3. **CAP-014 (planning_and_decomposition) is present only in CORPUS-002** at position 0.64. Its absence from CORPUS-001 is defensible (reactive dialog does not require decomposition), but its placement after enrichment and before output generation suggests it will occupy a recurring position in action-capable agents.
4. **No capability exists in the ontology between CAP-011 (self_evaluation) and CAP-017 (response_generation)** to handle branching: what executes when self-evaluation returns low confidence? Both entries describe this behaviorally in rationale text, but no dedicated capability (e.g., `conditional_routing` or `escalation_trigger`) models it structurally.

---

## 5. Risk Analysis

### Risk Distribution by Severity and Probability

| severity | count | entries |
|---|---|---|
| critical | 4 | both |
| high | 6 | both |

| probability | count |
|---|---|
| occasional | 6 |
| frequent | 4 |

Both entries rate overall risk as **high**. No entry has been rated low or medium risk.

### Risk Groups

#### Security (1 risk)

| entry | risk_id | description | severity | probability |
|---|---|---|---|---|
| CORPUS-001 | RISK-002 | Missed mandatory escalation — agent handles legal/billing dispute autonomously | critical | occasional |

Security risks are access-control and safety-gate failures. At corpus scale, this category is underrepresented: only one entry triggers a security-class risk, because CORPUS-002 has no access-control or human-safety requirement. As entries for medical, financial, and autonomous execution domains are added, this category will grow.

#### Hallucination (2 risks)

| entry | risk_id | description | severity | probability |
|---|---|---|---|---|
| CORPUS-001 | RISK-004 | Policy hallucination delivered as fact — customer acts on incorrect refund policy | high | occasional |
| CORPUS-002 | RISK-004 | Incorrect suggested fix introduces new bug | high | occasional |

Hallucination risk appears in every entry at high severity, occasional probability. Both instances are output-stage risks: the failure happens after generation (CAP-017), at the validation step (CAP-028). This confirms CAP-028 (output validation) as a structural dependency of hallucination risk mitigation — it appears in every entry precisely to contain these risks.

#### Execution (2 risks)

| entry | risk_id | description | severity | probability |
|---|---|---|---|---|
| CORPUS-002 | RISK-001 | Incorrect promotion: false negative on failed build reaches production | critical | occasional |
| CORPUS-002 | RISK-002 | Log truncation causes missed failures — context window exceeded | critical | frequent |

Both execution risks are in the engineering entry because CORPUS-001 does not invoke CAP-009 (tool_execution). This establishes a direct pattern: execution risks only arise in entries where the agent has write access to infrastructure. As action-capable agents grow in the corpus, this risk category will become the largest.

#### Compliance (1 risk)

| entry | risk_id | description | severity | probability |
|---|---|---|---|---|
| CORPUS-001 | RISK-001 | PII leak into audit logs — SOC2 compliance failure | critical | occasional |

Compliance risk is currently correlated with entries that declare `compliance_requirements`. CORPUS-002 declares no compliance requirements and has no compliance risk. This correlation will break as more regulated domains enter the corpus (healthcare, finance).

#### Operational (5 risks)

| entry | risk_id | description | severity | probability |
|---|---|---|---|---|
| CORPUS-001 | RISK-003 | Latency breach under load — retrieval + generation exceeds 5000ms budget | high | occasional |
| CORPUS-001 | RISK-005 | Customer trust loss in first two weeks from poor responses | high | frequent |
| CORPUS-002 | RISK-003 | Flaky test misclassification as regression — developer alert fatigue | high | frequent |
| CORPUS-002 | RISK-004 | Incorrect suggested fix introduces a new bug | high | occasional |
| CORPUS-002 | RISK-005 | Developer adoption failure from high comment volume | high | frequent |

Operational risks are the largest group (5 of 10). Three of the five are rated `frequent` probability. The adoption failure pattern (CORPUS-001 RISK-005 and CORPUS-002 RISK-005) is the only risk class that appears in both entries at equivalent form: both describe first-deployment trust collapse driven by output quality or volume.

### Most Risk-Involved Capabilities

| capability_id | name | risk_involvement_count |
|---|---|---|
| CAP-017 | response_generation | 5 |
| CAP-003 | intent_classification | 3 |
| CAP-028 | output_validation | 3 |
| CAP-001 | text_understanding | 2 |
| CAP-005 | short_term_context_management | 2 |
| CAP-011 | self_evaluation | 2 |
| CAP-026 | hallucination_detection | 2 |

CAP-017 (response_generation) is the most risk-implicated capability in the corpus: it appears in 5 of 10 risks across both entries. This is expected — it is the output gate and the point where all upstream errors manifest as user-facing failures.

---

## 6. Evaluation Analysis

### Evaluation Coverage per Capability

| capability_id | name | eval_count | evaluated_in |
|---|---|---|---|
| CAP-003 | intent_classification | 2 | both entries |
| CAP-017 | response_generation | 2 | both entries |
| CAP-028 | output_validation | 2 | both entries |
| CAP-005 | short_term_context_management | 1 | CORPUS-001 only |
| CAP-006 | long_term_memory_storage | 1 | CORPUS-002 only |
| CAP-007 | semantic_retrieval | 1 | CORPUS-001 only |
| CAP-009 | tool_execution | 1 | CORPUS-002 only |
| CAP-011 | self_evaluation | 1 | CORPUS-002 only |
| CAP-014 | planning_and_decomposition | 1 | CORPUS-002 only |
| CAP-018 | multi_turn_dialogue_management | 1 | CORPUS-001 only |
| CAP-023 | human_in_loop_escalation | 1 | CORPUS-001 only |
| CAP-025 | pii_detection_and_redaction | 1 | CORPUS-001 only |
| CAP-027 | compliance_logging | 1 | CORPUS-001 only |

### Unevaluated Capabilities (0 evaluations across corpus)

| capability_id | name | tier | risk_involved | gap_severity |
|---|---|---|---|---|
| CAP-001 | text_understanding | P0 in both | yes (2 risks) | **high** |
| CAP-026 | hallucination_detection | P2 in both | yes (2 risks) | medium |
| CAP-008 | episodic_memory | P2 in both | no | low |

**CAP-001 (text_understanding) is the highest-severity evaluation gap in the corpus.** It is P0 in both entries, involved in 2 risks, and has zero evaluation requirements across both entries. Both entries treat it as a prerequisite foundation but provide no test methodology to verify its adequacy. This gap should be addressed in the next revision of both entries.

CAP-026 (hallucination_detection) is involved in 2 risks and has no direct evaluation. Its risk is partially absorbed by CAP-028 evaluations, but a standalone hallucination detection test is absent.

### Evaluation Priority Distribution

| priority | count | percentage |
|---|---|---|
| required | 14 | 87.5% |
| recommended | 2 | 12.5% |

Both `recommended` evaluations are for lower-priority capabilities: CAP-028 policy validation (CORPUS-001) and CAP-014 root cause consolidation (CORPUS-002). The 87.5% required rate indicates a high-rigor evaluation standard across the current corpus.

### Pass Threshold Distribution

| range | count | capability examples |
|---|---|---|
| 1.00 | 1 | CAP-027 (compliance logging) |
| 0.95–0.99 | 5 | CAP-025 (0.99), CAP-023 (0.98), CAP-009 (0.99), CAP-011 (0.95), CAP-028 (0.95) |
| 0.90–0.94 | 4 | CAP-003 (0.90, 0.92), CAP-028 (0.90), CAP-005 (0.90) |
| 0.85–0.89 | 3 | CAP-007 (0.85), CAP-018 (0.88), CAP-006 (0.85), CAP-014 (0.85) |
| 0.80–0.84 | 2 | CAP-017 (0.80 in both entries) |

CAP-027 is the only capability requiring 100% pass threshold. Compliance logging completeness is binary — a missing log field is an audit finding regardless of rate. CAP-017 (response_generation) consistently receives the lowest threshold (0.80) across both entries, reflecting the inherent subjectivity of output quality evaluation.

---

## 7. Corpus Quality Metrics

### Per-Entry Metrics

| metric | CORPUS-001 | CORPUS-002 | avg |
|---|---|---|---|
| capability_count | 14 | 12 | 13.0 |
| P0_count | 9 | 7 | 8.0 |
| P1_count | 3 | 3 | 3.0 |
| P2_count | 2 | 2 | 2.0 |
| risk_count | 5 | 5 | 5.0 |
| eval_count | 9 | 7 | 8.0 |
| eval_coverage | 64% | 58% | 61.5% |
| risk_coverage | 36% | 42% | 39% |
| validation_confidence | 0.88 | 0.86 | 0.87 |
| effort_from_zero (days) | 35 | 28 | 31.5 |

### Corpus Quality Score: **0.949 / 1.0**

**Methodology:**

The quality score is a weighted composite of 6 factors per entry, averaged across all entries:

$$Q = 0.25 \cdot S + 0.20 \cdot \min\left(\frac{E/C}{0.7}, 1\right) + 0.15 \cdot \min\left(\frac{R/C}{0.35}, 1\right) + 0.20 \cdot V + 0.10 \cdot D + 0.10 \cdot F$$

Where:
- **S** = schema completeness (1.0 if all 8 required sections present). Weight 0.25.
- **E/C** = evaluation coverage ratio (evaluations / capabilities). Target ≥ 0.70. Weight 0.20.
- **R/C** = risk coverage ratio (risks / capabilities). Target ≥ 0.35. Weight 0.15.
- **V** = validation confidence score (0–1). Weight 0.20.
- **D** = dependency order present (1.0 / 0.0). Weight 0.10.
- **F** = effort estimate present (1.0 / 0.0). Weight 0.10.

Both entries achieve full schema completeness, dependency order, and effort estimate presence. The primary score drag is evaluation coverage: CORPUS-001 at 64% and CORPUS-002 at 58% against the 70% target. Closing the CAP-001 evaluation gap would raise both entries toward 0.97+.

---

## 8. Recommendations

Ranked by estimated intelligence value to the corpus.

### Missing Capability Patterns

The following capability patterns are absent from all current entries:

1. **Streaming / real-time output** — neither entry models agents that produce incremental output. All current entries assume request-response. Streaming is a distinct execution model required for voice agents, live dashboards, and long-generation tasks.
2. **Multi-agent coordination** — no entry models a supervisor-worker pattern, agent handoff, or parallel agent execution. As agents are deployed in pipelines rather than in isolation, this becomes a first-class concern.
3. **Structured output generation** — both entries focus on natural-language response generation (CAP-017). Neither models agents whose primary output is JSON, SQL, or a structured schema. This capability class is required for data-transformation and code-generation agents.
4. **Feedback ingestion** — no entry models the agent learning from explicit user feedback signals (thumbs up/down, corrections). This is distinct from episodic memory (CAP-008) which stores events, not feedback-driven weight updates.
5. **Capability degradation under constraint** — neither entry models how the agent behaves when a P1 or P2 capability is unavailable at runtime. The corpus describes capability tiers but does not define graceful degradation paths.

### Missing Goal Classes

The current corpus covers only `reactive_agent`. The following goal classes are absent:

| goal_class | description | example entry |
|---|---|---|
| `proactive_agent` | initiates actions without explicit trigger | monitoring alerting, scheduled summarization |
| `generative_agent` | primary output is a structured artifact | code generation, document drafting, schema design |
| `orchestration_agent` | coordinates other agents or tools | multi-agent pipeline, workflow engine |
| `learning_agent` | modifies behavior based on feedback | fine-tuning loop, RLHF pipeline |

### Highest-Value Next Corpus Entries — Ranked

| rank | suggested_entry | domain | domain_variant | rationale |
|---|---|---|---|---|
| 1 | Code Generation Agent | engineering | code_generation | Covers `generative_agent` goal class and `structured_output_generation` capability gap. High industry deployment frequency. |
| 2 | Data Transformation Agent | data | etl | Covers `structured_output_generation`, `planning_and_decomposition` at P0, and introduces schema validation as a new risk class. |
| 3 | Multi-Agent Orchestration Supervisor | platform | orchestration | Introduces `orchestration_agent` goal class. Exposes inter-agent trust, partial failure, and result aggregation as new capability requirements. |
| 4 | Medical Triage Assistant | healthcare | clinical | Adds HIPAA-equivalent compliance pressure, high-stakes escalation, and introduces the `safety_guardrails` capability class absent from current entries. |
| 5 | Financial Analysis Agent | finance | research | Covers proactive generation of structured reports, introduces regulatory constraints, and adds `numerical_reasoning` as a new capability class. |
| 6 | Customer Onboarding Agent | support | smb | Tests whether the enterprise support pattern (CORPUS-001) generalizes to SMB constraints: lower compliance, shorter conversations, lower latency budget. |

### Ontology Gaps Requiring Capability ID Assignment

The following capabilities are referenced by behavior in current entries but have no CAP-ID in the ontology:

- `conditional_routing` — the branching behavior triggered by low-confidence self-evaluation
- `parallel_retrieval` — CAP-006 and CAP-007 execute at the same position but are modeled sequentially
- `graceful_degradation` — runtime fallback when a P1/P2 capability is unavailable
- `structured_output_generation` — JSON/SQL/schema output, distinct from natural-language CAP-017
