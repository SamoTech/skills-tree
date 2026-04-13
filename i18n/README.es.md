<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/SamoTech/skills-tree/main/docs/assets/logo-dark.svg">
  <img src="https://raw.githubusercontent.com/SamoTech/skills-tree/main/docs/assets/logo-light.svg" alt="Skills Tree" width="200" height="52">
</picture>

# Árbol de Habilidades

### El Sistema Operativo de Habilidades para Agentes de IA — Construye Agentes Más Inteligentes, Más Rápido

> **515+ habilidades listas para producción. 16 categorías. Versionadas, evaluadas y en constante evolución.**
> **Deja de redescubrir. Empieza a construir sobre lo que la comunidad ya ha demostrado.**

[![Stars](https://img.shields.io/github/stars/SamoTech/skills-tree?style=for-the-badge&color=22c55e&logo=github)](https://github.com/SamoTech/skills-tree/stargazers)
[![PRs Welcome](https://img.shields.io/badge/PRs-Bienvenidos-brightgreen?style=for-the-badge)](../CONTRIBUTING.md)
[![License: MIT](https://img.shields.io/badge/Licencia-MIT-yellow?style=for-the-badge)](../LICENSE)
[![Skills](https://img.shields.io/badge/Habilidades-515%2B-8b5cf6?style=for-the-badge)](../skills/)
[![GitHub Pages](https://img.shields.io/badge/Docs-En_vivo-22c55e?style=for-the-badge&logo=github)](https://samotech.github.io/skills-tree)

**[🌐 Explorar UI en Vivo](https://samotech.github.io/skills-tree) · [🗺️ Sistemas](../systems/) · [🏗️ Planos](../blueprints/) · [📊 Benchmarks](../benchmarks/) · [🔬 Laboratorios](../labs/) · [🤝 Contribuir](../CONTRIBUTING.md) · [🗺 Hoja de Ruta](../meta/ROADMAP.md)**

---

🌐 **Leer en otros idiomas:** [English](../README.md) · [العربية](README.ar.md) · [中文](README.zh.md) · 🇪🇸 Español · [Français](README.fr.md) · [Deutsch](README.de.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [हिन्दी](README.hi.md)

</div>

---

## El Problema

Cada desarrollador de agentes de IA redescubre las mismas habilidades desde cero.

Alguien aprende RAG a las malas. Otro descifra la inyección de memoria a las 2am. Un tercero pasa una semana comparando ReAct con LATS — y nunca comparte los resultados. Un cuarto tropieza con los mismos modos de fallo que tú ya encontraste el mes pasado.

**Ese conocimiento colectivo desaparece en hilos de Slack, repositorios privados y marcadores de Twitter.**

Skills Tree soluciona eso.

---

## Qué Es

**Skills Tree es el sistema operativo compartido para las capacidades de los agentes de IA.**

Un índice vivo, versionado y impulsado por la comunidad de todo lo que un agente puede hacer — documentado con código funcional, benchmarks reales, modos de fallo e historial de evolución. Cada habilidad está lista para producción. Cada sistema muestra cómo se combinan las habilidades. Cada benchmark es reproducible.

No es una lista. Es infraestructura.

---

## 🗂️ Las 16 Categorías de Habilidades

| # | Categoría | Habilidades | Qué Cubre |
|---|---|---|---|
| 01 | 👁️ **Percepción** | 36 | Texto, imágenes, PDFs, código, sensores, bases de datos, pantallas |
| 02 | 🧠 **Razonamiento** | 41 | Planificación, deducción, abducción, cadenas causales, sentido común |
| 03 | 🗄️ **Memoria** | 26 | Trabajo, episódica, semántica, vectorial, inyección, olvido |
| 04 | ⚡ **Ejecución de Acciones** | 37 | E/S de archivos, HTTP, email, shell, escritura en bases de datos |
| 05 | 💻 **Código** | 42 | Escribir, ejecutar, depurar, revisar, refactorizar, probar, desplegar |
| 06 | 💬 **Comunicación** | 28 | Resumir, traducir, redactar, argumentar, adaptar el tono |
| 07 | 🔧 **Uso de Herramientas** | 55 | 55+ APIs — GitHub, Slack, Stripe, OpenAI, MCP, A2A |
| 08 | 🎭 **Multimodal** | 25 | Imágenes, audio, video, VQA, 3D, gráficos |
| 09 | 🤖 **Patrones Agénticos** | 36 | ReAct, CoT, ToT, MCTS, LATS, RAG, Debate |
| 10 | 🖥️ **Uso del Computador** | 37 | Clic, escritura, desplazamiento, OCR, terminal, VM, árbol a11y |
| 11 | 🌐 **Web** | 28 | Búsqueda, scraping, rastreo, inicio de sesión, formularios, RSS |
| 12 | 📊 **Datos** | 18 | ETL, SQL, embeddings, series temporales, detección de anomalías |
| 13 | 🎨 **Creativo** | 27 | Copywriting, prompts de imágenes, SVG, música, guiones |
| 14 | 🔒 **Seguridad** | 20 | Sandboxing, escaneo de secretos, registros de auditoría, rollback |
| 15 | 🎼 **Orquestación** | 29 | Multi-agente, máquinas de estado, reintentos, consenso |
| 16 | 🏺 **Específico de Dominio** | 52 | Médico, legal, finanzas, DevOps, educación, ciencia |

---

## Una Habilidad en 60 Segundos

Cada archivo de habilidad es autocontenido y listo para producción:

````markdown
# Inyección de Memoria
Categoría: memory | Nivel: intermediate | Estabilidad: stable | Versión: v2

## Descripción
Inyecta dinámicamente memorias pasadas relevantes en el prompt del sistema
de un agente antes de cada turno — dándole contexto del usuario al modelo
sin llenar la ventana de contexto.

## Ejemplo
```python
client.messages.create(
    system=f"{base_system}\n\n## Memoria\n{top_k_memories}",
    messages=[{"role": "user", "content": user_message}]
)
```

## Benchmarks  → benchmarks/memory/injection-strategies.md
## Relacionadas → working-memory.md · rag.md · vector-store-retrieval.md
## Changelog   → v1 (2025-03) · v2 (2026-04, puntuación de recuperación añadida)
````

Cada habilidad incluye:
- ✅ Qué hace y por qué importa
- ✅ Entradas/salidas tipadas
- ✅ Código Python ejecutable (`claude-opus-4-5` / `gpt-4o`)
- ✅ Tabla de frameworks (LangChain, LangGraph, CrewAI, mem0…)
- ✅ Modos de fallo y casos extremos
- ✅ Vínculos a habilidades relacionadas
- ✅ Historial de versiones

---

## Inicio Rápido

```bash
# Clonar
git clone https://github.com/SamoTech/skills-tree.git

# Buscar una habilidad por palabra clave
grep -r "memory injection" skills/ --include="*.md" -l

# Leer un sistema completo de principio a fin
cat systems/research-agent.md

# Ver resultados de benchmarks
cat benchmarks/tool-use/function-calling-comparison.md
```

O **[explora la UI en vivo →](https://samotech.github.io/skills-tree)**

---

## 🤝 Cómo Contribuir

| Tipo | Qué Es | Formato del Título del PR |
|---|---|---|
| **Nueva Habilidad** | Una capacidad aún no indexada | `feat: add [skill] to [category]` |
| **Mejora de Habilidad** | Subir v1→v2 con mejor contenido | `improve: [skill] — v1→v2` |
| **Benchmark** | Comparativa directa con datos reales | `benchmark: [skill-a] vs [skill-b]` |
| **Sistema / Plano** | Flujo de trabajo o arquitectura multi-habilidad | `system: add [name]` |

Guía completa: **[CONTRIBUTING.md](../CONTRIBUTING.md)**

---

<div align="center">

**[⭐ Dale una estrella](https://github.com/SamoTech/skills-tree) · [🌐 Explorar habilidades](https://samotech.github.io/skills-tree) · [🤝 Contribuir](../CONTRIBUTING.md) · [💖 Patrocinar](https://github.com/sponsors/SamoTech)**

*El Sistema Operativo de Habilidades para Agentes de IA — construido por la comunidad, para la comunidad.*

</div>
