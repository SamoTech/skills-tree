---
title: "MCP OAuth Authentication"
category: 14-security
level: advanced
stability: experimental
description: "Authenticate remote MCP and agent tools with OAuth while keeping credentials outside skill definitions and enforcing explicit authorization boundaries."
added: "2026-10"
version: v1
tags: [security, oauth, mcp, authentication, authorization]
---

# MCP OAuth Authentication

## Description
Authenticate a remote MCP server or agent-facing service through OAuth without embedding credentials in a skill, tool schema, repository, or generated artifact. Treat authentication and authorization as separate contracts: OAuth establishes identity/session state; authorization determines which tools and operations the agent may invoke.

## When to Use
- A remote MCP server requires OAuth/OIDC authentication.
- Tokens rotate or expire during long-running agent sessions.
- A skill must describe authentication requirements without carrying secrets.
- Tool availability depends on the authenticated principal.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Authorization-server metadata, client configuration, redirect policy, requested scopes, runtime identity, and protected-resource metadata when available. |
| Outputs | Authenticated session state, token metadata needed for runtime use, granted scopes, and explicit authorization status. |
| Never output | Client secrets, refresh tokens, access tokens, or other credentials in skill text, logs, prompts, or generated indexes. |

## Procedure
1. Discover protected-resource and authorization-server metadata from authoritative configuration.
2. Validate redirect URI, issuer, audience/resource, PKCE requirements, and requested scopes.
3. Complete authorization using the approved client and user interaction boundary.
4. Store tokens only in the runtime credential store; never in skill files or prompts.
5. Before each privileged tool call, verify that the identity and granted scope authorize the operation.
6. On expiry or invalidation, fail closed and require the defined re-authentication path.
7. Record non-secret authentication evidence sufficient to diagnose failures.

## Failure Modes
- OAuth succeeds but the MCP session exposes no authorized tools.
- Stale or revoked refresh token.
- Redirect URI mismatch.
- Wrong audience/resource or scope.
- Authentication succeeds but authorization is insufficient.
- Tokens or authorization codes leak into logs or model context.

## Security Boundary
OAuth does not grant permission to perform arbitrary tool actions. Tool authorization remains authoritative and must be evaluated independently.

## Evidence
Public 2026 ecosystem evidence includes recurring MCP OAuth interoperability and failure reports, including remote MCP authentication contract discussions and client-side OAuth failures. These are demand corroboration, not adoption measurements.

## Related
- mcp-tool.md
- permission-checking.md
- approval-before-destructive-tools.md
- secret-scanning.md
