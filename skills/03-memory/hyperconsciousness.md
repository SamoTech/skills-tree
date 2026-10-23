---
title: "Hyperconsciousness Memory Store"
category: 03-memory
level: intermediate
stability: experimental
added: "2026-10"
updated: "2026-10"
version: v1
description: "Use the Hyperconsciousness CLI or MCP server as an append-only store for agent knowledge, with an explicit store path and narrow, expiring grants. This procedure covers a synthetic local example and the checks to make before exposing records to an agent."
tags: [agent-memory, encrypted-storage, local-first, mcp]
related: [long-term-memory, memory-access-auditing]
---

# Hyperconsciousness Memory Store

## Description

Hyperconsciousness (HC) is an MIT-licensed developer-alpha project with a Rust engine, CLI, MCP/HTTP server, and agent skills. Use its CLI to create and inspect a separate local store, or configure an MCP client with a grant when an agent needs a bounded view of selected records. HC records are append-only; this procedure does not treat the store as a mutable key-value database or a replacement for a verified backup.

## When to Use

- An agent workflow needs persistent knowledge in an explicitly selected HC store.
- You want to test a memory flow using synthetic notes before connecting a real store.
- An agent should read only notes matching a limited kind, tag, sensitivity, and expiry.

## Inputs and Outputs

| Area | Contract |
|---|---|
| Inputs | A local HC installation, an explicit store directory, synthetic or approved note text, and the intended agent read scope. |
| Outputs | A local append receipt and a readback, or an MCP grant configuration for the selected scope. |
| Safety | Pass `--dir` on every CLI command. Use synthetic content for tests. Review the recipient, scope, and expiry before sharing a grant. |

## Procedure

1. Install HC from source using the current project instructions, or use another official distribution documented by the project. Confirm the `hc` executable is available.
2. Choose a new directory for a synthetic test store. Do not omit `--dir` or reuse a personal or work store for the example below.
3. Start the store, append a clearly synthetic note, then read and inspect its status. Keep each command pointed at the same directory.
4. Before an agent connects, decide which records it needs. Prefer a grant restricted by kind, tags, sensitivity, and expiration rather than exposing broader access.
5. Configure the MCP client with the grant ID and an absolute store path. Verify the connected agent can retrieve only the intended records, and revoke the grant when access should end.
6. Treat records returned to an agent as visible to that agent and its model provider. Encryption at rest does not keep returned plaintext from a hosted model. Keep credentials and private source material out of demonstrations.
7. Follow the project's recovery-verification procedure before relying on a backup. A successful local read is not proof that a backup can be restored.

## Runnable Example

This isolated smoke test creates a temporary store, writes one synthetic record, then reads that store. It requires the HC CLI and Python 3; it does not touch a default store.

```python
import subprocess
import tempfile

with tempfile.TemporaryDirectory(prefix="hc-skill-demo-") as store:
    def hc(*args):
        return subprocess.run(["hc", *args, "--dir", store], check=True, text=True, capture_output=True)
    hc("start")
    hc("write", "Synthetic demo note only", "--tags", "demo", "--sensitivity", "normal")
    print(hc("read").stdout)
    print(hc("status").stdout)
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| A command reads or writes the wrong store | `--dir` was omitted or a different path was used | Pass the same explicit directory to every command and confirm it before writing. |
| The agent sees more notes than intended | The grant scope is broader than the needed kind, tags, sensitivity, or duration | Create a least-scope, expiring grant and test retrieval with synthetic records first. |
| A model provider receives sensitive plaintext | A granted record is returned to an agent using a hosted model | Share only approved content; encryption at rest does not hide plaintext from the recipient. |
| A backup cannot be restored | A successful read was mistaken for recovery verification | Run the documented recovery verification and restore drill before depending on the backup. |
| A record needs correction or removal | HC's knowledge log is append-only | Follow the project's documented correction or retraction procedure; do not imply that retraction erases prior copies. |

## Limitations and Security Boundaries

HC is in developer alpha, and its commands and APIs may change. No independent security audit is claimed. Scoped grants constrain HC access; they are not operating-system process isolation. A local encrypted store does not prevent an authorized recipient from retaining plaintext it has already received. Consult the project's current security constraints and recovery documentation before using important data.

## Related Skills

- [Long-Term Memory](long-term-memory.md) — defines durable memory, provenance, retention, and retrieval rules.
- [Memory Access Auditing](memory-access-auditing.md) — covers review of access activity and its limitations.

## Changelog

| Date | Version | Change |
|---|---|---|
| 2026-10 | v1 | Add a scoped procedure for an isolated HC memory-store example. |
