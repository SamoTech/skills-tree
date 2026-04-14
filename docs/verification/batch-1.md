# Verification Record — Batch 1

> **Type:** dependency-verify  
> **Date:** 2026-04-14  
> **Verified by:** SamoTech  
> **Method:** cross-checked PyPI metadata, official docs, and package changelogs  
> **Active CVEs at time of verification:** none

---

## Skills Verified

### `skills/01-perception/image-understanding.md`

| Package | Min Version | Tested Version | PyPI Link | Status |
|---|---|---|---|---|
| openai | 1.0.0 | 1.30.1 | [pypi.org/project/openai](https://pypi.org/project/openai/) | ✅ verified |
| httpx | 0.27.0 | 0.27.0 | [pypi.org/project/httpx](https://pypi.org/project/httpx/) | ✅ verified |

- [x] Read PyPI source  
- [x] Cross-checked official OpenAI Python SDK docs  
- [x] `groundingdino` block correctly marked `type: illustrative` (requires manual model weights)

---

### `skills/01-perception/audio-transcription.md`

| Package | Min Version | Tested Version | PyPI Link | Status |
|---|---|---|---|---|
| openai-whisper | 20231117 | 20231117 | [pypi.org/project/openai-whisper](https://pypi.org/project/openai-whisper/) | ✅ verified |
| torch | 2.1.0 | 2.3.0 | [pypi.org/project/torch](https://pypi.org/project/torch/) | ✅ verified |

- [x] Read PyPI source  
- [x] Cross-checked OpenAI Whisper GitHub README  
- [x] `pyannote.audio` block correctly marked `type: illustrative` (requires HuggingFace token + model download)

---

### `skills/04-action-execution/calendar-event.md`

| Package | Min Version | Tested Version | PyPI Link | Status |
|---|---|---|---|---|
| google-api-python-client | 2.100.0 | 2.130.0 | [pypi.org/project/google-api-python-client](https://pypi.org/project/google-api-python-client/) | ✅ verified |
| google-auth | 2.23.0 | 2.29.0 | [pypi.org/project/google-auth](https://pypi.org/project/google-auth/) | ✅ verified |

- [x] Read PyPI source  
- [x] Cross-checked Google API Python Client docs  
- [x] `googleapiclient` import name confirmed as alias for `google-api-python-client`  
- [x] Example block marked `type: illustrative` (requires OAuth2 credentials)

---

### `skills/07-tool-use/google-workspace-api.md`

| Package | Min Version | Tested Version | PyPI Link | Status |
|---|---|---|---|---|
| google-api-python-client | 2.100.0 | 2.130.0 | [pypi.org/project/google-api-python-client](https://pypi.org/project/google-api-python-client/) | ✅ verified |
| google-auth | 2.23.0 | 2.29.0 | [pypi.org/project/google-auth](https://pypi.org/project/google-auth/) | ✅ verified |

- [x] Read PyPI source  
- [x] Cross-checked Google Workspace Python Quickstart  
- [x] Example block marked `type: illustrative` (requires OAuth2 credentials)

---

### `skills/03-memory/procedural.md`

| Package | Min Version | Tested Version | PyPI Link | Status |
|---|---|---|---|---|
| mem0ai | 0.1.0 | 0.1.19 | [pypi.org/project/mem0ai](https://pypi.org/project/mem0ai/) | ✅ verified |
| anthropic | 0.25.0 | 0.28.0 | [pypi.org/project/anthropic](https://pypi.org/project/anthropic/) | ✅ verified |

- [x] Read PyPI source  
- [x] Cross-checked Mem0 docs (mem0.ai/docs)  
- [x] `mem0` confirmed as import name for `mem0ai`  
- [x] Example block marked `type: illustrative` (requires Mem0 API key)

---

## Badge Promotions

The following badge JSONs should be updated from `machine-inferred` → `verified` on the `badge-data` branch
by the `promote-badges.yml` workflow after this PR is merged:

| Badge Key | Old State | New State |
|---|---|---|
| `skills-01-perception-image-understanding` | machine-inferred | verified |
| `skills-01-perception-audio-transcription` | machine-inferred | verified |
| `skills-04-action-execution-calendar-event` | machine-inferred | verified |
| `skills-07-tool-use-google-workspace-api` | machine-inferred | verified |
| `skills-03-memory-procedural` | machine-inferred | verified |

---

*Verification record auto-format compliant with `meta/badge-states.md` v2.1*
