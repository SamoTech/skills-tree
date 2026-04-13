<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/SamoTech/skills-tree/main/docs/assets/logo-dark.svg">
  <img src="https://raw.githubusercontent.com/SamoTech/skills-tree/main/docs/assets/logo-light.svg" alt="Skills Tree" width="200" height="52">
</picture>

# Árvore de Habilidades

### O Sistema Operacional de Habilidades para Agentes de IA — Construa Agentes Mais Inteligentes, Mais Rápido

> **515+ habilidades prontas para produção. 16 categorias. Versionadas, avaliadas e em constante evolução.**
> **Pare de redescobrir. Comece a construir sobre o que a comunidade já provou.**

[![Stars](https://img.shields.io/github/stars/SamoTech/skills-tree?style=for-the-badge&color=22c55e&logo=github)](https://github.com/SamoTech/skills-tree/stargazers)
[![PRs Welcome](https://img.shields.io/badge/PRs-Bem_vindos-brightgreen?style=for-the-badge)](../CONTRIBUTING.md)
[![License: MIT](https://img.shields.io/badge/Licença-MIT-yellow?style=for-the-badge)](../LICENSE)
[![Skills](https://img.shields.io/badge/Habilidades-515%2B-8b5cf6?style=for-the-badge)](../skills/)
[![GitHub Pages](https://img.shields.io/badge/Docs-Ao_vivo-22c55e?style=for-the-badge&logo=github)](https://samotech.github.io/skills-tree)

**[🌐 Explorar UI ao vivo](https://samotech.github.io/skills-tree) · [🗺️ Sistemas](../systems/) · [🏗️ Projetos](../blueprints/) · [📊 Benchmarks](../benchmarks/) · [🔬 Laboratórios](../labs/) · [🤝 Contribuir](../CONTRIBUTING.md) · [🗺 Roteiro](../meta/ROADMAP.md)**

🌐 **Ler em outros idiomas:** [English](../README.md) · [العربية](README.ar.md) · [中文](README.zh.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · 🇧🇷 Português · [Русский](README.ru.md) · [हिन्दी](README.hi.md)

</div>

---

## O Problema

Cada desenvolvedor de agentes de IA redescobre as mesmas habilidades do zero.

Alguém aprende RAG da maneira difícil. Outro descobre a injeção de memória às 2 da manhã. Um terceiro passa uma semana comparando ReAct e LATS — e nunca compartilha os resultados. Um quarto tropeça nos mesmos modos de falha que você já encontrou no mês passado.

**Esse conhecimento coletivo está desaparecendo em threads do Slack, repositórios privados e favoritos do Twitter.**

Skills Tree resolve isso.

---

## O Que É Isso?

**Skills Tree é o sistema operacional compartilhado para capacidades de agentes de IA.**

Um índice vivo, versionado e impulsionado pela comunidade de tudo o que um agente pode fazer — documentado com código funcional, benchmarks reais, modos de falha e histórico de evolução. Cada habilidade está pronta para produção. Cada sistema mostra como as habilidades se combinam. Cada benchmark é reproduzível.

Não é uma lista. É infraestrutura.

---

## 🗂️ As 16 Categorias de Habilidades

| # | Categoria | Habilidades | O que cobre |
|---|---|---|---|
| 01 | 👁️ **Percepção** | 36 | Texto, imagens, PDFs, código, sensores, bancos de dados, telas |
| 02 | 🧠 **Raciocínio** | 41 | Planejamento, dedução, abdução, cadeias causais, senso comum |
| 03 | 🗄️ **Memória** | 26 | Trabalho, episódica, semântica, vetorial, injeção, esquecimento |
| 04 | ⚡ **Execução de Ações** | 37 | E/S de arquivos, HTTP, e-mail, shell, escrita em banco de dados |
| 05 | 💻 **Código** | 42 | Escrever, executar, depurar, revisar, refatorar, testar, implantar |
| 06 | 💬 **Comunicação** | 28 | Resumir, traduzir, redigir, argumentar, adaptar o tom |
| 07 | 🔧 **Uso de Ferramentas** | 55 | 55+ APIs — GitHub, Slack, Stripe, OpenAI, MCP, A2A |
| 08 | 🎭 **Multimodal** | 25 | Imagens, áudio, vídeo, VQA, 3D, gráficos |
| 09 | 🤖 **Padrões Agênticos** | 36 | ReAct, CoT, ToT, MCTS, LATS, RAG, Debate |
| 10 | 🖥️ **Uso do Computador** | 37 | Clique, digitação, rolagem, OCR, terminal, VM, árvore de acessibilidade |
| 11 | 🌐 **Web** | 28 | Pesquisa, scraping, rastreamento, login, formulários, RSS |
| 12 | 📊 **Dados** | 18 | ETL, SQL, embeddings, séries temporais, detecção de anomalias |
| 13 | 🎨 **Criativo** | 27 | Copywriting, prompts de imagem, SVG, música, scripts |
| 14 | 🔒 **Segurança** | 20 | Sandboxing, varredura de segredos, logs de auditoria, rollback |
| 15 | 🎼 **Orquestração** | 29 | Multi-agente, máquinas de estado, retentativas, consenso |
| 16 | 🏺 **Específico do Domínio** | 52 | Medicina, direito, finanças, DevOps, educação, ciência |

---

## Início Rápido

```bash
# Clonar
git clone https://github.com/SamoTech/skills-tree.git

# Encontrar uma habilidade por palavra-chave
grep -r "memory injection" skills/ --include="*.md" -l

# Ler um sistema completo do início ao fim
cat systems/research-agent.md

# Ver resultados de benchmarks
cat benchmarks/tool-use/function-calling-comparison.md
```

Ou **[explore a UI ao vivo →](https://samotech.github.io/skills-tree)**

---

## 🤝 Como Contribuir

| Tipo | O que é | Formato do título do PR |
|---|---|---|
| **Nova Habilidade** | Uma capacidade ainda não indexada | `feat: add [skill] to [category]` |
| **Melhoria de Habilidade** | Atualizar v1→v2 com conteúdo melhor | `improve: [skill] — v1→v2` |
| **Benchmark** | Comparação direta com dados reais | `benchmark: [skill-a] vs [skill-b]` |
| **Sistema / Projeto** | Fluxo de trabalho ou arquitetura multi-habilidade | `system: add [name]` |

Guia completo: **[CONTRIBUTING.md](../CONTRIBUTING.md)**

---

<div align="center">

**[⭐ Dar uma estrela](https://github.com/SamoTech/skills-tree) · [🌐 Explorar habilidades](https://samotech.github.io/skills-tree) · [🤝 Contribuir](../CONTRIBUTING.md) · [💖 Patrocinar](https://github.com/sponsors/SamoTech)**

*O Sistema Operacional de Habilidades para Agentes de IA — construído pela comunidade, para a comunidade.*

</div>
