# i18n — Internationalization

This directory contains translated versions of skill files from `skills/`.

---

## Directory Structure

```
i18n/
  <language-code>/         # BCP-47 language tag, e.g. ar, fr, de, zh-Hans
    <category>/            # Mirrors the skills/ category structure
      <skill-name>.md      # Translated skill file
```

**Example:**
```
i18n/
  ar/
    02-reasoning/
      chain-of-thought.md
  fr/
    05-code/
      code-generation.md
```

---

## Translation Policy

1. **English is the source of truth.** All translations are derived from `skills/` and should stay in sync with the English original's version.
2. **Frontmatter stays in English.** Field keys (`title`, `category`, `level`, etc.) must remain in English. Only the `description` value and body content should be translated.
3. **`translated_from` field required.** Add this field to the frontmatter to record which English source version the translation is based on:
   ```yaml
   translated_from: "skills/02-reasoning/chain-of-thought.md"
   translation_version: "v2"  # version of the English skill this was translated from
   ```
4. **Filename must match the English source filename exactly.**
5. **No new skills in i18n.** Translations only — new skills must be submitted to `skills/` first.

---

## Supported Languages

| Language | Code | Status |
|----------|------|--------|
| Arabic | `ar` | Planned |
| French | `fr` | Planned |
| German | `de` | Planned |
| Chinese (Simplified) | `zh-Hans` | Planned |
| Spanish | `es` | Planned |

To propose a new language, open an issue using the **New Skill / Translation** template.

---

## Validation

Translated files are not currently covered by the automated schema validator or badge pipeline. This is tracked in [meta/KNOWN-LIMITATIONS.md](../meta/KNOWN-LIMITATIONS.md).
