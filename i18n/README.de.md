<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/SamoTech/skills-tree/main/docs/assets/logo-dark.svg">
  <img src="https://raw.githubusercontent.com/SamoTech/skills-tree/main/docs/assets/logo-light.svg" alt="Skills Tree" width="200" height="52">
</picture>

# Fähigkeitsbaum

### Das Fähigkeits-Betriebssystem für KI-Agenten — Intelligentere Agenten, Schneller Bauen

> **515+ produktionsreife Fähigkeiten. 16 Kategorien. Versioniert, getestet und ständig weiterentwickelt.**
> **Hör auf, alles neu zu entdecken. Bau auf dem auf, was die Community bereits bewiesen hat.**

[![Stars](https://img.shields.io/github/stars/SamoTech/skills-tree?style=for-the-badge&color=22c55e&logo=github)](https://github.com/SamoTech/skills-tree/stargazers)
[![PRs Welcome](https://img.shields.io/badge/PRs-Willkommen-brightgreen?style=for-the-badge)](../CONTRIBUTING.md)
[![License: MIT](https://img.shields.io/badge/Lizenz-MIT-yellow?style=for-the-badge)](../LICENSE)
[![Skills](https://img.shields.io/badge/Fähigkeiten-515%2B-8b5cf6?style=for-the-badge)](../skills/)
[![GitHub Pages](https://img.shields.io/badge/Docs-Live-22c55e?style=for-the-badge&logo=github)](https://samotech.github.io/skills-tree)

**[🌐 Live-UI erkunden](https://samotech.github.io/skills-tree) · [🗺️ Systeme](../systems/) · [🏗️ Blaupausen](../blueprints/) · [📊 Benchmarks](../benchmarks/) · [🔬 Labor](../labs/) · [🤝 Beitragen](../CONTRIBUTING.md) · [🗺 Roadmap](../meta/ROADMAP.md)**

🌐 **In anderen Sprachen lesen:** [English](../README.md) · [العربية](README.ar.md) · [中文](README.zh.md) · [Español](README.es.md) · [Français](README.fr.md) · 🇩🇪 Deutsch · [日本語](README.ja.md) · [한국어](README.ko.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [हिन्दी](README.hi.md)

</div>

---

## Das Problem

Jeder KI-Agenten-Entwickler entdeckt dieselben Fähigkeiten von Grund auf neu.

Einer lernt RAG auf die harte Tour. Ein anderer findet um 2 Uhr nachts heraus, wie Memory Injection funktioniert. Ein Dritter verbringt eine Woche damit, ReAct und LATS zu vergleichen — und teilt die Ergebnisse nie. Ein Vierter stolpert über dieselben Fehler, die du letzten Monat gemacht hast.

**Dieses kollektive Wissen verschwindet in Slack-Threads, privaten Repositories und Twitter-Lesezeichen.**

Skills Tree löst das.

---

## Was ist das?

**Skills Tree ist das gemeinsame Betriebssystem für KI-Agenten-Fähigkeiten.**

Ein lebendiges, versioniertes, community-getriebenes Verzeichnis von allem, was ein Agent tun kann — dokumentiert mit funktionierendem Code, echten Benchmarks, Fehlermodi und Entwicklungshistorie. Jede Fähigkeit ist produktionsreif. Jedes System zeigt, wie Fähigkeiten kombiniert werden. Jeder Benchmark ist reproduzierbar.

Es ist keine Liste. Es ist Infrastruktur.

---

## 🗂️ Die 16 Fähigkeitskategorien

| # | Kategorie | Fähigkeiten | Was sie abdeckt |
|---|---|---|---|
| 01 | 👁️ **Wahrnehmung** | 36 | Text, Bilder, PDFs, Code, Sensoren, Datenbanken, Bildschirme |
| 02 | 🧠 **Reasoning** | 41 | Planung, Deduktion, Abduktion, Kausalverkettung, gesunder Menschenverstand |
| 03 | 🗄️ **Gedächtnis** | 26 | Arbeitsgedächtnis, episodisch, semantisch, Vektor, Injektion, Vergessen |
| 04 | ⚡ **Aktionsausführung** | 37 | Datei-I/O, HTTP, E-Mail, Shell, Datenbankschreibvorgänge |
| 05 | 💻 **Code** | 42 | Schreiben, Ausführen, Debuggen, Überprüfen, Refaktorieren, Testen, Bereitstellen |
| 06 | 💬 **Kommunikation** | 28 | Zusammenfassen, Übersetzen, Verfassen, Argumentieren, Tonwechsel |
| 07 | 🔧 **Werkzeugnutzung** | 55 | 55+ APIs — GitHub, Slack, Stripe, OpenAI, MCP, A2A |
| 08 | 🎭 **Multimodal** | 25 | Bilder, Audio, Video, VQA, 3D, Diagramme |
| 09 | 🤖 **Agentische Muster** | 36 | ReAct, CoT, ToT, MCTS, LATS, RAG, Debatte |
| 10 | 🖥️ **Computernutzung** | 37 | Klicken, Tippen, Scrollen, OCR, Terminal, VM, Zugänglichkeitsbaum |
| 11 | 🌐 **Web** | 28 | Suche, Scraping, Crawling, Login, Formulare, RSS |
| 12 | 📊 **Daten** | 18 | ETL, SQL, Embeddings, Zeitreihen, Anomalieerkennung |
| 13 | 🎨 **Kreativ** | 27 | Texterstellung, Bildprompts, SVG, Musik, Skripte |
| 14 | 🔒 **Sicherheit** | 20 | Sandboxing, Geheimnis-Scan, Audit-Logs, Rollback |
| 15 | 🎼 **Orchestrierung** | 29 | Multi-Agenten, Zustandsmaschinen, Wiederholung, Konsens |
| 16 | 🏺 **Domänenspezifisch** | 52 | Medizin, Recht, Finanzen, DevOps, Bildung, Wissenschaft |

---

## Schnellstart

```bash
# Klonen
git clone https://github.com/SamoTech/skills-tree.git

# Fähigkeit nach Stichwort suchen
grep -r "memory injection" skills/ --include="*.md" -l

# Ein vollständiges System von Anfang bis Ende lesen
cat systems/research-agent.md

# Benchmark-Ergebnisse anzeigen
cat benchmarks/tool-use/function-calling-comparison.md
```

Oder **[Live-UI erkunden →](https://samotech.github.io/skills-tree)**

---

## 🤝 Wie man beiträgt

| Typ | Was es ist | PR-Titelformat |
|---|---|---|
| **Neue Fähigkeit** | Eine noch nicht indexierte Fähigkeit | `feat: add [skill] to [category]` |
| **Fähigkeits-Upgrade** | v1→v2 mit besserem Inhalt | `improve: [skill] — v1→v2` |
| **Benchmark** | Direktvergleich mit echten Zahlen | `benchmark: [skill-a] vs [skill-b]` |
| **System / Blaupause** | Multi-Fähigkeits-Workflow oder Architektur | `system: add [name]` |

Vollständiger Leitfaden: **[CONTRIBUTING.md](../CONTRIBUTING.md)**

---

<div align="center">

**[⭐ Dieses Repo mit einem Stern versehen](https://github.com/SamoTech/skills-tree) · [🌐 Fähigkeiten erkunden](https://samotech.github.io/skills-tree) · [🤝 Beitragen](../CONTRIBUTING.md) · [💖 Sponsoren](https://github.com/sponsors/SamoTech)**

*Das Fähigkeits-Betriebssystem für KI-Agenten — von der Community gebaut, für die Community.*

</div>
