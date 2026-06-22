# R02E_DUPLICATE_AUDIT.md

Mission: R-02E.1 — Collision Audit  
Date: 2026-06-22  
Audit type: Duplicate ID / Path / Slug / Category Overlap

---

## Audit Methodology

1. Loaded all 85 confirmed nodes from `data/SKILLS_GRAPH.json` (R-02B state)
2. Loaded all R-02E enumerated pending files: 17 from `11-web`, 18 from `12-data`, 14 from `13-creative` — all verified via GitHub Contents API this session
3. Applied node ID rule: `"skill:" + filename_without_extension`
4. Built two index maps: `id → [(category, path)]` and `path → [(id, category)]`
5. Identified entries where `len(entries) > 1` in the ID map
6. Cross-checked high-risk families (web-scraping, web-search, dom-inspection, form-fill, sql, embedding, social-media, image)
7. Confirmed path uniqueness — every path string appears exactly once

---

## Duplicate Node IDs

| Node ID | Path A | Category A | Path B | Category B |
|---|---|---|---|---|
| `skill:web-scraping` | `skills/04-action-execution/web-scraping.md` | `04-action-execution` | `skills/11-web/web-scraping.md` | `11-web` |

**Total duplicate IDs: 1**

---

## Duplicate Paths

None detected.

**Total duplicate paths: 0**

---

## Duplicate Slugs

Slug = filename without `.md` extension.

| Slug | File A | File B |
|---|---|---|
| `web-scraping` | `skills/04-action-execution/web-scraping.md` | `skills/11-web/web-scraping.md` |

**Total duplicate slugs: 1**

---

## Category Overlap Audit

Cross-category ID conflicts detected:

| Node ID | Category A | Category B | Conflict type |
|---|---|---|---|
| `skill:web-scraping` | `04-action-execution` | `11-web` | Same ID, different categories |

---

## Near-Miss Table (same concept, different slugs — no collision)

These were investigated as potential collisions but confirmed clean:

| Concept | ID in graph | Candidate ID from R-02E | Verdict |
|---|---|---|---|
| DOM inspection | `skill:url-dom-inspection` (01-perception) | `skill:dom-inspection` (11-web) | CLEAN — different slugs |
| Form interaction | `skill:form-fill` (04-action-execution) | `skill:form-filling` (11-web) | CLEAN — different slugs |
| URL navigation | `skill:url-navigation` (04-action-execution) | `skill:url-fetching` (11-web) | CLEAN — different slugs |
| SQL | `skill:sql-query-generation` (05-code) | `skill:sql-execution` (12-data) | CLEAN — different slugs |
| Social media | `skill:social-media-reading` (01-perception) | `skill:social-media-post` (13-creative) | CLEAN — different slugs |
| Image | `skill:image-understanding` (01-perception) | `skill:image-gen-prompt` (13-creative) | CLEAN — different slugs |
| Web search | (none in graph) | `skill:web-search` (11-web) | CLEAN — unique |
| Web search agents | (none in graph) | `skill:web-search-tool-agents` (11-web) | CLEAN — unique |

---

## Full Enumeration (all 134 raw entries)

### 01-perception (36)

