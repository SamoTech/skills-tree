<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/SamoTech/skills-tree/main/docs/assets/logo-dark.svg">
  <img src="https://raw.githubusercontent.com/SamoTech/skills-tree/main/docs/assets/logo-light.svg" alt="Skills Tree" width="200" height="52">
</picture>

# 技能树

### AI 智能体技能操作系统 — 更快构建更智能的智能体

> **515+ 生产就绪技能。16 个分类。版本控制、基准测试、持续演进。**
> **告别重复探索。在社区已验证的基础上直接构建。**

[![Stars](https://img.shields.io/github/stars/SamoTech/skills-tree?style=for-the-badge&color=22c55e&logo=github)](https://github.com/SamoTech/skills-tree/stargazers)
[![PRs Welcome](https://img.shields.io/badge/PRs-欢迎贡献-brightgreen?style=for-the-badge)](../CONTRIBUTING.md)
[![License: MIT](https://img.shields.io/badge/许可证-MIT-yellow?style=for-the-badge)](../LICENSE)
[![Skills](https://img.shields.io/badge/技能数-515%2B-8b5cf6?style=for-the-badge)](../skills/)
[![GitHub Pages](https://img.shields.io/badge/文档-在线-22c55e?style=for-the-badge&logo=github)](https://samotech.github.io/skills-tree)

**[🌐 浏览在线 UI](https://samotech.github.io/skills-tree) · [🗺️ 系统](../systems/) · [🏗️ 蓝图](../blueprints/) · [📊 基准测试](../benchmarks/) · [🔬 实验室](../labs/) · [🤝 贡献](../CONTRIBUTING.md) · [🗺 路线图](../meta/ROADMAP.md)**

---

🌐 **其他语言：** [English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md)

</div>

---

## 问题所在

每个 AI 智能体开发者都在从零开始重新探索同样的技能。

有人费力学习 RAG。有人凌晨两点才摸清记忆注入的门道。有人花一周时间对比 ReAct 与 LATS，却从未分享结果。还有人踩到了你上个月刚踩过的同一个坑。

**这些集体知识正在消失于 Slack 频道、私有仓库和 Twitter 收藏夹中。**

技能树正是为了解决这个问题而生。

---

## 这是什么

**技能树是 AI 智能体能力的共享操作系统。**

一个活跃的、有版本控制的、社区驱动的智能体能力索引——配有可运行代码、真实基准测试、失败案例分析和演进历史。每项技能都经过生产验证。每个系统都展示技能的组合方式。每个基准测试都可复现。

这不是一个列表。这是基础设施。

---

## 🗂️ 16 个技能分类

| # | 分类 | 技能数 | 涵盖内容 |
|---|---|---|---|
| 01 | 👁️ **感知** | 36 | 文本、图像、PDF、代码、传感器、数据库、屏幕 |
| 02 | 🧠 **推理** | 41 | 规划、演绎、溯因、因果链、常识推理 |
| 03 | 🗄️ **记忆** | 26 | 工作记忆、情节记忆、语义记忆、向量、注入、遗忘 |
| 04 | ⚡ **动作执行** | 37 | 文件 I/O、HTTP、邮件、Shell、数据库写入 |
| 05 | 💻 **代码** | 42 | 编写、运行、调试、审查、重构、测试、部署 |
| 06 | 💬 **沟通** | 28 | 摘要、翻译、起草、论证、语调适配 |
| 07 | 🔧 **工具使用** | 55 | 55+ API — GitHub、Slack、Stripe、OpenAI、MCP、A2A |
| 08 | 🎭 **多模态** | 25 | 图像、音频、视频、VQA、3D、图表 |
| 09 | 🤖 **智能体模式** | 36 | ReAct、CoT、ToT、MCTS、LATS、RAG、辩论 |
| 10 | 🖥️ **计算机使用** | 37 | 点击、输入、滚动、OCR、终端、VM、无障碍树 |
| 11 | 🌐 **网络** | 28 | 搜索、抓取、爬虫、登录、表单填写、RSS 解析 |
| 12 | 📊 **数据** | 18 | ETL、SQL、嵌入、时间序列、异常检测 |
| 13 | 🎨 **创意** | 27 | 文案写作、图像提示词、SVG、音乐、脚本 |
| 14 | 🔒 **安全** | 20 | 沙箱、密钥扫描、审计日志、回滚 |
| 15 | 🎼 **编排** | 29 | 多智能体、状态机、重试、共识 |
| 16 | 🏺 **领域专项** | 52 | 医疗、法律、金融、DevOps、教育、科学 |

---

## 60 秒了解一项技能

每个技能文件自包含且生产就绪：

````markdown
# 记忆注入
分类: memory | 级别: intermediate | 稳定性: stable | 版本: v2

## 描述
在每轮对话前将相关历史记忆动态注入智能体的系统提示词，
在不撑满上下文窗口的情况下为模型提供用户上下文。

## 示例
```python
client.messages.create(
    system=f"{base_system}\n\n## 记忆\n{top_k_memories}",
    messages=[{"role": "user", "content": user_message}]
)
```

## 基准测试 → benchmarks/memory/injection-strategies.md
## 相关技能 → working-memory.md · rag.md · vector-store-retrieval.md
## 更新日志 → v1 (2025-03) · v2 (2026-04, 新增检索评分)
````

每项技能包含：
- ✅ 功能描述及重要性说明
- ✅ 类型化输入/输出
- ✅ 可运行 Python 代码（`claude-opus-4-5` / `gpt-4o`）
- ✅ 框架对比表（LangChain、LangGraph、CrewAI、mem0……）
- ✅ 失败模式与边界情况
- ✅ 相关技能交叉链接
- ✅ 版本历史

---

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/SamoTech/skills-tree.git

# 按关键词搜索技能
grep -r "memory injection" skills/ --include="*.md" -l

# 完整阅读一个系统
cat systems/research-agent.md

# 查看基准测试结果
cat benchmarks/tool-use/function-calling-comparison.md
```

或 **[浏览在线 UI →](https://samotech.github.io/skills-tree)**

---

## 🤝 如何贡献

| 类型 | 内容 | PR 标题格式 |
|---|---|---|
| **新技能** | 尚未收录的能力 | `feat: add [skill] to [category]` |
| **技能升级** | v1 升级至 v2，内容更丰富 | `improve: [skill] — v1→v2` |
| **基准测试** | 附真实数据的对比测试 | `benchmark: [skill-a] vs [skill-b]` |
| **系统 / 蓝图** | 多技能工作流或架构 | `system: add [name]` |

完整指南：**[CONTRIBUTING.md](../CONTRIBUTING.md)**

---

<div align="center">

**[⭐ Star 本仓库](https://github.com/SamoTech/skills-tree) · [🌐 浏览技能](https://samotech.github.io/skills-tree) · [🤝 贡献](../CONTRIBUTING.md) · [💖 赞助](https://github.com/sponsors/SamoTech)**

*AI 智能体技能操作系统 — 由社区构建，为社区服务。*

</div>
