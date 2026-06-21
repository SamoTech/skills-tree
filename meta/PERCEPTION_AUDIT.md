# PERCEPTION AUDIT — TASK-005A

> **Status:** READ-ONLY audit. No graph modifications. No nodes created.
> **Graph baseline:** 47 nodes · 93 edges · 0 `01-perception` nodes
> **Source directory:** `skills/01-perception/` — 34 skill files + README
> **Executed:** 2026-06-21T10:04Z

---

## Scoring Methodology

Each candidate is scored on three axes, each 0.0–1.0:

| Axis | Definition |
|---|---|
| **Duplicate Risk** | Semantic overlap with existing 47 nodes (lower = safer) |
| **Production Relevance** | How often this skill appears in real deployed agentic systems |
| **Goal Coverage** | Which constitution goals (G01–G08) and M-05 this node would satisfy |

**Composite Score** = `(production_relevance × 0.45) + ((1 − duplicate_risk) × 0.30) + (goal_coverage × 0.25)`

Goal coverage scoring: G03 (multimodal input) = +0.40, G05 (autonomous agents) = +0.30, G06 (document workflows) = +0.25, M-05 (perceive dimension) = always +0.05 for any `01-perception` node.

---

## Full Candidate Table — All 34 Files

| # | Filename | Candidate Node ID | Duplicate Risk | Risk Reason | Prod. Relevance | Goal Coverage | **Composite** |
|---|---|---|---|---|---|---|---|
| 1 | `ocr.md` | `skill:ocr` | **0.05** | Unique — no existing OCR concept | **0.97** | G03·G06·M-05 → 0.70 | **0.888** |
| 2 | `document-parsing.md` | `skill:document-parsing` | **0.15** | Slight overlap with `skill:data-extraction` (different scope) | **0.95** | G05·G06·M-05 → 0.60 | **0.888** |
| 3 | `image-understanding.md` | `skill:image-understanding` | **0.08** | No visual-perception node exists | **0.93** | G03·G05·M-05 → 0.75 | **0.882** |
| 4 | `screen-reading.md` | `skill:screen-reading` | **0.12** | Slight overlap with `skill:browser-automation` (different: observation vs control) | **0.91** | G03·G05·M-05 → 0.75 | **0.864** |
| 5 | `structured-data-reading.md` | `skill:structured-data-reading` | **0.22** | Meaningful overlap with `skill:data-extraction`; distinct: schema-aware reading vs extraction action | **0.94** | G05·G06·M-05 → 0.60 | **0.849** |
| 6 | `audio-transcription.md` | `skill:audio-transcription` | **0.05** | Fully unique — no audio node exists | **0.88** | G03·M-05 → 0.45 | **0.845** |
| 7 | `code-reading.md` | `skill:code-reading` | **0.18** | Semantic neighbor of `skill:code-generation`; distinct: comprehension vs synthesis | **0.92** | G05·M-05 → 0.35 | **0.838** |
| 8 | `api-response-parsing.md` | `skill:api-response-parsing` | **0.35** | Overlaps `skill:api-integration` + `skill:data-extraction` — distinct but adjacent | **0.90** | G05·M-05 → 0.35 | **0.808** |
| 9 | `database-reading.md` | `skill:database-reading` | **0.20** | No DB-read node; `skill:data-extraction` is output-focused, this is query/schema read | **0.88** | G05·G06·M-05 → 0.60 | **0.802** |
| 10 | `email-parsing.md` | `skill:email-parsing` | **0.10** | Unique — no email concept in graph | **0.85** | G05·G06·M-05 → 0.60 | **0.795** |
| 11 | `file-system-reading.md` | `skill:file-system-reading` | **0.10** | Unique — no FS read node | **0.84** | G05·M-05 → 0.35 | **0.786** |
| 12 | `chart-reading.md` | `skill:chart-reading` | **0.10** | Unique — no visual chart-reading node | **0.82** | G03·M-05 → 0.45 | **0.779** |
| 13 | `url-dom-inspection.md` | `skill:url-dom-inspection` | **0.20** | Overlaps `skill:web-scraping`; distinct: structural inspection vs data collection | **0.83** | G05·M-05 → 0.35 | **0.770** |
| 14 | `text-reading.md` | `skill:text-reading` | **0.40** | High overlap with `skill:prompt-engineering` input side; too generic | **0.80** | M-05 → 0.05 | **0.709** |
| 15 | `pdf-parsing.md` | `skill:pdf-parsing` | **0.20** | Sub-skill of document-parsing; risk of being redundant if #2 selected | **0.80** | G06·M-05 → 0.30 | **0.721** |
| 16 | `markdown-parsing.md` | `skill:markdown-parsing` | **0.30** | Adjacent to `skill:structured-data-reading`; narrow scope | **0.78** | G05·M-05 → 0.35 | **0.705** |
| 17 | `multimodal-document-reading.md` | `skill:multimodal-input` | **0.20** | Bridges ocr + image-understanding; risk of redundancy if both #1 and #3 selected | **0.85** | G03·M-05 → 0.45 | **0.749** |
| 18 | `table-extraction.md` | `skill:table-extraction` | **0.30** | Overlaps `skill:structured-data-reading` and `skill:data-extraction` | **0.78** | G06·M-05 → 0.30 | **0.696** |
| 19 | `log-parsing.md` | `skill:log-parsing` | **0.10** | Unique; narrow scope (DevOps focus) | **0.75** | G05·M-05 → 0.35 | **0.692** |
| 20 | `video-understanding.md` | `skill:video-understanding` | **0.10** | Unique; extension of image-understanding; narrower deployment | **0.72** | G03·M-05 → 0.45 | **0.683** |
| 21 | `handwriting-recognition.md` | `skill:handwriting-recognition` | **0.10** | Unique; sub-domain of OCR; less universal | **0.70** | G03·M-05 → 0.45 | **0.671** |
| 22 | `sensor-reading.md` | `skill:sensor-reading` | **0.05** | Unique; low production deployment in LLM agents today | **0.62** | G03·M-05 → 0.45 | **0.630** |
| 23 | `json-schema-validation.md` | `skill:json-schema-validation` | **0.45** | Significant overlap with `skill:structured-data-reading` and `skill:data-extraction` | **0.78** | M-05 → 0.05 | **0.628** |
| 24 | `html-reading.md` | `skill:html-reading` | **0.35** | Overlaps `skill:url-dom-inspection` and `skill:web-scraping` | **0.75** | M-05 → 0.05 | **0.613** |
| 25 | `xml-parsing.md` | `skill:xml-parsing` | **0.35** | Narrow subset of structured-data-reading | **0.72** | M-05 → 0.05 | **0.601** |
| 26 | `conversation-history-reading.md` | `skill:conversation-history-reading` | **0.55** | Significant overlap with `skill:context-management` | **0.75** | M-05 → 0.05 | **0.589** |
| 27 | `knowledge-graph-reading.md` | `skill:knowledge-graph-reading` | **0.30** | Unique concept; narrow deployment scope | **0.65** | M-05 → 0.05 | **0.578** |
| 28 | `spreadsheet-reading.md` | `skill:spreadsheet-reading` | **0.20** | Sub-skill; covered by structured-data-reading if #5 selected | **0.68** | G06·M-05 → 0.30 | **0.576** |
| 29 | `git-diff-reading.md` | `skill:git-diff-reading` | **0.15** | Unique concept; very narrow DevOps scope | **0.60** | M-05 → 0.05 | **0.556** |
| 30 | `binary-file-reading.md` | `skill:binary-file-reading` | **0.10** | Unique; very low LLM-agent production relevance | **0.55** | M-05 → 0.05 | **0.533** |
| 31 | `geospatial-reading.md` | `skill:geospatial-reading` | **0.05** | Unique; very narrow scope | **0.50** | M-05 → 0.05 | **0.511** |
| 32 | `calendar-parsing.md` | `skill:calendar-parsing` | **0.15** | Narrow; low centrality potential | **0.55** | M-05 → 0.05 | **0.510** |
| 33 | `network-traffic-reading.md` | `skill:network-traffic-reading` | **0.10** | Unique; security/infra niche, low LLM-agent relevance | **0.48** | M-05 → 0.05 | **0.494** |
| 34 | `social-media-reading.md` | `skill:social-media-reading` | **0.15** | Narrow; not architecture-level | **0.50** | M-05 → 0.05 | **0.487** |
| 35 | `time-series-reading.md` | `skill:time-series-reading` | **0.15** | Narrow analytics scope | **0.48** | M-05 → 0.05 | **0.483** |
| 36 | `contract-reading.md` | `skill:contract-reading` | **0.10** | Unique; vertical-specific (legal) | **0.45** | M-05 → 0.05 | **0.475** |

