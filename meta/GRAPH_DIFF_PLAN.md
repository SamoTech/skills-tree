# GRAPH DIFF PLAN — TASK-005A

> **Status:** READ-ONLY projection. No modifications applied.
> **Baseline:** 47 nodes · 93 edges · schema_version 1.3
> **Projection:** 53 nodes · 108 edges
> **Delta:** +6 nodes · +15 edges

---

## Exact Node Definitions (Ready to Insert)

```json
{"id": "skill:ocr",                     "type": "Skill", "name": "Optical Character Recognition", "category": "01-perception", "level": "intermediate", "stability": "stable",   "centrality": {"in_degree": 0, "out_degree": 2, "degree": 2, "degree_centrality": 0.0377}},
{"id": "skill:document-parsing",         "type": "Skill", "name": "Document Parsing",              "category": "01-perception", "level": "intermediate", "stability": "stable",   "centrality": {"in_degree": 1, "out_degree": 3, "degree": 4, "degree_centrality": 0.0755}},
{"id": "skill:image-understanding",      "type": "Skill", "name": "Image Understanding",           "category": "01-perception", "level": "intermediate", "stability": "stable",   "centrality": {"in_degree": 0, "out_degree": 2, "degree": 2, "degree_centrality": 0.0377}},
{"id": "skill:screen-reading",           "type": "Skill", "name": "Screen Reading",               "category": "01-perception", "level": "intermediate", "stability": "stable",   "centrality": {"in_degree": 0, "out_degree": 2, "degree": 2, "degree_centrality": 0.0377}},
{"id": "skill:structured-data-reading",  "type": "Skill", "name": "Structured Data Reading",       "category": "01-perception", "level": "beginner",     "stability": "stable",   "centrality": {"in_degree": 0, "out_degree": 2, "degree": 2, "degree_centrality": 0.0377}},
{"id": "skill:audio-transcription",      "type": "Skill", "name": "Audio Transcription",          "category": "01-perception", "level": "intermediate", "stability": "stable",   "centrality": {"in_degree": 0, "out_degree": 1, "degree": 1, "degree_centrality": 0.0189}}
```

> **Note on centrality:** Values above are projections based on the 15-edge plan below.
> Actual runtime centrality will be recomputed by EvidenceDeriver after insert.
> `degree_centrality` = `degree / (N-1)` where N = 53 after insert.

---

## Exact Edge Plan — 15 New Edges

### Cluster A — OCR edges (2 edges)

```json
{"source": "skill:ocr", "target": "skill:document-parsing",        "type": "SUPPORTS",     "confidence": 0.95},
{"source": "skill:ocr", "target": "skill:image-understanding",     "type": "RECOMMENDED_WITH", "confidence": 0.88}
```

**Rationale:**
- `OCR → document-parsing SUPPORTS 0.95`: OCR is the enabling mechanism for parsing scanned/image-based documents. Raw text produced by OCR feeds directly into document-parsing pipelines.
- `OCR → image-understanding RECOMMENDED_WITH 0.88`: OCR is frequently paired with image understanding (e.g., a screenshot contains both visual layout and embedded text). Not a hard dependency — image understanding works independently of OCR.

---

### Cluster B — Document Parsing edges (3 edges)

```json
{"source": "skill:document-parsing", "target": "skill:structured-data-reading", "type": "REQUIRES",     "confidence": 0.92},
{"source": "skill:document-parsing", "target": "skill:rag-retrieval",           "type": "RECOMMENDED_WITH", "confidence": 0.90},
{"source": "skill:document-parsing", "target": "skill:data-extraction",         "type": "SUPPORTS",     "confidence": 0.87}
```

**Rationale:**
- `document-parsing → structured-data-reading REQUIRES 0.92`: To parse a document you must be able to read its structural data types (JSON metadata, table rows, section headers). Structured data reading is a prerequisite.
- `document-parsing → rag-retrieval RECOMMENDED_WITH 0.90`: Documents are the most common corpus for RAG. Parsing is the ingestion step before retrieval — these two are deployed together in nearly every document-QA pipeline.
- `document-parsing → data-extraction SUPPORTS 0.87`: After parsing structure, agents extract specific data points. Parsing enables extraction but is not the same act.

