# Dependency Badge State Machine

> **The tooling is not the product. The product is the trust.**
> If a badge says "Verified", a user should be able to copy-paste that code and sleep soundly.
> If the tooling ever threatens that truth, the tooling must lose.

This document is the canonical definition of the four-state trust contract for all `deps` badges in Skills Tree.
Every badge you see on a skill file is generated from the `badge-data` branch and served via GitHub Pages.
No badge state is ever written directly into Markdown — badge data lives in the metadata layer, not the content layer.

---

## The Four States

| State | Badge | Color | Meaning | User Contract |
|---|---|---|---|---|
| `unscanned` | ![unscanned](https://img.shields.io/badge/deps-unscanned-lightgrey?style=flat-square) | Grey | Skill exists; dependency metadata has not been extracted yet | **Do not assume safety. Inspect manually before use.** |
| `machine-inferred` | ![machine-inferred](https://img.shields.io/badge/deps-machine--inferred-yellow?style=flat-square) | Yellow | AST sweep extracted imports; PyPI confirmed packages exist; not human-verified | **Packages exist. Versions are approximate. Verify before production use.** |
| `verified` | ![verified](https://img.shields.io/badge/deps-verified-22c55e?style=flat-square&color=22c55e) | Green | Human-confirmed: packages exist, versions tested, no active CVEs | **Safe to copy-paste. Re-check when your own deps update.** |
| `advisory` | ![advisory](https://img.shields.io/badge/deps-%E2%9A%A0%EF%B8%8F%20CVE%20advisory-critical?style=flat-square) | Red | One or more dependencies have an active CVE in the OSV database | **Do NOT use in production until advisory is resolved. See skill file for details.** |

---

## Sub-States (Machine-Inferred Only)

Within the `machine-inferred` state, the AST sweep assigns a confidence sub-state:

| Sub-state | Badge Color | Meaning |
|---|---|---|
| `pypi-confirmed` | 🟡 Yellow | All extracted packages found on PyPI |
| `pypi-unknown` | 🟠 Orange | One or more packages not found on PyPI — likely pseudo-code or a typo |
| `pypi-uncertain` | 🔘 Grey-yellow | Network timeout during PyPI check — will retry on next run |

Orange badges (`pypi-unknown`) require the skill author to add `type: illustrative` to the affected code block
before the badge can advance to `machine-inferred`. They cannot be promoted to `verified`.

---

## State Transitions

```
                    ┌─────────────┐
     (Day Zero)     │  unscanned  │  (grey)
                    └──────┬──────┘
                           │  AST sweep + PyPI check
                           ▼
              ┌────────────────────────┐
              │  machine-inferred      │  (yellow / orange)
              │  (pypi-confirmed       │
              │   pypi-unknown         │
              │   pypi-uncertain)      │
              └──────────┬─────────────┘
                         │  Human verification PR
                         ▼
                  ┌─────────────┐
      (steady)    │  verified   │  (green)  ◄──────────┐
                  └──────┬──────┘                      │
                         │  OSV advisory detected       │  Advisory resolved
                         ▼                              │  + re-verify
                  ┌─────────────┐                       │
     (critical)   │  advisory   │  (red) ───────────────┘
                  └─────────────┘
```

**Rules:**
- `unscanned` → `machine-inferred`: **automated only** (AST sweep Action)
- `machine-inferred` → `verified`: **human PR required** (see verification template)
- `verified` → `advisory`: **automated only** (OSV cron, max 15-min latency)
- `advisory` → `verified`: **human PR required** (maintainer confirms fix or unaffected)
- No state ever regresses automatically except `verified` → `advisory`
- `pypi-unknown` orange badges **cannot** be promoted without author annotation

---

## SLA: 15-Minute CVE Detection Window

Skills Tree guarantees badge states are updated within **15 minutes** of a CVE
appearing in the [OSV database](https://osv.dev) for any package present in `meta/skills-sbom.cdx.json`.

This SLA is enforced by `.github/workflows/osv-watch.yml` (cron: `*/15 * * * *`).

This SLA applies to packages with `confidence: verified` or `confidence: machine-inferred` in skill frontmatter.
Packages not yet in the SBOM (i.e., skills still `unscanned`) are outside the SLA.

---

## Badge URL Format

Every skill file contains exactly one dependency badge in this format:

```markdown
![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/BADGE_KEY.json&cacheSeconds=900&style=flat-square)
```

Where `BADGE_KEY` is the skill file path with `/` replaced by `-` and `.md` removed:
- `skills/03-memory/memory-injection.md` → `skills-03-memory-memory-injection`
- `skills/07-tool-use/github-api.md` → `skills-07-tool-use-github-api`

Badge JSON files live on the `badge-data` orphan branch, served as static files via GitHub Pages.

---

## Adding `dependencies` to a Skill (Frontmatter Schema)

```yaml
---
title: "Memory Injection"
category: memory
level: intermediate
stability: stable
version: v2
dependencies:
  - package: langchain-core       # PyPI package name (hyphenated)
    min_version: "0.3.0"          # minimum version the skill works with
    tested_version: "0.3.41"      # exact version used when writing the skill
    confidence: verified          # machine-inferred | verified
  - package: mem0ai
    min_version: "0.1.0"
    tested_version: "0.1.19"
    confidence: machine-inferred
code_blocks:
  - id: "example-1"
    type: executable              # executable | illustrative
  - id: "example-2"
    type: illustrative
    note: "Conceptual only — anthropic SDK shown for illustration"
---
```

**`confidence` values:**
- `machine-inferred` — extracted by AST sweep; PyPI-confirmed but not human-run
- `verified` — human ran the code, confirmed versions, opened a verification PR

AST sweep only parses code blocks with `type: executable` or blocks with no `type` annotation.
Blocks explicitly marked `type: illustrative` are skipped and never contribute to the SBOM.

---

## Verification PR Template

When submitting a verification PR, use this template:

```
Type: dependency-verify
Skill: skills/03-memory/memory-injection.md
Packages verified:
  - langchain-core==0.3.41 ✅
  - mem0ai==0.1.19 ✅
Method: [ ] ran example locally  [ ] read PyPI source  [ ] cross-checked docs
Active CVEs at time of verification: none / [CVE ID if known-unaffected]
Notes:
```

A verified PR promotes:
- Frontmatter `confidence: machine-inferred` → `confidence: verified`
- Badge JSON on `badge-data` branch: `machine-inferred` → `verified`

---

## Rubric Stability (LLM-as-a-Judge)

The semantic domain-agnosticism judge (`meta/semantic-rubric.json`) is validated against
a golden set of 200 labeled examples (`meta/judge-golden-set.jsonl`) on every rubric PR.

| Metric | Required threshold |
|---|---|
| Cohen's Kappa | ≥ 0.82 |
| False positive rate (trap class) | ≤ 10% |
| Hidden set Kappa | ≥ 0.78 (monthly check) |

If a rubric change causes Kappa to drop below threshold, the PR is blocked automatically.

---

*Last updated: April 2026 — v2.1 — Dependency Watchdog shipped*
