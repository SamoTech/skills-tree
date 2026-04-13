<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/SamoTech/skills-tree/main/docs/assets/logo-dark.svg">
  <img src="https://raw.githubusercontent.com/SamoTech/skills-tree/main/docs/assets/logo-light.svg" alt="Skills Tree" width="200" height="52">
</picture>

# スキルツリー

### AIエージェントのスキルOS — より賢いエージェントを、より速く構築

> **515以上の本番対応スキル。16カテゴリ。バージョン管理済み、ベンチマーク済み、常に進化中。**
> **再発見をやめ、コミュニティがすでに証明したものの上に構築しよう。**

[![Stars](https://img.shields.io/github/stars/SamoTech/skills-tree?style=for-the-badge&color=22c55e&logo=github)](https://github.com/SamoTech/skills-tree/stargazers)
[![PRs Welcome](https://img.shields.io/badge/PRs-歓迎-brightgreen?style=for-the-badge)](../CONTRIBUTING.md)
[![License: MIT](https://img.shields.io/badge/ライセンス-MIT-yellow?style=for-the-badge)](../LICENSE)
[![Skills](https://img.shields.io/badge/スキル数-515%2B-8b5cf6?style=for-the-badge)](../skills/)
[![GitHub Pages](https://img.shields.io/badge/ドキュメント-公開中-22c55e?style=for-the-badge&logo=github)](https://samotech.github.io/skills-tree)

**[🌐 ライブUIを見る](https://samotech.github.io/skills-tree) · [🗺️ システム](../systems/) · [🏗️ ブループリント](../blueprints/) · [📊 ベンチマーク](../benchmarks/) · [🔬 ラボ](../labs/) · [🤝 貢献する](../CONTRIBUTING.md) · [🗺 ロードマップ](../meta/ROADMAP.md)**

🌐 **他の言語で読む:** [English](../README.md) · [العربية](README.ar.md) · [中文](README.zh.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · 🇯🇵 日本語 · [한국어](README.ko.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [हिन्दी](README.hi.md)

</div>

---

## 問題

AIエージェントを開発するすべての人が、同じスキルをゼロから再発見しています。

ある人はRAGを苦労して学ぶ。別の人は深夜2時にメモリインジェクションの仕組みを解明する。3人目はReActとLATSを比較するのに一週間費やし、結果を共有しない。4人目はあなたが先月つまずいたのと同じ失敗パターンに遭遇する。

**そのような集合知は、Slackのスレッド、プライベートリポジトリ、Twitterのブックマークの中に消えていきます。**

Skills Treeはこれを解決します。

---

## これは何か

**Skills Treeは、AIエージェントの能力のための共有オペレーティングシステムです。**

エージェントができるすべてのことの、生きた・バージョン管理された・コミュニティ主導のインデックス — 動作するコード、実際のベンチマーク、失敗モード、進化の歴史とともに文書化されています。すべてのスキルは本番対応済み。すべてのシステムはスキルの組み合わせ方を示します。すべてのベンチマークは再現可能です。

リストではありません。インフラです。

---

## 🗂️ 16のスキルカテゴリ

| # | カテゴリ | スキル数 | カバー内容 |
|---|---|---|---|
| 01 | 👁️ **知覚** | 36 | テキスト、画像、PDF、コード、センサー、データベース、画面 |
| 02 | 🧠 **推論** | 41 | 計画、演繹、帰納、因果連鎖、常識推論 |
| 03 | 🗄️ **メモリ** | 26 | ワーキングメモリ、エピソード、セマンティック、ベクター、インジェクション、忘却 |
| 04 | ⚡ **アクション実行** | 37 | ファイルI/O、HTTP、メール、シェル、データベース書き込み |
| 05 | 💻 **コード** | 42 | 作成、実行、デバッグ、レビュー、リファクタリング、テスト、デプロイ |
| 06 | 💬 **コミュニケーション** | 28 | 要約、翻訳、下書き、議論、トーン適応 |
| 07 | 🔧 **ツール使用** | 55 | 55以上のAPI — GitHub、Slack、Stripe、OpenAI、MCP、A2A |
| 08 | 🎭 **マルチモーダル** | 25 | 画像、音声、動画、VQA、3D、チャート |
| 09 | 🤖 **エージェントパターン** | 36 | ReAct、CoT、ToT、MCTS、LATS、RAG、ディベート |
| 10 | 🖥️ **コンピューター使用** | 37 | クリック、入力、スクロール、OCR、ターミナル、VM、アクセシビリティツリー |
| 11 | 🌐 **ウェブ** | 28 | 検索、スクレイピング、クローリング、ログイン、フォーム、RSS |
| 12 | 📊 **データ** | 18 | ETL、SQL、埋め込み、時系列、異常検知 |
| 13 | 🎨 **クリエイティブ** | 27 | コピーライティング、画像プロンプト、SVG、音楽、スクリプト |
| 14 | 🔒 **セキュリティ** | 20 | サンドボックス、シークレットスキャン、監査ログ、ロールバック |
| 15 | 🎼 **オーケストレーション** | 29 | マルチエージェント、状態機械、リトライ、コンセンサス |
| 16 | 🏺 **ドメイン固有** | 52 | 医療、法律、金融、DevOps、教育、科学 |

---

## クイックスタート

```bash
# クローン
git clone https://github.com/SamoTech/skills-tree.git

# キーワードでスキルを検索
grep -r "memory injection" skills/ --include="*.md" -l

# システム全体を最初から最後まで読む
cat systems/research-agent.md

# ベンチマーク結果を見る
cat benchmarks/tool-use/function-calling-comparison.md
```

または **[ライブUIを見る →](https://samotech.github.io/skills-tree)**

---

## 🤝 貢献方法

| 種類 | 内容 | PRタイトル形式 |
|---|---|---|
| **新しいスキル** | まだインデックスされていない能力 | `feat: add [skill] to [category]` |
| **スキルアップグレード** | v1→v2へ改善 | `improve: [skill] — v1→v2` |
| **ベンチマーク** | 実際の数値による直接比較 | `benchmark: [skill-a] vs [skill-b]` |
| **システム / ブループリント** | マルチスキルワークフローまたはアーキテクチャ | `system: add [name]` |

完全ガイド: **[CONTRIBUTING.md](../CONTRIBUTING.md)**

---

<div align="center">

**[⭐ スターを付ける](https://github.com/SamoTech/skills-tree) · [🌐 スキルを見る](https://samotech.github.io/skills-tree) · [🤝 貢献する](../CONTRIBUTING.md) · [💖 スポンサー](https://github.com/sponsors/SamoTech)**

*AIエージェントのスキルOS — コミュニティによって構築され、コミュニティのために。*

</div>