---

### Cluster C — Image Understanding edges (2 edges)

```json
{"source": "skill:image-understanding", "target": "skill:prompt-engineering",  "type": "REQUIRES",         "confidence": 0.91},
{"source": "skill:image-understanding", "target": "skill:react-pattern",       "type": "RECOMMENDED_WITH", "confidence": 0.84}
```

**Rationale:**
- `image-understanding → prompt-engineering REQUIRES 0.91`: Multimodal prompting requires distinct prompt engineering techniques — image placement in context window, alt-text crafting, vision-specific system prompts. Cannot be effective without prompt engineering.
- `image-understanding → react-pattern RECOMMENDED_WITH 0.84`: Vision-capable agents commonly use ReAct (observe screenshot → reason → act). Not a hard dependency, but high co-deployment frequency.

---

### Cluster D — Screen Reading edges (2 edges)

```json
{"source": "skill:screen-reading", "target": "skill:browser-automation",  "type": "LEARN_BEFORE",     "confidence": 0.93},
{"source": "skill:screen-reading", "target": "skill:image-understanding",  "type": "REQUIRES",         "confidence": 0.89}
```

**Rationale:**
- `screen-reading → browser-automation LEARN_BEFORE 0.93`: You must be able to read/understand what is on a screen before you can automate interactions with it. Screen reading is the perceptual foundation of computer-use agents.
- `screen-reading → image-understanding REQUIRES 0.89`: Screen reading IS image understanding applied to UI surfaces. The agent receives a screenshot (an image) and must understand its visual content — image understanding is a hard prerequisite.

---

### Cluster E — Structured Data Reading edges (2 edges)

```json
{"source": "skill:structured-data-reading", "target": "skill:prompt-engineering", "type": "LEARN_BEFORE",     "confidence": 0.88},
{"source": "skill:structured-data-reading", "target": "skill:api-integration",    "type": "RECOMMENDED_WITH", "confidence": 0.86}
```

**Rationale:**
- `structured-data-reading → prompt-engineering LEARN_BEFORE 0.88`: Agents must parse tool responses (JSON), config files (YAML), and structured outputs before they can use them to build subsequent prompts. Structured data reading precedes effective prompt engineering in a pipeline.
- `structured-data-reading → api-integration RECOMMENDED_WITH 0.86`: API integration produces structured responses (JSON/XML) that must be read. The two skills are almost always co-present in any agent using external APIs.

---

### Cluster F — Audio Transcription edges (2 edges)

```json
{"source": "skill:audio-transcription", "target": "skill:prompt-engineering",  "type": "LEARN_BEFORE", "confidence": 0.85},
{"source": "skill:audio-transcription", "target": "skill:context-management",   "type": "SUPPORTS",     "confidence": 0.83}
```

**Rationale:**
- `audio-transcription → prompt-engineering LEARN_BEFORE 0.85`: Transcribed text must be correctly formatted and injected into the context window using prompt engineering techniques (speaker labeling, turn separation, timestamps).
- `audio-transcription → context-management SUPPORTS 0.83`: Audio generates long transcripts that require context window management — chunking, summarisation, selective retention. Transcription feeds context management.

---

### Cross-Cluster Integrity Edge (2 edges)

```json
{"source": "skill:ocr",            "target": "skill:structured-data-reading", "type": "LEARN_BEFORE", "confidence": 0.87},
{"source": "skill:screen-reading", "target": "skill:structured-data-reading", "type": "RECOMMENDED_WITH", "confidence": 0.81}
```

**Rationale:**
- `ocr → structured-data-reading LEARN_BEFORE 0.87`: OCR output is raw text that often contains structured data (tables, key-value pairs in forms). Agents must apply structured data reading on top of OCR output.
- `screen-reading → structured-data-reading RECOMMENDED_WITH 0.81`: UI screens frequently display structured data (tables, forms, dashboards). Reading screens well often requires structured data reading as a companion skill.

---

## Edge Type Distribution — Projected