---

## Existing Node Duplicate Map

Nodes in current graph most likely to collide with perception candidates:

| Existing Node | Collision Risk With | Risk Level |
|---|---|---|
| `skill:data-extraction` | `skill:structured-data-reading`, `skill:table-extraction` | Medium |
| `skill:api-integration` | `skill:api-response-parsing` | Low-Medium |
| `skill:browser-automation` | `skill:screen-reading`, `skill:url-dom-inspection` | Low |
| `skill:web-scraping` | `skill:url-dom-inspection`, `skill:html-reading` | Low-Medium |
| `skill:context-management` | `skill:conversation-history-reading` | High |
| `skill:rag-retrieval` | `skill:structured-data-reading` | Low |
| `skill:code-generation` | `skill:code-reading` | Low |

**No existing node maps to:** `skill:ocr`, `skill:image-understanding`, `skill:audio-transcription`, `skill:screen-reading`, `skill:document-parsing` — zero collision.

---

## Constitution Alignment

| Constitution Requirement | Current State | After +6 Perception Nodes |
|---|---|---|
| M-05: Perceive dimension populated | ❌ 0 nodes | ✅ 6 nodes |
| G03: Multimodal input handling | ❌ blocked | ✅ unblocked |
| G05: Autonomous agent workflows | ⚠️ partial | ✅ strengthened |
| G06: Document processing pipelines | ❌ blocked | ✅ unblocked |
| Category coverage ≥3 nodes | ❌ 0/3 | ✅ 6/3 (200%) |