| Node ID | Path |
|---|---|
| skill:api-response-parsing | skills/01-perception/api-response-parsing.md |
| skill:audio-transcription | skills/01-perception/audio-transcription.md |
| skill:binary-file-reading | skills/01-perception/binary-file-reading.md |
| skill:calendar-parsing | skills/01-perception/calendar-parsing.md |
| skill:chart-reading | skills/01-perception/chart-reading.md |
| skill:code-reading | skills/01-perception/code-reading.md |
| skill:contract-reading | skills/01-perception/contract-reading.md |
| skill:conversation-history-reading | skills/01-perception/conversation-history-reading.md |
| skill:database-reading | skills/01-perception/database-reading.md |
| skill:document-parsing | skills/01-perception/document-parsing.md |
| skill:email-parsing | skills/01-perception/email-parsing.md |
| skill:file-system-reading | skills/01-perception/file-system-reading.md |
| skill:geospatial-reading | skills/01-perception/geospatial-reading.md |
| skill:git-diff-reading | skills/01-perception/git-diff-reading.md |
| skill:handwriting-recognition | skills/01-perception/handwriting-recognition.md |
| skill:html-reading | skills/01-perception/html-reading.md |
| skill:image-understanding | skills/01-perception/image-understanding.md |
| skill:json-schema-validation | skills/01-perception/json-schema-validation.md |
| skill:knowledge-graph-reading | skills/01-perception/knowledge-graph-reading.md |
| skill:log-parsing | skills/01-perception/log-parsing.md |
| skill:markdown-parsing | skills/01-perception/markdown-parsing.md |
| skill:multimodal-document-reading | skills/01-perception/multimodal-document-reading.md |
| skill:network-traffic-reading | skills/01-perception/network-traffic-reading.md |
| skill:ocr | skills/01-perception/ocr.md |
| skill:pdf-parsing | skills/01-perception/pdf-parsing.md |
| skill:screen-reading | skills/01-perception/screen-reading.md |
| skill:sensor-reading | skills/01-perception/sensor-reading.md |
| skill:social-media-reading | skills/01-perception/social-media-reading.md |
| skill:spreadsheet-reading | skills/01-perception/spreadsheet-reading.md |
| skill:structured-data-reading | skills/01-perception/structured-data-reading.md |
| skill:table-extraction | skills/01-perception/table-extraction.md |
| skill:text-reading | skills/01-perception/text-reading.md |
| skill:time-series-reading | skills/01-perception/time-series-reading.md |
| skill:url-dom-inspection | skills/01-perception/url-dom-inspection.md |
| skill:video-understanding | skills/01-perception/video-understanding.md |
| skill:xml-parsing | skills/01-perception/xml-parsing.md |

### 04-action-execution (21)

| Node ID | Path |
|---|---|
| skill:api-call | skills/04-action-execution/api-call.md |
| skill:assertion | skills/04-action-execution/assertion.md |
| skill:calendar-event | skills/04-action-execution/calendar-event.md |
| skill:clipboard-ops | skills/04-action-execution/clipboard-ops.md |
| skill:database-write | skills/04-action-execution/database-write.md |
| skill:drag-drop | skills/04-action-execution/drag-drop.md |
| skill:email-send | skills/04-action-execution/email-send.md |
| skill:file-ops | skills/04-action-execution/file-ops.md |
| skill:form-fill | skills/04-action-execution/form-fill.md |
| skill:http-request | skills/04-action-execution/http-request.md |
| skill:keyboard-input | skills/04-action-execution/keyboard-input.md |
| skill:message-send | skills/04-action-execution/message-send.md |
| skill:mouse-click | skills/04-action-execution/mouse-click.md |
| skill:notification-trigger | skills/04-action-execution/notification-trigger.md |
| skill:os-command | skills/04-action-execution/os-command.md |
| skill:payment-action | skills/04-action-execution/payment-action.md |
| skill:screenshot-capture | skills/04-action-execution/screenshot-capture.md |
| skill:tab-management | skills/04-action-execution/tab-management.md |
| skill:ui-state-toggle | skills/04-action-execution/ui-state-toggle.md |
| skill:url-navigation | skills/04-action-execution/url-navigation.md |
| skill:web-scraping | skills/04-action-execution/web-scraping.md |

### 05-code (28)

| Node ID | Path |
|---|---|
| skill:algorithm-design | skills/05-code/algorithm-design.md |
| skill:api-client-generation | skills/05-code/api-client-generation.md |
| skill:bug-fixing | skills/05-code/bug-fixing.md |
| skill:cicd-generation | skills/05-code/cicd-generation.md |
| skill:code-execution-sandbox | skills/05-code/code-execution-sandbox.md |
| skill:code-explanation | skills/05-code/code-explanation.md |
| skill:code-generation | skills/05-code/code-generation.md |
| skill:code-interpreter-agent | skills/05-code/code-interpreter-agent.md |
| skill:code-review | skills/05-code/code-review.md |
| skill:code-search | skills/05-code/code-search.md |
| skill:code-translation | skills/05-code/code-translation.md |
| skill:db-schema-design | skills/05-code/db-schema-design.md |
| skill:debugging | skills/05-code/debugging.md |
| skill:dependency-auditor | skills/05-code/dependency-auditor.md |
| skill:dependency-management | skills/05-code/dependency-management.md |
| skill:dockerfile-generation | skills/05-code/dockerfile-generation.md |
| skill:documentation-generation | skills/05-code/documentation-generation.md |
| skill:git-operations | skills/05-code/git-operations.md |
| skill:github-api | skills/05-code/github-api.md |
| skill:integration-test-writing | skills/05-code/integration-test-writing.md |
| skill:linting-formatting | skills/05-code/linting-formatting.md |
| skill:performance-profiling | skills/05-code/performance-profiling.md |
| skill:refactoring | skills/05-code/refactoring.md |
| skill:regex-generation | skills/05-code/regex-generation.md |
| skill:repl-interaction | skills/05-code/repl-interaction.md |
| skill:security-scanning | skills/05-code/security-scanning.md |
| skill:sql-query-generation | skills/05-code/sql-query-generation.md |
| skill:unit-test-generation | skills/05-code/unit-test-generation.md |