| Edge Type | Current | Added | Projected |
|---|---|---|---|
| `REQUIRES` | 51 | 4 | **55** |
| `RECOMMENDED_WITH` | 28 | 6 | **34** |
| `SUPPORTS` | 4 | 3 | **7** |
| `LEARN_BEFORE` | 10 | 2 | **12** |
| **TOTAL** | **93** | **15** | **108** |

---

## Graph Before / After Projection

### BEFORE (Current Baseline)

```
Nodes : 47
Edges : 93
Categories populated:
  09-agentic-patterns   : 24 nodes (51%)
  02-reasoning          : 10 nodes (21%)
  03-memory             :  4 nodes ( 9%)
  07-tool-use           :  2 nodes ( 4%)
  15-orchestration      :  2 nodes ( 4%)
  05-code               :  1 node  ( 2%)
  04-action-execution   :  1 node  ( 2%)
  10-computer-use       :  1 node  ( 2%)
  11-web                :  1 node  ( 2%)
  12-data               :  1 node  ( 2%)
  01-perception         :  0 nodes ( 0%)  ← BLOCKED
Constitution M-05       : FAIL
Goal G03                : FAIL
Goal G06                : FAIL
Avg confidence          : 0.899
Hub node                : skill:prompt-engineering (degree 11)
```

### AFTER (Post TASK-005B)

```
Nodes : 53
Edges : 108
Categories populated:
  09-agentic-patterns   : 24 nodes (45%)
  02-reasoning          : 10 nodes (19%)
  01-perception         :  6 nodes (11%)  ← NEW
  03-memory             :  4 nodes ( 8%)
  07-tool-use           :  2 nodes ( 4%)
  15-orchestration      :  2 nodes ( 4%)
  [other categories]    :  5 nodes ( 9%)
Constitution M-05       : PASS  (6 nodes ≥ 3 threshold)
Goal G03                : PASS  (image-understanding + audio-transcription + screen-reading)
Goal G06                : PASS  (document-parsing + ocr + structured-data-reading)
Avg confidence (proj.)  : 0.897  (±0.002 — new edges slightly lower mean)
Hub node (proj.)        : skill:prompt-engineering (degree 14, gains 3 new in_degree edges)
New in_degree on RAG    : skill:rag-retrieval gains 1 edge from document-parsing
```

---

## Validation Checklist for TASK-005B

Before committing the graph, TASK-005B must verify:

- [ ] All 6 node IDs are unique (no collision with existing 47 IDs)
- [ ] All 15 edge source/target IDs resolve to existing nodes (after insertion of the 6 new ones)
- [ ] No self-loops (source ≠ target on all edges)
- [ ] No duplicate edges (same source+target+type combination)
- [ ] All confidence values in range [0.70, 1.00]
- [ ] `statistics` block updated: `total_nodes: 53`, `total_edges: 108`
- [ ] `statistics.edge_types` updated to projected distribution above
- [ ] `avg_confidence` recomputed from all 108 edges
- [ ] `_note` field updated with TASK-005B completion record
- [ ] `generated_at` updated to commit timestamp
- [ ] MEMORY_STATE.md version bumped to v1.4.0
- [ ] Governance TASK-005 status set to `COMPLETE`

---

## Risk Flags for TASK-005B Agent

| Flag | Detail |
|---|---|
| **F-01** | `skill:structured-data-reading` has 0.22 duplicate risk vs `skill:data-extraction` — edge `document-parsing → data-extraction SUPPORTS` must clarify separation in `_note` |
| **F-02** | `skill:screen-reading → skill:image-understanding REQUIRES` creates a dependency path: `screen-reading → image-understanding → prompt-engineering` — verify no cycle |
| **F-03** | `skill:prompt-engineering` will become the highest-degree node (degree ~14) — monitor for over-centralisation in next audit |
| **F-04** | `skill:ocr` has 0 in_degree after insert — acceptable for a new foundational node, but should gain in_degree in TASK-005C when `handwriting-recognition` or `pdf-parsing` is added |
| **F-05** | `avg_confidence` may drop below 0.895 if edge plan is followed exactly — acceptable per constitution threshold of 0.880 |
