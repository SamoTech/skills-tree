# NODE SELECTION — TASK-005A

> **Status:** READ-ONLY selection plan. No graph modifications.
> **Selection target:** 6 nodes from 34 candidates in `skills/01-perception/`
> **Constraint:** Composite score ≥ 0.84, duplicate risk < 0.25, goal coverage includes M-05

---

## Selected 6 Nodes — Ranked by Composite Score

### RANK 1 — `skill:ocr`

| Field | Value |
|---|---|
| **Node ID** | `skill:ocr` |
| **Name** | Optical Character Recognition (OCR) |
| **Source File** | `skills/01-perception/ocr.md` (7,179 bytes — largest in category) |
| **Category** | `01-perception` |
| **Level** | `intermediate` |
| **Stability** | `stable` |
| **Composite Score** | **0.888** |
| **Duplicate Risk** | 0.05 — no existing node covers OCR |
| **Production Relevance** | 0.97 — deployed in document automation, invoice processing, form digitisation |
| **Goal Coverage** | G03 (multimodal input), G06 (document workflows), M-05 |
| **Why selected** | Largest file signals richest content. Foundational perceptual primitive — ocr bridges physical/digital documents into agent context. Hub candidate: `skill:document-parsing` and `skill:image-understanding` both depend on it. |

---

### RANK 2 — `skill:document-parsing`

| Field | Value |
|---|---|
| **Node ID** | `skill:document-parsing` |
| **Name** | Document Parsing |
| **Source File** | `skills/01-perception/document-parsing.md` (3,444 bytes) |
| **Category** | `01-perception` |
| **Level** | `intermediate` |
| **Stability** | `stable` |
| **Composite Score** | **0.888** |
| **Duplicate Risk** | 0.15 — `skill:data-extraction` handles output; this handles structural parsing input |
| **Production Relevance** | 0.95 — PDF/DOCX/PPTX parsing is universal in enterprise agentic workflows |
| **Goal Coverage** | G05 (autonomous agents), G06 (document workflows), M-05 |
| **Why selected** | Directly unblocks G06. Natural bridge between `skill:ocr` (raw text) and `skill:rag-retrieval` (semantic retrieval). |

---

### RANK 3 — `skill:image-understanding`

| Field | Value |
|---|---|
| **Node ID** | `skill:image-understanding` |
| **Name** | Image Understanding |
| **Source File** | `skills/01-perception/image-understanding.md` (3,238 bytes) |
| **Category** | `01-perception` |
| **Level** | `intermediate` |
| **Stability** | `stable` |
| **Composite Score** | **0.882** |
| **Duplicate Risk** | 0.08 — fully unique; no visual-modality node in graph |
| **Production Relevance** | 0.93 — GPT-4V, Claude vision, Gemini all deployed with image inputs |
| **Goal Coverage** | G03 (multimodal input), G05 (autonomous agents), M-05 |
| **Why selected** | Primary multimodal perception node. Directly satisfies G03. Creates the first visual-modality edge in the graph. Connects to `skill:ocr` (text in images) and `skill:chart-reading` (future). |

---

### RANK 4 — `skill:screen-reading`

| Field | Value |
|---|---|
| **Node ID** | `skill:screen-reading` |
| **Name** | Screen Reading |
| **Source File** | `skills/01-perception/screen-reading.md` (4,084 bytes) |
| **Category** | `01-perception` |
| **Level** | `intermediate` |
| **Stability** | `stable` |
| **Composite Score** | **0.864** |
| **Duplicate Risk** | 0.12 — `skill:browser-automation` is control-side; screen-reading is observation-side |
| **Production Relevance** | 0.91 — computer-use agents (Claude, Operator) are rapidly deployed |
| **Goal Coverage** | G03 (multimodal input), G05 (autonomous agents), M-05 |
| **Why selected** | Computer-use agent dimension. Connects observation (`skill:screen-reading`) to action (`skill:browser-automation`) forming the perceive→act loop, foundational to autonomous agents. |

---

### RANK 5 — `skill:structured-data-reading`

| Field | Value |
|---|---|
| **Node ID** | `skill:structured-data-reading` |
| **Name** | Structured Data Reading |
| **Source File** | `skills/01-perception/structured-data-reading.md` (3,451 bytes) |
| **Category** | `01-perception` |
| **Level** | `beginner` |
| **Stability** | `stable` |
| **Composite Score** | **0.849** |
| **Duplicate Risk** | 0.22 — acceptable; `skill:data-extraction` is output-oriented; this is schema-aware input reading |
| **Production Relevance** | 0.94 — JSON/CSV/YAML/TOML reading is the most common agent I/O pattern |
| **Goal Coverage** | G05 (autonomous agents), G06 (document workflows), M-05 |
| **Why selected** | Backbone of all agent input pipelines. Provides `LEARN_BEFORE` anchor for `skill:api-response-parsing` and `skill:document-parsing`. Highest production frequency of any data-perception node. |

---

### RANK 6 — `skill:audio-transcription`

| Field | Value |
|---|---|
| **Node ID** | `skill:audio-transcription` |
| **Name** | Audio Transcription |
| **Source File** | `skills/01-perception/audio-transcription.md` (3,077 bytes) |
| **Category** | `01-perception` |
| **Level** | `intermediate` |
| **Stability** | `stable` |
| **Composite Score** | **0.845** |
| **Duplicate Risk** | 0.05 — fully unique; no audio node in graph |
| **Production Relevance** | 0.88 — Whisper API, AssemblyAI, voice agents widely deployed |
| **Goal Coverage** | G03 (multimodal input), M-05 |
| **Why selected** | Completes the multimodal triad: visual (`skill:image-understanding`), document (`skill:ocr`), audio (`skill:audio-transcription`). Fully unique — zero collision risk. Required for voice-first agent architectures. |

---

## Rejected Candidates — Reasons

| Node ID | Score | Rejection Reason |
|---|---|---|
| `skill:code-reading` | 0.838 | Displaced by 6 higher-scorers; can be TASK-005C |
| `skill:api-response-parsing` | 0.808 | Duplicate risk 0.35 with `skill:api-integration` — defer |
| `skill:database-reading` | 0.802 | Strong candidate for TASK-005C; no urgent goal dependency |
| `skill:text-reading` | 0.709 | Duplicate risk 0.40; too generic |
| `skill:multimodal-input` | 0.749 | Redundant if `skill:ocr` + `skill:image-understanding` + `skill:audio-transcription` all present |
| All others | <0.72 | Below threshold or too narrow scope |

---

## Selected Node Summary

```
RANK  NODE ID                        LEVEL         STABILITY  COMPOSITE
1     skill:ocr                      intermediate  stable     0.888
2     skill:document-parsing         intermediate  stable     0.888
3     skill:image-understanding      intermediate  stable     0.882
4     skill:screen-reading           intermediate  stable     0.864
5     skill:structured-data-reading  beginner      stable     0.849
6     skill:audio-transcription      intermediate  stable     0.845
```