### 11-web (17) — R-02E enumerated, pending graph write

| Node ID | Path |
|---|---|
| skill:api-discovery | skills/11-web/api-discovery.md |
| skill:browser-navigation | skills/11-web/browser-navigation.md |
| skill:captcha-solving | skills/11-web/captcha-solving.md |
| skill:cookie-management | skills/11-web/cookie-management.md |
| skill:dom-inspection | skills/11-web/dom-inspection.md |
| skill:form-filling | skills/11-web/form-filling.md |
| skill:js-execution | skills/11-web/js-execution.md |
| skill:link-extraction | skills/11-web/link-extraction.md |
| skill:rss-parsing | skills/11-web/rss-parsing.md |
| skill:sitemap-parsing | skills/11-web/sitemap-parsing.md |
| skill:url-fetching | skills/11-web/url-fetching.md |
| skill:url-screenshot | skills/11-web/url-screenshot.md |
| skill:web-crawling | skills/11-web/web-crawling.md |
| skill:web-login | skills/11-web/web-login.md |
| **skill:web-scraping** ⚠️ | **skills/11-web/web-scraping.md** |
| skill:web-search-tool-agents | skills/11-web/web-search-tool-agents.md |
| skill:web-search | skills/11-web/web-search.md |

### 12-data (18) — R-02E enumerated, pending graph write

| Node ID | Path |
|---|---|
| skill:anomaly-detection | skills/12-data/anomaly-detection.md |
| skill:csv-processing | skills/12-data/csv-processing.md |
| skill:data-aggregation | skills/12-data/data-aggregation.md |
| skill:data-cleaning | skills/12-data/data-cleaning.md |
| skill:data-filtering | skills/12-data/data-filtering.md |
| skill:data-joining | skills/12-data/data-joining.md |
| skill:data-summarization | skills/12-data/data-summarization.md |
| skill:data-visualization | skills/12-data/data-visualization.md |
| skill:embedding-generation | skills/12-data/embedding-generation.md |
| skill:etl-pipeline | skills/12-data/etl-pipeline.md |
| skill:json-transformation | skills/12-data/json-transformation.md |
| skill:nosql-query | skills/12-data/nosql-query.md |
| skill:pandas-operations | skills/12-data/pandas-operations.md |
| skill:schema-inference | skills/12-data/schema-inference.md |
| skill:similarity-search | skills/12-data/similarity-search.md |
| skill:sql-execution | skills/12-data/sql-execution.md |
| skill:statistical-analysis | skills/12-data/statistical-analysis.md |
| skill:time-series | skills/12-data/time-series.md |

### 13-creative (14) — R-02E enumerated, pending graph write

| Node ID | Path |
|---|---|
| skill:avatar-design | skills/13-creative/avatar-design.md |
| skill:blog-writing | skills/13-creative/blog-writing.md |
| skill:copywriting | skills/13-creative/copywriting.md |
| skill:creative-writing | skills/13-creative/creative-writing.md |
| skill:game-level-design | skills/13-creative/game-level-design.md |
| skill:image-gen-prompt | skills/13-creative/image-gen-prompt.md |
| skill:logo-design | skills/13-creative/logo-design.md |
| skill:lyrics-writing | skills/13-creative/lyrics-writing.md |
| skill:meme-generation | skills/13-creative/meme-generation.md |
| skill:music-composition | skills/13-creative/music-composition.md |
| skill:presentation-gen | skills/13-creative/presentation-gen.md |
| skill:social-media-post | skills/13-creative/social-media-post.md |
| skill:svg-generation | skills/13-creative/svg-generation.md |
| skill:video-script | skills/13-creative/video-script.md |

---

## Summary

| Audit type | Result |
|---|---|
| Duplicate IDs | 1 (`skill:web-scraping`) |
| Duplicate paths | 0 |
| Duplicate slugs | 1 (`web-scraping`) |
| Category overlaps | 1 (04-action-execution / 11-web) |
| Near-misses (clean) | 8 |
| All nodes traceable | YES |
