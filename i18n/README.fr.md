<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/SamoTech/skills-tree/main/docs/assets/logo-dark.svg">
  <img src="https://raw.githubusercontent.com/SamoTech/skills-tree/main/docs/assets/logo-light.svg" alt="Skills Tree" width="200" height="52">
</picture>

# Arbre de Compétences

### Le Système d'Exploitation des Compétences pour Agents IA — Construisez des Agents Plus Intelligents, Plus Rapidement

> **515+ compétences prêtes pour la production. 16 catégories. Versionnées, évaluées et en constante évolution.**
> **Arrêtez de tout redécouvrir. Construisez sur ce que la communauté a déjà prouvé.**

[![Stars](https://img.shields.io/github/stars/SamoTech/skills-tree?style=for-the-badge&color=22c55e&logo=github)](https://github.com/SamoTech/skills-tree/stargazers)
[![PRs Welcome](https://img.shields.io/badge/PRs-Bienvenus-brightgreen?style=for-the-badge)](../CONTRIBUTING.md)
[![License: MIT](https://img.shields.io/badge/Licence-MIT-yellow?style=for-the-badge)](../LICENSE)
[![Skills](https://img.shields.io/badge/Compétences-515%2B-8b5cf6?style=for-the-badge)](../skills/)
[![GitHub Pages](https://img.shields.io/badge/Docs-En_ligne-22c55e?style=for-the-badge&logo=github)](https://samotech.github.io/skills-tree)

**[🌐 Explorer l'UI en direct](https://samotech.github.io/skills-tree) · [🗺️ Systèmes](../systems/) · [🏗️ Plans](../blueprints/) · [📊 Benchmarks](../benchmarks/) · [🔬 Laboratoires](../labs/) · [🤝 Contribuer](../CONTRIBUTING.md) · [🗺 Feuille de route](../meta/ROADMAP.md)**

🌐 **Lire dans d'autres langues :** [English](../README.md) · [العربية](README.ar.md) · [中文](README.zh.md) · [Español](README.es.md) · 🇫🇷 Français · [Deutsch](README.de.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [हिन्दी](README.hi.md)

</div>

---

## Le Problème

Chaque développeur d'agents IA redécouvre les mêmes compétences depuis zéro.

Quelqu'un apprend RAG à la dure. Un autre découvre l'injection de mémoire à 2h du matin. Un troisième passe une semaine à comparer ReAct et LATS — sans jamais partager les résultats. Un quatrième trébuche sur les mêmes erreurs que vous avez rencontrées le mois dernier.

**Ces connaissances collectives disparaissent dans des fils Slack, des dépôts privés et des favoris Twitter.**

Skills Tree résout ce problème.

---

## Qu'est-ce que c'est ?

**Skills Tree est le système d'exploitation partagé pour les capacités des agents IA.**

Un index vivant, versionné et alimenté par la communauté de tout ce qu'un agent peut faire — documenté avec du code fonctionnel, de vrais benchmarks, des modes d'échec et un historique d'évolution. Chaque compétence est prête pour la production. Chaque système montre comment les compétences se combinent. Chaque benchmark est reproductible.

Ce n'est pas une liste. C'est une infrastructure.

---

## 🗂️ Les 16 Catégories de Compétences

| # | Catégorie | Compétences | Ce qu'elle couvre |
|---|---|---|---|
| 01 | 👁️ **Perception** | 36 | Texte, images, PDF, code, capteurs, bases de données, écrans |
| 02 | 🧠 **Raisonnement** | 41 | Planification, déduction, abduction, chaînes causales, sens commun |
| 03 | 🗄️ **Mémoire** | 26 | Travail, épisodique, sémantique, vectorielle, injection, oubli |
| 04 | ⚡ **Exécution d'actions** | 37 | E/S de fichiers, HTTP, e-mail, shell, écriture en base de données |
| 05 | 💻 **Code** | 42 | Écrire, exécuter, déboguer, réviser, refactoriser, tester, déployer |
| 06 | 💬 **Communication** | 28 | Résumer, traduire, rédiger, argumenter, adapter le ton |
| 07 | 🔧 **Utilisation d'outils** | 55 | 55+ APIs — GitHub, Slack, Stripe, OpenAI, MCP, A2A |
| 08 | 🎭 **Multimodal** | 25 | Images, audio, vidéo, VQA, 3D, graphiques |
| 09 | 🤖 **Patterns agentiques** | 36 | ReAct, CoT, ToT, MCTS, LATS, RAG, Débat |
| 10 | 🖥️ **Utilisation de l'ordinateur** | 37 | Clic, saisie, défilement, OCR, terminal, VM, arbre d'accessibilité |
| 11 | 🌐 **Web** | 28 | Recherche, scraping, crawling, connexion, formulaires, RSS |
| 12 | 📊 **Données** | 18 | ETL, SQL, embeddings, séries temporelles, détection d'anomalies |
| 13 | 🎨 **Créatif** | 27 | Copywriting, prompts d'images, SVG, musique, scripts |
| 14 | 🔒 **Sécurité** | 20 | Sandboxing, scan de secrets, journaux d'audit, rollback |
| 15 | 🎼 **Orchestration** | 29 | Multi-agents, machines à états, réessais, consensus |
| 16 | 🏺 **Domaine spécifique** | 52 | Médical, juridique, finance, DevOps, éducation, science |

---

## Démarrage rapide

```bash
# Cloner
git clone https://github.com/SamoTech/skills-tree.git

# Rechercher une compétence par mot-clé
grep -r "memory injection" skills/ --include="*.md" -l

# Lire un système complet de bout en bout
cat systems/research-agent.md

# Consulter les résultats de benchmarks
cat benchmarks/tool-use/function-calling-comparison.md
```

Ou **[explorez l'UI en direct →](https://samotech.github.io/skills-tree)**

---

## 🤝 Comment contribuer

| Type | Description | Format du titre PR |
|---|---|---|
| **Nouvelle compétence** | Une capacité pas encore indexée | `feat: add [skill] to [category]` |
| **Amélioration** | Monter v1→v2 avec du meilleur contenu | `improve: [skill] — v1→v2` |
| **Benchmark** | Comparaison directe avec de vrais chiffres | `benchmark: [skill-a] vs [skill-b]` |
| **Système / Plan** | Workflow ou architecture multi-compétences | `system: add [name]` |

Guide complet : **[CONTRIBUTING.md](../CONTRIBUTING.md)**

---

<div align="center">

**[⭐ Étoiler ce dépôt](https://github.com/SamoTech/skills-tree) · [🌐 Explorer les compétences](https://samotech.github.io/skills-tree) · [🤝 Contribuer](../CONTRIBUTING.md) · [💖 Sponsoriser](https://github.com/sponsors/SamoTech)**

*Le Système d'Exploitation des Compétences pour Agents IA — construit par la communauté, pour la communauté.*

</div>
