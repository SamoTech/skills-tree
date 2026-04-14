---
title: Memory Injection
category: 03-memory
level: intermediate
stability: stable
added: "2025-03"
description: "Apply memory injection in AI agent workflows."
version: v2
tags: [memory, context, personalization, rag]
updated: 2026-04
---


![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-03-memory-memory-injection.json)

# Memory Injection

## Description

Apply memory injection in AI agent workflows.

## What It Does

Dynamically retrieves and injects relevant memories (past conversations, user facts, preferences) into the model's system prompt before each turn. Gives the agent long-term user context without filling the context window with raw history.

The key insight: **you don't inject all memories — you retrieve the most relevant ones for the current query.**
