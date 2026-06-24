# README Conversion Audit

**Initiative:** INITIATIVE-014A.2 — Phase 1  
**Date:** 2026-06-24  
**Auditor:** Content Architect + Growth Architect  

---

## Scoring Method

Each dimension scored 0–10 against Show HN conversion best practices.

---

## Above-the-Fold Audit (First Screen — 768px viewport)

| Element | Present | Score | Finding |
|---------|---------|-------|---------|
| Product logo | ✅ | 9 | SVG logo renders correctly |
| One-line tagline | ✅ | 7 | "The AI Agent Skill OS" is clear |
| Stat line (nodes/edges) | ✅ | 8 | "367 skills" — **stale** (actual: 368) |
| Live demo CTA | ✅ | 6 | Buried below badges |
| Blueprint Generator CTA | ❌ | 2 | Not in hero — most differentiating surface hidden |
| **"This Week's Highlights"** | ⚠️ | 1 | Shows "No skill changes this week" — **first non-logo content a visitor reads. Signals inactivity. Must be removed from hero.** |
| Star request | ⚠️ | 4 | Buried in badges row, not visible as emotional ask |

**Above-the-fold score: 5.3/10**

---

## Demo Visibility

| Element | Score | Finding |
|---------|-------|---------|
| Interactive link | 7 | Present but not prominent |
| Screenshot / GIF | 0 | **Missing entirely** — highest-impact addition |
| Blueprint demo link | 3 | Only in nav links, not called out |
| Zero-friction copy | 8 | No install required is stated |

**Demo visibility score: 4.5/10**

---

## Social Proof

| Element | Score | Finding |
|---------|-------|---------|
| Star badge | 7 | Present |
| Contributor badge | 7 | Present |
| Comparison table | 9 | Excellent — detailed vs. LangChain, HF Hub |
| Testimonials | 0 | None (expected at this stage) |

**Social proof score: 5.8/10**

---

## Contributor Onboarding Friction

| Element | Score | Finding |
|---------|-------|---------|
| CONTRIBUTING.md linked | 8 | Multiple links |
| First contribution clarity | 6 | PR title formats shown |
| `good first issue` label | 0 | **No issues open — zero contributor funnel** |
| Issue templates | unknown | Needs verification |

**Contributor friction score: 3.5/10**

---

## Star Request Visibility

| Element | Score | Finding |
|---------|-------|---------|
| Star CTA | 5 | Buried in footer |
| Emotional star ask | 0 | No "If this helps you, star it" copy |
| Twitter share link | 8 | Pre-populated tweet present |

**Star visibility score: 4.3/10**

---

## Top 5 Conversion Fixes (Ranked by Impact)

1. **Remove "This Week's Highlights" from hero** — replace with static value row: `368 nodes · 780 edges · 50 blueprints · MIT · No auth`
2. **Add screenshot/GIF of Explorer** — first visual impression of the interactive product
3. **Promote Blueprint Generator to hero section** — second live demo link immediately after Explorer
4. **Fix stale node count** — 367 → 368 in tagline
5. **Add emotional star ask** — "If Skills Tree saved you time, please ⭐ star it"

---

## Overall Conversion Score: 46/100

**Target for Show HN launch: 75+/100**  
**Gap: 29 points — addressable in README V2 (INITIATIVE-014A.3)**
