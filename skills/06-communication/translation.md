---
title: "Translation"
category: 06-communication
level: basic
stability: stable
description: "Translate text between languages with an LLM while preserving meaning, tone, and inline placeholders (URLs, code, ICU variables)."
added: "2025-03"
version: v3
tags: [translation, multilingual, i18n]
updated: "2026-04"
dependencies:
  - package: anthropic
    min_version: "0.39.0"
    tested_version: "0.39.0"
    confidence: verified
code_blocks:
  - id: "example-translate"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-06-communication-translation.json)

# Translation

## Description

Converts text from a source language to a target language without losing meaning, register, or any inline tokens that must survive the round-trip (URLs, code, JSX variables, ICU placeholders like `{count, plural, ...}`). Modern frontier LLMs typically beat both Google Translate and DeepL on context-rich content; they trail dedicated MT systems on extremely short or terminology-heavy snippets.

## When to Use

- Localizing UI strings, docs, user-generated content.
- Translating with **explicit tone instructions** ("formal Arabic", "casual European Portuguese").
- Translating content that contains code, URLs, or ICU placeholders that a generic MT would mangle.
- When you need **glossary enforcement** (always translate "Skills Tree" as "Skills Tree", never "شجرة المهارات").

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `text` | `str` | Source text |
| `source_lang` | `str \| None` | ISO code or natural language name (auto-detect if None) |
| `target_lang` | `str` | ISO code or natural language name |
| `glossary` | `dict[str,str]` | Terms that must be rendered exactly as given |
| `tone` | `str` | "formal", "casual", "marketing", … |
| → `translation` | `str` | Translated text |
| → `notes` | `list[str]` | Caveats from the model (ambiguity, idioms) |

## Runnable Example

```python
# pip install anthropic
from __future__ import annotations
import json
import re
import anthropic

client = anthropic.Anthropic()

PLACEHOLDER_RE = re.compile(r"(\{[^{}]+\}|`[^`]+`|https?://\S+)")

SYSTEM = """You are a professional localizer. Rules:
- Preserve every token wrapped by ⟦…⟧ EXACTLY as-is, in place.
- Apply the glossary verbatim — never translate listed terms.
- Match the requested tone.
- Reply ONLY with strict JSON: {"translation": "...", "notes": ["..."]}."""

def freeze_placeholders(text: str) -> tuple[str, list[str]]:
    placeholders: list[str] = []
    def repl(m: re.Match) -> str:
        placeholders.append(m.group(0))
        return f"⟦{len(placeholders) - 1}⟧"
    return PLACEHOLDER_RE.sub(repl, text), placeholders

def restore(text: str, placeholders: list[str]) -> str:
    for i, ph in enumerate(placeholders):
        text = text.replace(f"⟦{i}⟧", ph)
    return text

def translate(text: str, target_lang: str, source_lang: str | None = None,
              glossary: dict[str, str] | None = None, tone: str = "neutral") -> dict:
    frozen, placeholders = freeze_placeholders(text)
    user = {
        "source_lang": source_lang or "auto",
        "target_lang": target_lang,
        "tone": tone,
        "glossary": glossary or {},
        "text": frozen,
    }
    msg = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        system=SYSTEM,
        messages=[{"role": "user", "content": json.dumps(user, ensure_ascii=False)}],
    )
    obj = json.loads(msg.content[0].text)
    obj["translation"] = restore(obj["translation"], placeholders)
    return obj

if __name__ == "__main__":
    out = translate(
        text="Welcome to `skills-tree`! Visit https://samotech.github.io/skills-tree to start. {count, plural, one {1 skill} other {# skills}} loaded.",
        target_lang="Arabic",
        glossary={"skills-tree": "skills-tree"},
        tone="friendly",
    )
    print(out["translation"])
    print(out["notes"])
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Placeholders translated/dropped | Model rewrites code/URLs | Freeze with `⟦n⟧` tokens (above) and restore after |
| Glossary ignored | Model "improves" branded terms | Pass glossary in the user payload + reinforce in system |
| Pluralization broken | ICU `{count, plural, ...}` rewritten | Treat ICU as a placeholder and translate _inside_ each branch separately if needed |
| Inconsistent register across runs | Temperature too high | Fix temperature at 0; cache by `(text_hash, lang, tone)` |
| Long doc loses cohesion | Independent chunk translation | Translate with overlap or pass a glossary built from earlier chunks |
| RTL/LTR mojibake in display | Caller renders in raw UTF-8 with wrong direction | Wrap target with proper `dir="rtl"` markup downstream |

## Frameworks & Models

| Service | Strengths | Weaknesses |
|---|---|---|
| Claude / GPT-4o | Tone control, glossaries, code-aware | Higher cost than dedicated MT |
| DeepL | Best-in-class for EU languages | No glossary at low tiers |
| Google Translate | Best coverage of low-resource languages | Loses nuance, breaks placeholders |
| NLLB / Madlad-400 | Self-hosted, 200+ languages | Lower quality on long-context |

## Model Comparison

| Capability | claude-opus-4-5 | gpt-4o | gemini-2.0-flash |
|---|---|---|---|
| Tone fidelity | 5 | 4 | 3 |
| Placeholder preservation | 5 | 4 | 3 |
| Low-resource languages | 3 | 3 | 4 |

## Related Skills

- [Multilingual Output](multilingual-output.md)
- [Paraphrasing](paraphrasing.md)
- [Tone Adjustment](tone-adjustment.md)

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Initial entry |
| 2026-02 | v2 | Glossary support |
| 2026-04 | v3 | Placeholder freezing, JSON schema output, model comparison |
